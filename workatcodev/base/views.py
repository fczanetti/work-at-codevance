from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse
from workatcodev.base.forms import NewUserForm


def denied_access(request):
    return render(request, 'base/denied_access.html')


class Mylogin(LoginView):
    template_name = 'registration/login.html'


@login_required
@permission_required('base.add_user', login_url='/denied_access/')
def new_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('payments:home'))
        else:
            return render(request, 'base/new_user.html', {'form': form})
    form = NewUserForm()
    return render(request, 'base/new_user.html', {'form': form})
