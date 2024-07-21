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
    
    
    # def display_biography(self):
    #     print(f"Name: {self.get_author_name()}\nCountry of Birth: {self.get_home_country()}\nDate of Birth: {self.get_date_of_birth()}")
    #     print("List of Books Authored in our Library:")
    #     if not self.get_authored_books():
    #         print("No books have been added for this author yet")
    #     else:
    #         for book in self.get_authored_books():
    #             print(book.get_title())
