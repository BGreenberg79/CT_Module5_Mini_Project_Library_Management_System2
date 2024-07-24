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

    def display_user_details(self):
        conn = connect_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT u.id AS UserID, u.name AS Name, u.card_number AS CardNumber, b.title AS BorrowedBookTitle, bb.borrow_date AS BorrowDate, bb.return_date AS ReturnDate FROM Users u, Books b, BorrowedBooks bb WHERE bb.user_id=u.id AND bb.book_id=b.id"
                cursor.execute(query)
                print("User Details:")
                for row in cursor.fetchall():
                    print(row)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

'''
The User class instantiates objects protected attributes for name and card number that match it's table columns. We have getters and setters for each attribute. We also have an add to table
method that uses the INSERT INTO and VALUES syntax for an SQL query that will use cursor and conn methods to execute the query and commit the addition to our database. This method is in a try/except/finally block to catch any errors and close out our cursor and connection.
Lastly the display_user_details method uses a SELECT query in SQL to retrieve rows with UserID, Name, CardNumber, BorrowedBookTitle, BorrowDate, and ReturnDate from the Users, Books, and BorrowedBooks tables where the book and user id's match in all tables.
We then use a for loop and the fetchall method to print all of the queries results once executed, before closing the connection
'''