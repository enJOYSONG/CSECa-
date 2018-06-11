from django.db import models
from account.models import Professor, Student

# Create your models here.
class Lecture(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student)

class LectureNotice(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=False)
    content = models.TextField(max_length=1000,null=False)
    content_at= models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(null=True)
    limited_date=models.DateTimeField(null=True)
    is_notice=models.BooleanField()