from django.urls import reverse
from model_bakery import baker

from workatcodev.payments.models import Anticipation


def test_approval_anticpation(client_logged_operator,
                              payment):
    """
    Approves an anticipation and certifies its
    status has changed.
    """
    antic = baker.make(Anticipation, payment=payment)
    client_logged_operator.post(reverse('payments:update_antic',
                                        kwargs={'act': 'A', 'id': antic.pk}))
    antic.refresh_from_db()
    assert antic.status == 'A'


def test_denial_anticpation(client_logged_operator,
                            payment):
    """
    Denies an anticipation and certifies its
    status has changed.
    """
    antic = baker.make(Anticipation, payment=payment)
    client_logged_operator.post(reverse('payments:update_antic',
                                        kwargs={'act': 'D', 'id': antic.pk}))
    antic.refresh_from_db()
    assert antic.status == 'D'
