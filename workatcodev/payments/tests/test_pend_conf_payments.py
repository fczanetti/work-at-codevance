from datetime import date, datetime, timedelta

import pytest
from django.urls import reverse
from model_bakery import baker

from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import Anticipation
from django.utils.translation import gettext_lazy as _

from workatcodev.utils import format_value


@pytest.fixture
def resp_filter_pending_conf_user_01(client_logged_supplier_01,
                                     payment_user_01_anticipation_created,
                                     payment_user_01_anticipation_related_status_a,
                                     payment_user_01_anticipation_related_status_d,
                                     payment_user_02_anticipation_created,
                                     payment_supplier_01):
    """
    Creates a request filtering payments with status = 'PC'
    (pending confirmation) and returns the response.
    """
    resp = client_logged_supplier_01.get(reverse('payments:home'), {'status': 'PC'})
    return resp


@pytest.fixture
def resp_filter_pending_conf_operator(client_logged_operator,
                                      payment_user_01_anticipation_created,
                                      payment_user_02_anticipation_created):
    """
    Creates a request by an operator filtering
    pending confirmation payments.
    """
    resp = client_logged_operator.get(reverse('payments:home'), {'status': 'PC'})
    return resp


@pytest.fixture
def resp_filter_pending_conf_common_user(client_logged_common_user,
                                         payment_user_01_anticipation_created,
                                         payment_user_02_anticipation_created):
    """
    Creates a request by a common user filtering
    pending confirmation payments.
    """
    resp = client_logged_common_user.get(reverse('payments:home'), {'status': 'PC'})
    return resp


def test_filter_pend_conf_supplier_01_status_a_or_d_not_shown(resp_filter_pending_conf_user_01,
                                                              payment_user_01_anticipation_related_status_a,
                                                              payment_user_01_anticipation_related_status_d):
    """
    Certifies that a payment is not shown if it has an anticipation
    related and this anticipation has status = 'A' (Approved) or
    'D' (Denied).
    """
    va = format_value(payment_user_01_anticipation_related_status_a.anticipation.new_value)
    vd = format_value(payment_user_01_anticipation_related_status_d.anticipation.new_value)
    assert_not_contains(resp_filter_pending_conf_user_01, va)
    assert_not_contains(resp_filter_pending_conf_user_01, vd)


def test_filter_pend_conf_supplier_01_orig_due_date_reached(db, client_logged_supplier_01,
                                                            payment_supplier_01):
    """
    Certifies that a payment is not shown if its original due date was already reached.
    """
    baker.make(Anticipation, payment=payment_supplier_01)
    payment_supplier_01.due_date = date.today()
    payment_supplier_01.save()
    v = format_value(payment_supplier_01.anticipation.new_value)
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'PC'})
    assert_not_contains(resp, v)


def test_pend_conf_supplier_02_not_shown(resp_filter_pending_conf_user_01,
                                         payment_user_02_anticipation_created):
    """
    Certifies that no payments from other suppliers are shown.
    """
    v = format_value(payment_user_02_anticipation_created.anticipation.new_value)
    assert_not_contains(resp_filter_pending_conf_user_01, payment_user_02_anticipation_created.supplier)
    assert_not_contains(resp_filter_pending_conf_user_01, v)


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
    assert_contains(resp_filter_pending_conf_user_01, f'<div class="payment-value">{_("New value (US$)")}</div>')
    assert_contains(resp_filter_pending_conf_user_01, f'<div>{_("Supplier - Original value")}</div>')
    assert_contains(resp_filter_pending_conf_user_01, f'<div '
                                                      f'class="payment-due-date">{_("New due date")}<span>/</span>'
                                                      f'</div>')


def test_new_infos_pend_conf_filter(resp_filter_pending_conf_user_01,
                                    payment_user_01_anticipation_created):
    """
    Certifies that the new payment infos are shown when
    filtering pending confirmation payments.
    """
    new_d = payment_user_01_anticipation_created.anticipation.new_due_date
    new_due_date = (datetime.strptime(new_d, '%Y-%m-%d').strftime('%d/%m/%Y'))
    v = format_value(payment_user_01_anticipation_created.anticipation.new_value)
    assert_contains(resp_filter_pending_conf_user_01, v)
    assert_contains(resp_filter_pending_conf_user_01, payment_user_01_anticipation_created)
    assert_contains(resp_filter_pending_conf_user_01, new_due_date)


def test_payment_with_no_anticipation_not_shown(resp_filter_pending_conf_user_01,
                                                payment_supplier_01):
    """
    Certifies that payments with no anticipation
    created are not shown.
    """
    assert_not_contains(resp_filter_pending_conf_user_01, payment_supplier_01)


def test_operator_can_see_pend_conf_paym_from_all_supp(resp_filter_pending_conf_operator,
                                                       payment_user_01_anticipation_created,
                                                       payment_user_02_anticipation_created):
    """
    Certifies that an operator can see pending confirmation
    payments from all suppliers.
    """
    assert_contains(resp_filter_pending_conf_operator, payment_user_01_anticipation_created)
    assert_contains(resp_filter_pending_conf_operator, payment_user_02_anticipation_created)


def test_common_user_can_see_pend_conf_paym_from_all_supp(resp_filter_pending_conf_common_user,
                                                          payment_user_01_anticipation_created,
                                                          payment_user_02_anticipation_created):
    """
    Certifies that an operator can see pending confirmation
    payments from all suppliers.
    """
    assert_contains(resp_filter_pending_conf_common_user, payment_user_01_anticipation_created)
    assert_contains(resp_filter_pending_conf_common_user, payment_user_02_anticipation_created)


def test_approval_or_denial_buttons_not_present_for_suppliers(resp_filter_pending_conf_user_01,
                                                              payment_user_01_anticipation_created):
    """
    Certifies that approval or denial buttons are not present for suppliers.
    """
    assert_not_contains(resp_filter_pending_conf_user_01,
                        f'<a class="approval-anticip-link" '
                        f'href="{payment_user_01_anticipation_created.anticipation.get_approval_url()}">{_("Approve")}'
                        f'</a>')
    assert_not_contains(resp_filter_pending_conf_user_01,
                        f'<a class="denial-anticip-link" '
                        f'href="{payment_user_01_anticipation_created.anticipation.get_denial_url()}">{_("Deny")}</a>')


def test_approval_or_denial_buttons_not_present_for_common_user(resp_filter_pending_conf_common_user,
                                                                payment_user_01_anticipation_created):
    """
    Certifies that approval or denial buttons are not present for common users.
    """
    assert_not_contains(resp_filter_pending_conf_common_user,
                        f'<a class="approval-anticip-link" '
                        f'href="{payment_user_01_anticipation_created.anticipation.get_approval_url()}">{_("Approve")}'
                        f'</a>')
    assert_not_contains(resp_filter_pending_conf_common_user,
                        f'<a class="denial-anticip-link" '
                        f'href="{payment_user_01_anticipation_created.anticipation.get_denial_url()}">{_("Deny")}</a>')


def test_approval_and_denial_buttons_present_for_operators(resp_filter_pending_conf_operator,
                                                           payment_user_02_anticipation_created):
    """
    Certifies that approval and denial buttons are present for operators.
    """
    assert_contains(resp_filter_pending_conf_operator,
                    f'<a class="approval-anticip-link" '
                    f'href="{payment_user_02_anticipation_created.anticipation.get_approval_url()}">{_("Approve")}</a>')
    assert_contains(resp_filter_pending_conf_operator,
                    f'<a class="denial-anticip-link" '
                    f'href="{payment_user_02_anticipation_created.anticipation.get_denial_url()}">{_("Deny")}</a>')


def test_outdated_anticipation_not_shown(payment, client_logged_operator):
    """
    Certifies that approve or deny buttons are not shown
    for a payment that has an anticipation with new due
    date before today. This is because these anticipations
    are not available to approve or deny anymore.
    """
    d = date.today() - timedelta(days=1)
    ant = baker.make(Anticipation, payment=payment, new_due_date=d)
    resp = client_logged_operator.get(reverse('payments:home'), {'status': 'PC'})
    assert_not_contains(resp, ant.get_approval_url())
    assert_not_contains(resp, ant.get_denial_url())
    assert_contains(resp, _('Date exceeded'))
