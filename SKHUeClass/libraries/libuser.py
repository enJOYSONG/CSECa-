from django.core.exceptions import ObjectDoesNotExist

def user_check(request):
    try:
        request.user.student
    except ObjectDoesNotExist:
        return request.user.professor
    else:
        return request.user.student