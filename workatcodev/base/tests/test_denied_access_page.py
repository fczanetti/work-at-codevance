import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model
from django.urls import reverse

from workatcodev.django_assertions import assert_contains


@pytest.fixture
def client_logged(db, client):
    """
    Creates a user and returns a client logged with
    this user.
    """
    user = baker.make(get_user_model())
    client.force_login(user)
    return client


@pytest.fixture
def resp_denied_access_page(client_logged):
    """
    Creates a request accessing denied access page and
    returns a response.
    """
    resp = client_logged.get(reverse('base:denied_access'))
    return resp


def test_status_code_denied_access_page(resp_denied_access_page):
    """
    Certifies that denied access page is loaded successfully.
    """
    assert resp_denied_access_page.status_code == 200


def test_titles_denied_access_page(resp_denied_access_page):
    """
    Certifies that the title of denied access page is present.
    """
    assert_contains(resp_denied_access_page, '<title>Pagamentos - Acesso negado</title>')
    assert_contains(resp_denied_access_page, '<h1 id="main-content-title">Desculpe, mas você não tem acesso a este '
                                             'conteúdo.</h1>')
