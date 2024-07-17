import re
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
        self.__books_in_genre = []
    
    def get_genre_name(self):
        return self.__genre_name
    
    def get_fict_or_nonfict(self):
        return self.__fict_or_nonfict
    
    def get_description(self):
        return self.__description
    
    def get_books_in_genre(self):
        return self.__books_in_genre
    
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
    
    def add_books_in_genre(self, new_book):
        self.get_books_in_genre().append(new_book)

    def display_genre_details(self):
        print(f"Genre Name: {self.get_genre_name()}\nGenre Type: {self.get_fict_or_nonfict()}\nDescripton: {self.get_description()}")
        print("Books from this Genre:")
        if not self.get_books_in_genre():
            print("No books have been added with this genre yet")
        else:
            for book in self.get_books_in_genre():
                print(book)

'''
The init method for the Genre class, we instantiate objets with variabeles for genre_name, fiction or nonfiction, and description, as well as an empty list books in genre. I then have getters
for all four of those variables, and regex validated setters for genre name, fiction or nonfition, and description. I then have an add_books_in_genre() method that will append new book titles to the books_in_genre list using that list's getter.
Lastly the display_genre_details method prints Genre Name, Type, and Description on individual lines using the getter to do each. 
I then loop through the books in genre list using the getter method, and print each book variable from the for loop. In this case I do not have the .get_title() getter method as I will be using
user input for the book_title in the main module when using this method instead of adding the whole book object and then printing that object's title when calling this display method.
I am making this one change to the Genre display method from the Author and User display method's as I noticed some issues when attempting to code this method as Genre is a parent method for Book and I believe the properties of inheritance
made it that Book objects could call Genre methods but Genre objects couldn't as easy call methods from their child class - Books. Thus to avoid any issues regarding inheritance and the relationship between Genre and Book, it became easier to populate the 
books in genre list with simple string representation of each individual book title for any given genre and then looping through that lists of strings when attempting to diplay it.
If the list is empty we have logic to handle that and a string is printed reflecting it.  
'''