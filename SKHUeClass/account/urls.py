from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^login$', login, name='login'),
    url(r'^join$', join, name='join'),
    url(r'^mypage$', userinfo, name='mypage'),
    url(r'^logout$', logoutUser, name='logout'),
]
