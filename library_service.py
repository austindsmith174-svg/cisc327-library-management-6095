"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books,
    get_patron_past_borrowed_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not isinstance(author, str) or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Check if patron already has this book checked out
    patron_books = get_patron_borrowed_books(patron_id)
    already_borrowed = any(book_id == b['book_id'] for b in patron_books)
    if already_borrowed:
        return False, "You already have this book checked out."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to return a book.
    Implements R4 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."

    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    # Get list of patrons borrowed books
    current_borrowed = get_patron_borrowed_books(patron_id)
    borrowed = any(book_id == book['book_id'] for book in current_borrowed)
    # make sure the book is currently borrowed by the patron
    if not borrowed:
        return False, "No borrow record found for this book and patron."

    # Calculate late fees
    late_fee_info = calculate_late_fee_for_book(patron_id, book_id)

    # Update availability and borrow record
    availability_success = update_book_availability(book_id, 1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    return_success = update_borrow_record_return_date(patron_id, book_id, datetime.now())
    if not return_success:
        return False, "Database error occurred while updating borrow record."

    return True, f'Successfully returned "{book["title"]}". Late fee: ${late_fee_info["fee_amount"]:.2f}.'



def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.

    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        Dict: {
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
        }
    """
    current_borrowed = get_patron_borrowed_books(patron_id)
    borrowed_books = [book for book in current_borrowed if book['book_id'] == book_id]
    sorted_list = sorted(borrowed_books, key=lambda x: x['borrow_date'])
    oldest_copy = sorted_list[0] if sorted_list else None
    if oldest_copy:
        # Calculate late fees
        days_overdue = (datetime.now() - oldest_copy['due_date']).days
        if days_overdue > 7:
            fee_amount = 3.50 + (days_overdue - 7) * 1.00
        elif days_overdue > 0:
            fee_amount = days_overdue * 0.50
        else:
            fee_amount = 0.00

        if fee_amount > 15:
            fee_amount = 15
            
        if fee_amount > 0:
            status = f"{fee_amount} dollars is due for a {days_overdue} day late fee."
        else:
            status = "No late fee."
    else:
        fee_amount = 0.00
        days_overdue = 0
        status = "No borrow record found for this book and patron."
    return {
        'fee_amount': fee_amount,
        'days_overdue': days_overdue,
        'status': status
    }



def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """

    Search for books in the catalog.
    
    Args:
        search_term: Term to search for
        search_type: 'title', 'author', or 'isbn'
    
    Returns:
        List[Dict]: List of matching books
    """
    all_books = get_all_books()
    search_term = search_term.strip().lower()
    results = []

    if search_type == "title":
        results = [
            book for book in all_books
            if search_term in book["title"].lower()
        ]
    elif search_type == "author":
        results = [
            book for book in all_books
            if search_term in book["author"].lower()
        ]
    elif search_type == "isbn":
        results = [
            book for book in all_books
            if search_term == book["isbn"]
        ]
    else:
        # Invalid search type, return empty list
        results = []

    return results

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    Args:
        patron_id: 6-digit library card ID
    
    Returns:
        Dict: {
            'currently_borrowed': List of currently borrowed books,
            'late_fees': Total late fees,
            'borrowing_history': List of all borrowing history
        }
    """
    currently_borrowed = get_patron_borrowed_books(patron_id)
    late_fees = sum(calculate_late_fee_for_book(patron_id, book['book_id'])['fee_amount'] for book in currently_borrowed)
    borrowing_history = get_patron_past_borrowed_books(patron_id)

    return {
        'currently_borrowed': currently_borrowed,
        'late_fees': late_fees,
        'borrowing_history': borrowing_history
    }
