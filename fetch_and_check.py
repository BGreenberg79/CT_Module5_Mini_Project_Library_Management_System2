from connect_mysql import connect_database
from Book import Book
from User import User
from Author import Author
from Genre import Genre

def fetch_genre_names():
    conn = connect_database()
    if conn is not None:
        try:
            genre_name_tuple = ()
            cursor = conn.cursor()
            query = "SELECT name FROM Genres"
            cursor.execute(query)
            for genre_name in cursor.fetchall():
                genre_name_tuple += genre_name
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return genre_name_tuple

def fetch_isbn_numbers():
    conn = connect_database()
    if conn is not None:
        try:
            isbn_tuple = ()
            cursor = conn.cursor()
            query = "SELECT isbn FROM Books"
            cursor.execute(query)
            for isbn_number in cursor.fetchall():
                isbn_tuple += isbn_number
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return isbn_tuple

def fetch_author_list():
    conn = connect_database()
    if conn is not None:
        try:
            author_list = []
            cursor = conn.cursor()
            query = "SELECT name, home_country, date_of_birth FROM Authors"
            cursor.execute(query)
            for row in cursor.fetchall():
                author_list.append(row)
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return author_list
        
def fetch_author_id(author_name, home_country):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM Authors WHERE name = %s AND home_country = %s"
            input_tuple = (author_name, home_country)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string

def fetch_author_id_name_only(author_name):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM Authors WHERE name = %s"
            input_tuple = (author_name,)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string


def get_author_object_from_table(author_id):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT name, home_country, date_of_birth FROM Authors WHERE id = %s"
            author_id_tup = (author_id,)
            cursor.execute(query, author_id_tup)
            for row in cursor.fetchall():
                author_name, author_home_country, author_dob = row
            author_from_table = Author(author_name, author_home_country, author_dob)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return author_from_table
        
def fetch_author_names():
    conn = connect_database()
    if conn is not None:
        try:
            author_name_tuple = ()
            cursor = conn.cursor()
            query = "SELECT name FROM AUthors"
            cursor.execute(query)
            for name in cursor.fetchall():
                author_name_tuple += name
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return author_name_tuple

def fetch_author_id_tup():
    conn = connect_database()
    if conn is not None:
        try:
            author_id_tup = ()
            cursor = conn.cursor()
            query = "SELECT id FROM Authors"
            cursor.execute(query)
            for row in cursor.fetchall():
                author_id_tup += row
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return author_id_tup
        
def fetch_genre_id_tup():
    conn = connect_database()
    if conn is not None:
        try:
            genre_id_tup = ()
            cursor = conn.cursor()
            query = "SELECT id from Genres"
            cursor.execute(query)
            for row in cursor.fetchall():
                genre_id_tup += row
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return genre_id_tup


def fetch_genre_id(genre_name):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM Genres WHERE name = %s"
            input_tuple = (genre_name,)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string

def get_book_object_from_table(book_id):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT b.title, a.name AS AuthorName, b.isbn, b.publication_date FROM Genres g, Books b, Authors a WHERE a.id = b.author_id AND g.id = b.genre_id AND b.id = %s"
            book_id_tup = (book_id,)
            cursor.execute(query, book_id_tup)
            for row in cursor.fetchall():
                book_title, author_name, book_isbn, book_pub_date = row
            book_from_table = Book(book_title, author_name, book_isbn, book_pub_date)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return book_from_table

def fetch_book_id_tup():
    conn = connect_database()
    if conn is not None:
        try:
            book_id_tup = ()
            cursor = conn.cursor()
            query = "SELECT id FROM Books"
            cursor.execute(query)
            for row in cursor.fetchall():
                book_id_tup += row
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return book_id_tup


def fetch_book_id_from_isbn(isbn):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM Books WHERE isbn = %s"
            input_tuple = (isbn,)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string
    
def fetch_book_id_from_title(title):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM Books WHERE title = %s"
            input_tuple = (title,)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string

def fetch_card_numbers():
    conn = connect_database()
    if conn is not None:
        try:
            card_num_tuple = ()
            cursor = conn.cursor()
            query = "SELECT card_number FROM Users"
            cursor.execute(query)
            for card_num in cursor.fetchall():
                card_num_tuple += card_num
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return card_num_tuple

def fetch_user_names():
    conn = connect_database()
    if conn is not None:
        try:
            user_name_tuple = ()
            cursor = conn.cursor()
            query = "SELECT name FROM Users"
            cursor.execute(query)
            for name in cursor.fetchall():
                user_name_tuple += name
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return user_name_tuple

def fetch_user_id_tup():
    conn = connect_database()
    if conn is not None:
        try:
            user_id_tup = ()
            cursor = conn.cursor()
            query = "SELECT id FROM Users"
            cursor.execute(query)
            for row in cursor.fetchall():
                user_id_tup += row
            ""
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return user_id_tup

def fetch_user_id_from_card_number(card_number):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM Users WHERE card_number = %s"
            input_tuple = (card_number,)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string

def fetch_user_id_from_name(name):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM Users WHERE name = %s"
            input_tuple = (name,)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string

def fetch_rental_id(book_id, user_id):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id FROM BorrowedBooks WHERE book_id = %s AND user_id = %s"
            input_tuple = (book_id, user_id)
            cursor.execute(query, input_tuple)
            for id in cursor.fetchall():
                id_tuple += id
            for item in id_tuple:
                id_string += item
            id_string.strip()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return id_string
        
def get_user_object_from_table(user_id):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT name, card_number FROM Users WHERE id = %s"
            user_id_tup = (user_id,)
            cursor.execute(query, user_id_tup)
            for row in cursor.fetchall():
                user_name, user_card_num = row
            user_from_table = User(user_name, user_card_num)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return user_from_table
        
def get_genre_object_from_table(genre_id):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT name, fict_or_nonfict, description FROM Genres WHERE id = %s"
            genre_id_tup = (genre_id,)
            cursor.execute(query, genre_id_tup)
            for row in cursor.fetchall():
                genre_name, genre_type, genre_descript = row
            genre_from_table = Genre(genre_name, genre_type, genre_descript)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return genre_from_table
        
'''
This module contains a litany of functions that returns tuples, strings, and objects for various attributes we need when looking up ID's from inputs, seeing if a user input is alredy in our database or not,
or unpacking tuples from our database into Class Objects for easy access to methods in our main module. This module was needed as I realized that the only way to avoid duplicates in our databse each time the user accesses the database in a new session would be
through SELECT and fetch all functions that could be called without a class object to start with. Notably every function in this module ends with a return statement fter the connections have all been closed, and not a single one of these functions has the conn.commit() syntax
as all actual updates or insertions into our database are handled by class methods. As those methods handle actual manipuation of our database it was imperative to have a logically strong way to retrieve existing class objects from our database.
'''