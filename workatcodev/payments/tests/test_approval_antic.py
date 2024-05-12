# from django.urls import reverse
# from model_bakery import baker
#
# from workatcodev.payments.models import Anticipation
#
#
# def test_approval_anticpation(client_logged_operator,
#                               payment):
#     """
#     Approves an anticipation and certifies its
#     status has changed.
#     """
#     antic = baker.make(Anticipation, payment=payment)
#     client_logged_operator.post(reverse('payments:approval', args=(antic.pk,)))
#     assert antic.status == 'A'
