# Generated by Django 2.0.3 on 2018-06-12 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0007_auto_20180612_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturenotice',
            name='is_assignment',
            field=models.BooleanField(default=False),
        ),
    ]
