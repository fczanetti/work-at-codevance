import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_payment_creation_page_supplier_01(supplier_01, client_logged_supplier_01):
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


def test_form_items_new_payment_page(resp_payment_creation_page_supplier_01):
    """
    Certifies that form items are present on the page.
    """
    assert_contains(resp_payment_creation_page_supplier_01, '<label for="id_due_date">Vencimento:</label>')
    assert_contains(resp_payment_creation_page_supplier_01, '<input type="date" name="due_date" '
                                                            'required id="id_due_date">')
    assert_contains(resp_payment_creation_page_supplier_01, '<label for="id_value">Valor:</label>')
    assert_contains(resp_payment_creation_page_supplier_01, '<input type="number" name="value" step="any" '
                                                            'required id="id_value">')
    assert_contains(resp_payment_creation_page_supplier_01, '<a href="/" id="canc-button">Cancelar</a>')
    assert_contains(resp_payment_creation_page_supplier_01, '<button type="submit" id="conf-button">Confirmar</button>')


def test_supplier_select_not_present(resp_payment_creation_page_supplier_01):
    """
    Certifies that the possibility of selecting a supplier when
    creating a payment is not present for a supplier.
    """
    assert_not_contains(resp_payment_creation_page_supplier_01, '<label for="id_supplier">Fornecedor:</label>')
    assert_not_contains(resp_payment_creation_page_supplier_01, '<select name="supplier" required id="id_supplier">')
