import pytest
from library_service import (
    search_books_in_catalog
)

def test_search_by_title():
    results = search_books_in_catalog("The Great Gatsby", "title")
    assert len(results) > 0
    for book in results:
        assert "The Great Gatsby".lower() in book['title'].lower()

def test_search_by_author():
    results = search_books_in_catalog("George Orwell", "author")
    assert len(results) > 0
    for book in results:
        assert "George Orwell".lower() in book['author'].lower()

def test_search_by_isbn():
    results = search_books_in_catalog("9780451524935", "isbn")
    assert len(results) > 0
    for book in results:
        assert "9780451524935" == book['isbn']

def test_search_no_results():
    results = search_books_in_catalog("NONEXISTENT_BOOK_NAME_63845762398456273694287364", "title")
    assert len(results) == 0
    results = search_books_in_catalog("NONEXISTENT_AUTHOR_NAME_63845762398456273694287364", "author")
    assert len(results) == 0
    results = search_books_in_catalog("0000000000000", "isbn")
    assert len(results) == 0