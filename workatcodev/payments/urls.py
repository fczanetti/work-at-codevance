from django.urls import path
from workatcodev.payments.views import home, anticipation

app_name = 'payments'
urlpatterns = [
    path('', home, name='home'),
    path('anticipation/<int:id>', anticipation, name='anticipation')
]
