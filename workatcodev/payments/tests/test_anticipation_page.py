from datetime import date

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


def test_title_is_present(resp_anticip_page_logged_supplier_01):
    """
    Certifies that the title is present on the anticipation page.
    """
    assert_contains(resp_anticip_page_logged_supplier_01, 'Antecipação de pagamento')


def test_payment_is_present(resp_anticip_page_logged_supplier_01, payment_supplier_01):
    """
    Certifies that the payment is present on the anticipation page.
    """
    due_date = date.strftime(payment_supplier_01.due_date, '%d/%m/%Y')
    assert_contains(resp_anticip_page_logged_supplier_01, f'{payment_supplier_01.supplier}')
    assert_contains(resp_anticip_page_logged_supplier_01, f'{due_date}')


def test_form_fields_are_present(resp_anticip_page_logged_supplier_01):
    """
    Certifies that the form fields and buttons are present.
    """
    assert_contains(resp_anticip_page_logged_supplier_01, '<label for="id_new_due_date">Novo vencimento:</label>')
    assert_contains(resp_anticip_page_logged_supplier_01, '<input type="date" name="new_due_date" required '
                                                          'id="id_new_due_date"')
    assert_contains(resp_anticip_page_logged_supplier_01, '<button type="submit" id="conf-button">Confirmar</button>')
    assert_contains(resp_anticip_page_logged_supplier_01, f'<a href="{reverse("payments:home")}" '
                                                          f'id="canc-button">Cancelar</a>')


def test_try_access_anticip_paym_supp_02_by_supp_01(supplier_01, client_logged_supplier_01, supplier_02, payment):
    """
    Certifies that a supplier can not access anticipation page
    of a payment that does not belong to him (Via URL).
    """
    payment.supplier = supplier_02
    payment.save()
    resp = client_logged_supplier_01.get(reverse('payments:anticipation', args=(payment.pk,)))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access/')


def test_operator_access_antic_page_all_suppliers(client_logged_operator, payment, supplier_02):
    """
    Certifies that an operator can access anticipation page and create anticipations
    for every available payments.
    """
    payment.supplier = supplier_02
    payment.save()
    resp = client_logged_operator.get(reverse('payments:anticipation', args=(payment.pk,)))
    assert resp.status_code == 200
    assert resp.request['PATH_INFO'].startswith('/anticipation')
