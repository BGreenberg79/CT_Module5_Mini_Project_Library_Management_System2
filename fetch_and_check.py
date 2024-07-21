from connect_mysql import connect_database
from Book import Book

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
            query = "SELECT name, home_country FROM Authors"
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
            query = "SELECT g.name AS GenreName, g.fict_or_nonfict AS GenreType, g.description, b.title, a.name AS AuthorName, b.isbn, b.publication_date FROM Genres g, Books b, Authors a WHERE a.id = b.author_id AND g.id = b.genre_id AND b.id = %s"
            book_id_tup = (book_id,)
            cursor.execute(query, book_id_tup)
            for row in cursor.fetchall():
                genre_name, genre_type, genre_descript, book_title, author_name, book_isbn, book_pub_date = row
            book_from_table = Book(genre_name, genre_type, genre_descript, book_title, author_name, book_isbn, book_pub_date)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
            return book_from_table

def fetch_book_id_from_isbn(isbn):
    conn = connect_database()
    if conn is not None:
        try:
            id_tuple = ()
            id_string = ""
            cursor = conn.cursor()
            query = "SELECT DISTINCT id from Books WHERE isbn = %s"
            input_tuple = (isbn,)
            cursor.execute(query, input_tuple)
            for id in cursor.fetch_all():
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