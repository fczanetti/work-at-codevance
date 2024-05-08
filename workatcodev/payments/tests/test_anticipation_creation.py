import pytest
from datetime import date, timedelta
from model_bakery import baker

from workatcodev.payments.models import Anticipation, Payment
from django.urls import reverse


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


@pytest.fixture
def resp_anticipation_creation(payment, supplier_01, client_logged_supplier_01):
    """
    Creates a request creating an anticipation from
    anticipation page and returns the response.
    """
    payment.supplier = supplier_01
    resp = client_logged_supplier_01.post(reverse('payments:anticipation', args=(payment.pk,)),
                                          {'new_due_date': date.today(), 'payment': payment.pk})
    return resp


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


def test_anticipation_created_via_form(resp_anticipation_creation, payment):
    """
    Certifies that an anticipation was created.
    """
    assert Anticipation.objects.filter(payment=payment).exists() is True
