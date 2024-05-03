from datetime import date

from workatcodev.payments.models import Payment, Supplier
from django.core.exceptions import ObjectDoesNotExist


def get_available_payments(user):
    """
    Returns all available payments for a specific user/supplier. Available payments
    must have due_date greater than today and there must be no anticipations related.
    """
    supplier = None
    try:
        supplier = Supplier.objects.get(user=user)
    except ObjectDoesNotExist:
        pass
    today_date = date.today()
    if supplier:
        payments = Payment.objects.filter(due_date__gt=today_date, anticipation=None, supplier=supplier.id)
        return list(payments)
    payments = Payment.objects.filter(due_date__gt=today_date, anticipation=None)
    return list(payments)


def get_unavailable_payments(user):
    """
    Returns all unavailable payments for a specific user. An unavailable payment
    must have its due_date smaller or equal today's date and there may be or not
    anticipation related. If there is an anticipation, its status has to be 'PC'
    (pending confirmation).
    """
    supplier = None
    try:
        supplier = Supplier.objects.get(user=user)
    except ObjectDoesNotExist:
        pass
    today = date.today()
    q1 = Payment.objects.prefetch_related('anticipation_set').filter(due_date__lte=today)
    payments = q1.exclude(anticipation__status='A').exclude(anticipation__status='D')
    if supplier:
        payments = payments.filter(supplier=supplier.id)
    return list(payments)
