import re
from connect_mysql import connect_database

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"

''' I import the regex module and copy over the name_regex pattern from my main module. I also define the SetterException custom Exception class in case any input in our User class's setters fail to meet Regex validation.'''

class User():
    def __init__(self, name, card_number):
        self.__name = name
        self.__card_number = card_number

    def get_name(self):
        return self.__name
    
    def get_card_number(self):
        return self.__card_number
    
    def set_name(self, new_name):
        try:
            if re.match(name_regex, new_name):
                self.__name = new_name
        except:
            raise SetterException("Invalid name formatting entered")
    
    def set_card_number(self, new_card_number):
        self.__card_number = new_card_number

    def add_user_to_table(self):
        conn = connect_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO Users (name, card_number) VALUES (%s, %s)"
                value_tuple = (self.get_name(), self.get_card_number())
                cursor.execute(query, value_tuple)
                conn.commit()
                print(f"User {self.get_name()} has been added to the users table")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    # def display_user_details(self):
    #     print(f"User Name: {self.get_name()}\nLibrary ID: {self.get_library_id()}")
    #     print("Returned Books:")
    #     if not self.get_borrowed_and_returned_books():
    #         print("No books have been returned yet by this user")
    #     else:
    #         for returned_book in self.get_borrowed_and_returned_books():
    #             print(f"{returned_book.get_title()}")
    #     print("Currently Borrowing:")
    #     if not self.get_currently_borrowed_books():
    #         print("No books currently borrowed by this user")
    #     else:
    #         for current_book in self.get_currently_borrowed_books():
    #             print(f"{current_book.get_title()}")
    