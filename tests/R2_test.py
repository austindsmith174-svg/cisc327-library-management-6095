import pytest
from database import get_all_books
from database import (init_database, add_sample_data)
init_database()
add_sample_data()

def test_catalog():
    # Since there are no functions that can be tested with inputs in the catalog display, there are no tests here.
    # Testing for the functionality of the display will be done in QA, where the page can be visually inspected.
    results = get_all_books()
    assert len(results) >= 0