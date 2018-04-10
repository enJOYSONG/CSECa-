from django.shortcuts import render
from rest_framework.views import APIView

class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')
