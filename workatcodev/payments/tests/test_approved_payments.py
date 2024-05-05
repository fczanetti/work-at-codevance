import pytest
from django.urls import reverse
from model_bakery import baker
from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import Anticipation


@pytest.fixture
def resp_filter_approved_user_01(client_logged_supplier_01,
                                 payment_user_01_anticipation_related_status_a,
                                 payment,
                                 payment_user_01_anticipation_related_status_d):
    """
    Creates a request filtering payments for which the anticipations
    were approved and returns a response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'AN'})
    return resp


def test_supplier_01_approved_payments(resp_filter_approved_user_01,
                                       payment_user_01_anticipation_related_status_a):
    """
    Certifies that payments with approved anticipation are shown
    when filtered.
    """
    assert_contains(resp_filter_approved_user_01,
                    f'{payment_user_01_anticipation_related_status_a.value:_.2f}'
                    .replace('.', ',').replace('_', '.'))


def test_supplier_01_paym_with_no_anticip_not_shown(resp_filter_approved_user_01, payment):
    """
    Certifies that payments for which no anticipation were
    created are not shown.
    """
    assert_not_contains(resp_filter_approved_user_01,
                        f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))


def test_suppl_01_paym_anticip_status_d_not_shown(resp_filter_approved_user_01,
                                                  payment_user_01_anticipation_related_status_d):
    """
    Certifies that payments with anticipation denied are
    not shown when filtering approved.
    """
    assert_not_contains(resp_filter_approved_user_01,
                        f'{payment_user_01_anticipation_related_status_d.value:_.2f}'
                        .replace('.', ',').replace('_', '.'))


def test_approved_payments_supplier_02_not_shown(client_logged_supplier_01, supplier_02, payment, supplier_01):
    """
    Certifies that approved payments from other users/suppliers
     are not shown.
    """
    payment.supplier = supplier_02
    payment.save()
    baker.make(Anticipation, payment=payment, status='AN')
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'AN'})
    assert_not_contains(resp, f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))
