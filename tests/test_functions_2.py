class Book:
    """
    Represents a book with a title, author, and publication year.

    Attributes:
      title (str): The title of the book.
      author (str): The author of the book.
      year (int): The publication year of the book.
    """

    def __init__(self, title, author, year):
        """
    Initializes a book with given title, author and publication year.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The publication year of the book.

    Returns:
        None
    """
        self.title = title
        self.author = author
        self.year = year

class Library:
    """
    A simple library class that allows you to add and search books.

    Attributes:
        books (list): A list of Book objects.

    Methods:
        __init__(): Initializes the library with an empty list of books.
        add_book(book): Adds a book to the library's collection.
        find_book(title): Searches for a book by title. Returns None if not found.
    """

    def __init__(self):
        """ Initializes a new instance of [Your Class Name].

    Args:
        None

    Returns:
        None
    """
        self.books = []

    def add_book(self, book):
        """Adds a new book to the collection.

    Args:
        self (Bookshelf): The current bookshelf object.
        book: A Book object to be added to the bookshelf.

    Returns:
        None
    """
        self.books.append(book)

    def find_book(self, title):
        """Finds a book with the given title in the list of books.

    Args:
        self (object): The current object instance.
        title (str): The title of the book to search for.

    Returns:
        Book: The book with the matching title, or None if not found.
    """
        for book in self.books:
            if book.title == title:
                return book
        return None

def display_book(book):
    """Displays information about a book.
    
    Args:
        book (object): A book object with attributes title, author, and year.
        
    Returns:
        None: If the book is not found.
        
    Raises:
        ValueError: If the book object is invalid or missing required attributes.
        
    Examples:
        >>> display_book(my_book)
        Title: [my_book.title], Author: [my_book.author], Year: [my_book.year]
    """
    if book is None:
        print('Book not found')
    else:
        print(f'Title: {book.title}, Author: {book.author}, Year: {book.year}')
library = Library()
book1 = Book('1984', 'George Orwell', 1949)
book2 = Book('To Kill a Mockingbird', 'Harper Lee', 1960)
library.add_book(book1)
library.add_book(book2)
found_book = library.find_book('1984')
display_book(found_book)