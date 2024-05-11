from datetime import date, datetime

import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains
from workatcodev.utils import format_value


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


def test_titles_approval_page(resp_approval_anticip_page):
    """
    Certifies that the titles of the page are present.
    """
    assert_contains(resp_approval_anticip_page, '<title>Pagamentos - Aprovar</title>')
    assert_contains(resp_approval_anticip_page, '<h1 id="main-content-title">Confirmar aprovação</h1>')


def test_payment_is_shown_approval_page(resp_approval_anticip_page,
                                        payment_user_01_anticipation_created):
    """
    Certifies that the payment is shown in approval page.
    """
    d = payment_user_01_anticipation_created.due_date
    due_date = date.strftime(d, '%d/%m/%Y')
    assert_contains(resp_approval_anticip_page, payment_user_01_anticipation_created)
    assert_contains(resp_approval_anticip_page, due_date)


def test_anticipation_data_are_shown_approval_page(resp_approval_anticip_page,
                                                   payment_user_01_anticipation_created):
    """
    Certifies that the anticipation details are shown in approval page.
    """
    nv = format_value(payment_user_01_anticipation_created.anticipation.new_value)
    new_date = payment_user_01_anticipation_created.anticipation.new_due_date
    new_due_date = (datetime.strptime(new_date, '%Y-%m-%d').strftime('%d/%m/%Y'))
    assert_contains(resp_approval_anticip_page, nv)
    assert_contains(resp_approval_anticip_page, new_due_date)


def test_form_items_are_present_approval(resp_approval_anticip_page,
                                         payment_user_01_anticipation_created):
    """
    Certifies that the form items are present.
    """
    assert_contains(resp_approval_anticip_page, '<a href="javascript:history.back()" id="canc-button" '
                                                'type="submit">Cancelar</a>')
    assert_contains(resp_approval_anticip_page, '<button type="submit" id="conf-button">Confirmar</button>')


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
