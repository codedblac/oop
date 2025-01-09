# Parent class: Book
class Book:
    def __init__(self, title, author, genre):
        # Initializing the basic attributes for a Book
        self.title = title  # The title of the book
        self.author = author  # The author of the book
        self.__genre = genre  # Genre of the book (Encapsulated)


    def get_genre(self):
        return self.__genre


    def display_info(self):
        print(f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.__genre}\n")


    def read(self):
        print(f"Reading '{self.title}' by {self.author}...")



class Ebook(Book):
    def __init__(self, title, author, genre, file_size):
        # Initializing parent class attributes (title, author, and genre)
        super().__init__(title, author, genre)
        self.file_size = file_size  # Size of the ebook file in MB


    def read(self):
        print(f"Opening the ebook '{self.title}' on your device... (File size: {self.file_size}MB)")


    def show_file_size(self):
        print(f"The file size of '{self.title}' is {self.file_size}MB.")



class PrintedBook(Book):
    def __init__(self, title, author, genre, pages):
        # Initializing parent class attributes (title, author, and genre)
        super().__init__(title, author, genre)
        self.pages = pages  # Number of pages in the printed book


    def read(self):
        print(f"Flipping through the pages of the printed book '{self.title}'... (Total Pages: {self.pages})")


    def show_page_count(self):
        print(f"'{self.title}' has {self.pages} pages.")


# Example: Creating instances of each book class to demonstrate functionality
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "Novel")
ebook1 = Ebook("Digital Fortress", "Dan Brown", "Thriller", 5)  # Ebook with a file size
printed_book1 = PrintedBook("Moby Dick", "Herman Melville", "Adventure", 635)  # Printed book with pages

# Displaying information and using methods for each book

# Display information about the basic Book
book1.display_info()
book1.read()

# Using the Ebook class and its unique methods
ebook1.display_info()  # Inherited method from Book class
ebook1.show_file_size()  # Ebook-specific method
ebook1.read()  # Overridden method

# Using the PrintedBook class and its unique methods
printed_book1.display_info()  # Inherited method from Book class
printed_book1.show_page_count()  # PrintedBook-specific method
printed_book1.read()  # Overridden method
