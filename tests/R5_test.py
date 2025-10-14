import pytest
from library_service import (
    calculate_late_fee_for_book,
    return_book_by_patron,
)
from database import (
    insert_borrow_record,
)
from datetime import datetime, timedelta
now = datetime.now()

def test_no_late_fee_for_book():
    insert_borrow_record('999999', 1, now - timedelta(seconds=5), now)
    response_dict = calculate_late_fee_for_book('999999', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)
    

    assert fee_amount == 0.00
    assert days_overdue == 0
    assert status == "No late fee."
    return_book_by_patron('999999', 1)

def test_1day_late_fee_for_book():
    insert_borrow_record('999999', 1, now - timedelta(days=15), now - timedelta(days=1)) 
    response_dict = calculate_late_fee_for_book('999999', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 0.5
    assert days_overdue == 1
    assert status == f"{fee_amount} dollars is due for a {days_overdue} day late fee."
    return_book_by_patron('999999', 1)


def test_7day_late_fee_for_book():
    insert_borrow_record('999999', 1, now - timedelta(days=21), now - timedelta(days=7)) 
    response_dict = calculate_late_fee_for_book('999999', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 3.50
    assert days_overdue == 7
    assert status == f"{fee_amount} dollars is due for a {days_overdue} day late fee."
    return_book_by_patron('999999', 1)

def test_14day_late_fee_for_book():
    insert_borrow_record('999999', 1, now - timedelta(days=28), now - timedelta(days=14)) 
    response_dict = calculate_late_fee_for_book('999999', 1)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 10.50
    assert days_overdue == 14
    assert status == f"{fee_amount} dollars is due for a {days_overdue} day late fee."
    return_book_by_patron('999999', 1)

def invalid_patron_or_book():
    response_dict = calculate_late_fee_for_book('25312351253', -9999)
    fee_amount = response_dict.get('fee_amount', None)
    days_overdue = response_dict.get('days_overdue', None)
    status = response_dict.get('status', None)

    assert fee_amount == 0.00
    assert days_overdue == 0
    assert status == "Invalid patron ID or book ID."
