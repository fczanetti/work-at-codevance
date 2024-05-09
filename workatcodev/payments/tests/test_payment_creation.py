from datetime import date, timedelta
import pytest

from workatcodev.django_assertions import assert_contains
from workatcodev.payments.models import Payment
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


@pytest.fixture
def resp_payment_creation_supplier_01(client_logged_supplier_01, supplier_01):
    """
    Creates a payment via payment creation page and
    returns a response.
    """
    due_date = date.today() + timedelta(days=10)
    resp = client_logged_supplier_01.post(reverse('payments:new_payment'), {'supplier': supplier_01.pk,
                                                                            'due_date': due_date,
                                                                            'value': 12345.12})
    return resp


def test_payment_created_successfully_supp_01(resp_payment_creation_supplier_01):
    """
    Certifies that the payment was created successfully.
    """
    assert Payment.objects.filter(value=12345.12).exists() is True


def test_payment_not_created_with_due_date_earlier_than_today(client_logged_supplier_01, supplier_01):
    """
    Certifies that no payments are created with due_date
    earlier than today.
    """
    today = date.today() - timedelta(days=1)
    resp = client_logged_supplier_01.post(reverse('payments:new_payment'), {'supplier': supplier_01.pk,
                                                                            'due_date': today,
                                                                            'value': 1000})
    assert_contains(resp, _('Due date must be today or some day after.'))
    assert Payment.objects.filter(value=1000).filter(due_date=today).exists() is False
