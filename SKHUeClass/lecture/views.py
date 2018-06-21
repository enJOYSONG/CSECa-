from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render,redirect, get_object_or_404
from .models import Lecture, LectureNotice, LectureQuestion, QuestionComment, Assignment, LectureInfo, Team
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from account.models import BaseUser, Student
from django.db.models import Case, When,Value, CharField,F,Q,Sum
from libraries.libuser import user_check
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

@login_required
@permission_required('lecture.add_lecture', raise_exception=True)
def main(request):
    if request.method == "GET":

        return render(request, 'lectureCreate.html')

    if request.method == "POST":
        user = user_check(request)

        new_lecture = Lecture(name=request.POST['lecture_name'],
                              professor=user)
        new_lecture.save()

        return redirect('lecture_list')

@login_required
def my_lecture_list(request):
    if request.method == "GET":
        user = user_check(request)
        lectures = None
        is_permissioned = False
        if type(user) is Student:
            lectures = Lecture.objects.filter(id__in=LectureInfo.objects.filter(student=user).values('lecture_id'))

        else:
            lectures = Lecture.objects.filter(professor=user)
            is_permissioned = True

        return render(request, 'lectureList.html', {'lectures': lectures})

    if request.method == "POST":
        user = user_check(request)

        lecture_id = request.POST['h1']
        lecture = Lecture.objects.get(id=lecture_id)

        if LectureInfo.objects.filter(lecture=lecture, student=user).exists() == False:
            lecture_info = LectureInfo(lecture=lecture, student=user)
            lecture_info.save()


        return redirect('my_lecture_list')

@login_required
def lecture_detail(request, lecture_id):
    if request.method == "GET":
        user = user_check(request)
        is_permissioned = False
        lecture = get_object_or_404(Lecture.objects.prefetch_related('lecturenotice_set', 'lecturequestion_set'), id=lecture_id)

        if type(user) is Student:
            notice_list = lecture.lecturenotice_set.annotate(is_done=Case(When(assignment__student=user, then=Value("Y")), default=Value("N"),output_field=CharField()),
                                                             point=Case(When(assignment__student=user,
                                                                               then='assignment__point'), default=Value(""),
                                                                          output_field=CharField())

                                                             ).order_by('-id')

            if lecture.ta == user:
                is_permissioned = True



        else:
            notice_list = lecture.lecturenotice_set.order_by('-id')

            if lecture.professor == user:
                is_permissioned = True


        question_list = lecture.lecturequestion_set.order_by('-id')
        team_list = lecture.team_set.order_by('name')


        return render(request, 'myLecture.html', {'lecture': lecture, 'notice_list': notice_list, 'question_list': question_list, \
                                                  'team_list':team_list, 'is_permissioned':is_permissioned})

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
        file_url = settings.AWS_CLOUDFRONT_DOMAIN + "/" + request.FILES['file'].name

        if notice.assignment_set.filter(student=student):
            assignment = notice.assignment_set.get(student=student)
            assignment.description = request.POST['description']
            assignment.file = file_url
        else:
            assignment = Assignment()
            assignment.notice = notice
            assignment.student = student
            assignment.description = request.POST['description']
            assignment.file = file_url

        assignment.save()

        default_storage.save(request.FILES['file'].name, request.FILES['file'])
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
        info = LectureInfo.objects.filter(lecture=lecture)
        student_list = Assignment.objects.filter(notice__lecture=lecture).values('student_id').annotate(username=F('student__base_user__username'),
                                                                                                        fullname=F('student__base_user__first_name'),
                                                                                                        grade=F('student__grade'),
                                                                                                        department=F('student__base_user__department'),
                                                                                                        total_point=Sum('point'))

        return render(request, 'studentList.html', {'student_list':student_list})

    # if request.method=="POST":

@login_required
def team(request, lecture_or_team_id):
    if request.method == "POST":
        lecture = get_object_or_404(Lecture, id=lecture_or_team_id)
        if Team.objects.filter(Q(lecture=lecture, leader=request.user.student) | \
                               Q(lecture=lecture, members=request.user.student)).exists():
            return JsonResponse({'status': 300}, safe=False)

        else:
            team = Team()
            team.lecture = lecture
            team.name = request.user.get_full_name() + "팀"
            team.leader = request.user.student
            team.save()

        #return redirect('lecture_detail', lecture_id)
        return JsonResponse({'status': 200, 'redirect_url':  lecture_or_team_id}, safe=False)

    if request.method == "PUT":
        team = get_object_or_404(Team, id=lecture_or_team_id)
        if Team.objects.filter(Q(lecture=team.lecture, leader=request.user.student)|
                               Q(lecture=team.lecture, members=request.user.student)).exists():
            return JsonResponse({'status': 300}, safe=False)
        else:
            team.members.add(request.user.student)

        return JsonResponse({'status': 200, 'redirect_url':  team.lecture.id}, safe=False)

