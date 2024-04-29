from django.shortcuts import render

from workatcodev.payments import facade
from workatcodev.payments.forms import FilterStatusForm
from django.utils.translation import gettext_lazy as _


def home(request):
    TITLES = {'A': _('Available for anticipation'),
              'U': _('Unavailable for anticipation'),
              'PC': _('Pending anticipation confirmation'),
              'AN': _('Anticipated payments'),
              'D': _('Denied anticipation')}
    if request.method == 'POST':
        form = FilterStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            payments = facade.get_payments(status)
            context = {'payments': payments, 'form': form, 'title': TITLES[status]}
            return render(request, 'payments/home.html', context=context)
    status = 'A'
    payments = facade.get_payments(status=status)
    form = FilterStatusForm()
    context = {'payments': payments, 'form': form, 'title': TITLES[status]}
    return render(request, 'payments/home.html', context=context)


def anticipation(request, id):
    return render(request, 'payments/anticipation.html')
