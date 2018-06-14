from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from .models import Lecture, LectureNotice, LectureQuestion, QuestionComment, Assignment, LectureInfo
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from account.models import BaseUser, Student
from django.db.models import Case, When,Value, CharField,F
from libraries.libuser import user_check

@login_required
def main(request):
    if request.method == "GET":
        user = user_check(request)

        if type(user) is Student:
            return redirect('my_lecture_list')

        return render(request, 'lectureCreate.html')

    if request.method == "POST":
        user = user_check(request)

        if type(user) is Student:
            return redirect('my_lecture_list')


        new_lecture = Lecture(name=request.POST['lecture_name'],
                              professor=request.user.professor)
        new_lecture.save()
        return redirect('lecture_list')

@login_required
def my_lecture_list(request):
    if request.method == "GET":
        user = user_check(request)

        if type(user) is Student:
            lectures = Lecture.objects.filter(id__in=LectureInfo.objects.filter(student=user).values('lecture_id'))

        lectures = Lecture.objects.filter(professor=user)

        return render(request, 'lectureList.html', {'lectures': lectures})

    if request.method == "POST":
        user = user_check(request)

        if type(user) is Student:
            return redirect('my_lecture_list')

        lecture_id = request.POST['h1']
        lecture = Lecture.objects.get(id=lecture_id)

        if LectureInfo.objects.filter(lecture=lecture, student=request.user.student).exists() == False:
            lecture_info = LectureInfo(lecture=lecture, student=request.user.student)
            lecture_info.save()


        return redirect('my_lecture_list')

@login_required
def lecture_detail(request, lecture_id):
    if request.method == "GET":
        user = user_check(request)
        lecture = get_object_or_404(Lecture.objects.prefetch_related('lecturenotice_set', 'lecturequestion_set'), id=lecture_id)

        if type(user) is Student:
            notice_list = lecture.lecturenotice_set.annotate(is_done=Case(When(assignment__student=user, then=Value("Y")), default=Value("N"),output_field=CharField()),
                                                             point=Case(When(assignment__student=user,
                                                                               then='assignment__point'), default=Value(""),
                                                                          output_field=CharField())

                                                             ).order_by('lecturenotice__id')



        else:
            notice_list = lecture.lecturenotice_set.order_by('-id')


        question_list = lecture.lecturequestion_set.order_by('-id')
        return render(request, 'myLecture.html', {'lecture': lecture, 'notice_list': notice_list, 'question_list': question_list})

@login_required
def lecture_list(request):
        if request.method == "GET":
            lectures = Lecture.objects.select_related('professor__base_user').all()
            return render(request, 'lectureApply.html', {'lectures': lectures})

@login_required
def noticeWrite(request, lecture_id):
    if request.method =="GET":
        return render(request, 'noticeWrite.html', {'lecture_id':  lecture_id})

    if request.method=='POST':
        lec = Lecture.objects.get(id=lecture_id)
        lecNotice = LectureNotice()

        lecNotice.lecture = lec
        lecNotice.title= request.POST['title']
        lecNotice.content = request.POST['content']
        lecNotice.file = request.POST['file']
        lecNotice.is_notice = request.POST.get('is_notice', False)
        lecNotice.is_assignment = request.POST.get('is_assignment', False)
        lecNotice.limited_date = request.POST['limited_date']
        #lecNotice.content_at = django.utils.timezone.now()
        lecNotice.updated_at = timezone.now()


        lecNotice.save()
        return redirect('lecture_detail', lecture_id)

@login_required
def noticeView(request, notice_id):
    if request.method == "GET":
        notice = get_object_or_404(LectureNotice, id=notice_id)
        return render(request, 'noticeView.html', {'notice': notice})

@login_required
def questionWrite(request, lecture_id):
    if request.method =="GET":
        return render(request, 'questionWrite.html', {'lecture_id':  lecture_id})

    if request.method=='POST':
        lec = Lecture.objects.get(id=lecture_id)
        user = BaseUser.objects.get(id=request.user.id)
        lecQuestion = LectureQuestion()

        lecQuestion.lecture = lec
        lecQuestion.person = user
        lecQuestion.title = request.POST['title']
        lecQuestion.content = request.POST['content']
        lecQuestion.file = request.POST['file']


        lecQuestion.save()
        return redirect('lecture_detail', lecture_id)

@login_required
def questionView(request, question_id):
    if request.method == "GET":
        question = get_object_or_404(LectureQuestion, id=question_id)
        comments = question.questioncomment_set.all()
        return render(request, 'questionView.html', {'question': question,'comments': comments})

@login_required
def commentWrite(request, question_id):
    if request.method == "POST":
        question = LectureQuestion.objects.get(id=question_id)
        user = BaseUser.objects.get(id=request.user.id)
        comment = QuestionComment()

        comment.question = question
        comment.person = user
        comment.comment = request.POST['comment']

        comment.save()
        return redirect('questionView', question_id)

@login_required
def assignmentSubmit(request, notice_id):
    if request.method == "GET":
        notice = LectureNotice.objects.get(id=notice_id)
        student = Student.objects.get(base_user=request.user)
        if notice.assignment_set.filter(student=student):
            assignment = notice.assignment_set.get(student=student)
            return render(request, 'assignmentSubmit.html', {'notice': notice, 'assignment': assignment})
        return render(request, 'assignmentSubmit.html', {'notice': notice})
    if request.method == "POST":
        notice = LectureNotice.objects.get(id=notice_id)
        student = Student.objects.get(base_user=request.user)

        if notice.assignment_set.filter(student=student):
            assignment = notice.assignment_set.get(student=student)
            assignment.description = request.POST['description']
            assignment.file = request.POST['file']
        else:
            assignment = Assignment()
            assignment.notice = notice
            assignment.student = student
            assignment.description = request.POST['description']
            assignment.file = request.POST['file']

        assignment.save()
        return redirect('lecture_detail', notice.lecture_id)

@login_required
def assignmentList(request, lecture_id):
    if request.method == "GET":
        lecture = Lecture.objects.get(id=lecture_id)
        notices = lecture.lecturenotice_set.filter(is_assignment=True)
        return render(request, "assignmentList.html", {'lecture':lecture, 'notices': notices})

@login_required
def assignmentCheck(request, notice_id):
    if request.method == "GET":
        notice = LectureNotice.objects.get(id=notice_id)
        assignments = notice.assignment_set.all()
        return render(request, "assignmentCheck.html", {'assignments': assignments})

@login_required
def assignmentPoint(request, assignment_id):
    if request.method == "POST":
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.point = request.POST['point']
        assignment.comment = request.POST['comment']

        assignment.save()
        return redirect('assignmentCheck',assignment.notice_id)


@login_required
def studentList(request, lecture_id):
    if request.method == "GET":
        lecture = Lecture.objects.get(id=lecture_id)
        students = lecture.students.all()

        return render(request, 'studentList.html', {'students': students})

    # if request.method=="POST":