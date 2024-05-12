import pytest
from django.urls import reverse
from workatcodev.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_home_page_logged_user(client_logged_common_user,
                               available_payments_user_01):
    """
    Creates a request to home page with authenticated
    user and returns its response.
    """
    resp = client_logged_common_user.get(reverse('payments:home'))
    return resp


@pytest.fixture
def resp_home_page_logged_user_no_payments_available(client_logged_common_user):
    """
    Creates a request to home page with authenticated
    user and returns its response. No payments are available in this response.
    """
    resp = client_logged_common_user.get(reverse('payments:home'))
    return resp


def test_home_page_logged_user(resp_home_page_logged_user):
    """
    Certify that home page is loaded successfully.
    """
    assert resp_home_page_logged_user.status_code == 200


def test_title_home_page(resp_home_page_logged_user):
    """
    Certifies that home page title is present.
    """
    assert_contains(resp_home_page_logged_user, '<title>Pagamentos - Home</title>')


def test_links_navbar(resp_home_page_logged_user):
    """
    Certify that navbar links are present.
    """
    assert_contains(resp_home_page_logged_user, '<a class="navbar-link" href="">Início</a>')
    assert_contains(resp_home_page_logged_user, '<a class="navbar-link" href="">Histórico</a>')


def test_filter_form_home_page_exists(resp_home_page_logged_user):
    """
    Certifies that there is a form for filtering payments status in the home page.
    """
    assert_contains(resp_home_page_logged_user, '<form id="filter_form" action="/" method="GET">')
    assert_contains(resp_home_page_logged_user, '<label for="id_status">Status:</label>')
    assert_contains(resp_home_page_logged_user, '<select name="status" id="id_status">')
    assert_contains(resp_home_page_logged_user, '<button id="filter_button" type="submit">Filtrar</button>')


def test_title_payment_infos_present(resp_home_page_logged_user):
    """
    Certifies that the titles of payment infos are present
    when there is at least one payment listed.
    """
    assert_contains(resp_home_page_logged_user, '<div>Fornecedor</div>')
    assert_contains(resp_home_page_logged_user, '<div class="payment-due-date">Vencimento<span>/</span></div>')
    assert_contains(resp_home_page_logged_user, '<div class="payment-value">Valor (R$)</div>')


def test_title_payment_infos_not_present(resp_home_page_logged_user_no_payments_available):
    """
    Certifies that the titles of payment infos are not present
    when there are no payments listed.
    """
    assert_not_contains(resp_home_page_logged_user_no_payments_available, '<div>Fornecedor</div>')
    assert_not_contains(resp_home_page_logged_user_no_payments_available, '<div class="payment-due-date">Vencimento')
    assert_not_contains(resp_home_page_logged_user_no_payments_available, '<div class="payment-value">Valor (R$)</div>')


def test_anticip_button_not_present_for_common_user(resp_home_page_logged_user,
                                                    available_payments_user_01):
    """
    Certifies that the button for creating anticipation
    is not shown to a common user.
    """
    for payment in available_payments_user_01:
        assert_not_contains(resp_home_page_logged_user, f'<a class="anticipation-link" '
                                                        f'href="{payment.create_anticipation()}">Antecipar</a>')


def test_anticip_button_present_for_operator(client_logged_operator,
                                             available_payments_user_01):
    """
    Certifies that the button for creating anticipation
    is shown to an operator.
    """
    resp = client_logged_operator.get(reverse('payments:home'))
    for payment in available_payments_user_01:
        assert_contains(resp, f'<a class="anticipation-link" href="{payment.create_anticipation()}">Antecipar</a>')


def test_anticip_button_present_for_supplier(client_logged_supplier_01,
                                             available_payments_user_01):
    """
    Certifies that the button for creating anticipation
    is shown to a supplier.
    """
    resp = client_logged_supplier_01.get(reverse('payments:home'))
    for payment in available_payments_user_01:
        assert_contains(resp, f'<a class="anticipation-link" href="{payment.create_anticipation()}">Antecipar</a>')
