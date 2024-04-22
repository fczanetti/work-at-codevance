from django.contrib import admin
from workatcodev.payments.models import Supplier


def email(obj):
    return obj.user.email


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['corporate_name', email, 'cnpj']
