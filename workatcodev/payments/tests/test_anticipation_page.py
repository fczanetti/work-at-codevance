import pytest
from model_bakery import baker
from django.urls import reverse
from django.contrib.auth import get_user_model

from workatcodev.django_assertions import assert_contains
from workatcodev.payments.models import Supplier, Payment


@pytest.fixture
def user_01(db):
    """
    Creates and returns a user.
    """
    user_01 = baker.make(get_user_model(), email='supplier01_email.com')
    return user_01


@pytest.fixture
def supplier_01(db, user_01):
    """
    Creates and return a logged supplier.
    """
    supplier_01 = baker.make(Supplier, user=user_01)
    return supplier_01


@pytest.fixture
def payment_supplier_01(supplier_01):
    """
    Creates and returns a payment related to supplier_01.
    """
    payment_01 = baker.make(Payment, supplier=supplier_01)
    return payment_01


@pytest.fixture
def client_logged_supplier_01(user_01, client):
    """
    Creates and returns a client logged with supplier_01 user.
    """
    client.force_login(user_01)
    return client


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
