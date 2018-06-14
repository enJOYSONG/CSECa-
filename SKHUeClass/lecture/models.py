from django.db import models
from account.models import Professor, Student, BaseUser
from django.utils import timezone

# Create your models here.
class Lecture(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
    ta = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name="ta_student")

class LectureInfo(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mid_score = models.IntegerField(default= 0)
    final_score = models.IntegerField(default= 0)

class Team(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE),
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True),
    members = models.ManyToManyField(Student, related_name="team_members")

class LectureNotice(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=False)
    content = models.TextField(max_length=1000,null=False)
    content_at= models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(null=True)
    limited_date=models.DateTimeField(null=True)
    is_notice=models.BooleanField()
    is_assignment = models.BooleanField(default=False)

class LectureQuestion(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    person = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(max_length=1000, null=False)
    content_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(null=True)

class QuestionComment(models.Model):
    question = models.ForeignKey(LectureQuestion, on_delete=models.CASCADE)
    person = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(max_length=1000, null=False)
    content_at = models.DateTimeField(default=timezone.now)

class Assignment(models.Model):
    notice = models.ForeignKey(LectureNotice, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, null=True)
    file = models.FileField(null=True)
    point = models.IntegerField(null=True)
    comment = models.CharField(max_length=100, null=True)