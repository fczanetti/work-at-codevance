from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model


class NewUserForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'email',  'is_operator', 'password1', 'password2']
