import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import Anticipation
from model_bakery import baker


@pytest.fixture
def resp_filter_denied_user_01(client_logged_supplier_01,
                               payment_user_01_anticipation_related_status_d):
    """
    Creates a request filtering payments with anticipation denied
    and returns its response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'D'})
    return resp


def test_supplier_01_denied_payments(resp_filter_denied_user_01,
                                     payment_user_01_anticipation_related_status_d):
    """
    Certifies that payments with denied anticipation are shown
    when filtered.
    """
    assert_contains(resp_filter_denied_user_01,
                    f'{payment_user_01_anticipation_related_status_d.value:_.2f}'.replace('.', ',')
                    .replace('_', '.'))


def test_supplier_01_paym_with_no_anticip_not_shown(resp_filter_denied_user_01, payment):
    """
    Certifies that payments for which no anticipation were
    created are not shown.
    """
    assert_not_contains(resp_filter_denied_user_01,
                        f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))


def test_suppl_01_paym_anticip_status_a_not_shown(resp_filter_denied_user_01,
                                                  payment_user_01_anticipation_related_status_a):
    """
    Certifies that payments with anticipation approved are
    not shown when filtering denied.
    """
    assert_not_contains(resp_filter_denied_user_01,
                        f'{payment_user_01_anticipation_related_status_a.value:_.2f}'
                        .replace('.', ',').replace('_', '.'))


def test_denied_payments_supplier_02_not_shown(client_logged_supplier_01, supplier_02, payment, supplier_01):
    """
    Certifies that denied payments from other users/suppliers
     are not shown.
    """
    payment.supplier = supplier_02
    payment.save()
    baker.make(Anticipation, payment=payment, status='D')
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'D'})
    assert_not_contains(resp, f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))
