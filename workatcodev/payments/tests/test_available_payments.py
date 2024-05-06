import pytest
from django.urls import reverse
from datetime import date

from workatcodev.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_filter_available_user_01(client_logged_supplier_01, available_payments_user_01,
                                  unavailable_payments_user_01_due_date,
                                  payment_user_01_anticipation_created,
                                  available_payments_user_02):
    """
    Filter available payments for supplier_01 and returns its response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'A'})
    return resp


def test_filter_available_payments_user_01(resp_filter_available_user_01, available_payments_user_01):
    """
    Certifies that user_01 available payments are shown when filtered.
    """
    for payment in available_payments_user_01:
        due_date = date.strftime(payment.due_date, '%d/%m/%Y')
        assert_contains(resp_filter_available_user_01, payment.supplier)
        assert_contains(resp_filter_available_user_01, due_date)
        assert_contains(resp_filter_available_user_01,
                        f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))


def test_unavailable_payments_not_shown_due_date(resp_filter_available_user_01, unavailable_payments_user_01_due_date):
    """
    Certifies that payments with due date smaller or equal today are not
    shown when filtering available payments.
    """
    for payment in unavailable_payments_user_01_due_date:
        due_date = date.strftime(payment.due_date, '%d/%m/%Y')
        assert_not_contains(resp_filter_available_user_01, due_date)


def test_unavailable_payments_not_shown_anticipation_created(
        resp_filter_available_user_01, payment_user_01_anticipation_created):
    """
    Certifies that payments with anticipation created and related are not
    shown when filtering available payments.
    """
    assert_not_contains(resp_filter_available_user_01,
                        f"""<div class="payment-value">{payment_user_01_anticipation_created.value:_.2f}"""
                        .replace('.', ',').replace('_', '.'))


def test_available_payments_from_supplier_02_not_shown(resp_filter_available_user_01, available_payments_user_02):
    """
    Certifies that available payments from supplier_02 are not shown when
    supplier_01 is logged and filtering available.
    """
    for payment in available_payments_user_02:
        assert_not_contains(resp_filter_available_user_01, payment.supplier)
        assert_not_contains(resp_filter_available_user_01, f'{payment.value: _.2f}'
                            .replace('.', ',').replace('_', '.'))


def test_title_available_payments(resp_filter_available_user_01):
    """
    Certifies that the title for available payments
    is present.
    """
    assert_contains(resp_filter_available_user_01, 'Disponíveis para antecipação')
