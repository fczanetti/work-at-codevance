import pytest
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth import get_user_model

from workatcodev.django_assertions import assert_contains


@pytest.fixture
def logged_client(client, db):
    user = baker.make(get_user_model())
    client.force_login(user)
    return client


@pytest.fixture
def resp_home_page_logged_user(logged_client):
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


def test_filter_form_home_page_exists(resp_home_page_logged_user):
    """
    Certifies that there is a form for filtering payments status in the home page.
    """
    assert_contains(resp_home_page_logged_user, '<form id="filter_form" action="" method="POST">')
    assert_contains(resp_home_page_logged_user, '<label for="id_status">Status:</label>')
    assert_contains(resp_home_page_logged_user, '<select name="status" id="id_status">')
    assert_contains(resp_home_page_logged_user, '<button id="filter_button" type="submit">Filtrar</button>')


# def test_filter_form_home_page(db, logged_client):
#     """
#     Filter each payment per status once and guarantees that only the
#     filtered payment appears on the page/response. Also confirms that
#     the title is correct.
#     """
#     av_status = ['A', 'U', 'PC', 'AN', 'D']
#     TITLES = {'A': _('Available for anticipation'),
#               'U': _('Unavailable for anticipation'),
#               'PC': _('Pending anticipation confirmation'),
#               'AN': _('Anticipated payments'),
#               'D': _('Denied anticipation')}
#     payments = []
#     due_date = date.today() + timedelta(days=3)
#     for s in av_status:
#         payments.append(baker.make(Payment, due_date=due_date, status=s))
#     for s in av_status:
#         curr_payment = payments.pop(0)
#         resp = logged_client.post(reverse('payments:home'), {'status': s})
#         assert_contains(resp, curr_payment.supplier)
#         assert_contains(resp, TITLES[s])
#         assert_not_contains(resp, payments[0].supplier)
#         assert_not_contains(resp, payments[1].supplier)
#         assert_not_contains(resp, payments[2].supplier)
#         assert_not_contains(resp, payments[3].supplier)
#         payments.insert(4, curr_payment)
