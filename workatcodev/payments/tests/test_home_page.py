from datetime import date, timedelta

import pytest
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth import get_user_model

from workatcodev.django_assertions import assert_contains
from workatcodev.payments.models import Payment


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
    assert_contains(resp_home_page_logged_user, '<a class="navbar-link" href="">Liberação pendente</a>')
    assert_contains(resp_home_page_logged_user, '<a class="navbar-link" href="">Aprovados</a>')
    assert_contains(resp_home_page_logged_user, '<a class="navbar-link" href="">Negados</a>')
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
        assert_contains(resp_home_page_logged_user, payment.value)
        assert_contains(resp_home_page_logged_user, payment.status)
