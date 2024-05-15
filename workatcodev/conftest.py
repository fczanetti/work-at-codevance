import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model


@pytest.fixture
def user_plain_password(db):
    """
    Creates and returns a user with plain password.
    """
    user = baker.make(get_user_model())
    senha = 'senha'
    user.set_password(senha)
    user.save()
    user.senha_plana = senha
    return user
