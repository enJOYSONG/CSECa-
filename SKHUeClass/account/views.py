from django.shortcuts import render, redirect
from rest_framework.views import APIView

def main(request):
    if request.method == "GET":
        return render(request, 'login.html')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        return redirect('/lecture')


def join(request):
    if request.method == "GET":
        return render(request, 'join.html')


def userinfo(request):
    if request.method == "GET":
        return render(request, 'myPage.html')
