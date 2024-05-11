import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains


@pytest.fixture
def resp_approval_anticip_page(client_logged_operator,
                               payment_user_01_anticipation_created):
    """
    Creates a request to approval anticipation
    page and returns a response.
    """
    resp = client_logged_operator.get(reverse('payments:approval',
                                              args=(payment_user_01_anticipation_created.anticipation.pk,)))
    return resp


def test_status_code_approval_anticip_page(resp_approval_anticip_page):
    """
    Certifies that approval anticipation page is loaded successfully.
    """
    assert resp_approval_anticip_page.status_code == 200


def test_title_approval_page(resp_approval_anticip_page):
    """
    Certifies that the title of the page is present.
    """
    assert_contains(resp_approval_anticip_page, '<title>Pagamentos - Aprovar</title>')


def test_access_denied_suppliers(client_logged_supplier_01,
                                 payment_user_01_anticipation_created):
    """
    Certifies that suppliers can not access approval anticipation page.
    """
    resp = client_logged_supplier_01.get(reverse('payments:approval',
                                                 args=(payment_user_01_anticipation_created.anticipation.pk,)))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access')


def test_access_denied_common_user(client_logged_common_user,
                                   payment_user_01_anticipation_created):
    """
    Certifies that common users can not access approval anticipation page.
    """
    resp = client_logged_common_user.get(reverse('payments:approval',
                                                 args=(payment_user_01_anticipation_created.anticipation.pk,)))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access')
