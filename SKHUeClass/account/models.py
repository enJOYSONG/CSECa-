from django.db import models

# Create your models here.
class BaseUser(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

class Professor(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)

class Student(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)


