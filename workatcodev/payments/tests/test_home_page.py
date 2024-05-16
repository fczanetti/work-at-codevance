import pytest
from django.urls import reverse
from workatcodev.django_assertions import assert_contains, assert_not_contains
from django.utils.translation import gettext_lazy as _


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


@pytest.fixture
def resp_home_page_supplier_01(client_logged_supplier_01,
                               available_payments_user_01):
    """
    Creates a request to home page by supplier 01 and returns a response.
    """
    resp = client_logged_supplier_01.get(reverse('payments:home'))
    return resp


@pytest.fixture
def resp_home_page_operator(client_logged_operator,
                            available_payments_user_01):
    """
    Creates a request to home page by an operator and returns a response.
    """
    resp = client_logged_operator.get(reverse('payments:home'))
    return resp


def test_invalid_param_url(client_logged_common_user):
    """
    Certifies that if an invalid parameter is tried in
    the URL a 404 error is raised. Valid parameters are
    the filtering options ('A', 'U', 'PC', 'AN', 'D').
    """
    resp = client_logged_common_user.get(reverse('payments:home', args=('B',)))
    assert resp.status_code == 404


def test_home_page_logged_user(resp_home_page_logged_user):
    """
    Certify that home page is loaded successfully.
    """
    assert resp_home_page_logged_user.status_code == 200


def test_title_home_page(resp_home_page_logged_user):
    """
    Certifies that home page title is present.
    """
    assert_contains(resp_home_page_logged_user, f'<title>{_("Payments - Home")}</title>')


def test_links_navbar(resp_home_page_logged_user):
    """
    Certify that navbar links and title are present.
    """
    assert_contains(resp_home_page_logged_user, f'<a class="navbar-link" '
                                                f'href="{reverse("payments:home")}">{_("Home")}</a>')
    assert_contains(resp_home_page_logged_user, f'<a class="navbar-link" '
                                                f'href="{reverse("payments:logs")}">{_("Logs")}</a>')
    assert_contains(resp_home_page_logged_user, f'<div id="logo">{_("Payments")}</div>')


def test_filter_form_home_page_exists(resp_home_page_logged_user):
    """
    Certifies that there is a form for filtering payments status in the home page.
    """
    assert_contains(resp_home_page_logged_user, '<form id="filter_form" action="/" method="GET">')
    assert_contains(resp_home_page_logged_user, '<label for="id_status">Status:</label>')
    assert_contains(resp_home_page_logged_user, '<select name="status" id="id_status">')
    assert_contains(resp_home_page_logged_user, f'<button id="filter_button" type="submit">{_("Filter")}</button>')


def test_title_payment_infos_present(resp_home_page_logged_user):
    """
    Certifies that the titles of payment infos are present
    when there is at least one payment listed.
    """
    assert_contains(resp_home_page_logged_user, f'<div>{_("Supplier")}</div>')
    assert_contains(resp_home_page_logged_user, f'<div class="payment-due-date">{_("Due date")}<span>/</span></div>')
    assert_contains(resp_home_page_logged_user, f'<div class="payment-value">{_("Value (US$)")}</div>')


def test_title_payment_infos_not_present(resp_home_page_logged_user_no_payments_available):
    """
    Certifies that the titles of payment infos are not present
    when there are no payments listed.
    """
    assert_not_contains(resp_home_page_logged_user_no_payments_available, f'<div>{_("Supplier")}</div>')
    assert_not_contains(resp_home_page_logged_user_no_payments_available,
                        f'<div class="payment-due-date">{_("Due date")}')
    assert_not_contains(resp_home_page_logged_user_no_payments_available,
                        f'<div class="payment-value">{_("Value (US$)")}</div>')


def test_anticip_button_not_present_for_common_user(resp_home_page_logged_user,
                                                    available_payments_user_01):
    """
    Certifies that the button for creating anticipation
    is not shown to a common user.
    """
    for payment in available_payments_user_01:
        assert_not_contains(resp_home_page_logged_user, f'<a class="anticipation-link" '
                                                        f'href="{payment.create_anticipation()}">{_("Anticipate")}</a>')


def test_anticip_button_present_for_operator(resp_home_page_operator,
                                             available_payments_user_01):
    """
    Certifies that the button for creating anticipation
    is shown to an operator.
    """
    for payment in available_payments_user_01:
        assert_contains(resp_home_page_operator, f'<a class="anticipation-link" '
                                                 f'href="{payment.create_anticipation()}">{_("Anticipate")}</a>')


def test_anticip_button_present_for_supplier(resp_home_page_supplier_01,
                                             available_payments_user_01):
    """
    Certifies that the button for creating anticipation
    is shown to a supplier.
    """
    for payment in available_payments_user_01:
        assert_contains(resp_home_page_supplier_01, f'<a class="anticipation-link" '
                                                    f'href="{payment.create_anticipation()}">{_("Anticipate")}</a>')


def test_new_payment_button_present_for_suppliers(resp_home_page_supplier_01):
    """
    Certifies that the new payment button is present for suppliers.
    """
    assert_contains(resp_home_page_supplier_01, f'<a class="navbar-link" '
                                                f'href="{reverse("payments:new_payment")}">{_("New payment")}</a>')


def test_new_payment_button_present_for_operators(resp_home_page_operator):
    """
    Certifies that the new payment button is present for operators.
    """
    assert_contains(resp_home_page_operator, f'<a class="navbar-link" '
                                             f'href="{reverse("payments:new_payment")}">{_("New payment")}</a>')


def test_new_payment_button_not_present_for_common_users(resp_home_page_logged_user):
    """
    Certifies that the new payment button is not present for common users.
    """
    assert_not_contains(resp_home_page_logged_user, f'<a class="navbar-link" '
                                                    f'href="{reverse("payments:new_payment")}">{_("New payment")}</a>')


def test_redirect_login_user_not_authenticated(client, db):
    """
    Certifies that non authenticated users can not
    access home page.
    """
    resp = client.get(reverse('payments:home'))
    assert resp.status_code == 302
    assert resp.url.startswith('/accounts/login')


def test_new_user_link_present_for_operator(resp_home_page_operator):
    """
    Certifies that new user link is present for operators.
    """
    assert_contains(resp_home_page_operator, f'<a class="navbar-link" href="{reverse("base:new_user")}">'
                                             f'{_("New user")}</a>')


def test_new_user_link_not_present_for_suppliers(resp_home_page_supplier_01):
    """
    Certifies that new user link is not present for suppliers.
    """
    assert_not_contains(resp_home_page_supplier_01, f'{_("New user")}')


def test_new_user_link_not_present_for_common_user(resp_home_page_logged_user):
    """
    Certifies that new user link is not present for common users.
    """
    assert_not_contains(resp_home_page_logged_user, f'{_("New user")}')
