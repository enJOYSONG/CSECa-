from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^my_lecture_list$', my_lecture_list, name='my_lecture_list'),
    url(r'^lecture_detail$', lecture_detail, name='lecture_detail'),
    url(r'^lecture_list$', lecture_list, name='lecture_list'),
    url(r'^noticeWrite$', noticeWrite, name='noticeWrite')

]
