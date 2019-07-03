# Generated by Django 2.2.2 on 2019-07-02 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher', '0004_auto_20190702_0340'),
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_number', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=300)),
                ('group_name', models.CharField(max_length=100)),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.course')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.session')),
            ],
        ),
    ]
