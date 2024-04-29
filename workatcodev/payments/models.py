from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from workatcodev import settings


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
    value = models.PositiveIntegerField(verbose_name='Valor')
    status = models.CharField(choices=settings.PAYMENT_STATUS_CHOICES,
                              verbose_name='Status', default='A', editable=False)

    def __str__(self):
        return f'{self.supplier} - R${self.value:.2f}'

    def check_payment_due_date(self):
        """
        This function receives an instance of Payment and verify if its due date is equal or
        earlier than today's date. If so, the payment's status will be changed to Unavailable (U).
        """
        due_date_str = str(self.due_date)
        if date.fromisoformat(due_date_str) <= date.today():
            self.status = 'U'
        return

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        The function check_payment_due_date() is used to make sure the payment status is not saved
        with status='A' (Available) if it is created with due_date equal to today's date.
        """
        self.check_payment_due_date()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Anticipation(models.Model):
    STATUS_CHOICES = {'A': 'Approved',
                      'PC': 'Pending confirmation',
                      'D': 'Denied'}
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='Pagamento')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Data da solicitação')
    new_due_date = models.DateField(verbose_name='Novo vencimento')
    new_value = models.PositiveIntegerField(verbose_name='Valor com desconto', editable=False)
    update = models.DateField(auto_now=True, verbose_name='Atualização')
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='Status', default='PC', editable=False)

    def __str__(self):
        return f'{self.payment}'

    def check_date_and_availability(self):
        """
        This method guarantees that no anticipation is created if selected a date before the day
        of creation, and also if the payment status is different from available ('A').
        """
        new_due_date = self.new_due_date
        if date.fromisoformat(str(new_due_date)) < date.today():
            raise ValueError('The new payment date must be today or some day after.')
        if self.payment.status != 'A':
            raise ValueError('An anticipation can not be created from an unavailable payment.')

    def new_payment_value(self):
        """
        Calculates the new value for the payment based on the new date of payment.
        """
        i_rate = settings.INTEREST_RATE
        orig_date = date.fromisoformat(str(self.payment.due_date))
        new_date = date.fromisoformat(str(self.new_due_date))
        n_days = (orig_date - new_date).days
        new_value = self.payment.value - (self.payment.value * (i_rate / 30) * n_days)
        return new_value

    def clean(self):
        """
        If no exceptions are raised from self.check_date_and_availability() the new value for
        a payment will be calculated and provided for the field self.new_value.
        """
        self.check_date_and_availability()
        new_value = self.new_payment_value()
        self.new_value = new_value

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.clean()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
