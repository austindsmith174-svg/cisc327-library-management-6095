import pytest
from library_service import (
    get_patron_status_report
)

# Note: Since some of these tests depend on the implementation of other functions (like late fee calculation), 
# these tests will always fail until those functions are implemented, and test data is set up accordingly.

def test_get_patron_status_report():
    results = get_patron_status_report("123123")
    borrowed_books = results.get('borrowed_books', [])
    late_fee = results.get('late_fee', 0.0)
    num_borrowed = results.get('num_borrowed', 0)
    borrowed_history = results.get('borrowed_history', [])  

    assert "The Great Gatsby" in [book['title'] for book in borrowed_books]
    assert late_fee == 3.50
    assert num_borrowed == 2
    assert "1984" in [book['title'] for book in borrowed_history]

def test_get_patron_status_report_invalid_id():
    results = get_patron_status_report("-144999000")
    assert results == {}

def test_get_patron_status_report_no_borrows():
    results = get_patron_status_report("555555")
    assert results.get('borrowed_books', []) == []
    assert results.get('late_fee', 0.0) == 0.0
    assert results.get('num_borrowed', 0) == 0
    assert results.get('borrowed_history', []) == []

def test_get_patron_status_report_no_late_fees():
    results = get_patron_status_report("789789")
    assert results.get('late_fee', 0.0) == 0.0
    assert results.get('num_borrowed', 0) == 1
    assert "To Kill a Mockingbird" in [book['title'] for book in results.get('borrowed_books', [])]
    assert "To Kill a Mockingbird" in [book['title'] for book in results.get('borrowed_history', [])]
