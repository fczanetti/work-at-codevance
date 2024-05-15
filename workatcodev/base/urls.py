from django.urls import path
from workatcodev.base.views import denied_access, Mylogin


app_name = 'base'
urlpatterns = [
    path('denied_access/', denied_access, name='denied_access'),
    path('accounts/login/', Mylogin.as_view(), name='login')
]
