from django import forms

from workatcodev import settings
from workatcodev.payments.models import Anticipation


class FilterStatusForm(forms.Form):
    status = forms.ChoiceField(choices=settings.PAYMENT_STATUS_CHOICES)


class AnticipationForm(forms.ModelForm):
    class Meta:
        model = Anticipation
        fields = ['payment', 'new_due_date']
        widgets = {'new_due_date': forms.DateInput(attrs={'type': 'date'})}
