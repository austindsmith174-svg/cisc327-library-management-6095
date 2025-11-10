import pytest
from services.library_service import (
    get_patron_status_report
)
from database import (
    insert_borrow_record, update_borrow_record_return_date
)

from database import (init_database, add_sample_data)
init_database()
add_sample_data()

from datetime import datetime, timedelta
now = datetime.now()

def test_get_patron_status_report():
    insert_borrow_record("123123", 1, now - timedelta(days=21), now-timedelta(days=7))
    insert_borrow_record("123123", 3, now - timedelta(days=5), now + timedelta(days=9))
    update_borrow_record_return_date("123123", 3, now)
    results = get_patron_status_report("123123")
    borrowed_books = results.get('currently_borrowed', [])
    late_fee = results.get('late_fees', 0.0)
    borrowed_history = results.get('borrowing_history', [])  

    assert "The Great Gatsby" in [book['title'] for book in borrowed_books]
    assert late_fee == 3.50
    assert "1984" in [book['title'] for book in borrowed_history]

def test_get_patron_status_report_invalid_id():
    results = get_patron_status_report("-144999000")
    assert results.get('currently_borrowed', []) == []
    assert results.get('late_fees', 0.0) == 0.0
    assert results.get('borrowing_history', []) == []

def test_get_patron_status_report_no_borrows():
    results = get_patron_status_report("555555")
    assert results.get('currently_borrowed', []) == []
    assert results.get('late_fees', 0.0) == 0.0
    assert results.get('borrowing_history', []) == []

def test_get_patron_status_report_no_late_fees():
    insert_borrow_record("789789", 2, now - timedelta(days=21), now-timedelta(days=7))
    update_borrow_record_return_date("789789", 2, now)
    insert_borrow_record("789789", 2, now, now+timedelta(days=14))

    results = get_patron_status_report("789789")
    assert "To Kill a Mockingbird" in [book['title'] for book in results.get('currently_borrowed', [])]
    assert results.get('late_fees', 0.0) == 0.0
    assert "To Kill a Mockingbird" in [book['title'] for book in results.get('borrowing_history', [])]