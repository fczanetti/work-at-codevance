from django.db import models
from django.contrib.auth import get_user_model
from workatcodev.payments import facade


class Supplier(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    corporate_name = models.CharField(max_length=128, verbose_name='Razão Social')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', unique=True)

    def __str__(self):
        return self.corporate_name


class Payment(models.Model):
    STATUS_CHOICES = {'U': 'Unavailable',
                      'A': 'Available',
                      'PC': 'Pending confirmation',
                      'AN': 'Anticipated',
                      'D': 'Denied'}
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Fornecedor')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Criação')
    due_date = models.DateField(verbose_name='Vencimento')
    value = models.PositiveIntegerField(verbose_name='Valor')
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='Status', default='A', editable=False)

    def __str__(self):
        return f'{self.supplier} - R${self.value:.2f}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        The function check_payment_due_date() is used to make sure the payment status is not saved
        with status='A' (Available) if it is created with due_date equal to today's date.
        """
        facade.check_payment_due_date(self)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
