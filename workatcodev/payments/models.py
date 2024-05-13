from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group
from workatcodev.base.facade import add_payment_permission, add_anticipation_permission
from workatcodev.utils import format_value, available_anticipation


class Supplier(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    corporate_name = models.CharField(max_length=128, verbose_name='Razão Social')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', unique=True)

    def __str__(self):
        return self.corporate_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Creates a supplier group if it does not exist
        and add some permissions to it. To finish, add
        the supplier being saved to the group.
        """
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        obj = self.user
        suppliers_group, created = Group.objects.get_or_create(name='Suppliers')
        if created:
            # Adding permissions to supplier group.
            add_payment_permission(suppliers_group)
            add_anticipation_permission(suppliers_group)
        obj.groups.add(suppliers_group)


class Payment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Fornecedor')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Criação')
    due_date = models.DateField(verbose_name='Vencimento')
    value = models.FloatField(verbose_name='Valor')

    def __str__(self):
        return f'{self.supplier} - R${format_value(self.value)}'

    def create_anticipation(self):
        """
        Returns a link to anticipation creation page.
        """
        return f'{reverse("payments:anticipation", args=(self.pk,))}'

    def is_available(self):
        """
        Returns True if self.due_date was not reached yet,
        otherwise returns False.
        """
        due_date_str = str(self.due_date)
        if date.fromisoformat(due_date_str) <= date.today():
            return False
        return True


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

    def get_approval_url(self):
        return reverse('payments:update_antic', kwargs={'act': 'A', 'id': self.pk})

    def get_denial_url(self):
        return reverse('payments:update_antic', kwargs={'act': 'D', 'id': self.pk})

    def approve(self):
        """
        Approve an anticipation.
        """
        if available_anticipation(self.pk):
            self.status = 'A'
            self.save()
        else:
            raise ValueError('This anticipation can not be approved or does not exist.')


class RequestLog(models.Model):
    ACTION_CHOICES = {'A': 'Approval', 'D': 'Denial', 'R': 'Request'}
    anticipation = models.ForeignKey(Anticipation, on_delete=models.CASCADE, verbose_name='Antecipação')
    created_at = models.DateField(auto_now_add=True, verbose_name='Registrado em')
    user = models.ForeignKey(get_user_model(), verbose_name='Usuário', on_delete=models.CASCADE)
    action = models.CharField(choices=ACTION_CHOICES, verbose_name='Ação', max_length=8)

    def __str__(self):
        return f'{self.anticipation} / {self.action}'
