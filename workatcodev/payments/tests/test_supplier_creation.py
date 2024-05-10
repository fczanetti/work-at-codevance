from django.contrib.auth.models import Group


def test_supplier_group_created(supplier_01):
    """
    Certifies that a supplier group is created when
    creating/saving a supplier.
    """
    assert Group.objects.filter(name='Suppliers').exists()


def test_supplier_added_to_group(supplier_01):
    """
    Certifies the supplier, after created, was added
    to the supplier group.
    """
    assert supplier_01.user.groups.filter(name='Suppliers').exists()


def test_supplier_has_permissions(supplier_01):
    """
    Certifies that a supplier, when created, has permissions
    to add payments and add anticipations.
    """
    assert supplier_01.user.has_perm('payments.add_payment')
    assert supplier_01.user.has_perm('payments.add_anticipation')
