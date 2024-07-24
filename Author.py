import re
from connect_mysql import connect_database

name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
date_regex = r'^\d{4}-\d{2}-\d{2}'

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

class Author():
    def __init__(self, author_name, home_country, date_of_birth):
        self.__author_name = author_name
        self.__home_country = home_country
        self.__date_of_birth = date_of_birth

    def get_author_name(self):
        return self.__author_name
    
    def get_home_country(self):
        return self.__home_country
    
    def get_date_of_birth(self):
        return self.__date_of_birth
    
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
            raise SetterException("Invalid date format, enter YYYY-MM-DD")
        
    def add_author_to_table(self):
        conn = connect_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO Authors (name, home_country, date_of_birth) VALUES (%s, %s, %s)"
                value_tuple = (self.get_author_name(), self.get_home_country(), self.get_date_of_birth())
                cursor.execute(query, value_tuple)
                conn.commit()
                print(f"{self.get_author_name()} has been added to the Authors table")
            except Exception as e:
                print(f"Error:{e}")
            finally:
                cursor.close()
                conn.close()
    
    
    def display_biography(self):
        conn = connect_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT a.name AS AuthorName, a.home_country AS HomeCountry, a.date_of_birth AS AuthorDateOfBirth, b.title AS BooksWrittenByAuthor FROM Authors a, Books b WHERE a.id = b.author_id"
                cursor.execute(query)
                print("Author Details:")
                for row in cursor.fetchall():
                    print(row)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

'''
The author class instantiates objects protected attributes for name, home country, and date of birth that match it's table columns. We have getters and setters for each attribute. We also have an add to table
method that uses the INSERT INTO and VALUES syntax for an SQL query that will use cursor and conn methods to execute the query and commit the addition to our database. This method is in a try/except/finally block to catch any errors and close out our cursor and connection.
Lastly the display_biography uses a SELECT query in SQL to retrieve rows with name, home country, date of birth, and books written by author from the Books and Authors tables where the author id's match in both tables.
We then use a for loop and the fetchall method to print all of the queries results, before closing the connection
'''