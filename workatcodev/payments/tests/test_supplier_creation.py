from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from workatcodev.django_assertions import assert_contains
from workatcodev.payments.models import Supplier


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


def test_post_new_supplier(client_logged_operator, user_01):
    """
    Creates a new supplier and certifies:
    - the supplier was saved in database;
    - the user is redirected to home page.
    """
    resp = client_logged_operator.post(reverse('payments:new_supplier'), {'user': user_01.pk,
                                                                          'corporate_name': 'Supplier Company',
                                                                          'cnpj': '11111111111111'})
    assert Supplier.objects.filter(corporate_name='Supplier Company').exists()
    assert resp.status_code == 302
    assert resp.url == reverse('payments:home')


def test_message_error_invalid_cnpj(client_logged_operator, user_01):
    """
    Certifies that an error message is shown when
    typed an invalid CNPJ and the supplier is not saved.
    """
    resp = client_logged_operator.post(reverse('payments:new_supplier'), {'user': user_01.pk,
                                                                          'corporate_name': 'Supplier Company',
                                                                          'cnpj': 'invalid123'})
    assert_contains(resp, _("Type only numbers, please."))
    assert Supplier.objects.filter(corporate_name='Supplier Company').exists() is False
