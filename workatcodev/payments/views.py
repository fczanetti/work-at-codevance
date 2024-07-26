from datetime import date

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseNotFound
from workatcodev.payments import facade
from workatcodev.payments.forms import FilterStatusForm, AnticipationForm, NewPaymentForm, NewSupplierForm
from django.utils.translation import gettext_lazy as _
from workatcodev.utils import get_supplier_or_none, available_anticipation
# from workatcodev.payments.tasks import send_email
from workatcodev.payments.models import RequestLog, Anticipation


@login_required
def home(request, status='A'):
    # The TITLES are the ones to be shown at home page
    # acording to what payments were filtered.
    TITLES = {'A': _('Available for anticipation'),
              'U': _('Unavailable for anticipation'),
              'PC': _('Pending anticipation confirmation'),
              'AN': _('Anticipated payments'),
              'D': _('Denied anticipation')}
    if status not in TITLES:
        return HttpResponseNotFound(_('Page not found. Make sure the URL is correct.'))

    # Select what function to execute based on what
    # payments were filtered.
    GET_PAYM_FUNC = {'A': facade.get_available_payments,
                     'U': facade.get_unavailable_payments,
                     'PC': facade.get_pend_conf_payments,
                     'AN': facade.get_approved_payments,
                     'D': facade.get_denied_payments}

    # When using the form to filter, the status must be
    # the one chosen. If the URL is typed without chosing
    # a specific status, it will be the standard 'A'
    try:
        status = request.GET['status']
    except KeyError:
        pass
    function = GET_PAYM_FUNC[status]
    payments = function(request.user)
    form = FilterStatusForm(initial={'status': status})
    context = {'payments': payments, 'form': form, 'title': TITLES[status], 'status': status, 'today': date.today()}
    return render(request, 'payments/home.html', context=context)


@login_required
@permission_required('payments.add_anticipation', login_url='/denied_access/')
def anticipation(request, id):
    """
    :param id: A payment ID.
    """
    payment = facade.check_payment_availability(id)

    # If there is a supplier related to current user
    # it will be brought, otherwise None will return
    if get_supplier_or_none(request.user):

        # Checks if a user is trying to anticipate a payment
        # that does not belong to him. If so, he is redirected
        # to denied page
        if payment.supplier.user.id != request.user.id:
            return redirect(reverse('base:denied_access'))

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
            ant = Anticipation.objects.get(payment=payment)
            RequestLog.objects.create(anticipation=ant,
                                      user=request.user, action='R')

            # Sending email informing about the new anticipation (deactivated)
            # send_email.delay_on_commit(sub='new_ant',
            #                            recipient=[f'{payment.supplier.user.email}'],
            #                            ant_id=ant.pk)
            return redirect(reverse('payments:home'))
        else:
            return render(request, 'payments/anticipation.html',
                          {'form': form, 'payment': payment})
    form = AnticipationForm()
    return render(request, 'payments/anticipation.html',
                  {'form': form, 'payment': payment})


@login_required
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


@login_required
@permission_required('payments.change_anticipation', login_url='/denied_access/')
def update_antic(request, act, id):
    """
    :param act: The action to execute in the anticipation, Approve or Deny
    :param id: The anticipation ID
    """
    if act not in ['A', 'D']:
        return HttpResponseNotFound(_('Page not found. Make sure the URL is correct.'))

    # If there is no anticipation available,
    # None will be returned
    anticipation = available_anticipation(id)
    if not anticipation:
        return HttpResponseNotFound(_('Page not found. Make sure this anticipation '
                                      'exists and is pending confirmation.'))
    if request.method == 'POST':
        anticipation.status = act
        anticipation.save()
        RequestLog.objects.create(anticipation=anticipation,
                                  user=request.user, action=act)

        # Sending email informing about the status update (deactivated)
        # send_email.delay_on_commit(sub=act, ant_id=id,
        #                            recipient=[f'{anticipation.payment.supplier.user.email}'])
        return redirect(reverse('payments:home', args=('PC',)))
    context = {'anticipation': anticipation, 'act': act}
    return render(request, 'payments/update_antic.html', context=context)


@login_required
def logs(request):
    # get_logs will check if it is a supplier requesting. If so,
    # only its logs will be brought, otherwise is will bring all
    # logs registered
    reg = facade.get_logs(request.user)
    return render(request, 'payments/logs.html', {'logs': reg})


@login_required
@permission_required('payments.add_supplier', login_url='/denied_access/')
def new_supplier(request):
    if request.method == 'POST':
        form = NewSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('payments:home'))
        else:
            return render(request, 'payments/new_supplier.html', {'form': form})
    form = NewSupplierForm()
    return render(request, 'payments/new_supplier.html', {'form': form})
