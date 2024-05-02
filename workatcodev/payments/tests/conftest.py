import pytest
from datetime import date, timedelta
from workatcodev.payments.models import Supplier, Payment, Anticipation
from model_bakery import baker
from django.contrib.auth import get_user_model


@pytest.fixture
def payment(db):
    """
    Creates and return an instance of Payment.
    """
    d = date.today() + timedelta(days=5)
    payment = baker.make(Payment, due_date=d)
    return payment


@pytest.fixture
def user_01(db):
    """
    Creates and returns a user.
    """
    user_01 = baker.make(get_user_model(), email='supplier01_email.com')
    return user_01


@pytest.fixture
def user_02(db):
    """
    Creates and returns a user.
    """
    user_02 = baker.make(get_user_model(), email='supplier02_email.com')
    return user_02


@pytest.fixture
def supplier_01(db, user_01):
    """
    Creates and return a supplier.
    """
    supplier_01 = baker.make(Supplier, user=user_01)
    return supplier_01


@pytest.fixture
def supplier_02(db, user_02):
    """
    Creates and return a supplier.
    """
    supplier_02 = baker.make(Supplier, user=user_02)
    return supplier_02


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
def available_payments_user_01(db, supplier_01):
    """
    Creates and returns a list of available payments for supplier_01.
    """
    due_date = date.today() + timedelta(days=5)
    payments_list = baker.make(Payment, due_date=due_date, _quantity=3, supplier=supplier_01)
    return payments_list


@pytest.fixture
def available_payments_user_02(db, supplier_02):
    """
    Creates and returns a list of available payments for supplier_02.
    """
    due_date = date.today() + timedelta(days=5)
    payments_list = baker.make(Payment, due_date=due_date, _quantity=3, supplier=supplier_02)
    return payments_list


@pytest.fixture
def unavailable_payments_user_01_due_date(db, supplier_01):
    """
    Creates and returns unavailable payments due to due_date.
    """
    due_date = date.today()
    payment = baker.make(Payment, due_date=due_date, _quantity=2, supplier=supplier_01)
    return payment


@pytest.fixture
def unavailable_payment_user_01_anticipation_created(db, supplier_01):
    """
    Creates and returns an unavailable payment due to anticipation related. This payment
    will have a $1.00 value to diferentiate from others.
    """
    due_date = date.today() + timedelta(days=5)
    new_due_date = str(date.today() + timedelta(days=1))
    payment_ant = baker.make(Payment, due_date=due_date, supplier=supplier_01, value=1)
    baker.make(Anticipation, payment=payment_ant, new_due_date=new_due_date)
    return payment_ant


@pytest.fixture
def unavailable_payment(db):
    """
    Creates and returns an unavailable payment. A payment is classified as unavailable when
    its due date has already arrived or passed.
    """
    today = date.today()
    unav_paym = baker.make(Payment, due_date=today)
    return unav_paym
