from datetime import date


def check_payment_due_date(payment):
    """
    This function receives an instance of Payment and verify if its due date is equal or
    earlier than today's date. If so, the payment's status will be changed to Unavailable (U).
    """
    if payment.due_date <= date.today():
        payment.status = 'U'
    return
