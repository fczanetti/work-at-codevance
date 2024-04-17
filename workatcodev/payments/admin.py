from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from workatcodev.base.admin import UserAdmin
from workatcodev.payments.models import Operator, Supplier


@admin.register(Operator)
class OperatorAdmin(UserAdmin):
    list_display = ['first_name', 'email', 'is_staff']


@admin.register(Supplier)
class SupplierAdmin(UserAdmin):
    list_display = ["corporate_name", "cnpj", "email"]
    fieldsets = (
        (_("Personal info"), {"fields": ("corporate_name", "cnpj", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("corporate_name", "cnpj", "email", "password1", "password2"),
            },
        ),
    )
