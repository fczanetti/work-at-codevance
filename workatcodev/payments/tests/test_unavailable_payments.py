from datetime import date

import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains, assert_not_contains
from django.utils.translation import gettext_lazy as _

from workatcodev.utils import format_value


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
    resp = client_logged_supplier_01.get(reverse('payments:home'), {'status': 'U'})
    return resp


def test_supplier_01_unavailable_payments_due_date(resp_filter_unavailable_user_01,
                                                   unavailable_payments_user_01_due_date):
    """
    Certifies that supplier_01 unavailable payments due to due_date
    are shown when filtered.
    """
    for payment in unavailable_payments_user_01_due_date:
        due_date = date.strftime(payment.due_date, '%d/%m/%Y')
        v = format_value(payment.value)
        assert_contains(resp_filter_unavailable_user_01, payment.supplier)
        assert_contains(resp_filter_unavailable_user_01, due_date)
        assert_contains(resp_filter_unavailable_user_01, v)


def test_supplier_01_unav_payments_anticip_related_status_a_or_d(resp_filter_unavailable_user_01,
                                                                 payment_user_01_anticipation_related_status_a,
                                                                 payment_user_01_anticipation_related_status_d):
    """
    Certifies that payments with an anticipation related with status 'A' or 'D'
    (Approved or Denied) are not shown when filtering unavailable.
    """
    va = format_value(payment_user_01_anticipation_related_status_a.value)
    vd = format_value(payment_user_01_anticipation_related_status_d.value)
    assert_not_contains(resp_filter_unavailable_user_01, va)
    assert_not_contains(resp_filter_unavailable_user_01, vd)


def test_unavailable_payments_from_supplier_02_not_shown(resp_filter_unavailable_user_01,
                                                         unavailable_payments_user_02_due_date):
    """
    Certifies that unavailable payments from other suppliers/users are not shown.
    """
    for payment in unavailable_payments_user_02_due_date:
        v = format_value(payment.value)
        assert_not_contains(resp_filter_unavailable_user_01, payment.supplier)
        assert_not_contains(resp_filter_unavailable_user_01, v)


def test_title_unavailable_payments(resp_filter_unavailable_user_01):
    """
    Certifies that the title for unavailable payments is present.
    """
    assert_contains(resp_filter_unavailable_user_01, _('Unavailable for anticipation'))


def test_supp_01_pend_conf_payments_shown_if_due_date_reached(client_logged_supplier_01,
                                                              payment_user_01_anticipation_created):
    """
    Certifies that payments for which the anticipation is
    pending confirmation are shown if their due_date was
    already reached.
    """
    payment_user_01_anticipation_created.due_date = date.today()
    payment_user_01_anticipation_created.save()
    v = format_value(payment_user_01_anticipation_created.value)
    resp = client_logged_supplier_01.get(reverse('payments:home'), {'status': 'U'})
    assert_contains(resp, v)


def test_common_user_can_see_unav_payments_from_all_supp(client_logged_common_user,
                                                         unavailable_payments_user_01_due_date,
                                                         unavailable_payments_user_02_due_date):
    """
    Certifies that common user can see unavailable payments from all suppliers.
    """
    resp = client_logged_common_user.get(reverse('payments:home'), {'status': 'U'})
    for payment in unavailable_payments_user_01_due_date:
        v = format_value(payment.value)
        assert_contains(resp, v)
    for payment in unavailable_payments_user_02_due_date:
        v = format_value(payment.value)
        assert_contains(resp, v)


def test_operator_can_see_unav_payments_from_all_supp(client_logged_operator,
                                                      unavailable_payments_user_01_due_date,
                                                      unavailable_payments_user_02_due_date):
    """
    Certifies that operators can see unavailable payments from all suppliers.
    """
    resp = client_logged_operator.get(reverse('payments:home'), {'status': 'U'})
    for payment in unavailable_payments_user_01_due_date:
        v = format_value(payment.value)
        assert_contains(resp, v)
    for payment in unavailable_payments_user_02_due_date:
        v = format_value(payment.value)
        assert_contains(resp, v)
