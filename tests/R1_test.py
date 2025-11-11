import pytest
from services.library_service import (
    add_book_to_catalog
)
from database import (init_database, add_sample_data)
init_database()
add_sample_data()
def test_add_book_success():
    success, message = add_book_to_catalog("Winnie the Pooh", "A. A. Milne", "1231231231123", 1)
    assert success == True
    assert message == 'Book "Winnie the Pooh" has been successfully added to the catalog.'

def test_add_book_missing_title():
    success, message = add_book_to_catalog("", "A. A. Milne", "1231231231123", 1)
    assert success == False
    assert message == "Title is required."

def test_add_book_long_title():
    long_title = "A" * 999
    success, message = add_book_to_catalog(long_title, "A. A. Milne", "1231231231123", 1)
    assert success == False
    assert message == "Title must be less than 200 characters."

def test_add_book_integer_author():
    success, message = add_book_to_catalog("Winnie the Pooh", 123, "1231231231123", 1)
    assert success == False 
    assert message == "Author is required."

def test_add_book_long_author():
    long_author = "A" * 999
    success, message = add_book_to_catalog("Winnie the Pooh", long_author, "1231231231123", 1)
    assert success == False
    assert message == "Author must be less than 100 characters."

def test_add_book_invalid_isbn_length():
    success, message = add_book_to_catalog("Winnie the Pooh", "A. A. Milne", "12345", 1)
    assert success == False
    assert message == "ISBN must be exactly 13 digits." 

# NEW FOR A3

def test_negative_copies():
    success, message = add_book_to_catalog("Winnie the Pooh", "A. A. Milne", "1231231231123", -5)
    assert success == False
    assert message == "Total copies must be a positive integer."

def test_repeated_isbn():
    success, message = add_book_to_catalog("Another Book", "Some Author", "1231231231123", 3)
    assert success == False
    assert message == "A book with this ISBN already exists."

def test_insert_book_db_failure(mocker):
    mocker.patch('services.library_service.insert_book', return_value=False)
    success, message = add_book_to_catalog("Winnie the Pooh", "A. A. Milne", "3213213213213", 2)
    assert success == False
    assert message == "Database error occurred while adding the book."