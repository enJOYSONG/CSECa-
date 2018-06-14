# Generated by Django 2.0.3 on 2018-06-14 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_student_ista'),
        ('lecture', '0009_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid_score', models.IntegerField(default=0)),
                ('final_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('members', models.ManyToManyField(to='account.Student')),
            ],
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='students',
        ),
        migrations.AddField(
            model_name='lectureinfo',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.Lecture'),
        ),
        migrations.AddField(
            model_name='lectureinfo',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Student'),
        ),
    ]