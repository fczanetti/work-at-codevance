from django.urls import path
from workatcodev.payments.views import home

app_name = 'payments'
urlpatterns = [
    path('', home, name='home')
]
