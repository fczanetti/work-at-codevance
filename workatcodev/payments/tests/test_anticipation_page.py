from datetime import date

import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
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
    Certifies that anticipation page is loaded successfully with logged supplier.
    """
    assert resp_anticip_page_logged_supplier_01.status_code == 200


def test_title_anticipation_page(resp_anticip_page_logged_supplier_01):
    """
    Certifies that the title of the anticipation page is present.
    """
    assert_contains(resp_anticip_page_logged_supplier_01, f'<title>{_("Payments - Anticipate")}</title>')


def test_title_is_present(resp_anticip_page_logged_supplier_01):
    """
    Certifies that the title is present on the anticipation page.
    """
    assert_contains(resp_anticip_page_logged_supplier_01, f'{_("Payment anticipation")}')


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
    assert_contains(resp_anticip_page_logged_supplier_01, '<label for="id_new_due_date">')
    assert_contains(resp_anticip_page_logged_supplier_01, '<input type="date" name="new_due_date" required '
                                                          'id="id_new_due_date"')
    assert_contains(resp_anticip_page_logged_supplier_01, '<button type="submit" id="conf-button">')
    assert_contains(resp_anticip_page_logged_supplier_01, f'<a href="{reverse("payments:home")}" id="canc-button">')


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


def test_access_anticip_page_common_user_not_allowed(client_logged_common_user,
                                                     payment_supplier_01):
    """
    Certifies that a common user can not access anticipation page.
    """
    resp = client_logged_common_user.get(reverse('payments:anticipation', args=(payment_supplier_01.pk,)))
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


def test_access_anticip_page_incorrect_id(client_logged_operator):
    """
    Certifies that a 404 error is raised if a user tries to
    use an incorrect ID in the URL (an ID that does not belong
    to any payment).
    """
    with pytest.raises(ValueError):
        client_logged_operator.get(reverse('payments:anticipation', args=(12345,)))


def test_redirect_login_user_not_authenticated(client, db, payment):
    """
    Certifies that non authenticated users can not
    access anticipation page.
    """
    resp = client.get(reverse('payments:anticipation', args=(payment.pk,)))
    assert resp.status_code == 302
    assert resp.url.startswith('/accounts/login')


def test_anticip_page_not_loaded_for_payments_with_anticip_related(payment_user_01_anticipation_created,
                                                                   client_logged_operator):
    """
    Certifies that anticipation page is not loaded if tried with
    a payment for which an anticipation was already created.
    """
    with pytest.raises(ValueError):
        client_logged_operator.get(reverse('payments:anticipation',
                                           args=(payment_user_01_anticipation_created.pk,)))
