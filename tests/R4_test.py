import pytest
from library_service import (
    return_book_by_patron
)

from database import (init_database, add_sample_data)
init_database()
add_sample_data()

def test_return_book_by_patron_success():
    success, message = return_book_by_patron('123456', 1)
    assert success == True
    assert message == "Successfully returned \"The Great Gatsby\". Late fee: $0.00."

def test_return_book_by_patron_invalid_patron_id():
    success, message = return_book_by_patron('12345', 1)
    assert success == False
    assert message == "Invalid patron ID. Must be exactly 6 digits."

def test_return_book_by_patron_book_not_found():
    success, message = return_book_by_patron('123456', -999)
    assert success == False
    assert message == "Book not found."

def test_return_book_by_patron_no_borrow_record():
    success, message = return_book_by_patron('123456', 2)
    assert success == False
    assert message == "No borrow record found for this book and patron."
