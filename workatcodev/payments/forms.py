from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from workatcodev.payments.models import Anticipation, Payment
from datetime import date


class FilterStatusForm(forms.Form):
    PAYMENT_STATUS_CHOICES = {'A': _('Available'),
                              'U': _('Unavailable'),
                              'PC': _('Pending confirmation'),
                              'AN': _('Anticipated'),
                              'D': _('Denied')}
    status = forms.ChoiceField(choices=PAYMENT_STATUS_CHOICES)


class AnticipationForm(forms.ModelForm):
    class Meta:
        model = Anticipation
        fields = ['payment', 'new_due_date', 'new_value']
        widgets = {'new_due_date': forms.DateInput(attrs={'type': 'date'})}

    def clean_new_due_date(self):
        d = self.cleaned_data['new_due_date']
        if d < date.today():
            raise ValidationError(_('The new payment date must be today or some day after.'), code='invalid')
        return d


class NewPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['supplier', 'due_date', 'value']
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}

    def clean_due_date(self):
        d = self.cleaned_data['due_date']
        if d < date.today():
            raise ValidationError(_('Due date must be today or some day after.'), code='invalid')
        return d

    def clean_value(self):
        v = self.cleaned_data['value']
        if v <= 0:
            raise ValidationError(_('The value must be bigger than zero.'))
        return v
