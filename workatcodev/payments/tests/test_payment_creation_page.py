import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from workatcodev.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_payment_creation_page_supplier_01(client_logged_supplier_01):
    """
    Creates a request to payment creation page and
    returns a response.
    """
    resp = client_logged_supplier_01.get(reverse('payments:new_payment'))
    return resp


@pytest.fixture
def resp_payment_creation_page_operator(client_logged_operator):
    """
    Creates a request by an operator to payment creation page and
    returns a response.
    """
    resp = client_logged_operator.get(reverse('payments:new_payment'))
    return resp


def test_operator_can_access_paym_creation_page(resp_payment_creation_page_operator):
    """
    Certifies that an operator can access payment creation page.
    """
    assert resp_payment_creation_page_operator.status_code == 200


def test_status_code_paym_creat_page_supp_01(resp_payment_creation_page_supplier_01):
    """
    Certifies that payment creation page is loaded successfully
    when requested by a supplier.
    """
    assert resp_payment_creation_page_supplier_01.status_code == 200


def test_title_new_payment_page(resp_payment_creation_page_supplier_01):
    """
    Certifies that the titles of the page are present.
    """
    assert_contains(resp_payment_creation_page_supplier_01, f'<title>{_("Payments - New payment")}</title>')
    assert_contains(resp_payment_creation_page_supplier_01, f'<h1 class="main-content-title">{_("New payment")}</h1>')


def test_form_items_new_payment_page(resp_payment_creation_page_supplier_01):
    """
    Certifies that form items are present on the page.
    """
    assert_contains(resp_payment_creation_page_supplier_01, '<label for="id_due_date">')
    assert_contains(resp_payment_creation_page_supplier_01, '<input type="date" name="due_date" '
                                                            'required id="id_due_date">')
    assert_contains(resp_payment_creation_page_supplier_01, '<input type="number" name="value" step="any" '
                                                            'required id="id_value">')
    assert_contains(resp_payment_creation_page_supplier_01, '<a href="/" id="canc-button">')
    assert_contains(resp_payment_creation_page_supplier_01, '<button type="submit" id="conf-button">')


def test_supplier_select_not_present(resp_payment_creation_page_supplier_01):
    """
    Certifies that the possibility of selecting a supplier when
    creating a payment is not present for a supplier.
    """
    assert_not_contains(resp_payment_creation_page_supplier_01, f'<label for="id_supplier">{_("Supplier:")}</label>')
    assert_not_contains(resp_payment_creation_page_supplier_01, '<select name="supplier" required id="id_supplier">')


def test_supplier_select_present_for_operator(resp_payment_creation_page_operator):
    """
    Certifies that the possibility of selecting a supplier when
    creating a payment is present for an operator.
    """
    assert_contains(resp_payment_creation_page_operator, '<label for="id_supplier">')
    assert_contains(resp_payment_creation_page_operator, '<select name="supplier" required id="id_supplier">')


def test_common_user_can_not_access_paym_creat_page(client_logged_common_user):
    """
    Certifies that a common user can not access
    payment creation page.
    """
    resp = client_logged_common_user.get(reverse('payments:new_payment'))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access')
