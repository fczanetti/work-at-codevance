import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from workatcodev.django_assertions import assert_contains


@pytest.fixture
def resp_new_supplier_page_operator(client_logged_operator):
    """
    Creates a request to new supplier page by an
    operator and returns a response.
    """
    resp = client_logged_operator.get(reverse('payments:new_supplier'))
    return resp


def test_status_code_new_supplier_page(resp_new_supplier_page_operator):
    """
    Certifies that new supplier page is loaded successfully.
    """
    assert resp_new_supplier_page_operator.status_code == 200


def test_title_new_supplier_page(resp_new_supplier_page_operator):
    """
    Certifies that titles are present.
    """
    assert_contains(resp_new_supplier_page_operator, f'<title>{_("Payments - New supplier")}</title>')
    assert_contains(resp_new_supplier_page_operator, f'<h1 class="main-content-title">{_("New supplier")}</h1>')


def test_redirect_non_logged_users(client):
    """
    Certifies that non logged users are redirected to
    login page when trying to access new supplier page.
    """
    resp = client.get(reverse('payments:new_supplier'))
    assert resp.status_code == 302
    assert resp.url.startswith('/accounts/login')


def test_access_denied_for_common_user(client_logged_common_user):
    """
    Certifies that common users can not access new
    supplier page.
    """
    resp = client_logged_common_user.get(reverse('payments:new_supplier'))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access/')


def test_access_denied_for_suppliers(client_logged_supplier_01):
    """
    Certifies that suppliers can not access new
    supplier page.
    """
    resp = client_logged_supplier_01.get(reverse('payments:new_supplier'))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access/')
