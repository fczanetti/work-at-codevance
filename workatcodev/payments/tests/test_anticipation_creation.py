import pytest
from datetime import date, timedelta

from workatcodev.django_assertions import assert_contains
from workatcodev.payments.models import Anticipation, Payment
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


@pytest.fixture
def resp_anticipation_creation(payment_supplier_01, client_logged_supplier_01):
    """
    Creates a request creating an anticipation from
    anticipation page and returns the response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:anticipation', args=(payment_supplier_01.pk,)),
                                          {'new_due_date': date.today(), 'payment': payment_supplier_01.pk})
    return resp


def test_anticipation_created_via_form(resp_anticipation_creation, payment_supplier_01):
    """
    Certifies that an anticipation was created.
    """
    assert Anticipation.objects.filter(payment=payment_supplier_01).exists() is True


def test_anticipation_value(payment_supplier_01, client_logged_supplier_01):
    """
    Certifies that the new payment value is equal to 984.00.
    """
    due_date = str(date.today() + timedelta(days=17))
    new_due_date = str(date.today() + timedelta(days=1))
    payment_supplier_01.value = 1000
    payment_supplier_01.due_date = due_date
    payment_supplier_01.save()
    client_logged_supplier_01.post(reverse('payments:anticipation', args=(payment_supplier_01.pk,)),
                                   {'new_due_date': new_due_date,
                                    'payment': payment_supplier_01.pk})
    assert Payment.objects.get(id=payment_supplier_01.pk).anticipation.new_value == 984.00


def test_attempt_creation_antic_unavailable_payment(unavailable_payment, supplier_01, client_logged_supplier_01):
    """
    Certifies that an anticipation is not created for an unavailable payment.
    """
    unavailable_payment.supplier = supplier_01
    unavailable_payment.save()
    new_due_date = str(date.today() + timedelta(days=1))
    with pytest.raises(ValueError):
        client_logged_supplier_01.post(reverse('payments:anticipation',
                                               args=(unavailable_payment.pk,)),
                                       {'new_due_date': new_due_date,
                                        'payment': unavailable_payment.pk})


def test_attempt_creation_antic_for_date_earlier_than_today(db, payment, supplier_01, client_logged_supplier_01):
    """
    Certifies that an anticipation is not created with a new due date earlier than the
    day of creation, and the user is informed via error message.
    """
    payment.supplier = supplier_01
    payment.save()
    new_due_date = str(date.today() - timedelta(days=1))
    resp = client_logged_supplier_01.post(reverse('payments:anticipation',
                                                  args=(payment.pk,)),
                                          {'new_due_date': new_due_date,
                                           'payment': payment.pk})
    assert_contains(resp, _('The new payment date must be today or some day after.'))
