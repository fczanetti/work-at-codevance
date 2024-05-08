from django.contrib import admin

from workatcodev.payments import facade
from workatcodev.payments.models import Supplier, Payment, Anticipation


def email(obj):
    return obj.user.email


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['corporate_name', email, 'cnpj']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'creation_date', 'due_date', 'value']


@admin.register(Anticipation)
class AnticipationAdmin(admin.ModelAdmin):
    list_display = ['payment', 'creation_date', 'new_due_date', 'new_value', 'update', 'status']
    fieldsets = (
        (None, {"fields": ("payment", "new_due_date")}),
    )

    def save_model(self, request, obj, form, change):
        new_value = facade.new_payment_value(obj.payment, obj.new_due_date)
        obj.new_value = new_value
        super().save_model(request, obj, form, change)
