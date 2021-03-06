# Generated by Django 2.0.3 on 2018-06-12 06:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0004_lecture_ta'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=1000)),
                ('content_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(null=True, upload_to='')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.Lecture')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000)),
                ('content_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.LectureNotice')),
            ],
        ),
    ]
