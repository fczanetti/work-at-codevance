import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from workatcodev.base.models import User


@pytest.fixture
def user_operator(db):
    """
    Creates and returns an operator.
    """
    operator = baker.make(get_user_model(), is_operator=True)
    return operator


@pytest.fixture
def user_not_operator(db):
    """
    Creates and returns a comon user.
    """
    operator = baker.make(get_user_model(), is_operator=False)
    return operator


def test_group_creation(user_operator):
    """
    Certifies that a group named Operators is created when creating/saving a user.
    """
    assert Group.objects.filter(name=_('Operators')).exists()


def test_user_is_operator(user_operator):
    """
    Certifies that a user created as operator belongs to the Operators group.
    """
    assert user_operator.groups.filter(name=_('Operators')).exists()


def test_user_is_not_operator(user_not_operator):
    """
    Certifies that a user created as non operator does not belong to the Operators group.
    """
    assert not user_not_operator.groups.filter(name=_('Operators')).exists()


def test_operator_has_permissions(user_operator):
    """
    Certifies that an operator, when created, has permissions
    to create payments, create and change anticipations.
    """
    assert user_operator.has_perm('payments.add_payment')
    assert user_operator.has_perm('payments.add_anticipation')
    assert user_operator.has_perm('payments.change_anticipation')


def test_new_user_via_post_form(client_logged_operator):
    """
    Creates a user via post form, certifies the
    user was saved in database and the redirect
    was to home page.
    """
    resp = client_logged_operator.post(reverse('base:new_user'), {'first_name': 'Primeiro nome',
                                                                  'email': 'email1213@email.com',
                                                                  'is_operator': False,
                                                                  'password1': 'pass123#',
                                                                  'password2': 'pass123#'})
    assert User.objects.filter(email='email1213@email.com').exists()
    assert resp.status_code == 302
    assert resp.url == reverse('payments:home')
