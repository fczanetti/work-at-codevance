from django.urls import path
from workatcodev.payments.views import home, anticipation, new_payment, approval

app_name = 'payments'
urlpatterns = [
    path('', home, name='home'),
    path('<str:status>', home, name='home'),
    path('anticipation/<int:id>', anticipation, name='anticipation'),
    path('approval/<int:id>', approval, name='approval'),
    path('new_payment/', new_payment, name='new_payment')
]
