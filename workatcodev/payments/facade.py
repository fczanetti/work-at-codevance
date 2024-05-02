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
