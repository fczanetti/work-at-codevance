from django.urls import path
from workatcodev.payments.views import home, anticipation, new_payment

app_name = 'payments'
urlpatterns = [
    path('', home, name='home'),
    path('anticipation/<int:id>', anticipation, name='anticipation'),
    path('new_payment/', new_payment, name='new_payment')
]
