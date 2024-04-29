from datetime import date, timedelta

import pytest
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth import get_user_model

from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import Payment
from django.utils.translation import gettext_lazy as _


@pytest.fixture
def logged_client(client, db):
    user = baker.make(get_user_model())
    client.force_login(user)
    return client


@pytest.fixture
def available_payments(db):
    """
    Creates and returns a list of available payments.
    """
    due_date = date.today() + timedelta(days=5)
    payments_list = baker.make(Payment, due_date=due_date, _quantity=3)
    return payments_list


@pytest.fixture
def resp_home_page_logged_user(logged_client, available_payments):
    """
    Creates a request to home page with authenticated
    user and returns its response.
    """
    resp = logged_client.get(reverse('payments:home'))
    return resp


@pytest.fixture
def resp_home_page_logged_user_no_payments_available(logged_client):
    """
    Creates a request to home page with authenticated
    user and returns its response. No payments are available in this response.
    """
    resp = logged_client.get(reverse('payments:home'))
    return resp


def test_home_page_logged_user(resp_home_page_logged_user):
    """
    Certify that home page is loaded successfully.
    """
    assert resp_home_page_logged_user.status_code == 200


def test_title_home_page(resp_home_page_logged_user):
    """
    Certifies that home page title is present.
    """
    assert_contains(resp_home_page_logged_user, '<title>Pagamentos - Home</title>')


def test_links_navbar(resp_home_page_logged_user):
    """
    Certify that navbar links are present.
    """
    assert_contains(resp_home_page_logged_user, '<a class="navbar-link" href="">Início</a>')
    assert_contains(resp_home_page_logged_user, '<a class="navbar-link" href="">Histórico</a>')


def test_available_payments_home_page(resp_home_page_logged_user, available_payments):
    """
    Certifies that all the available payments are shown at home page
    for a comon logged user.
    """
    for payment in available_payments:
        due_date = date.strftime(payment.due_date, '%d/%m/%Y')
        assert_contains(resp_home_page_logged_user, payment.supplier)
        assert_contains(resp_home_page_logged_user, due_date)
        assert_contains(resp_home_page_logged_user,
                        f'{payment.value:_.2f}'.replace('.', ',').replace('_', '.'))


def test_unavailable_payments_home_page(resp_home_page_logged_user, unavailable_payment):
    """
    Certifies that the unavailable payments are not shown at home page.
    """
    due_date = date.strftime(unavailable_payment.due_date, '%d/%m/%Y')
    assert_not_contains(resp_home_page_logged_user, unavailable_payment.supplier)
    assert_not_contains(resp_home_page_logged_user, due_date)
    assert_not_contains(resp_home_page_logged_user,
                        f'{unavailable_payment.value:_.2f}'.replace('.', ',').replace('_', '.'))


def test_payments_list_titles_available(resp_home_page_logged_user, available_payments):
    """
    Certifies that the titles of the payments list are available
    if there is at least one payment listed.
    """
    assert_contains(resp_home_page_logged_user, '<div>Fornecedor</div>')
    assert_contains(resp_home_page_logged_user, '<div class="payment-due-date">Vencimento</div>')
    assert_contains(resp_home_page_logged_user, '<div class="payment-value">Valor (R$)</div>')


def test_payments_list_titles_not_available(resp_home_page_logged_user_no_payments_available):
    """
    Certifies that the titles of the payments list are not available
    if there is no payment listed. Also certifies that the message of
    no payments registered is available.
    """
    assert_not_contains(resp_home_page_logged_user_no_payments_available, '<div>Fornecedor</div>')
    assert_not_contains(resp_home_page_logged_user_no_payments_available,
                        '<div class="payment-due-date">Vencimento</div>')
    assert_not_contains(resp_home_page_logged_user_no_payments_available,
                        '<div class="payment-value">Valor (R$)</div>')
    assert_contains(resp_home_page_logged_user_no_payments_available, '<div>Não há pagamentos cadastrados.</div>')


def test_filter_form_home_page_exists(resp_home_page_logged_user):
    """
    Certifies that there is a form for filtering payments status in the home page.
    """
    assert_contains(resp_home_page_logged_user, '<form id="filter_form" action="" method="POST">')
    assert_contains(resp_home_page_logged_user, '<label for="id_status">Status:</label>')
    assert_contains(resp_home_page_logged_user, '<select name="status" id="id_status">')
    assert_contains(resp_home_page_logged_user, '<button id="filter_button" type="submit">Filtrar</button>')


def test_filter_form_home_page(db, logged_client):
    """
    Filter each payment per status once and guarantees that only the
    filtered payment appears on the page/response. Also confirms that
    the title is correct.
    """
    av_status = ['A', 'U', 'PC', 'AN', 'D']
    TITLES = {'A': _('Available for anticipation'),
              'U': _('Unavailable for anticipation'),
              'PC': _('Pending anticipation confirmation'),
              'AN': _('Anticipated payments'),
              'D': _('Denied anticipation')}
    payments = []
    due_date = date.today() + timedelta(days=3)
    for s in av_status:
        payments.append(baker.make(Payment, due_date=due_date, status=s))
    for s in av_status:
        curr_payment = payments.pop(0)
        resp = logged_client.post(reverse('payments:home'), {'status': s})
        assert_contains(resp, curr_payment.supplier)
        assert_contains(resp, TITLES[s])
        assert_not_contains(resp, payments[0].supplier)
        assert_not_contains(resp, payments[1].supplier)
        assert_not_contains(resp, payments[2].supplier)
        assert_not_contains(resp, payments[3].supplier)
        payments.insert(4, curr_payment)
