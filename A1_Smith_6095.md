### Project Implementation Status

| Function Name | Implementation Status | What is missing |
| ------------- | --------------------- | --------------- |
| Add Book To Catalog  | Complete | The ISBN field is not restricted to numbers, thus letters or words can be used for the ISBN. Not sure if this is proper. ISBNs are required to only be numbers since 2007. |
| Book Catalog Display | Complete | |
| Book Borrowing Interface | Complete | |
| Book Return Processing | Incomplete | Frontend is implemented, but there is no functionality behind the buttons |
| Late Fee Calculation API | Incomplete | The function behind the endpoint GET `/api/late_fee/<patron_id>/<book_id>` is empty, and still needs to be implemented. |
| Book Search Functionality | Incomplete | There is a frontend for the search function, but the function behind the API call if empty. |
| Patron Status Report | Incomplete | There is no frontend for this section and no mention in API calls. |

### Test Implementation Summary

Note, some of these tests, particularly R4 R5 R6 R7 will not work as they rely on other functions to be implemented.

# R1: Add Book To Catalog
The following have been tested for:
- success case
- missing title
- title over 200 characters
- integer for author name
- author name over 100 characters
- ISBN with 5 digit value

# R2: Book Catalog Display
There are no underlying library functions behind the catalog display, as it is just an HTML display of the SQLite connection/query, there was only a single test to do. The single test tests that the SQLite connection can be made, and that the list of books in the library is not empty.

# R3: Book Borrowing Interface
The following have been tested for:
- success case
- invalid patron id
- invalid book id
- attempting to book an unavailable book

# R4: Book Return Processing
The following have been tested for:
- success case
- invalid patron id
- invalid book id
- book not in borrow history

# R5: Late Fee Calculation API
The following have been tested for:
- no late fees found for patron
- 1 day late fees found for patron
- 7 day late fees found for patron
- 14 day late fees found for patron
- invalid patron id used

# R6: Book Search Functionality
- success case for title 
- success case for author 
- success case for ISBN 
- fail case for invalid title
- fail case for invalid author
- fail case for invalid ISBN

# R7: Patron Status Report 
- success case
- invalid id
- no books borrowed
- no late fees