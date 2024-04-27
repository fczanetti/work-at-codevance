import pytest
from model_bakery import baker
from workatcodev.payments.models import Payment
from datetime import date, timedelta


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
