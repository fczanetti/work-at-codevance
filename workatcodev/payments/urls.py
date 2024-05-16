from django.urls import path
from workatcodev.payments.views import home, anticipation, new_payment, update_antic, logs, new_supplier

app_name = 'payments'
urlpatterns = [
    path('', home, name='home'),
    path('<str:status>', home, name='home'),
    path('anticipation/<int:id>', anticipation, name='anticipation'),
    path('update/<str:act>/<int:id>', update_antic, name='update_antic'),
    path('new_payment/', new_payment, name='new_payment'),
    path('new_supplier/', new_supplier, name='new_supplier'),
    path('logs/', logs, name='logs')
]
