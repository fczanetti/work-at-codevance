from django.db import models
from workatcodev.base.models import User


class Operator(User):
    pass


class Supplier(User):
    corporate_name = models.CharField(max_length=64, verbose_name='Razão social')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', help_text='Use apenas números')

    def __str__(self):
        return self.corporate_name
