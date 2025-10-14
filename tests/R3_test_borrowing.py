import pytest
from datetime import datetime, timedelta
from library_service import (
    borrow_book_by_patron
)

def test_borrow_book_success():
    success, message = borrow_book_by_patron("123456", 1)
    due_date = datetime.now() + timedelta(days=14)
    assert success is True
    assert message == f'Successfully borrowed "The Great Gatsby". Due date: {due_date.strftime("%Y-%m-%d")}.'

def test_borrow_book_invalid_patron_id():
    success, message = borrow_book_by_patron("abcdef", 1)
    assert success is False
    assert message == "Invalid patron ID. Must be exactly 6 digits."

def test_borrow_book_not_found():
    success, message = borrow_book_by_patron("123456", -5999)
    assert success is False
    assert message == "Book not found."

def test_borrow_book_not_available():
    success, message = borrow_book_by_patron("123456", 3)
    assert success is False
    assert message == "This book is currently not available."