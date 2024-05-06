from datetime import date

import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_filter_unavailable_user_01(client_logged_supplier_01,
                                    unavailable_payments_user_01_due_date,
                                    payment_user_01_anticipation_related_status_a,
                                    payment_user_01_anticipation_related_status_d,
                                    unavailable_payments_user_02_due_date):
    """
    Creates a request by user_01/supplier_01 filtering
    unavailable payments ant returns its response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'U'})
    return resp


def test_supplier_01_unavailable_payments_due_date(resp_filter_unavailable_user_01,
                                                   unavailable_payments_user_01_due_date):
    """
    Certifies that supplier_01 unavailable payments due to due_date
    are shown when filtered.
    """
    for payment in unavailable_payments_user_01_due_date:
        due_date = date.strftime(payment.due_date, '%d/%m/%Y')
        assert_contains(resp_filter_unavailable_user_01, payment.supplier)
        assert_contains(resp_filter_unavailable_user_01, due_date)
        assert_contains(resp_filter_unavailable_user_01,
                        f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))


def test_supplier_01_unav_payments_anticip_related_status_a_or_d(resp_filter_unavailable_user_01,
                                                                 payment_user_01_anticipation_related_status_a,
                                                                 payment_user_01_anticipation_related_status_d):
    """
    Certifies that payments with an anticipation related with status 'A' or 'D'
    (Approved or Denied) are not shown when filtering unavailable.
    """
    assert_not_contains(resp_filter_unavailable_user_01,
                        f"""<div class="payment-value">{payment_user_01_anticipation_related_status_a.value:_.2f}"""
                        .replace('.', ',').replace('_', '.'))
    assert_not_contains(resp_filter_unavailable_user_01,
                        f"""<div class="payment-value">{payment_user_01_anticipation_related_status_d.value:_.2f}"""
                        .replace('.', ',').replace('_', '.'))


def test_unavailable_payments_from_supplier_02_not_shown(resp_filter_unavailable_user_01,
                                                         unavailable_payments_user_02_due_date):
    """
    Certifies that unavailable payments from other suppliers/users are not shown.
    """
    for payment in unavailable_payments_user_02_due_date:
        assert_not_contains(resp_filter_unavailable_user_01, payment.supplier)
        assert_not_contains(resp_filter_unavailable_user_01,
                            f"""<div class="payment-value">{payment.value:_.2f}"""
                            .replace('.', ',').replace('_', '.'))


def test_title_unavailable_payments(resp_filter_unavailable_user_01):
    """
    Certifies that the title for unavailable payments
    is present.
    """
    assert_contains(resp_filter_unavailable_user_01, 'Indisponíveis para antecipação')
