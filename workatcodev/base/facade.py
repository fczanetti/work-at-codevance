from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model


def add_payment_permission(group):
    """
    Adds the permission 'payments.add_payment' to the
    group informed.
    """
    from workatcodev.payments.models import Payment
    content_type = ContentType.objects.get_for_model(Payment)
    permission = Permission.objects.get(codename='add_payment', content_type=content_type)
    group.permissions.add(permission)


def add_anticipation_permission(group):
    """
    Adds the permission 'payments.add_anticipation' to the
    group informed.
    """
    from workatcodev.payments.models import Anticipation
    content_type = ContentType.objects.get_for_model(Anticipation)
    permission = Permission.objects.get(codename='add_anticipation', content_type=content_type)
    group.permissions.add(permission)


def change_anticipation_permission(group):
    """
    Adds the permission 'payments.change_anticipation' to the
    group informed.
    """
    from workatcodev.payments.models import Anticipation
    content_type = ContentType.objects.get_for_model(Anticipation)
    permission = Permission.objects.get(codename='change_anticipation', content_type=content_type)
    group.permissions.add(permission)


def add_user_permission(group):
    """
    Adds the permission 'base.add_user' to the
    group informed.
    """
    content_type = ContentType.objects.get_for_model(get_user_model())
    permission = Permission.objects.get(codename='add_user', content_type=content_type)
    group.permissions.add(permission)
