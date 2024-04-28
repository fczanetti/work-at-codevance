from django.shortcuts import render

from workatcodev.payments import facade


def home(request):
    available_payments = facade.get_available_payments()
    context = {'available_payments': available_payments}
    return render(request, 'payments/home.html', context=context)
