from django import forms

from workatcodev import settings


class FilterStatusForm(forms.Form):
    status = forms.ChoiceField(choices=settings.PAYMENT_STATUS_CHOICES)
