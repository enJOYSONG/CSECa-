from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def main(request):
    if request.method == "GET":
        return render(request, 'login.html')

@csrf_protect
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password, request=request)

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/lecture/my_lecture_list')
        else:
            return redirect('/login')



@csrf_protect
def join(request):
    if request.method == "GET":
           return render(request, 'join.html')

    if request.method == "POST":
        if BaseUser.objects.filter(username=request.POST['id']).exists() :
            return redirect('/join')

        else:
            bu = BaseUser.objects.create_user(
                username=request.POST['id'],
                password=request.POST['password'],
                email = request.POST['email'],
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                department = request.POST['department'],
                phone = request.POST['phone']
            )

            bu.save()

            job = request.POST['job']

            if(job == "학생"):
                std = Student(
                    base_user = bu,
                    grade = request.POST['grade']
                )
                std.save()
            else:
                prof = Professor(
                    base_user = bu
                )
                prof.save()

            return redirect('/login')



@login_required
def userinfo(request):
    if request.method == "GET":
        return render(request, 'myPage.html', {'info': {'username':request.user.username,
                                                        'name':request.user.get_full_name(),
                                                        'department': request.user.department,
                                                        'grade': request.user.student.grade,
                                                        'phonenum': request.user.phone,
                                                        'email': request.user.email}})

    if request.method == "POST":

        request.user.email = request.POST['email']
        request.user.department = request.POST['department']
        request.user.phone = request.POST['phone']
        request.user.student.grade = request.POST['grade']

        if request.POST['password'] == '':
            request.user.student.save()
            request.user.save()
            return redirect('/mypage')
        else:
            request.user.set_password(request.POST['password'])
            request.user.save()
            return redirect('/login')


@login_required
def logoutUser(request):
    auth.logout(request)
    return redirect('login')