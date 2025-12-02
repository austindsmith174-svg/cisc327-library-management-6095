from playwright.sync_api import Page, expect
import time
import random

BASE_URL = "http://127.0.0.1:5000"

def make_title():
    return f"Title {random.randint(1, 1000000)}"

def make_author():
    return f"Author {random.randint(1, 1000000)}"   

def make_isbn():
    return str(random.randint(1000000000000, 9999999999999))

def make_copies():
    return random.randint(1, 1000000)


def test_e2e_add_new_book(page: Page):
    page.goto(BASE_URL+"/add_book")

    title=make_title()
    author=make_author()
    isbn=make_isbn()
    copies=make_copies()
    
    page.get_by_role("textbox", name="Title").fill(title)
    page.get_by_role("textbox", name="Author").fill(author)
    page.get_by_role("textbox", name="ISBN").fill(isbn)
    page.get_by_label("Total copies").fill(str(copies))
    
    page.get_by_text("Add Book to Catalog").click()

    page.goto(BASE_URL)

    expect(page.get_by_text(title)).to_be_visible()
    expect(page.get_by_text(author)).to_be_visible()
    expect(page.get_by_text(isbn)).to_be_visible()

    testing_row = page.locator("tr", has_text=title)
    testing_row.get_by_placeholder("Patron ID (6 digits)").fill("111111")
    testing_row.get_by_role("button", name="Borrow").click()

    expect(testing_row.get_by_text(str(copies-1)+"/"+str(copies)+ " Available")).to_be_visible()
    expect(page.get_by_text("Successfully borrowed \""+title+"\".")).to_be_visible()




