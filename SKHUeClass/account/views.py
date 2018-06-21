from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from libraries.libuser import user_check
from lecture.models import Lecture
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from urllib.parse import parse_qsl
from json import loads,dumps


def main(request):
    if request.method == "GET":
        return redirect('login')

@csrf_protect
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('my_lecture_list')
        else:
            return render(request, 'login.html')

    if request.method == "POST":
        json_data = loads(request.POST['post_data'])
        user = auth.authenticate(username=json_data.get('username'), password=json_data.get('password'), request=request)

        if user is not None and user.is_active:
            auth.login(request, user)
            return JsonResponse({'status': 200, 'redirect_url':'/lecture/my_lecture_list'}, safe=False)
        else:
            return JsonResponse({'status': 400}, safe=False)



@csrf_protect
def join(request):
    if request.method == "GET":
           return render(request, 'join.html')

    if request.method == "POST":
        list = dict(parse_qsl(request.POST['post_data']))

        if BaseUser.objects.filter(username=list.get('id')).exists() :
            return JsonResponse({'status': 400}, safe=False)

        else:
            bu = BaseUser.objects.create_user(
                username=list.get('id'),
                password=list.get('password'),
                email = list.get('email'),
                first_name = list.get('first_name'),
                last_name = list.get('last_name'),
                department = list.get('department'),
                phone = list.get('phone')
            )

            bu.save()

            job = list.get('job')

            if(job == "학생"):
                std = Student(
                    base_user = bu,
                    grade = list.get('grade')
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

            return JsonResponse({'status': 200, 'redirect_url': '/login'}, safe=False)



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
            info['job'] = "학생"
        else:
            info['job'] = "교수"

        return render(request, 'myPage.html', {'info': info})

    if request.method == "POST":
        user = user_check(request)
        list = dict(parse_qsl(request.POST['post_data']))
        request.user.email = list.get('email')
        request.user.department = list.get('department')
        request.user.phone =list.get('phone')
        if type(user) is Student:
            request.user.student.grade = list.get('grade')

        request.user.save()

        if list.get('password') is None:
            request.user.save()
            return JsonResponse({'status': 200}, safe=False)
        else:
            request.user.set_password(list.get('password'))
            request.user.save()
            return JsonResponse({'status': 202, 'redirect_url': '/login'}, safe=False)


@login_required
def logoutUser(request):
    auth.logout(request)
    return redirect('login')