import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model
from workatcodev.payments.models import Supplier


@pytest.fixture
def operator(db):
    """
    Creates and returns a user/operator.
    """
    op = baker.make(get_user_model(), email='operator01@email.com', is_operator=True)
    return op


@pytest.fixture
def client_logged_operator(client, operator):
    """
    Creates a logged client from an operator.
    """
    client.force_login(operator)
    return client


@pytest.fixture
def common_user(db):
    """
    Creates a user that is neither an operator
    nor a supplier.
    """
    user = baker.make(get_user_model(), email='commonuser@email.com')
    return user


@pytest.fixture
def client_logged_common_user(client, common_user):
    """
    Creates a logged client from a common user.
    """
    client.force_login(common_user)
    return client


@pytest.fixture
def user_01(db):
    """
    Creates and returns a user.
    """
    user_01 = baker.make(get_user_model(), email='supplier01@email.com')
    return user_01


@pytest.fixture
def supplier_01(db, user_01):
    """
    Creates and return a supplier.
    """
    supplier_01 = baker.make(Supplier, user=user_01)
    return supplier_01


@pytest.fixture
def client_logged_supplier_01(user_01, client, supplier_01):
    """
    Creates and returns a client logged with supplier_01 user.
    """
    client.force_login(user_01)
    return client
