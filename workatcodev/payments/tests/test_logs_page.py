import pytest
from django.urls import reverse
from datetime import date
from workatcodev.django_assertions import assert_contains, assert_not_contains
from workatcodev.payments.models import RequestLog
from django.utils.translation import gettext_lazy as _


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
    a1 = {'act': 'A', 'id': payment_user_01_anticipation_created.anticipation.pk}
    a2 = {'act': 'D', 'id': payment_user_02_anticipation_created.anticipation.pk}
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


@pytest.fixture
def resp_logs_page_supplier_01(anticipations, client_logged_supplier_01):
    """
    Creates a request to logs page by supplier 01.
    """
    resp = client_logged_supplier_01.get(reverse('payments:logs'))
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
    assert_contains(resp_logs_page, f'<title>{_("Payments - Logs")}</title>')
    assert_contains(resp_logs_page, f'<h1 class="main-content-title">{_("Logs")}</h1>')
    assert_not_contains(resp_logs_page, f'{_("There are no logs.")}')


def test_no_logs_message(resp_logs_page_no_logs_created):
    """
    Certifies that the message is present if
    there are no logs registered.
    """
    assert_contains(resp_logs_page_no_logs_created, f'{_("There are no logs.")}')


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


def test_logs_supp_02_not_present_for_supp_01(resp_logs_page_supplier_01,
                                              payment_user_02_anticipation_created):
    """
    Certifies that logs from supplier 02 are not present for supplier 01.
    """
    assert_not_contains(resp_logs_page_supplier_01, payment_user_02_anticipation_created.anticipation)


def test_logs_supp_01_present_for_supp_01(resp_logs_page_supplier_01,
                                          payment_user_01_anticipation_created):
    """
    Certifies that logs from supplier 01 are present for supplier 01.
    """
    assert_contains(resp_logs_page_supplier_01, payment_user_01_anticipation_created.anticipation)
