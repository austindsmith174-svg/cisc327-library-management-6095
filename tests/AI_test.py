from library_service import *
from database import *
import pytest

# R1: Add Book To Catalog
def test_add_book_success():
    result = add_book_to_catalog("Test Book", "Author Name", "1234567890123", 5)
    assert result[0] is True
    assert "success" in result[1].lower()

def test_add_book_missing_title():
    result = add_book_to_catalog("", "Author Name", "1234567890123", 5)
    assert result[0] is False
    assert "title" in result[1].lower()

def test_add_book_invalid_isbn():
    result = add_book_to_catalog("Book", "Author", "12345", 5)
    assert result[0] is False
    assert "isbn" in result[1].lower()

# R2: Book Catalog Display
def test_catalog_display_all_books():
    books = get_all_books()
    assert isinstance(books, list)
    for book in books:
        assert "title" in book
        assert "author" in book
        assert "isbn" in book

def test_catalog_available_copies():
    add_book_to_catalog("Available Book", "Author", "1234567890124", 3)
    books = get_all_books()
    found = False
    for book in books:
        if book["isbn"] == "1234567890124":
            assert book["available_copies"] == book["total_copies"]
            found = True
    assert found

# R3: Book Borrowing Interface
def test_borrow_book_success():
    add_book_to_catalog("Borrowable Book", "Author", "1234567890125", 2)
    books = get_all_books()
    book_id = [b["book_id"] for b in books if b["isbn"] == "1234567890125"][0]
    patron_id = "123456"
    result = borrow_book(patron_id, book_id)
    assert result[0] is True
    assert "success" in result[1].lower()

def test_borrow_book_invalid_patron_id():
    add_book_to_catalog("Borrow Book", "Author", "1234567890126", 2)
    books = get_all_books()
    book_id = [b["book_id"] for b in books if b["isbn"] == "1234567890126"][0]
    result = borrow_book("abc123", book_id)
    assert result[0] is False
    assert "patron" in result[1].lower()

def test_borrow_book_limit_exceeded():
    add_book_to_catalog("Limit Book", "Author", "1234567890127", 6)
    books = get_all_books()
    book_id = [b["book_id"] for b in books if b["isbn"] == "1234567890127"][0]
    patron_id = "654321"
    for _ in range(5):
        borrow_book(patron_id, book_id)
    result = borrow_book(patron_id, book_id)
    assert result[0] is False
    assert "limit" in result[1].lower()

# R4: Book Return Processing
def test_return_book_success():
    add_book_to_catalog("Returnable Book", "Author", "1234567890128", 1)
    books = get_all_books()
    book_id = [b["book_id"] for b in books if b["isbn"] == "1234567890128"][0]
    patron_id = "111111"
    borrow_book(patron_id, book_id)
    result = return_book(patron_id, book_id)
    assert result[0] is True
    assert "success" in result[1].lower()

def test_return_book_not_borrowed():
    add_book_to_catalog("Not Borrowed", "Author", "1234567890129", 1)
    books = get_all_books()
    book_id = [b["book_id"] for b in books if b["isbn"] == "1234567890129"][0]
    patron_id = "222222"
    result = return_book(patron_id, book_id)
    assert result[0] is False
    assert "not borrowed" in result[1].lower()

# R5: Late Fee Calculation API
def test_late_fee_no_overdue():
    add_book_to_catalog("Fee Book", "Author", "1234567890130", 1)
    books = get_all_books()
    book_id = [b["book_id"] for b in books if b["isbn"] == "1234567890130"][0]
    patron_id = "333333"
    borrow_book(patron_id, book_id)
    fee, days = calculate_late_fee(patron_id, book_id)
    assert fee == 0
    assert days == 0

# R6: Book Search Functionality
def test_search_title_partial():
    add_book_to_catalog("Python Programming", "Alice", "1234567890132", 1)
    results = search_catalog("python", "title")
    assert any("Python Programming" in book["title"] for book in results)

def test_search_isbn_exact():
    add_book_to_catalog("ISBN Book", "Bob", "1234567890133", 1)
    results = search_catalog("1234567890133", "isbn")
    assert any(book["isbn"] == "1234567890133" for book in results)