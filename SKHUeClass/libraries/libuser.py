from django.core.exceptions import ObjectDoesNotExist
from account.models import Student
from lecture.models import LectureInfo, Lecture

def user_check(request):
    try:
        request.user.student
    except ObjectDoesNotExist:
        return request.user.professor
    else:
        return request.user.student

