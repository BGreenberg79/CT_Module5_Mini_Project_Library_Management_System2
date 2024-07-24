import re
from connect_mysql import connect_database

genre_regex = r"^[A-Za-z '\-]+$"
fiction_regex = r'fiction|non-fiction|Fiction|Non-Fiction'

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

'''
Here I copied the genre_regex and fiction_regex validators from the main module and imported the re module for regex validation.
'''

class Genre:
    def __init__(self, genre_name, fict_or_nonfict, description):
        self.__genre_name = genre_name
        self.__fict_or_nonfict = fict_or_nonfict
        self.__description = description
    
    def get_genre_name(self):
        return self.__genre_name
    
    def get_fict_or_nonfict(self):
        return self.__fict_or_nonfict
    
    def get_description(self):
        return self.__description
    
    def set_genre_name(self, new_genre):
        try:
            if re.match(genre_regex, new_genre):
                self.__genre_name = new_genre
        except:
            raise SetterException("Invalid genre name, please use primarily letters, hyphens, apostrophes and spaces")
        
    def set_fict_or_nonfict(self, new_type):
        try:
            if re.match(fiction_regex, new_type):
                self.__fict_or_nonfict = new_type
        except:
            raise SetterException("Please enter only Fiction or Non-Fiction")
        
    def set_description(self, edit_description):
        self.__description = edit_description
    
    def add_genre_to_table(self):
        conn = connect_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO Genres (name, fict_or_nonfict, description) VALUES (%s, %s, %s)"
                values_tuple = (self.get_genre_name(), self.get_fict_or_nonfict, self.get_description())
                cursor.execute(query, values_tuple)
                conn.commit()
                print(f"{self.get_genre_name()} has been added to Genres table")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()


    def update_genre_description(self, genre_id, new_genre_description):
        conn = connect_database()
        if conn is not None:
            try:
                self.set_description(new_genre_description)
                cursor = conn.cursor()
                query = "UPDATE Genres SET description=%s WHERE id=%s"
                values_tuple = (self.get_description(), genre_id)
                cursor.execute(query, values_tuple)
                conn.commit()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()


    def display_genre_details(self):
        conn = connect_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT g.name AS GenreName, g.fict_or_nonfict AS GenreType, g.description AS Description, b.title AS BooksInThisGenre FROM Genres g, Books b WHERE g.id = b.genre_id"
                cursor.execute(query)
                print("Genre Details:")
                for row in cursor.fetchall():
                    print(row)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

'''
The Genre class instantiates objects protected attributes for genre_name, fict_or_nonfict, and description that match it's table columns. We have getters and setters for each attribute. We also have an add genre to table
method that uses the INSERT INTO and VALUES syntax for an SQL query that will use cursor and conn methods to execute the query and commit the addition to our database. This method is in a try/except/finally block to catch any errors and close out our cursor and connection.
The display_genre_details method uses a SELECT query in SQL to retrieve rows with GenreName, GenreType(fiction or not), Description, and books written in this genre from the Books and Genres tables where the genre id's match in both tables.
We then use a for loop and the fetchall method to print all of the queries results, before closing the connection.
I also have an Update_genre_description method that connects to the database, uses the setter method for description, and uses UPDATE/SET/WHERE syntax to update the genre description at a certain genre_id. I then use cursor to execute this query with the appropriate values and commit the update to the database.
Finally I close the cursor and connection.
'''