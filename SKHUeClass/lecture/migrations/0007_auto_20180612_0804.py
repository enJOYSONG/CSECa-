# Generated by Django 2.0.3 on 2018-06-12 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0006_auto_20180612_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.LectureQuestion'),
        ),
    ]
