from workatcodev.payments.models import Payment


def get_available_payments():
    """
    Returns a list containing all available payments from database.
    """
    available_payments = Payment.objects.filter(status='A')
    return list(available_payments)
