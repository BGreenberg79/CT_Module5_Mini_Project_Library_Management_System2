import re

name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
date_regex = r'^\d{2}-\d{2}-\d{4}'

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

class Author():
    def __init__(self, author_name, home_country, date_of_birth):
        self.__author_name = author_name
        self.__home_country = home_country
        self.__date_of_birth = date_of_birth
        self.__authored_books = []

    def get_author_name(self):
        return self.__author_name
    
    def get_home_country(self):
        return self.__home_country
    
    def get_date_of_birth(self):
        return self.__date_of_birth
    
    def get_authored_books(self):
        return self.__authored_books
    
    def set_new_author_name(self, new_name):
        try:
            if re.match(name_regex, new_name):
                self.__author_name = new_name
        except:
            raise SetterException("Invalid formatting of first and last name")
    
    def set_new_home_country(self, new_country):
        self.__home_country = new_country
    
    def set_new_date_of_birth(self, new_dob):
        try:
            if re.match(date_regex, new_dob):
                self.__date_of_birth = new_dob
        except:
            raise SetterException("Invalid date format, enter MM-DD-YYYY")
    
    def add_authored_book(self, new_book):
        self.get_authored_books().append(new_book)
    
    def display_biography(self):
        print(f"Name: {self.get_author_name()}\nCountry of Birth: {self.get_home_country()}\nDate of Birth: {self.get_date_of_birth()}")
        print("List of Books Authored in our Library:")
        if not self.get_authored_books():
            print("No books have been added for this author yet")
        else:
            for book in self.get_authored_books():
                print(book.get_title())

'''
The Author class starts with an init function that instantiates objects with protected variables for author name, home country, date of birth, and an empty list of authored books.
I then have getters for all four of those variables. I then have a regex validated setter for new author name, a setter for new home cuntry, a regex validated setter for date of birth,
and an add_authored_book() method that appends new books to the authored_books list using the getter for the authored_book list. Lastly I have a display_biography method that on individual lines
prints the author's name, country of birth, and date of birth using getters. I then, also using the getter, loop through the uathored book list, and using the book Class's .get_title() method print the title of each Book object in the authored_book list
'''