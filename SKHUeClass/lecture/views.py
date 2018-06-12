from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from .models import Lecture, LectureNotice
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

@login_required
def main(request):
    if request.method == "GET":
        try:
            request.user.professor
        except ObjectDoesNotExist:
            return redirect('my_lecture_list')

        return render(request, 'lectureCreate.html')

    if request.method == "POST":
        try:
            request.user.professor
        except ObjectDoesNotExist:
            return redirect('my_lecture_list')


        new_lecture = Lecture(name=request.POST['lecture_name'],
                              professor=request.user.professor)
        new_lecture.save()
        return redirect('lecture_list')

@login_required
def my_lecture_list(request):
    if request.method == "GET":
        try:
            request.user.student
        except ObjectDoesNotExist:
            lectures = Lecture.objects.filter(professor=request.user.professor).all()
            return render(request, 'lectureList.html', {'lectures': lectures})

        lectures = request.user.student.lecture_set.all()

        return render(request, 'lectureList.html', {'lectures': lectures})

    if request.method == "POST":
        try:
            request.user.student
        except ObjectDoesNotExist:
            return redirect('my_lecture_list')

        lecture_id = request.POST['h1']
        lecture = Lecture.objects.get(id=lecture_id)

        lecture.students.add(request.user.student)

        return redirect('my_lecture_list')

@login_required
def lecture_detail(request, lecture_id):
    if request.method == "GET":
        lecture = get_object_or_404(Lecture, id=lecture_id)
        return render(request, 'myLecture.html', {'lecture': lecture})

@login_required
def lecture_list(request):
        if request.method == "GET":
            lectures = Lecture.objects.select_related('professor__base_user').all()
            return render(request, 'lectureApply.html', {'lectures': lectures})

def noticeWrite(request):
    if request.method =="GET":
        return render(request, 'noticeWrite.html')

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
        return redirect('lecture_detail')