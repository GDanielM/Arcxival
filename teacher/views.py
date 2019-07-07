from django.shortcuts import render, get_object_or_404, redirect
from teacher.models import course, session, teacher
from student.models import project, file
from django.core import serializers
from customuser.models import user_type


# Create your views here.

def thome(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
        if(request.method == 'POST'):
            course_code = course.objects.get(course_code=request.POST.get('course-code-list'))
            batch = request.POST.get('batch')
            session_id = course_code.course_code + batch
            date = request.POST.get('start-date')
            t_code = teacher.objects.get(email=request.user)
            print(t_code.teacher_code)

            sn = session(course_code=course_code, batch=batch, session_id=session_id, date=date, teacher_code=t_code)
            sn.save()

            with open("file.json", "w") as out:
                json_serializer = serializers.get_serializer('json')()
                json_serializer.serialize(session.objects.all(), stream=out)

        teacher_id = teacher.objects.get(email=request.user)
        print(teacher_id.teacher_code)
        sessions_obj = session.objects.filter(teacher_code=teacher_id.teacher_code)
        data = []

        for x in sessions_obj:
            tit = course.objects.get(course_code=x.course_code.course_code).course_title
            data.append({'session':x,'title':tit})
        print(data)

        return render(request, 'teacher/teach-home.html', {'data':data})
    else:
        if request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
            return redirect('shome')

def createsession(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
        if(request.method == 'POST'):
            course_code = request.POST.get('course-code')
            course_title = request.POST.get('course-title')
            credit = request.POST.get('credit-input')
            t_code = teacher.objects.get(email=request.user)
            c = course(course_code=course_code, course_title=course_title, course_credit=credit, teacher_code=t_code)
            c.save()

        course_obj = course.objects
        return render(request, 'teacher/create-session.html', {'courses':course_obj})
    else:
        if request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
            return redirect('shome')

def batchinfo(request, session_id):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
        session_obj = get_object_or_404(session, pk=session_id)
        print(session_obj.session_id)
        project_objs = project.objects.raw("select * from student_project where session_id LIKE %s",[session_obj.session_id])

        return render(request, 'teacher/teacher_projects.html', {'projects':project_objs, 'session':session_obj})
    else:
        if request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
            return redirect('shome')

def projectdetails(request, session_id, project_id):
    #print(project_title, session)
    if request.user.is_authenticated:
        if request.method == 'POST':
            for uploaded_file in request.FILES.getlist('file'):
                #uploaded_file = request.FILES['file']
                # fs = FileSystemStorage()
                # fs.save(uploaded_file.name, uploaded_file)

                project_ob = project.objects.get(project_id=request.POST.get("project_id"))
                file_obj = file(file_name=uploaded_file.name, project_id=project_ob, file_content=uploaded_file)
                file_obj.save()

        files = file.objects
        project_obj = get_object_or_404(project, pk=project_id)
        return render(request, 'upload.html', {'project_obj':project_obj,'files':files})
    else:
        print("TEACHER BA STUDENT NA")
        return HttpResponse(request, '<h1>TEACHER BA STUDENT NA</h1>')