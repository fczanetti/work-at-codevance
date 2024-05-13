import pytest
from django.urls import reverse

from workatcodev.django_assertions import assert_contains


@pytest.fixture
def resp_logs_page(client_logged_operator):
    """
    Creates a request to logs page and returns a response.
    """
    resp = client_logged_operator.get(reverse('payments:logs'))
    return resp


def test_status_code_logs_page(resp_logs_page):
    """
    Certifies that logs page is loaded successfully.
    """
    assert resp_logs_page.status_code == 200


def test_titles_logs_page(resp_logs_page):
    """
    Certifies that the titles are present.
    """
    assert_contains(resp_logs_page, '<title>Pagamentos - Registros</title>')
    assert_contains(resp_logs_page, '<h1 class="main-content-title">Registros</h1>')
