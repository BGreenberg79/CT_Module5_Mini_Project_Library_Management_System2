import re
from Genre import Genre

isbn_regex = r'\d{13}'
date_regex = r'^\d{2}-\d{2}-\d{4}'
name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
book_title_regex = r"^[A-Za-z0-9\s\-_,\.;:()]+$"

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

class Book(Genre):
    def __init__(self, genre_name, fict_or_nonfict, description, title, author, isbn, publication_date):
        super().__init__(genre_name, fict_or_nonfict, description)
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__publication_date = publication_date
        self.__availability_status = True

    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author
    
    def get_isbn(self):
        return self.__isbn
    
    def get_publication_date(self):
        return self.__publication_date
    
    def get_availability_status(self):
        return self.__availability_status
    
    def set_title(self, new_title):
        try:
            if re.match(book_title_regex, new_title):
                self.__title = new_title
        except:
            raise SetterException("Invalid book title when using setter")
        
    def set_author(self, new_author):
        try:
            if re.match(name_regex, new_author):
                self.__author = new_author
        except:
            raise SetterException("Invalid author name format when using setter")
        
    def set_isbn(self, new_isbn):
        try:
            if re.match(isbn_regex, new_isbn):
                self.__isbn = new_isbn
        except:
            raise SetterException("Invalid ISBN format when using setter")
    
    def set_publication_date(self, new_pub_date):
        try:
            if re.match(date_regex, new_pub_date):
                self.__publication_date = new_pub_date
        except:
            raise SetterException("Invalid date format when using setter")
    
    def set_availability_status(self, new_status):
        try:
            if isinstance(new_status, bool) == True:
                self.__availability_status = new_status
        except:
            raise SetterException("Please use boolean when adjusting availability status")
    
    def borrow_book(self):
        if self.get_availability_status() == True:
            self.set_availability_status(False)
            print(f"{self.get_title()} by {self.get_author()} has succesfully been borrowed")
            return True
        else:
            print(f"All copies of {self.get_title()} by {self.get_author()} have already been borrowed and are currently unavailable for rental")
            return False
        
    def return_book(self):
        if self.get_availability_status() == False:
            self.set_availability_status(True)
            print(f"{self.get_title()} by {self.get_author()} has been returned and is now availavle to be borrowed")
            return True
        else:
            print(f"{self.get_title()} was already available and had not been borrowed, thus it can't be returned.")
            return False
        
    def display_details(self):
        print(f"Title: {self.get_title()}\nAuthor: {self.get_author()}\nISBN: {self.get_isbn()}\nPublication Date: {self.get_publication_date()}\nAvailable to Borrow: {self.get_availability_status()}\nGenre: {self.get_genre_name()}\nGenre Type: {self.get_fict_or_nonfict()}\nGenre Description: {self.get_description()}")

'''
The Book module starts with imports for both re (for regex validation) and of the Genre class from the Genre module.  I then copy over regex patterns for ISBN, names, book titles, and dates.
I then define the SetterException custom exception class. The Book class starts with the Genre class in parentheses as Genre is its parents class. Likewise when we define Books init method it includes the variables needed to instantiate
a Genre class as well, and then has the super.__init__ syntax inside of it. I then have variables for title, author, isbn, publication date, and a Boolean for availability status that is set to always start as True
I have getters for each of the 5 variables specific to the book class and regex validated setters for them as well. Notably unique for the set_availability_status setter I use an if statement followed
by the built in isinstance() function to ensure that the new_status being used is a True or False boolean and if it is inot we raise our custom SetterException. I then define the borrrow_book method which first checks if
get_availability_status() method will return as true for the object we are calling it on. If it does we can then use the availability status setter calling it with a False boolean and printing the result before returning a True result.
In the else statement I print a message stating that the book is unavailable to be borrowed and return a False boolean. In return book I use the exact same logic flipped to ensure that the book being returned is returning as a False boolean using the getter
beofre setting its new status to a True boolean. Once I do this I print the result and return a True output for the method. Otherwise I print that the book was already available and return a False output.
Lastly the display_details() method uses getters to print through every piece of information each book object has including all 5 variables specific to the Book class and the 3 variables it inherits from its parent Genre class.
'''