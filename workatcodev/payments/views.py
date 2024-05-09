from django.shortcuts import render, redirect, reverse

from workatcodev.payments import facade
from workatcodev.payments.forms import FilterStatusForm, AnticipationForm, NewPaymentForm
from django.utils.translation import gettext_lazy as _

from workatcodev.payments.models import Payment, Supplier


def home(request):
    TITLES = {'A': _('Available for anticipation'),
              'U': _('Unavailable for anticipation'),
              'PC': _('Pending anticipation confirmation'),
              'AN': _('Anticipated payments'),
              'D': _('Denied anticipation')}
    GET_PAYM_FUNC = {'A': facade.get_available_payments,
                     'U': facade.get_unavailable_payments,
                     'PC': facade.get_pend_conf_payments,
                     'AN': facade.get_approved_payments,
                     'D': facade.get_denied_payments}
    if request.method == 'POST':
        form = FilterStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            function = GET_PAYM_FUNC[status]
            payments = function(request.user)
            context = {'payments': payments, 'form': form, 'title': TITLES[status], 'status': status}
            return render(request, 'payments/home.html', context=context)
    status = 'A'
    function = GET_PAYM_FUNC[status]
    payments = function(request.user)
    form = FilterStatusForm()
    context = {'payments': payments, 'form': form, 'title': TITLES[status], 'status': status}
    return render(request, 'payments/home.html', context=context)


def anticipation(request, id):
    payment = Payment.objects.get(id=id)
    if not payment.is_available():
        raise ValueError(_('Unavailable payments can not be anticipated.'))
    if request.method == 'POST':
        new_due_date = request.POST['new_due_date']
        new_value = facade.new_payment_value(payment, new_due_date)
        data = {'payment': f'{payment.pk}', 'new_due_date': request.POST['new_due_date'], 'new_value': new_value}
        form = AnticipationForm(data)
        if form.is_valid():
            form.save()
            return redirect(reverse('payments:home'))
        else:
            return render(request, 'payments/anticipation.html', {'form': form, 'payment': payment})
    form = AnticipationForm()
    return render(request, 'payments/anticipation.html', {'form': form, 'payment': payment})


def new_payment(request):
    context = {'form': NewPaymentForm()}
    supplier = None
    if Supplier.objects.filter(user=request.user).exists():
        supplier = Supplier.objects.get(user=request.user)
        context['supplier'] = supplier
    if request.method == 'POST':
        if supplier:
            data = {'supplier': supplier, 'due_date': request.POST['due_date'], 'value': request.POST['value']}
            form = NewPaymentForm(data)
        else:
            form = NewPaymentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect(reverse('payments:home'))
        else:
            return render(request, 'payments/new_payment.html', context=context)
    return render(request, 'payments/new_payment.html', context=context)
