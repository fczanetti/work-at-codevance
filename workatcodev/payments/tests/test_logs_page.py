import pytest
from django.urls import reverse
from datetime import date
from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import RequestLog


@pytest.fixture
def anticipations(client_logged_operator, payment,
                  payment_user_01_anticipation_created,
                  payment_user_02_anticipation_created):
    """
    - creates an anticipation for payment;
    - approve payment_user_01_anticipation_created anticipation;
    - denies payment_user_02_anticipation_created anticipation;
    """
    new_date = date.today()
    a1 = {'act': 'A', 'id': payment_user_01_anticipation_created.pk}
    a2 = {'act': 'D', 'id': payment_user_02_anticipation_created.pk}
    client_logged_operator.post(reverse('payments:anticipation', args=(payment.pk,)), {'new_due_date': new_date})
    client_logged_operator.post(reverse('payments:update_antic', kwargs=a1))
    client_logged_operator.post(reverse('payments:update_antic', kwargs=a2))


@pytest.fixture
def resp_logs_page(client_logged_operator, anticipations):
    """
    Creates a request to logs page and returns a response.
    """
    resp = client_logged_operator.get(reverse('payments:logs'))
    return resp


@pytest.fixture
def resp_logs_page_no_logs_created(client_logged_operator):
    """
    Creates a request to logs page without logs registered
    and returns a response.
    """
    resp = client_logged_operator.get(reverse('payments:logs'))
    return resp


def test_status_code_logs_page(resp_logs_page):
    """
    Certifies that logs page is loaded successfully.
    """
    assert resp_logs_page.status_code == 200


def test_titles_logs_page_and_message(resp_logs_page):
    """
    Certifies that the titles are present and no logs
    message is not present.
    """
    assert_contains(resp_logs_page, '<title>Pagamentos - Registros</title>')
    assert_contains(resp_logs_page, '<h1 class="main-content-title">Registros</h1>')
    assert_not_contains(resp_logs_page, 'Não há registros.')


def test_no_logs_message(resp_logs_page_no_logs_created):
    """
    Certifies that the message is present if
    there are no logs registered.
    """
    assert_contains(resp_logs_page_no_logs_created, 'Não há registros.')


def test_logs_infos_present(resp_logs_page):
    """
    Certifies that the logs generated are present
    in the logs page.
    """
    for log in RequestLog.objects.all():
        creation_date = date.strftime(log.created_at, '%d/%m/%Y')
        assert_contains(resp_logs_page, log.anticipation)
        assert_contains(resp_logs_page, creation_date)
        assert_contains(resp_logs_page, log.user)
        assert_contains(resp_logs_page, log.action)
