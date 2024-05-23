import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from workatcodev.django_assertions import assert_contains
from workatcodev.payments.forms import NewSupplierForm


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


def test_form_items_new_supplier_page(resp_new_supplier_page_operator):
    """
    Certifies that the form items are present.
    """
    assert_contains(resp_new_supplier_page_operator, '<label for="id_user">')
    assert_contains(resp_new_supplier_page_operator, '<select name="user" required id="id_user">')
    assert_contains(resp_new_supplier_page_operator, '<label for="id_corporate_name">')
    assert_contains(resp_new_supplier_page_operator, '<input type="text" name="corporate_name" maxlength="128"')
    assert_contains(resp_new_supplier_page_operator, '<label for="id_cnpj">')
    assert_contains(resp_new_supplier_page_operator, '<input type="text" name="cnpj" maxlength="14" required')
    assert_contains(resp_new_supplier_page_operator, '<a href="/" id="canc-button">')
    assert_contains(resp_new_supplier_page_operator, '<button type="submit" id="conf-button">')


def test_user_options_new_supplier_form(operator, user_02, supplier_01,
                                        resp_new_supplier_page_operator):
    """
    Certifies that operators or users that already have
    a supplier related are not shown in the form.
    """
    form = NewSupplierForm()
    assert operator not in form.fields['user'].queryset
    assert supplier_01.user not in form.fields['user'].queryset
    assert user_02 in form.fields['user'].queryset
