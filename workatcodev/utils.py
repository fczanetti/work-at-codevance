from django.core.exceptions import ObjectDoesNotExist
from datetime import date


def format_value(v):
    """
    Receives a value and returns it formatted
    in dots and coma (1.000.000,00).
    """
    return f'{v:_.2f}'.replace('.', ',').replace('_', '.')


def get_supplier_or_none(user):
    """
    Receives a user and checks if there is a supplier
    related. If so, the supplier is returned, otherwise
    None is returned.
    """
    if not user.is_authenticated:
        return None
    from workatcodev.payments.models import Supplier
    supplier = None
    try:
        supplier = Supplier.objects.get(user=user)
    except ObjectDoesNotExist:
        return supplier
    return supplier


def available_anticipation(antic_id):
    """
    Checks if anticipation exists and confirms that it
    meets the necessary requirements to be approved. If
    so, the anticipation is returned.
    The requirements are:
    - the id must be correct for an anticipation;
    - the anticipation status has to be equal to 'PC';
    - finally, the new_due_date must be today or some
    day after.
    """
    from workatcodev.payments.models import Anticipation
    try:
        anticipation = Anticipation.objects.get(id=antic_id, status='PC', new_due_date__gte=date.today())
    except ObjectDoesNotExist:
        return None
    return anticipation
