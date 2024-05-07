from datetime import datetime

import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import Anticipation
from model_bakery import baker
from django.utils.translation import gettext_lazy as _


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
                    f'{payment_user_01_anticipation_related_status_d.anticipation.new_value:_.2f}'
                    .replace('.', ',').replace('_', '.'))


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


def test_title_approved_payments(resp_filter_denied_user_01):
    """
    Certifies that the title for denied payments
    is present.
    """
    assert_contains(resp_filter_denied_user_01, _('Denied anticipation'))


def test_new_value_titles_denied(resp_filter_denied_user_01):
    """
    Certifies that new value title is present when
    filtering denied payments.
    """
    assert_contains(resp_filter_denied_user_01, '<div class="payment-value">Novo valor (R$)</div>')
    assert_contains(resp_filter_denied_user_01, '<div>Fornecedor - Valor orig.</div>')
    assert_contains(resp_filter_denied_user_01, '<div class="payment-due-date">Novo '
                                                'vencimento<span>/</span></div>')


def test_new_infos_denied_filter(resp_filter_denied_user_01,
                                 payment_user_01_anticipation_related_status_d):
    """
    Certifies that the new payment infos are shown when
    filtering approved payments.
    """
    new_due_date = (datetime
                    .strptime(payment_user_01_anticipation_related_status_d.anticipation.new_due_date, '%Y-%m-%d')
                    .strftime('%d/%m/%Y'))
    assert_contains(resp_filter_denied_user_01,
                    f'{payment_user_01_anticipation_related_status_d.anticipation.new_value:_.2f}'
                    .replace('.', ',').replace('_', '.'))
    assert_contains(resp_filter_denied_user_01, payment_user_01_anticipation_related_status_d)
    assert_contains(resp_filter_denied_user_01, new_due_date)
