from datetime import date, timedelta
from model_bakery import baker
import pytest

from workatcodev.payments.models import Payment


def test_payment_not_created_with_due_date_earlier_than_today(db):
    """
    Certifies that no payments are created with due_date
    earlier than today.
    """
    today = date.today() - timedelta(days=1)
    with pytest.raises(ValueError):
        baker.make(Payment, due_date=today)


def test_payment_created_with_due_date_greater_than_today(db):
    """
    Certifies that payments are created with due_date
    greater than or equal today.
    """
    today = date.today()
    payment = baker.make(Payment, due_date=today, value=1)
    assert Payment.objects.filter(id=payment.pk).exists() is True
