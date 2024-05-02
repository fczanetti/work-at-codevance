import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains


@pytest.fixture
def resp_anticip_page_logged_supplier_01(client_logged_supplier_01, payment_supplier_01):
    """
    Creates a request to anticipation page with logged supplier and
    returns the response.
    """
    resp = client_logged_supplier_01.get(reverse('payments:anticipation', args=(payment_supplier_01.pk,)))
    return resp


def test_status_code_antic_page_logged_supplier_01(resp_anticip_page_logged_supplier_01):
    """
    Certifies that anticipation page is loaded successfully with
    logged supplier.
    """
    assert resp_anticip_page_logged_supplier_01.status_code == 200


def test_title_anticipation_page(resp_anticip_page_logged_supplier_01):
    """
    Certifies that the title of the anticipation page is present.
    """
    assert_contains(resp_anticip_page_logged_supplier_01, '<title>Pagamentos - Antecipar</title>')
