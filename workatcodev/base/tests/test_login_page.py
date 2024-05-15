import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from workatcodev.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_login_page(client):
    """
    Creates a request to login page and returns a response.
    """
    resp = client.get(reverse('base:login'))
    return resp


def test_login_page_status_code(resp_login_page):
    """
    Certifies that login page is loaded successfully.
    """
    assert resp_login_page.status_code == 200


def test_titles_login_page_are_present(resp_login_page):
    """
    Certifies that the titles are present.
    """
    assert_contains(resp_login_page, f'<title>{_("Payments - Login")}</title>')
    assert_contains(resp_login_page, '<h1 class="main-content-title">Login</h1>')


def test_form_items_are_present(resp_login_page):
    """
    Certify that form items are present.
    """
    assert_contains(resp_login_page, '<label for="id_username">')
    assert_contains(resp_login_page, '<label for="id_password">')
    assert_contains(resp_login_page, '<button type="submit" id="login-button">Login</button>')


def test_links_navbar_not_present(resp_login_page):
    """
    Certify that navbar links are not present if the user is
    not authenticated.
    """
    assert_not_contains(resp_login_page, f'<a class="navbar-link" href="{reverse("payments:home")}">{_("Home")}</a>')
    assert_not_contains(resp_login_page, f'<a class="navbar-link" href="{reverse("payments:new_payment")}">'
                                         f'{_("New payment")}</a>')
    assert_not_contains(resp_login_page, f'<a class="navbar-link" href="{reverse("payments:logs")}">{_("Logs")}</a>')
