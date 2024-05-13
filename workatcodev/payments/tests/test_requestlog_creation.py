from datetime import date
import pytest
from django.urls import reverse
from workatcodev.payments.models import RequestLog


@pytest.fixture
def new_anticipation(client_logged_supplier_01, payment_supplier_01):
    """
    Request an anticipation for a payment and certifies that a request log is created.
    """
    new_due_date = date.today()
    client_logged_supplier_01.post(reverse('payments:anticipation',
                                           args=(payment_supplier_01.pk,)),
                                   {'new_due_date': new_due_date})
    return payment_supplier_01.anticipation


def test_request_log_anticip_creation(new_anticipation):
    """
    Certifies that a request log is created when creating a new anticipation.
    """
    log = RequestLog.objects.filter(anticipation__new_value=new_anticipation.new_value)
    assert log.exists()
    assert log[0].action == 'R'


def test_request_log_anticip_approval(new_anticipation, client_logged_operator):
    """
    Certifies that a request log is created when an anticipation is approved.
    """
    client_logged_operator.post(reverse('payments:update_antic',
                                        kwargs={'act': 'A', 'id': new_anticipation.pk})),
    log = RequestLog.objects.filter(anticipation=new_anticipation, action='A')
    assert log.exists()


def test_request_log_anticip_denial(new_anticipation, client_logged_operator):
    """
    Certifies that a request log is created when an anticipation is denied.
    """
    client_logged_operator.post(reverse('payments:update_antic',
                                        kwargs={'act': 'D', 'id': new_anticipation.pk})),
    log = RequestLog.objects.filter(anticipation=new_anticipation, action='D')
    assert log.exists()
