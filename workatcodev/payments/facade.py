from workatcodev.payments.models import Payment


def get_payments(status):
    """
    Returns a list containing all payments from database based on the status chosen.
    """
    payments = Payment.objects.filter(status=status)
    return list(payments)
