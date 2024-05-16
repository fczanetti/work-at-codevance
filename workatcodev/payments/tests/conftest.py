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
def user_02(db):
    """
    Creates and returns a user.
    """
    user_02 = baker.make(get_user_model(), email='supplier02@email.com')
    return user_02


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
    due_date = date.today() + timedelta(days=1)
    payment_01 = baker.make(Payment, supplier=supplier_01, due_date=due_date)
    return payment_01


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
def unavailable_payments_user_02_due_date(db, supplier_02):
    """
    Creates and returns unavailable payments due to due_date.
    """
    due_date = date.today()
    payment = baker.make(Payment, due_date=due_date, _quantity=2, supplier=supplier_02)
    return payment


@pytest.fixture
def payment_user_01_anticipation_created(db, supplier_01):
    """
    Creates and returns a payment with anticipation related
    (status='PC').
    """
    due_date = date.today() + timedelta(days=5)
    new_due_date = str(date.today() + timedelta(days=1))
    payment_ant = baker.make(Payment, due_date=due_date, supplier=supplier_01)
    baker.make(Anticipation, payment=payment_ant, new_due_date=new_due_date)
    return payment_ant


@pytest.fixture
def payment_user_02_anticipation_created(db, supplier_02):
    """
    Creates and returns a payment with anticipation requested
    but not approved or denied (status='PC').
    """
    d = date.today() + timedelta(days=5)
    payment = baker.make(Payment, supplier=supplier_02, due_date=d)
    baker.make(Anticipation, payment=payment)
    return payment


@pytest.fixture
def payment_user_01_anticipation_related_status_a(db, supplier_01):
    """
    Creates and returns a payment with anticipation related. The status of this
    anticipation is 'A' (Approved).
    """
    due_date = date.today() + timedelta(days=5)
    new_due_date = str(date.today() + timedelta(days=1))
    payment_ant = baker.make(Payment, due_date=due_date, supplier=supplier_01)
    baker.make(Anticipation, payment=payment_ant, new_due_date=new_due_date, status='A')
    return payment_ant


@pytest.fixture
def payment_user_01_anticipation_related_status_d(db, supplier_01):
    """
    Creates and returns a payment with anticipation related. The status of this
    anticipation is 'D' (Denied), and the supplier is supplier_01.
    """
    due_date = date.today() + timedelta(days=5)
    new_due_date = str(date.today() + timedelta(days=1))
    payment_ant = baker.make(Payment, due_date=due_date, supplier=supplier_01)
    baker.make(Anticipation, payment=payment_ant, new_due_date=new_due_date, status='D')
    return payment_ant


@pytest.fixture
def payment_user_02_anticipation_related_status_d(db, supplier_02):
    """
    Creates and returns a payment with anticipation related. The status of this
    anticipation is 'D' (Denied), and the supplier is supplier_02.
    """
    due_date = date.today() + timedelta(days=5)
    new_due_date = str(date.today() + timedelta(days=1))
    payment_ant = baker.make(Payment, due_date=due_date, supplier=supplier_02)
    baker.make(Anticipation, payment=payment_ant, new_due_date=new_due_date, status='D')
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
