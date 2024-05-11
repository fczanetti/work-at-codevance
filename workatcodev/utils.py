from django.core.exceptions import ObjectDoesNotExist


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
    from workatcodev.payments.models import Supplier
    supplier = None
    try:
        supplier = Supplier.objects.get(user=user)
    except ObjectDoesNotExist:
        return supplier
    return supplier
