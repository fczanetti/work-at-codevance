from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import permission_required

from workatcodev.payments import facade
from workatcodev.payments.forms import FilterStatusForm, AnticipationForm, NewPaymentForm
from django.utils.translation import gettext_lazy as _
from workatcodev.utils import get_supplier_or_none
from workatcodev.payments.models import Payment


def home(request):
    # The TITLES are the ones to be shown at home page
    # acording to what payments were filtered.
    TITLES = {'A': _('Available for anticipation'),
              'U': _('Unavailable for anticipation'),
              'PC': _('Pending anticipation confirmation'),
              'AN': _('Anticipated payments'),
              'D': _('Denied anticipation')}

    # Select what function to execute based on what
    # payments were filtered.
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

            # Execute to return the payments filtered. If
            # the user is not a supplier, payments from all
            # suppliers will be returned.
            payments = function(request.user)
            context = {'payments': payments, 'form': form, 'title': TITLES[status], 'status': status}
            return render(request, 'payments/home.html', context=context)

    # When request.method = GET, the available
    # ('A') payments will be brought.
    status = 'A'
    function = GET_PAYM_FUNC[status]
    payments = function(request.user)
    form = FilterStatusForm()
    context = {'payments': payments, 'form': form, 'title': TITLES[status], 'status': status}
    return render(request, 'payments/home.html', context=context)


@permission_required('payments.add_anticipation', login_url='/denied_access/')
def anticipation(request, id):
    payment = Payment.objects.get(id=id)

    # If there is a supplier related to current user
    # it will be brought, otherwise None will return
    if get_supplier_or_none(request.user):
        if payment.supplier.user.id != request.user.id:
            return redirect(reverse('base:denied_access'))

    # If payment is not available (due_date reached) an error will
    # be raised, because no anticipations can be created from it
    if not payment.is_available():
        raise ValueError(_('Unavailable payments can not be anticipated.'))
    if request.method == 'POST':
        new_due_date = request.POST['new_due_date']

        # Calculating the new value for a payment
        new_value = facade.new_payment_value(payment, new_due_date)

        # This data was created because of new_value. new_value is not
        # filled in the form, it has to be calculated and then bound
        # to it to be saved
        data = {'payment': f'{payment.pk}',
                'new_due_date': request.POST['new_due_date'],
                'new_value': new_value}
        form = AnticipationForm(data)
        if form.is_valid():
            form.save()
            return redirect(reverse('payments:home'))
        else:
            return render(request, 'payments/anticipation.html',
                          {'form': form, 'payment': payment})
    form = AnticipationForm()
    return render(request, 'payments/anticipation.html',
                  {'form': form, 'payment': payment})


@permission_required('payments.add_payment', login_url='/denied_access/')
def new_payment(request):
    context = {'form': NewPaymentForm()}

    # If there is a supplier related to current user
    # it will be brought, otherwise None will return
    supplier = get_supplier_or_none(request.user)
    if supplier:
        context['supplier'] = supplier
    if request.method == 'POST':
        if supplier:

            # If a supplier is adding a new payment it can not select
            # the supplier to complete the form, the select option is
            # not shown. In this case the supplier has to be brought
            # from the request, added to data and then to the form
            data = {'supplier': supplier,
                    'due_date': request.POST['due_date'],
                    'value': request.POST['value']}
            form = NewPaymentForm(data)
        else:

            # If it is an operator adding a new payment it is able to
            # select for which supplier it is adding to, and in this
            # case request.POST has all the necessary information to
            # be saved.
            form = NewPaymentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect(reverse('payments:home'))
        else:
            return render(request, 'payments/new_payment.html', context=context)
    return render(request, 'payments/new_payment.html', context=context)


@permission_required('payments.change_anticipation', login_url='/denied_access/')
def approval(request, id):
    return render(request, 'payments/approval.html')
