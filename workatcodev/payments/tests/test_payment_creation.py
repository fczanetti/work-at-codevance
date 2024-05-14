from datetime import date, timedelta
import pytest

from workatcodev.django_assertions import assert_contains
from workatcodev.payments.models import Payment
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


@pytest.fixture
def resp_payment_creation_by_operator(client_logged_operator, supplier_02):
    """
    Creates a payment by operator via payment creation page and
    returns a response.
    """
    due_date = date.today() + timedelta(days=10)
    resp = client_logged_operator.post(reverse('payments:new_payment'), {'supplier': supplier_02.pk,
                                                                         'due_date': due_date,
                                                                         'value': 12345.12})
    return resp


def test_payment_created_successfully_supp_01(resp_payment_creation_by_operator):
    """
    Certifies that the payment was created successfully.
    """
    assert Payment.objects.filter(value=12345.12).exists() is True


def test_payment_not_created_with_due_date_earlier_than_today(client_logged_operator, supplier_01):
    """
    Certifies that no payments are created with due_date
    earlier than today.
    """
    today = date.today() - timedelta(days=1)
    resp = client_logged_operator.post(reverse('payments:new_payment'), {'supplier': supplier_01.pk,
                                                                         'due_date': today,
                                                                         'value': 1000})
    assert_contains(resp, _('Due date must be today or some day after.'))
    assert Payment.objects.filter(value=1000).filter(due_date=today).exists() is False


def test_payment_creation_not_informing_supplier(client_logged_supplier_01, supplier_01):
    """
    Certifies that a payment can be created without having to select the
    supplier. For this to work, the supplier must create its own payments,
    and it will be identified from the request.
    """
    today = date.today() + timedelta(days=10)
    client_logged_supplier_01.post(reverse('payments:new_payment'), {'due_date': today,
                                                                     'value': 25})
    assert Payment.objects.filter(value=25).filter(supplier=supplier_01).exists() is True


def test_payment_not_created_with_value_smaller_than_or_equal_zero(client_logged_operator, supplier_01):
    """
    Certifies that no payments are created with value smaller than or equal zero.
    """
    d = date.today() - timedelta(days=1)
    resp = client_logged_operator.post(reverse('payments:new_payment'), {'supplier': supplier_01.pk,
                                                                         'due_date': d,
                                                                         'value': 0})
    assert_contains(resp, _('The value must be bigger than zero.'))
    assert Payment.objects.filter(value=0).filter(due_date=d).exists() is False
