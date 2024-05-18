import pytest
from datetime import date, timedelta

from workatcodev.django_assertions import assert_contains
from workatcodev.payments.models import Anticipation, Payment
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from unittest import mock


@pytest.fixture
def resp_anticipation_creation(payment_supplier_01, client_logged_supplier_01):
    """
    Creates a request creating an anticipation from
    anticipation page and returns the response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:anticipation', args=(payment_supplier_01.pk,)),
                                          {'new_due_date': date.today()})
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
                                   {'new_due_date': new_due_date})
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
                                       {'new_due_date': new_due_date})


def test_attempt_creation_antic_for_date_earlier_than_today(db, payment_supplier_01, client_logged_supplier_01):
    """
    Certifies that an anticipation is not created with a new due date earlier than the
    day of creation, and the user is informed via error message.
    """
    new_due_date = str(date.today() - timedelta(days=1))
    resp = client_logged_supplier_01.post(reverse('payments:anticipation',
                                                  args=(payment_supplier_01.pk,)),
                                          {'new_due_date': new_due_date})
    assert_contains(resp, _('The new payment date must be today or some day after.'))


@mock.patch('workatcodev.payments.views.send_email.delay_on_commit')
def test_send_email_called(mock_send_email, payment, client_logged_operator):
    """
    Certifies that send_email() is called when creating an anticipation.
    """
    rev, post_d = reverse('payments:anticipation', args=(payment.pk,)), {'new_due_date': date.today()}
    client_logged_operator.post(rev, post_d)
    mock_send_email.assert_called_once_with(sub='new_ant',
                                            recipient=[f'{payment.supplier.user.email}'],
                                            ant_id=payment.anticipation.pk)
