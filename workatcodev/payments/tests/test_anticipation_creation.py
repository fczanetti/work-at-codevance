import pytest
from datetime import date, timedelta
from model_bakery import baker

from workatcodev.payments.models import Anticipation, Payment


@pytest.fixture
def anticipation(db):
    """
    Creates and returns an Anticipation with expected new value.
    """
    due_date = str(date.today() + timedelta(days=17))
    new_due_date = str(date.today() + timedelta(days=1))
    payment = baker.make(Payment, value=1000, due_date=due_date)
    an = baker.make(Anticipation, payment=payment, new_due_date=new_due_date)
    return an


def test_anticipation_value(anticipation):
    """
    Certifies that the new payment value is equal to 984.00.
    """
    assert anticipation.new_value == 984.00


def test_attempt_creation_antic_unavailable_payment(unavailable_payment):
    """
    Certifies that an anticipation is not created for an unavailable payment.
    """
    with pytest.raises(ValueError):
        baker.make(Anticipation, payment=unavailable_payment)


def test_attempt_creation_antic_for_date_earlier_than_today(db, payment):
    """
    Certifies that an anticipation is not created with a new due date earlier than the
    day of creation.
    """
    new_due_date = str(date.today() - timedelta(days=1))
    with pytest.raises(ValueError):
        baker.make(Anticipation, payment=payment, new_due_date=new_due_date)


def test_anticipation_already_created(db, payment):
    """
    Certifies that no more than one anticipation is created for the same payment.
    """
    baker.make(Anticipation, payment=payment)
    with pytest.raises(ValueError):
        baker.make(Anticipation, payment=payment)


def test_anticipation_update(db, payment):
    """
    Certifies that an anticipation can be changed.
    """
    d = date.today()
    d2 = d + timedelta(days=1)
    ant = baker.make(Anticipation, payment=payment, new_due_date=d)
    ant.new_due_date = d2
    ant.save()
    assert ant.new_due_date == d2
