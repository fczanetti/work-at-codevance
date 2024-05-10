from datetime import datetime

import pytest
from django.urls import reverse
from model_bakery import baker
from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import Anticipation
from django.utils.translation import gettext_lazy as _
from workatcodev.utils import format_value


@pytest.fixture
def resp_filter_approved_user_01(client_logged_supplier_01,
                                 payment_supplier_01,
                                 payment_user_01_anticipation_related_status_a,
                                 payment_user_01_anticipation_related_status_d,
                                 payment):
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
    v = format_value(payment_user_01_anticipation_related_status_a.anticipation.new_value)
    new_d = payment_user_01_anticipation_related_status_a.anticipation.new_due_date
    new_due_date = (datetime.strptime(new_d, '%Y-%m-%d').strftime('%d/%m/%Y'))
    assert_contains(resp_filter_approved_user_01, v)
    assert_contains(resp_filter_approved_user_01, payment_user_01_anticipation_related_status_a)
    assert_contains(resp_filter_approved_user_01, new_due_date)


def test_supplier_01_paym_with_no_anticip_not_shown(resp_filter_approved_user_01,
                                                    payment_supplier_01):
    """
    Certifies that payments for which no anticipation were
    created are not shown.
    """
    assert_not_contains(resp_filter_approved_user_01, payment_supplier_01)


def test_suppl_01_paym_anticip_status_d_not_shown(resp_filter_approved_user_01,
                                                  payment_user_01_anticipation_related_status_d):
    """
    Certifies that payments with anticipation denied are
    not shown when filtering approved.
    """
    v = format_value(payment_user_01_anticipation_related_status_d.anticipation.new_value)
    assert_not_contains(resp_filter_approved_user_01, v)


def test_approved_payments_supplier_02_not_shown(client_logged_supplier_01,
                                                 supplier_02, payment, supplier_01):
    """
    Certifies that payments with approved anticipation from other users/suppliers
    are not shown.
    """
    payment.supplier = supplier_02
    payment.save()
    baker.make(Anticipation, payment=payment, status='AN')
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'AN'})
    v = format_value(payment.anticipation.new_value)
    assert_not_contains(resp, v)


def test_title_approved_payments(resp_filter_approved_user_01):
    """
    Certifies that the title for approved payments
    is present.
    """
    assert_contains(resp_filter_approved_user_01, _('Anticipated payments'))


def test_new_value_titles_approved(resp_filter_approved_user_01):
    """
    Certifies that new value title is present when
    filtering approved payments.
    """
    assert_contains(resp_filter_approved_user_01, '<div class="payment-value">Novo valor (R$)</div>')
    assert_contains(resp_filter_approved_user_01, '<div>Fornecedor - Valor orig.</div>')
    assert_contains(resp_filter_approved_user_01, '<div class="payment-due-date">Novo '
                                                  'vencimento<span>/</span></div>')


def test_logged_common_user_can_see_all_approved_payments(client_logged_common_user,
                                                          payment_user_01_anticipation_related_status_a,
                                                          payment, supplier_02):
    """
    Certifies that a user that is neither a supplier nor an operator
    can see payments from all suppliers.
    """
    baker.make(Anticipation, payment=payment, status='A')
    payment.supplier = supplier_02
    payment.save()
    resp = client_logged_common_user.post(reverse('payments:home'), {'status': 'AN'})
    v1 = format_value(payment_user_01_anticipation_related_status_a.anticipation.new_value)
    v2 = format_value(payment.anticipation.new_value)
    assert_contains(resp, v1)
    assert_contains(resp, v2)


def test_logged_operator_can_see_all_approved_payments(client_logged_operator,
                                                       payment_user_01_anticipation_related_status_a,
                                                       payment, supplier_02):
    """
    Certifies that an operator can see payments from all suppliers.
    """
    baker.make(Anticipation, payment=payment, status='A')
    payment.supplier = supplier_02
    payment.save()
    resp = client_logged_operator.post(reverse('payments:home'), {'status': 'AN'})
    v1 = format_value(payment_user_01_anticipation_related_status_a.anticipation.new_value)
    v2 = format_value(payment.anticipation.new_value)
    assert_contains(resp, v1)
    assert_contains(resp, v2)
