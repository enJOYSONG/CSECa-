from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from libraries.libuser import user_check
from lecture.models import Lecture
from django.contrib.contenttypes.models import ContentType

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
                content_type = ContentType.objects.get_for_model(Lecture)
                permission = auth.models.Permission.objects.get(
                    codename='add_lecture',
                    content_type=content_type,
                )
                bu.user_permissions.add(permission)
                bu.save

            return redirect('/login')



@login_required
def userinfo(request):
    if request.method == "GET":
        user = user_check(request)
        info = {'username': request.user.username,
         'name': request.user.get_full_name(),
         'department': request.user.department,
         'phonenum': request.user.phone,
         'email': request.user.email}

        if type(user) is Student:
            info['grade'] = user.grade

        return render(request, 'myPage.html', {'info': info})

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