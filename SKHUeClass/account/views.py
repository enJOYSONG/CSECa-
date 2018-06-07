from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect
from .models import *

def main(request):
    if request.method == "GET":
        return render(request, 'login.html')

@csrf_protect
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        return redirect('/lecture/my_lecture_list')

@csrf_protect
def join(request):
    if request.method == "GET":
           return render(request, 'join.html')

    if request.method == "POST":
        bu = BaseUser()
        std = Student()
        prof = Professor()
        job = request.POST['job']

        bu.id = request.POST['id']
        bu.password = request.POST['password']
        bu.email = request.POST['email']
        bu.name = request.POST['name']
        bu.department = request.POST['department']
        bu.phone = request.POST['phone']
        bu.save()

        if(job == "학생"):
            std.base_user = bu
            std.grade = request.POST['grade']
            std.save()
        else:
            prof.base_user = bu
            prof.save()

        return render(request, 'login.html')


def userinfo(request):
    if request.method == "GET":
        return render(request, 'myPage.html')
