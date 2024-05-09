from django.urls import path
from workatcodev.base.views import denied_access


app_name = 'base'
urlpatterns = [
    path('denied_access/', denied_access, name='denied_access')
]
