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
        return render(request, 'join.html')


def userinfo(request):
    if request.method == "GET":
        return render(request, 'myPage.html')
