def test_payment_status_after_creation(payment):
    """
    Certifies that a payment created has the status = Available.
    """
    assert payment.status == 'A'


def test_unavailable_status_payment(unavailable_payment):
    """
    Certifies that a payment created with due date earlier or equal today's date
    has its status changed to unavailable.
    """
    assert unavailable_payment.status == 'U'
