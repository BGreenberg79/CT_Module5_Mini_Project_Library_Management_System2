import re

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"

''' I import the regex module and copy over the name_regex pattern from my main module. I also define the SetterException custom Exception class in case any input in our User class's setters fail to meet Regex validation.'''

class User():
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id
        self.__borrowed_and_returned_books = []
        self.__currently_borrowed_books = []

    def get_name(self):
        return self.__name
    
    def get_library_id(self):
        return self.__library_id
    
    def get_borrowed_and_returned_books(self):
        return self.__borrowed_and_returned_books
    
    def get_currently_borrowed_books(self):
        return self.__currently_borrowed_books
    
    def set_name(self, new_name):
        try:
            if re.match(name_regex, new_name):
                self.__name = new_name
        except:
            raise SetterException("Invalid name formatting entered")
    
    def set_library_id(self, new_id):
        self.__library_id = new_id

    def add_to_returned_list(self, book):
        try:
            self.get_borrowed_and_returned_books().append(book)
            self.get_currently_borrowed_books().remove(book)
        except IndexError:
            print("Please ensure book you are attempting to add to the returned list is already currently being borrowed.")
    
    def add_to_currently_borrowed_list(self, book):
        self.get_currently_borrowed_books().append(book)

    def display_user_details(self):
        print(f"User Name: {self.get_name()}\nLibrary ID: {self.get_library_id()}")
        print("Returned Books:")
        if not self.get_borrowed_and_returned_books():
            print("No books have been returned yet by this user")
        else:
            for returned_book in self.get_borrowed_and_returned_books():
                print(f"{returned_book.get_title()}")
        print("Currently Borrowing:")
        if not self.get_currently_borrowed_books():
            print("No books currently borrowed by this user")
        else:
            for current_book in self.get_currently_borrowed_books():
                print(f"{current_book.get_title()}")
    
'''
The User class features the init method to instantiate objects in this class with protected variables for name, library ID, and empty lists for books currently borrowed, as well as a list for books borrowed and returned.
I have getters for each of these four variables and setters for name and library id. I then have a method for add_to_returned_list that will take a book append it safely to borrowed_and_returned_books list (using a getter) and subsequently removing it from the currently_borrowed_list.
This is further protected by having an exception for index errors in case the user attempts to call this method on a book that has not already been borrowed. I the  have a method to add books to the currently borrowed list. And lastly
have a display_user_details method that will print the user name and library ID of the object that calls it on separate lines, followed by a for loop through the returned books list and the currently borrowed books list using each lists getter method, and the book class' get_title method in anticipation of Book objects being in each of those lists.
If either list is empty logic is built in to print a message that reflects that.
'''