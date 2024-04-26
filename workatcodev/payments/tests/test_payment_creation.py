from datetime import date, timedelta

import pytest
from model_bakery import baker
from workatcodev.payments.models import Payment


@pytest.fixture
def payment(db):
    """
    Creates and return an instance of Payment.
    """
    d = date.today() + timedelta(days=5)
    payment = baker.make(Payment, due_date=d)
    return payment


@pytest.fixture
def unavailable_payment(db):
    """
    Creates and returns an unavailable payment. A payment is classified as unavailable when
    its due date has already arrived or passed.
    """
    today = date.today()
    unav_paym = baker.make(Payment, due_date=today)
    return unav_paym


def test_payment_status_after_creation(payment):
    """
    Certifies that a payment created has the status = Available.
    """
    assert payment.status == 'A'


def test_unavailable_status_payment(unavailable_payment):
    """
    Certifies that a payment created with due date earlier or equal today's date
    has its status changed to unavailable.
    """
    assert unavailable_payment.status == 'U'
