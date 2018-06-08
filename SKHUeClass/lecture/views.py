from django.shortcuts import render
from .models import Lecture, LectureNotice
from django.utils import timezone


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

def noticeWrite(request):
    if request.method =="GET":
        return render(request,'noticeWrite.html')
    if request.method=='POST':
        lec = Lecture.objects.get(id=1)
        lecNotice = LectureNotice()

        lecNotice.lecture = lec
        lecNotice.title= request.POST['title']
        lecNotice.content = request.POST['content']
        lecNotice.file = request.POST['file']
        lecNotice.is_notice = request.POST.get('is_notice',False)
        lecNotice.limited_date = request.POST['limited_date']
        #lecNotice.content_at = django.utils.timezone.now()
        lecNotice.updated_at = timezone.now()


        lecNotice.save()
        return render(request,'myLecture.html')
