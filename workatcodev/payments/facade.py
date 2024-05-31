from datetime import date

from workatcodev import settings
from workatcodev.payments.models import Payment, RequestLog
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from workatcodev.utils import get_supplier_or_none


def get_available_payments(user):
    """
    Returns all available payments for a specific user/supplier. Available payments
    must have due_date greater than today and there must be no anticipations related.
    """
    supplier = get_supplier_or_none(user)
    today_date = date.today()
    if supplier:
        payments = (Payment.objects.select_related('supplier')
                    .filter(due_date__gt=today_date, anticipation=None, supplier=supplier.id))
        return list(payments)
    payments = (Payment.objects.select_related('supplier')
                .filter(due_date__gt=today_date, anticipation=None))
    return list(payments)


def get_unavailable_payments(user):
    """
    Returns all unavailable payments for a specific user. An unavailable payment
    must have its due_date smaller or equal today's date and there may be or not
    anticipation related. If there is an anticipation, its status has to be 'PC'
    (pending confirmation).
    """
    supplier = get_supplier_or_none(user)
    today = date.today()
    q1 = Payment.objects.select_related('supplier').filter(due_date__lte=today)
    payments = q1.exclude(anticipation__status='A').exclude(anticipation__status='D')
    if supplier:
        payments = payments.filter(supplier=supplier.id)
    return list(payments)


def get_pend_conf_payments(user):
    """
    Returns all payments for which were created an anticipation,
    and the anticipations have to have status = 'PC' (pending
    confirmation). Also, the original due_date of the payment
    can not have been reached. If a specific supplier is requesting,
    only its payments will be shown.
    """
    supplier = get_supplier_or_none(user)
    today = date.today()
    q1 = Payment.objects.select_related('supplier').prefetch_related('anticipation')
    payments = q1.filter(anticipation__status='PC').filter(due_date__gt=today)
    if supplier:
        payments = payments.filter(supplier=supplier.id)
    return list(payments)


def get_approved_payments(user):
    """
    Returns all payments for which an anticipation was
    created and approved.
    """
    supplier = get_supplier_or_none(user)
    q1 = Payment.objects.select_related('supplier').prefetch_related('anticipation')
    payments = q1.filter(anticipation__status='A')
    if supplier:
        payments = payments.filter(supplier=supplier.id)
    return list(payments)


def get_denied_payments(user):
    """
    Returns all payments for which an anticipation was
    created but denied.
    """
    supplier = get_supplier_or_none(user)
    q1 = Payment.objects.select_related('supplier').prefetch_related('anticipation')
    payments = q1.filter(anticipation__status='D')
    if supplier:
        payments = payments.filter(supplier=supplier.id)
    return list(payments)


def new_payment_value(payment, new_due_date):
    """
    Calculates the new value for the payment based on the new date of payment.
    """
    i_rate = settings.INTEREST_RATE
    orig_date = date.fromisoformat(str(payment.due_date))
    new_date = date.fromisoformat(str(new_due_date))
    n_days = (orig_date - new_date).days
    new_value = payment.value - (payment.value * (i_rate / 30) * n_days)
    return new_value


def get_logs(user):
    """
    Returns all logs registered. If it is a supplier logged
    and requesting, only logs related to this supplier will
    be brought.
    """
    supplier = get_supplier_or_none(user)
    if supplier:

        # the select_related('user') is necessary here because, in the template,
        # the user field from RequestLog model is requested. If we do not user,
        # each log shown in the template will cause a new database query
        logs = (RequestLog.objects.select_related('anticipation__payment__supplier__user')
                .filter(anticipation__payment__supplier__user=user)
                .select_related('user'))
        return logs
    logs = (RequestLog.objects.select_related('anticipation__payment__supplier')
            .select_related('user')
            .order_by('-created_at'))

    return logs


def check_payment_availability(id):
    """
    Checks if a payment exists and can be anticipated.
    """
    # If the ID informed does not belong to any
    # payment the page is not loaded.
    try:
        payment = Payment.objects.get(id=id)
    except ObjectDoesNotExist:
        raise ValueError(_('This ID does not belong to a payment.'))

    # If payment is not available (due_date reached) an error will
    # be raised, because no anticipations can be created from it
    if not payment.is_available():
        raise ValueError(_('Unavailable payments can not be anticipated.'))

    # Checks if the payment already has an anticipation related
    if hasattr(payment, 'anticipation'):
        raise ValueError(_('This payment already has an anticipation related.'))

    return payment
