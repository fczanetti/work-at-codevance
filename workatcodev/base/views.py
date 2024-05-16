from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import permission_required, login_required


def denied_access(request):
    return render(request, 'base/denied_access.html')


class Mylogin(LoginView):
    template_name = 'registration/login.html'


@login_required
@permission_required('base.add_user', login_url='/denied_access/')
def new_user(request):
    return render(request, 'base/new_user.html')
