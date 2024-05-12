from datetime import datetime

import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains, assert_not_contains
from django.utils.translation import gettext_lazy as _

from workatcodev.utils import format_value


@pytest.fixture
def resp_filter_denied_user_01(client_logged_supplier_01,
                               payment_user_01_anticipation_related_status_d,
                               payment_user_02_anticipation_related_status_d,
                               payment_user_01_anticipation_related_status_a,
                               payment_user_01_anticipation_created,
                               payment_supplier_01, payment):
    """
    Creates a request filtering payments with anticipation denied
    and returns its response.
    """
    resp = client_logged_supplier_01.get(reverse('payments:home'), {'status': 'D'})
    return resp


def test_supplier_01_denied_payments(resp_filter_denied_user_01,
                                     payment_user_01_anticipation_related_status_d):
    """
    Certifies that payments with denied anticipation are shown when filtered.
    """
    v = format_value(payment_user_01_anticipation_related_status_d.anticipation.new_value)
    new_d = payment_user_01_anticipation_related_status_d.anticipation.new_due_date
    new_due_date = (datetime.strptime(new_d, '%Y-%m-%d').strftime('%d/%m/%Y'))
    assert_contains(resp_filter_denied_user_01, v)
    assert_contains(resp_filter_denied_user_01, payment_user_01_anticipation_related_status_d)
    assert_contains(resp_filter_denied_user_01, new_due_date)


def test_supplier_01_paym_with_no_anticip_not_shown(resp_filter_denied_user_01,
                                                    payment_supplier_01):
    """
    Certifies that payments for which no anticipation were created are not shown.
    """
    assert_not_contains(resp_filter_denied_user_01, payment_supplier_01)


def test_suppl_01_paym_anticip_status_a_not_shown(resp_filter_denied_user_01,
                                                  payment_user_01_anticipation_related_status_a):
    """
    Certifies that payments with anticipation approved are
    not shown when filtering denied.
    """
    v = format_value(payment_user_01_anticipation_related_status_a.anticipation.new_value)
    assert_not_contains(resp_filter_denied_user_01, v)


def test_denied_payments_supplier_02_not_shown(resp_filter_denied_user_01,
                                               payment_user_02_anticipation_related_status_d):
    """
    Certifies that denied payments from other users/suppliers are not shown.
    """
    v = format_value(payment_user_02_anticipation_related_status_d.anticipation.new_value)
    assert_not_contains(resp_filter_denied_user_01, v)


def test_title_approved_payments(resp_filter_denied_user_01):
    """
    Certifies that the title for denied payments is present.
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


def test_payments_with_anticip_status_pc_not_shown(resp_filter_denied_user_01,
                                                   payment_user_01_anticipation_created):
    """
    Certifies that an anticipation with status PC (pending
    confirmation) is not shown when filtering denied.
    """
    v = format_value(payment_user_01_anticipation_created.anticipation.new_value)
    assert_not_contains(resp_filter_denied_user_01, v)


def test_logged_common_user_can_see_paym_from_all_suppl(client_logged_common_user,
                                                        payment_user_01_anticipation_related_status_d,
                                                        payment_user_02_anticipation_related_status_d):
    """
    Certifies that a common user can see denied payments from all suppliers.
    """
    v1 = format_value(payment_user_01_anticipation_related_status_d.anticipation.new_value)
    v2 = format_value(payment_user_02_anticipation_related_status_d.anticipation.new_value)
    resp = client_logged_common_user.get(reverse('payments:home'), {'status': 'D'})
    assert_contains(resp, v1)
    assert_contains(resp, v2)


def test_logged_operator_can_see_paym_from_all_suppl(client_logged_operator,
                                                     payment_user_01_anticipation_related_status_d,
                                                     payment_user_02_anticipation_related_status_d):
    """
    Certifies that an operator can see denied payments from all suppliers.
    """
    v1 = format_value(payment_user_01_anticipation_related_status_d.anticipation.new_value)
    v2 = format_value(payment_user_02_anticipation_related_status_d.anticipation.new_value)
    resp = client_logged_operator.get(reverse('payments:home'), {'status': 'D'})
    assert_contains(resp, v1)
    assert_contains(resp, v2)
