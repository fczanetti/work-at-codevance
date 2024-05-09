import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains


@pytest.fixture
def resp_payment_creation_page_supplier_01(client_logged_supplier_01):
    """
    Creates a request to payment creation page and
    returns a response.
    """
    resp = client_logged_supplier_01.get(reverse('payments:new_payment'))
    return resp


def test_status_code_paym_creat_page_supp_01(resp_payment_creation_page_supplier_01):
    """
    Certifies that payment creation page is loaded successfully.
    """
    assert resp_payment_creation_page_supplier_01.status_code == 200


def test_title_new_payment_page(resp_payment_creation_page_supplier_01):
    """
    Certifies that the titles of the page are present.
    """
    assert_contains(resp_payment_creation_page_supplier_01, '<title>Pagamentos - Novo pagamento</title>')
    assert_contains(resp_payment_creation_page_supplier_01, '<h1 id="main-content-title">Novo pagamento</h1>')
