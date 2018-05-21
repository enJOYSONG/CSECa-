from django.shortcuts import render
from rest_framework.views import APIView


def lecture_list(request):
    if request.method == "GET":
        return render(request, 'lectureList.html')



def lecture_detail(request):
    if request.method == "GET":
        return render(request, 'myLecture.html')