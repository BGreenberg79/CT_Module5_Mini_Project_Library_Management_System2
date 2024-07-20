import re
from Genre import Genre
from connect_mysql import connect_database

isbn_regex = r'\d{13}'
date_regex = r'^\d{2}-\d{2}-\d{4}'
name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
book_title_regex = r"^[A-Za-z0-9\s\-_,\.;:()]+$"

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

class Book(Genre):
    def __init__(self, genre_name, fict_or_nonfict, description, book_id, title, author, isbn, publication_date):
        super().__init__(genre_name, fict_or_nonfict, description)
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__publication_date = publication_date
        self.__availability_status = True

    def get_book_id(self):
        return self.__book_id
    
    def set_book_id(self, new_book_id):
        self.__book_id = new_book_id

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
    
    def borrow_book(self, user_id, borrow_date):
        conn = connect_database()
        if self.get_availability_status() == True and conn is not None:
            try:
                self.set_availability_status(False)
                cursor = conn.cursor()
                query = "UPDATE Books SET availability=%s WHERE id=%s"
                values_tuple = (self.get_availability_status(), self.get_book_id())
                cursor.execute(query, values_tuple)
                conn.commit()
                new_rental = (user_id, self.get_book_id(), borrow_date)
                insert_query = "INSERT INTO BorrowedBooks (user_id, book_id, borrow_date) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, new_rental)
                conn.commit()                
                print(f"{self.get_title()} by {self.get_author()} has succesfully been borrowed")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
                print(f"All copies of {self.get_title()} by {self.get_author()} have already been borrowed and are currently unavailable for rental")
                return False
            
    def return_book(self, user_id, rental_id, return_date):
        conn = connect_database()
        if self.get_availability_status() == False and conn is not None:
            try:
                self.set_availability_status(True)
                cursor = conn.cursor()
                query = "UPDATE Books SET availability=%s WHERE id=%s"
                values_tuple = (self.get_availability_status(), self.get_book_id())
                cursor.execute(query, values_tuple)
                conn.commit()
                return_query = "Update BorrowedBooks SET return_date=%s WHERE id=%s AND book_id=%s AND user_id=%s"
                return_tuple = (return_date, rental_id, self.get_book_id(), user_id)
                cursor.execute(return_query, return_tuple)
                conn.commit()
                print(f"{self.get_title()} by {self.get_author()} has been returned and is now availavle to be borrowed")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print(f"{self.get_title()} was already available and had not been borrowed, thus it can't be returned.")
            return False
        
    def display_details(self):
        conn = connect_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT b.id as BooksID, b.title, a.name as AuthorName, g.name as Genre, g.fict_or_nonfict, b.isbn, b.publication_date, b.availability FROM Books b, Authors a, Genres g WHERE b.author_id=a.id AND b.genre_id=g.id"
                cursor.execute(query)
                print("Book Details:")
                for row in cursor.fetchall():
                    print(row)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

'''
-
'''