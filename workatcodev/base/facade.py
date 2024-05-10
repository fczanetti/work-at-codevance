from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


def add_payment_permission(group):
    """
    Adds the permission 'payment.add_payment' to the
    group informed.
    """
    from workatcodev.payments.models import Payment
    content_type = ContentType.objects.get_for_model(Payment)
    permission = Permission.objects.get(codename='add_payment', content_type=content_type)
    group.permissions.add(permission)


def add_anticipation_permission(group):
    """
    Adds the permission 'anticipation.add_anticipation' to the
    group informed.
    """
    from workatcodev.payments.models import Anticipation
    content_type = ContentType.objects.get_for_model(Anticipation)
    permission = Permission.objects.get(codename='add_anticipation', content_type=content_type)
    group.permissions.add(permission)


def change_anticipation_permission(group):
    """
    Adds the permission 'anticipation.change_anticipation' to the
    group informed.
    """
    from workatcodev.payments.models import Anticipation
    content_type = ContentType.objects.get_for_model(Anticipation)
    permission = Permission.objects.get(codename='change_anticipation', content_type=content_type)
    group.permissions.add(permission)
