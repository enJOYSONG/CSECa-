from django.shortcuts import render
from .models import Lecture


def my_lecture_list(request):
    if request.method == "GET":
        return render(request, 'lectureList.html')

    if request.method == "POST":

        lectures = Lecture.objects.all()
        return render(request, 'lectureApply.html', {'lectures': lectures})

def lecture_detail(request):
    if request.method == "GET":
        return render(request, 'myLecture.html')

def lecture_list(request):
        if request.method == "GET":
            lectures = Lecture.objects.all()
            return render(request, 'lectureApply.html', {'lectures': lectures})