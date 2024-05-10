import pytest
from django.urls import reverse
from datetime import date

from workatcodev.django_assertions import assert_contains, assert_not_contains
from django.utils.translation import gettext_lazy as _

from workatcodev.utils import format_value


@pytest.fixture
def resp_filter_available_user_01(client_logged_supplier_01,
                                  available_payments_user_01,
                                  unavailable_payments_user_01_due_date,
                                  payment_user_01_anticipation_created,
                                  available_payments_user_02):
    """
    Filter available payments for supplier_01 and returns its response.
    """
    resp = client_logged_supplier_01.post(reverse('payments:home'), {'status': 'A'})
    return resp


@pytest.fixture
def resp_filter_available_common_user(client_logged_common_user,
                                      available_payments_user_01,
                                      available_payments_user_02):
    """
    Creates a request by a user that is neither an operator nor a
    supplier and returns a response.
    """
    resp = client_logged_common_user.post(reverse('payments:home'), {'status': 'A'})
    return resp


@pytest.fixture
def resp_filter_available_operator(client_logged_operator,
                                   available_payments_user_01,
                                   available_payments_user_02):
    """
    Creates a request by an operator and returns a response.
    """
    resp = client_logged_operator.post(reverse('payments:home'), {'status': 'A'})
    return resp


def test_filter_available_payments_user_01(resp_filter_available_user_01,
                                           available_payments_user_01):
    """
    Certifies that user_01 available payments are shown when filtered.
    """
    for payment in available_payments_user_01:
        due_date = date.strftime(payment.due_date, '%d/%m/%Y')
        value = format_value(payment.value)
        assert_contains(resp_filter_available_user_01, payment.supplier)
        assert_contains(resp_filter_available_user_01, due_date)
        assert_contains(resp_filter_available_user_01, value)


def test_unavailable_payments_not_shown_due_date(resp_filter_available_user_01,
                                                 unavailable_payments_user_01_due_date):
    """
    Certifies that payments with due date smaller or equal today are not
    shown when filtering available payments.
    """
    for payment in unavailable_payments_user_01_due_date:
        due_date = date.strftime(payment.due_date, '%d/%m/%Y')
        assert_not_contains(resp_filter_available_user_01, due_date)


def test_unavailable_payments_not_shown_anticipation_created(resp_filter_available_user_01,
                                                             payment_user_01_anticipation_created):
    """
    Certifies that payments with anticipation created and related are not
    shown when filtering available payments.
    """
    v = format_value(payment_user_01_anticipation_created.value)
    assert_not_contains(resp_filter_available_user_01, v)


def test_available_payments_from_supplier_02_not_shown(resp_filter_available_user_01,
                                                       available_payments_user_02):
    """
    Certifies that available payments from supplier_02 are not shown when
    supplier_01 is logged and filtering available.
    """
    for payment in available_payments_user_02:
        v = format_value(payment.value)
        assert_not_contains(resp_filter_available_user_01, payment.supplier)
        assert_not_contains(resp_filter_available_user_01, v)


def test_title_available_payments(resp_filter_available_user_01):
    """
    Certifies that the title for available payments
    is present.
    """
    assert_contains(resp_filter_available_user_01, _('Available for anticipation'))


def test_link_anticipation(resp_filter_available_user_01,
                           available_payments_user_01):
    """
    Certifies that the links for creating anticipation are present.
    """
    for payment in available_payments_user_01:
        assert_contains(resp_filter_available_user_01, payment.create_anticipation())


def test_common_user_can_see_avail_payments_from_all_supp(resp_filter_available_common_user,
                                                          available_payments_user_01,
                                                          available_payments_user_02):
    """
    Certifies that a common user can see available payments from all suppliers.
    """
    for payment in available_payments_user_01:
        v = format_value(payment.value)
        assert_contains(resp_filter_available_common_user, v)
    for payment in available_payments_user_02:
        v = format_value(payment.value)
        assert_contains(resp_filter_available_common_user, v)


# def test_anticip_button_not_present_for_common_user(resp_filter_available_common_user,
#                                                     available_payments_user_01):
#     """
#     Certifies that the button for creating anticipation
#     is not shown to a common user.
#     """
#     for payment in available_payments_user_01:
#         assert_not_contains(resp_filter_available_common_user, f'<a class="anticipation-link" '
#                                                                f'href="{payment.create_anticipation()}">Antecipar</a>')


def test_operator_can_see_avail_payments_from_all_supp(resp_filter_available_operator,
                                                       available_payments_user_01,
                                                       available_payments_user_02):
    """
    Certifies that an operator can see available payments from all suppliers.
    """
    for payment in available_payments_user_01:
        v = format_value(payment.value)
        assert_contains(resp_filter_available_operator, v)
    for payment in available_payments_user_02:
        v = format_value(payment.value)
        assert_contains(resp_filter_available_operator, v)
