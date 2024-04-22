import pytest
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth import get_user_model


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


def test_home_page_logged_user(resp_home_page_logged_user):
    """
    Certify that home page is loaded successfully.
    """
    assert resp_home_page_logged_user.status_code == 200
