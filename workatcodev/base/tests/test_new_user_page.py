import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from workatcodev.django_assertions import assert_contains


@pytest.fixture
def resp_new_user_page_operator(client_logged_operator):
    """
    Creates a request to new user page by an operator.
    """
    resp = client_logged_operator.get(reverse('base:new_user'))
    return resp


def test_status_code_new_user_page(resp_new_user_page_operator):
    """
    Certify that new user page is loaded successfully.
    """
    assert resp_new_user_page_operator.status_code == 200


def test_access_denied_new_user_page_common_user(client_logged_common_user):
    """
    Certifies that common users can not access new user page.
    """
    resp = client_logged_common_user.get(reverse('base:new_user'))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access/')


def test_access_denied_new_user_page_supplier(client_logged_supplier_01):
    """
    Certifies that suppliers can not access new user page.
    """
    resp = client_logged_supplier_01.get(reverse('base:new_user'))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access/')


def test_login_redirect_new_user_page_non_logged_user(client):
    """
    Certifies that suppliers can not access new user page.
    """
    resp = client.get(reverse('base:new_user'))
    assert resp.status_code == 302
    assert resp.url.startswith('/accounts/login/')


def test_titles_new_user_page(resp_new_user_page_operator):
    """
    Certifies that the titles are present.
    """
    assert_contains(resp_new_user_page_operator, f'<title>{_("Payments - New user")}</title>')
    assert_contains(resp_new_user_page_operator, f'<h1 class="main-content-title">{_("New user")}</h1>')
