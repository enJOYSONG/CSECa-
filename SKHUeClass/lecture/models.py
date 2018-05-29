from django.db import models
from account.models import Professor

# Create your models here.
class Lecture(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

