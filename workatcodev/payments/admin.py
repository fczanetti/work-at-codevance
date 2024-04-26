from django.contrib import admin
from workatcodev.payments.models import Supplier, Payment


def email(obj):
    return obj.user.email


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['corporate_name', email, 'cnpj']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'creation_date', 'due_date', 'status', 'value']
