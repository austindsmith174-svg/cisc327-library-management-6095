import pytest
from library_service import (
    calculate_late_fee_for_book
)

def test_no_late_fee_for_book():
    response_dict = calculate_late_fee_for_book('123456', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 0.00
    assert days_overdue == 0
    assert status == "No late fee."

def test_1day_late_fee_for_book():
    response_dict = calculate_late_fee_for_book('123456', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 0.50
    assert days_overdue == 1
    assert status == f"{fee_amount} dollars is due for a {days_overdue} day late fee."

def test_7day_late_fee_for_book():
    response_dict = calculate_late_fee_for_book('123456', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 3.50
    assert days_overdue == 7
    assert status == f"{fee_amount} dollars is due for a {days_overdue} day late fee."

def test_14day_late_fee_for_book():
    response_dict = calculate_late_fee_for_book('123456', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 10.50
    assert days_overdue == 14
    assert status == f"{fee_amount} dollars is due for a {days_overdue} day late fee."

def invalid_patron_or_book():
    response_dict = calculate_late_fee_for_book('25312351253', -9999)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 0.00
    assert days_overdue == 0
    assert status == "Invalid patron ID or book ID."
