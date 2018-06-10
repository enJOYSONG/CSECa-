from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class BaseUser(AbstractUser):
    #학부 학과 enum
    DEPARTMENT_CHOICES = (
        ('CS', '컴퓨터공학과'),
        ('GL', '글로컬IT학과'),
        ('SW', '소프트웨어공학과'),
        ('JT', '정보통신공학과'),
        ('IT', 'IT자율융합학부'),
        ('etc', '기타'),
    )
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES, default='etc')
    phone = models.CharField(max_length=15, null=True)

class Professor(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=False)


class Student(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=False)
    grade = models.IntegerField(default=1)
    isTA = models.BooleanField(default=False)


