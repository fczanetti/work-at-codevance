from django.urls import path
from workatcodev.base.views import denied_access, Mylogin, new_user


app_name = 'base'
urlpatterns = [
    path('denied_access/', denied_access, name='denied_access'),
    path('accounts/login/', Mylogin.as_view(), name='login'),
    path('new_user/', new_user, name='new_user'),
]
