from datetime import date

from workatcodev import settings


def check_payment_due_date(payment):
    """
    This function receives an instance of Payment and verify if its due date is equal or
    earlier than today's date. If so, the payment's status will be changed to Unavailable (U).
    """
    due_date_str = str(payment.due_date)
    if date.fromisoformat(due_date_str) <= date.today():
        payment.status = 'U'
    return


def new_payment_value(orig_date, new_date, orig_value):
    """
    Calculates the new value for the payment based on the new date of payment.
    """
    i_rate = settings.INTEREST_RATE
    orig_date = date.fromisoformat(str(orig_date))
    new_date = date.fromisoformat(str(new_date))
    n_days = (orig_date - new_date).days
    new_value = orig_value - (orig_value * (i_rate / 30) * n_days)
    return new_value
