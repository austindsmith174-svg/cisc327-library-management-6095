"""
Patron Routes - Patron status functionality
"""

from flask import Blueprint, render_template, request, flash
from services.library_service import (
    get_patron_status_report
)

from database import get_patron_borrowed_books

patron_bp = Blueprint('patron', __name__)

@patron_bp.route('/patron')
def patron_status():
    """
    Display the patron status page.
    Web interface for R6: Patron Status Functionality
    """
    patron_id = request.args.get('patron_id', '').strip()
    status_report = get_patron_status_report(patron_id)
    currently_borrowed = status_report['currently_borrowed']
    late_fees = status_report['late_fees']
    borrowing_history = status_report['borrowing_history']
    return render_template('patron_status.html', currently_borrowed=currently_borrowed, late_fees=late_fees, borrowing_history=borrowing_history, patron_id=patron_id)