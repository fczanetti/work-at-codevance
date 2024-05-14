from datetime import date, datetime, timedelta
import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from workatcodev.django_assertions import assert_contains
from workatcodev.utils import format_value


@pytest.fixture
def resp_update_approval_anticip_page(client_logged_operator,
                                      payment_user_01_anticipation_created):
    """
    Creates a request to update anticipation
    page (approving) and returns a response.
    """
    d = {'act': 'A', 'id': payment_user_01_anticipation_created.anticipation.pk}
    resp = client_logged_operator.get(reverse('payments:update_antic', kwargs=d))
    return resp


def test_status_code_approval_anticip_page(resp_update_approval_anticip_page):
    """
    Certifies that approval anticipation page is loaded successfully.
    """
    assert resp_update_approval_anticip_page.status_code == 200


def test_titles_approval_page(resp_update_approval_anticip_page):
    """
    Certifies that the titles of the page are present.
    """
    assert_contains(resp_update_approval_anticip_page, f'<title>{_("Payments - Approve")}</title>')
    assert_contains(resp_update_approval_anticip_page, f'<h1 class="main-content-title">{_("Confirm approval")}</h1>')


def test_payment_is_shown_approval_page(resp_update_approval_anticip_page,
                                        payment_user_01_anticipation_created):
    """
    Certifies that the payment is shown in approval page.
    """
    d = payment_user_01_anticipation_created.due_date
    due_date = date.strftime(d, '%d/%m/%Y')
    assert_contains(resp_update_approval_anticip_page, payment_user_01_anticipation_created)
    assert_contains(resp_update_approval_anticip_page, due_date)


def test_anticipation_data_are_shown_approval_page(resp_update_approval_anticip_page,
                                                   payment_user_01_anticipation_created):
    """
    Certifies that the anticipation details are shown in approval page.
    """
    nv = format_value(payment_user_01_anticipation_created.anticipation.new_value)
    new_date = payment_user_01_anticipation_created.anticipation.new_due_date
    new_due_date = (datetime.strptime(new_date, '%Y-%m-%d').strftime('%d/%m/%Y'))
    assert_contains(resp_update_approval_anticip_page, nv)
    assert_contains(resp_update_approval_anticip_page, new_due_date)


def test_form_items_are_present_approval(resp_update_approval_anticip_page,
                                         payment_user_01_anticipation_created):
    """
    Certifies that the form items are present.
    """
    assert_contains(resp_update_approval_anticip_page, f'<a href="{reverse("payments:home", args=("PC",))}" '
                                                       f'id="canc-button" type="submit">{_("Cancel")}</a>')
    assert_contains(resp_update_approval_anticip_page, f'<button type="submit" '
                                                       f'id="conf-button">{_("Confirm")}</button>')


def test_access_denied_suppliers(client_logged_supplier_01,
                                 payment_user_01_anticipation_created):
    """
    Certifies that suppliers can not access approval anticipation page.
    """
    d = {'act': 'A', 'id': payment_user_01_anticipation_created.anticipation.pk}
    resp = client_logged_supplier_01.get(reverse('payments:update_antic', kwargs=d))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access')


def test_access_denied_common_user(client_logged_common_user,
                                   payment_user_01_anticipation_created):
    """
    Certifies that common users can not access approval anticipation page.
    """
    d = {'act': 'A', 'id': payment_user_01_anticipation_created.anticipation.pk}
    resp = client_logged_common_user.get(reverse('payments:update_antic', kwargs=d))
    assert resp.status_code == 302
    assert resp.url.startswith('/denied_access')


def test_page_not_found_for_approved_anticipation(client_logged_operator,
                                                  payment_user_01_anticipation_related_status_a):
    """
    Certifies that approval page is not loaded if tried to
    with an already approved anticipation.
    """
    d = {'act': 'A', 'id': payment_user_01_anticipation_related_status_a.anticipation.pk}
    resp = client_logged_operator.get(reverse('payments:update_antic', kwargs=d))
    assert resp.status_code == 404


def test_page_not_found_for_denied_anticipation(client_logged_operator,
                                                payment_user_01_anticipation_related_status_d):
    """
    Certifies that approval page is not loaded if tried to
    with an already denied anticipation.
    """
    d = {'act': 'A', 'id': payment_user_01_anticipation_related_status_d.anticipation.pk}
    resp = client_logged_operator.get(reverse('payments:update_antic', kwargs=d))
    assert resp.status_code == 404


def test_page_not_found_for_new_due_date_already_reached(client_logged_operator,
                                                         payment_user_01_anticipation_created):
    """
    Certifies that approval page is not loaded if anticipation
    new_due_date is some day before today.
    """
    d = {'act': 'A', 'id': payment_user_01_anticipation_created.anticipation.pk}
    payment_user_01_anticipation_created.anticipation.new_due_date = date.today() - timedelta(days=1)
    payment_user_01_anticipation_created.anticipation.save()
    resp = client_logged_operator.get(reverse('payments:update_antic', kwargs=d))
    assert resp.status_code == 404


def test_approval_page_not_found_for_act_diff_than_a_or_d(client_logged_operator,
                                                          payment_user_01_anticipation_related_status_d):
    """
    Certifies that approval page is not loaded if tried to
    with argument 'act' different from A or D.
    """
    d = {'act': 'C', 'id': payment_user_01_anticipation_related_status_d.anticipation.pk}
    resp = client_logged_operator.get(reverse('payments:update_antic', kwargs=d))
    assert resp.status_code == 404
