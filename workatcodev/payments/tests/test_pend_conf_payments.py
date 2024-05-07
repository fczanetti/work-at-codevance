from datetime import date, timedelta, datetime

import pytest
from django.urls import reverse
from model_bakery import baker

from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import Anticipation, Payment
from django.utils.translation import gettext_lazy as _


@pytest.fixture
def pending_confirm_payment_user_02(db, supplier_02):
    """
    Creates and returns a payment with anticipation requested
    but not approved or denied (status='PC').
    """
    d = date.today() + timedelta(days=5)
    payment = baker.make(Payment, supplier=supplier_02, due_date=d)
    baker.make(Anticipation, payment=payment)
    return payment


@pytest.fixture
def resp_filter_pending_conf_user_01(client_logged_supplier_01,
                                     payment_user_01_anticipation_created,
                                     payment_user_01_anticipation_related_status_a,
                                     payment_user_01_anticipation_related_status_d,
                                     pending_confirm_payment_user_02):
    """
    Creates a request filtering payments with status = 'PC'
    (pending confirmation) and returns the response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'PC'})
    return resp


# def test_filter_pending_confirmation_supplier_01(resp_filter_pending_conf_user_01,
#                                                  payment_user_01_anticipation_created):
#     """
#     Certifies that pending confirmation payments are shown when
#     filtered.
#     """
#     due_date = date.strftime(payment_user_01_anticipation_created.due_date, '%d/%m/%Y')
#     assert_contains(resp_filter_pending_conf_user_01, payment_user_01_anticipation_created.supplier)


def test_filter_pend_conf_supplier_01_status_a(resp_filter_pending_conf_user_01,
                                               payment_user_01_anticipation_related_status_a):
    """
    Certifies that a payment is not shown if it has an anticipation
    related and this anticipation has status = 'A' (Approved).
    """
    assert_not_contains(resp_filter_pending_conf_user_01,
                        f'{payment_user_01_anticipation_related_status_a.anticipation.new_value:_.2f}'
                        .replace('.', ',').replace('_', '.'))


def test_filter_pend_conf_supplier_01_status_d(resp_filter_pending_conf_user_01,
                                               payment_user_01_anticipation_related_status_d):
    """
    Certifies that a payment is not shown if it has an anticipation
    related and this anticipation has status = 'D' (Denied).
    """
    assert_not_contains(resp_filter_pending_conf_user_01,
                        f'{payment_user_01_anticipation_related_status_d.anticipation.new_value:_.2f}'
                        .replace('.', ',').replace('_', '.'))


def test_filter_pend_conf_supplier_01_orig_due_date_reached(db, payment, supplier_01, client_logged_supplier_01):
    """
    Certifies that a payment is not shown if its original due date
    was already reached.
    """
    baker.make(Anticipation, payment=payment)
    payment.due_date = date.today()
    payment.supplier = supplier_01
    payment.save()
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'PC'})
    assert_not_contains(resp, f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))


def test_pend_conf_supplier_02_not_shown(resp_filter_pending_conf_user_01, pending_confirm_payment_user_02):
    """
    Certifies that no payments from other suppliers are shown.
    """
    assert_not_contains(resp_filter_pending_conf_user_01, pending_confirm_payment_user_02.supplier)
    assert_not_contains(resp_filter_pending_conf_user_01,
                        f'{pending_confirm_payment_user_02.value:_.2f}'
                        .replace('.', ',').replace('_', '.'))


def test_title_pend_confirm_payments(resp_filter_pending_conf_user_01):
    """
    Certifies that the title for pending confirmation payments
    is present.
    """
    assert_contains(resp_filter_pending_conf_user_01, _('Pending anticipation confirmation'))


def test_new_value_titles_pend_conf(resp_filter_pending_conf_user_01):
    """
    Certifies that new value title is present when
    filtering pending confirmation payments.
    """
    assert_contains(resp_filter_pending_conf_user_01, '<div class="payment-value">Novo valor (R$)</div>')
    assert_contains(resp_filter_pending_conf_user_01, '<div>Fornecedor - Valor orig.</div>')
    assert_contains(resp_filter_pending_conf_user_01, '<div class="payment-due-date">Novo '
                                                      'vencimento<span>/</span></div>')


def test_new_infos_pend_conf_filter(resp_filter_pending_conf_user_01,
                                    payment_user_01_anticipation_created):
    """
    Certifies that the new payment infos are shown when
    filtering pending confirmation payments.
    """
    new_due_date = (datetime
                    .strptime(payment_user_01_anticipation_created.anticipation.new_due_date, '%Y-%m-%d')
                    .strftime('%d/%m/%Y'))
    assert_contains(resp_filter_pending_conf_user_01,
                    f'{payment_user_01_anticipation_created.anticipation.new_value:_.2f}'
                    .replace('.', ',').replace('_', '.'))
    assert_contains(resp_filter_pending_conf_user_01, payment_user_01_anticipation_created)
    assert_contains(resp_filter_pending_conf_user_01, new_due_date)
