from django.urls import reverse
from model_bakery import baker
# from unittest import mock
from workatcodev.payments.models import Anticipation


# (This test was commented because sending email was deactivated)
# @mock.patch('workatcodev.payments.views.send_email.delay_on_commit')
# def test_approval_anticpation(mock_send_email, client_logged_operator, payment):
def test_approval_anticpation(client_logged_operator, payment):
    """
    Approves an anticipation and certifies:
    - anticipation status changed;
    - send_email() function was called.
    """
    antic = baker.make(Anticipation, payment=payment)
    client_logged_operator.post(reverse('payments:update_antic',
                                        kwargs={'act': 'A', 'id': antic.pk}))
    antic.refresh_from_db()
    assert antic.status == 'A'
    # mock_send_email.assert_called_once_with(sub='A', recipient=[f'{payment.supplier.user.email}'],
    #                                         ant_id=antic.pk)


# (This test was commented because sending email was deactivated)
# @mock.patch('workatcodev.payments.views.send_email.delay_on_commit')
# def test_denial_anticpation(mock_send_email, client_logged_operator, payment):
def test_denial_anticpation(client_logged_operator, payment):
    """
    Denies an anticipation and certifies:
    - anticipation status changed;
    - send_email() function was called.
    """
    antic = baker.make(Anticipation, payment=payment)
    client_logged_operator.post(reverse('payments:update_antic',
                                        kwargs={'act': 'D', 'id': antic.pk}))
    antic.refresh_from_db()
    assert antic.status == 'D'
    # mock_send_email.assert_called_once_with(sub='D', recipient=[f'{payment.supplier.user.email}'],
    #                                         ant_id=antic.pk)
