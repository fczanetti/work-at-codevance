from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Supplier(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    corporate_name = models.CharField(max_length=128, verbose_name='Razão Social')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', unique=True)

    def __str__(self):
        return self.corporate_name


class Payment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Fornecedor')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Criação')
    due_date = models.DateField(verbose_name='Vencimento')
    value = models.FloatField(verbose_name='Valor')

    def __str__(self):
        return f'{self.supplier} - R${self.value:.2f}'

    def create_anticipation(self):
        """
        Returns a link to anticipation creation page.
        """
        return f'{reverse("payments:anticipation", args=(self.pk,))}'

    def check_payment_due_date(self):
        """
        This function makes sure no payments are created with due_date earlier
        than the day of creation.
        """
        due_date_str = str(self.due_date)
        if date.fromisoformat(due_date_str) < date.today():
            raise ValueError(_('Due date must be today or some day after.'))
        return

    def is_available(self):
        """
        Returns True if self.due_date was not reached yet,
        otherwise returns False.
        """
        due_date_str = str(self.due_date)
        if date.fromisoformat(due_date_str) <= date.today():
            return False
        return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        The function check_payment_due_date() is used to make sure the payment status is not saved
        if it is created with due_date earlier than today's date.
        """
        self.check_payment_due_date()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Anticipation(models.Model):
    STATUS_CHOICES = {'A': 'Approved',
                      'PC': 'Pending confirmation',
                      'D': 'Denied'}
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, verbose_name='Pagamento')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Data da solicitação')
    new_due_date = models.DateField(verbose_name='Novo vencimento')
    new_value = models.FloatField(verbose_name='Valor com desconto')
    update = models.DateField(auto_now=True, verbose_name='Atualização')
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='Status', default='PC', editable=False)

    def __str__(self):
        return f'{self.payment}'
