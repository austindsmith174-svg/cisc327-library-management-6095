import pytest
from datetime import datetime, timedelta
from services.library_service import (
    borrow_book_by_patron
)

from database import (init_database, add_sample_data)
init_database()
add_sample_data()

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

# NEW IN A3

def test_current_borrowed_failure(mocker):
    mocker.patch('services.library_service.get_patron_borrow_count', return_value= 50)

    success, message = borrow_book_by_patron("999222", 7)
    assert success is False
    assert message == "You have reached the maximum borrowing limit of 5 books."

def test_repeated_borrow(mocker):
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value=[{'book_id':4}])
    success, message = borrow_book_by_patron("555888",4)
    assert success is False
    assert message == "You already have this book checked out."

def test_failed_create_record(mocker):
    mocker.patch('services.library_service.insert_borrow_record', return_value=False)
    success, message = borrow_book_by_patron("313131", 1)
    assert success is False
    assert message == "Database error occurred while creating borrow record."

def test_failed_update_availability(mocker):
    mocker.patch('services.library_service.update_book_availability', return_value=None)
    success, message = borrow_book_by_patron("313131", 1)
    assert success is False
    assert message == "Database error occurred while updating book availability."