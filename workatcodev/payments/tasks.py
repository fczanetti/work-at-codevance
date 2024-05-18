from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from workatcodev.payments.models import Anticipation
from workatcodev.settings import DEFAULT_FROM_EMAIL
from celery import shared_task


@shared_task
def send_email(sub, recipient, ant_id):
    """
    Sends an email to suppliers informing about new
    anticipations or updates in existing ones.
    """
    anticipation = Anticipation.objects.get(id=ant_id)
    subjects = {'new_ant': _('New anticipation requested.'),
                'A': _('Anticipation approved.'),
                'D': _('Anticipation denied.')}
    message = render_to_string('payments/email.html',
                               context={'sub': sub, 'anticipation': anticipation})
    send_mail(subject=subjects[sub],
              html_message=message,
              recipient_list=recipient,
              from_email=DEFAULT_FROM_EMAIL,
              message=None)
