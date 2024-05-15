from django.shortcuts import render
from django.contrib.auth.views import LoginView


def denied_access(request):
    return render(request, 'base/denied_access.html')


class Mylogin(LoginView):
    template_name = 'registration/login.html'
