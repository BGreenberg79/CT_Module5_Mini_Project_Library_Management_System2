import re
from Book import Book
from User import User
from Author import Author
from Genre import Genre
from fetch_and_check import fetch_genre_names, fetch_isbn_numbers, fetch_author_id, fetch_genre_id, fetch_author_list, fetch_book_id_from_isbn, get_book_object_from_table, fetch_card_numbers, fetch_user_id_from_card_number, fetch_rental_id, fetch_book_id_from_title, fetch_book_id_tup, fetch_user_id_from_name, get_user_object_from_table, fetch_user_names, fetch_user_id_tup, fetch_author_id_name_only, get_author_object_from_table, fetch_author_names, fetch_author_id_tup, get_genre_object_from_table, fetch_genre_id_tup

''' Here we import each module for each of the 4 classes our main program will feature: Book, User, Author, and Genre. We also import the regular expression module.'''

input_regex = r'^\d{1}$'
isbn_regex = r'\d{13}'
date_regex = r'^\d{4}-\d{2}-\d{2}'
name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
book_title_regex = r"^[A-Za-z0-9\s\-_,\.;:()]+$"
genre_regex = r"^[A-Za-z '\-]+$"
fiction_regex = r'fiction|non-fiction|Fiction|Non-Fiction'

book_object_set = set()
user_object_set = set()
author_object_set = set()
genre_object_set = set()

''' 
Here I globally define regular expressions for menu input, ISBN numbers, publishing an birthdates, author and user names, book title, genres, and fiction vs. non-fiction'.
I also initialize our library and uer dictionaries and author and genre lists. Library dictionary uses ISBN as a unqique key identifier, while Users will use thie rlibrary ID as keys for their unique identifier.
'''

def book_operations_menu():
    global input_regex
    global date_regex
    global name_regex
    global isbn_regex
    global book_title_regex
    global genre_regex
    global fiction_regex
    global book_object_set
    global user_object_set
    global author_object_set
    global genre_object_set
    while True:
        book_title_message = "\nBooks Operations:"
        print(book_title_message)
        book_menu_input = input("1. Add a new book\n2. Borrow a book\n3. Return a book\n4. Search for a book\n5. Display all books\n6. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, book_menu_input):
            if book_menu_input == "1":
                try:
                    book_title = input("Enter title of book you are adding to library: ")
                    author_name = input("Enter author of book: ").title()
                    isbn = input("Enter 13 digit ISBN number (remove hyphens): ")
                    publication_date = input("Enter publication date (YYYY-MM-DD): ")
                    genre_name = input("What is this book's genre: ").title()
                    genre_type = input("Please enter if this genre is best categorized as Fiction or Non-Fiction: ").title()
                    genre_descript = input("Please enter a brief description of this genre: ")
                    if re.match(genre_regex, genre_name) and re.match(fiction_regex, genre_type):
                        new_genre = Genre(genre_name, genre_type, genre_descript)
                        genre_name_list = [genre.get_genre_name() for genre in genre_object_set]
                        if new_genre.get_genre_name() not in genre_name_list:
                            genre_object_set.add(new_genre)
                        if new_genre.get_genre_name() not in fetch_genre_names():
                            new_genre.add_genre_to_table()
                        else:
                            print(f"The genre {new_genre.get_genre_name()} is already in our database")
                    else:
                        print("Please enter a valid genre name and Fiction or Non-Fiction only in inputs")
                    author_home_country = input("Please enter their country of birth: ")
                    author_new_dob = input("Now please enter their date of birth in YYYY-MM-DD format: ")
                    if re.match(date_regex, author_new_dob):
                        new_author = Author(author_name, author_home_country, author_new_dob)
                        author_name_country_list = [(author.get_author_name(), author.get_home_country(), author.get_date_of_birth()) for author in author_object_set]
                        if (new_author.get_author_name(), new_author.get_home_country(), new_author.get_date_of_birth()) not in author_name_country_list:
                            author_object_set.add(new_author)
                        if (new_author.get_author_name(), new_author.get_home_country(), new_author.get_date_of_birth()) not in fetch_author_list():
                            new_author.add_author_to_table()
                        else:
                            print(f"{new_author.get_author_name()} from {new_author.get_home_country()} is already in our database")
                    else:
                        print("Pleae enter author's date of birth in valid format (YYYY-MM-DD)")
                    if re.match(book_title_regex, book_title) and re.match(name_regex, author_name) and re.match(isbn_regex, isbn) and re.match(date_regex, publication_date):
                        new_book = Book(book_title, author_name, isbn, publication_date)
                        book_isbn_list = [book.get_isbn() for book in book_object_set]
                        if new_book.get_isbn() not in book_isbn_list:
                            book_object_set.add(new_book)
                        if new_book.get_isbn() not in fetch_isbn_numbers():
                            author_id = fetch_author_id(author_name, author_home_country)
                            genre_id = fetch_genre_id(genre_name)
                            new_book.add_book_to_database(author_id, genre_id)
                        else:
                            print(f"{new_book.get_title()} with ISBN {new_book.get_isbn()} is already in our database")   
                    else:
                        print("Please ensure all inputs are in valid formats.")
                except Exception as e:
                    print(f"Error: {e}")
            elif book_menu_input == "2":
                try:
                    rental_isbn = input("Enter ISBN of book you wish to rent: ")
                    if re.match(isbn_regex, rental_isbn):
                        if rental_isbn in fetch_isbn_numbers():
                            rental_book_id = fetch_book_id_from_isbn(rental_isbn)
                            rental_book = get_book_object_from_table(rental_book_id)
                            card_num = input("Enter (or create) your Library card number here: ")
                            borrow_date = input("Please enter the date you borrowed this book: ")
                            if card_num not in fetch_card_numbers():
                                renter_name = input("We are setting up your new account, please enter your name here: ")
                                if re.match(name_regex, renter_name):
                                    new_user = User(renter_name, card_num)
                                    new_user.add_user_to_table()
                                    card_num_list = [user.get_card_number() for user in user_object_set]
                                    if new_user.get_card_number() not in card_num_list:
                                        user_object_set.add(new_user)
                            rental_user_id = fetch_user_id_from_card_number(card_num)
                            rental_book.borrow_book(rental_user_id, borrow_date, rental_book_id)
                        else:
                            print("Please ensure book with this ISBN number has been added to library before attempting to borrow it")
                    else:
                        print("Please ensure ISBN entered in proper format")
                except Exception as e:
                    print(f"Error: {e}")
            elif book_menu_input == "3":
                try:
                    return_isbn = input("Enter ISBN for book you wish to return to library: ")
                    if re.match(isbn_regex, return_isbn):
                        if return_isbn in fetch_isbn_numbers():
                            return_book_id = fetch_book_id_from_isbn(return_isbn)
                            return_book = get_book_object_from_table(return_book_id)
                            return_card_num = input("Enter your Library card number here: ")
                            return_date = input("Please enter the date you returned this book: ")
                            if return_card_num not in fetch_card_numbers():
                                print("Please ensure user has been registered to system before returning books.")
                            else:
                                return_user_id = fetch_user_id_from_card_number(return_card_num)
                                borrowed_books_id = fetch_rental_id(return_book_id, return_user_id)
                                return_book.return_book(return_book_id, return_user_id, borrowed_books_id, return_date)
                        else:
                            print("Please ensure book with this ISBN number has been added to library before attempting to return it")
                except Exception as e:
                    print(f"Error: {e}")
            elif book_menu_input == "4":
                try:
                    search_criteria = input("Please enter criteria you wish to search by (title or ISBN): ").lower()
                    if search_criteria == "title":
                        search_title = input("Enter title of book you are searching for: ")
                        if re.match(book_title_regex, search_title):
                            lookup_title_bookid = fetch_book_id_from_title(search_title)
                            title_book_display = get_book_object_from_table(lookup_title_bookid)
                            title_book_display.display_details()
                        else:
                            print("Please ensure valid title was entered into input")
                    elif search_criteria == "isbn":
                            search_isbn = input("Enter ISBN number (remove hyphens): ")
                            if re.match(isbn_regex, search_isbn):
                                lookup_isbn_bookid = fetch_book_id_from_isbn(search_isbn)
                                isbn_book_display = get_book_object_from_table(lookup_isbn_bookid)
                                isbn_book_display.display_details()
                            else:
                                print("Please ensure valid ISBN was entered into input")
                except Exception as e:
                    print(f"Error: {e}")
            elif book_menu_input == "5":
                list_of_book_objects = []
                for book_id in fetch_book_id_tup():
                    book_object = get_book_object_from_table(book_id)
                    list_of_book_objects.append(book_object)
                for index, book in enumerate(list_of_book_objects, 1):
                    print(f"{str(index)}:"), book.display_details()
            elif book_menu_input == "6":
                break
            else:
                print("Invalid input, please enter a digit 1 to 6\n")
    

'''
The book_operations function is the most complicated function in the program and it needs to reference global variables for all of its regular expression handling. 
The function works by giving users the option to add a book, which uses Book class methods, as well as Author and Genre classes to successfully add new and unique books, authors, and 
genres to their appropriate SQL tables referencing both class methods and my extensive lst of fetch_and_check functions. The fetch_and_check functions allow us to verify that a user is not inputing a duplicate,
as well as succesfully look up book_id's, genre_id's, and author_id's that are auto incremented. It also allows us to unpack a SELECT query tuple into Book objects so we can then call Book methods in our code.
Options two and three take in the appropriate inputs and use the aforementioned fetch and check functions to add entries to the BorrowedBooks table, update a the Book table and object's availability, and lastly UPDATE BorrowedBooks upon the return date.
Option 4 asks the user if they wish to look up a book's details by ISBN or title and then uses that information to fetch the appropriate book_id, unpack a tuple into a book object and then run the .display_details() method on that object.
Lastly Option 5 runs the .display_details() method on every book in our database by fetching every book_id, and then using each book_id to get book objects and add those book objects into a temporary list that we can then run the enumerate function
on to create a numbered list where every book's details are displayed. Option 6 returns users to the main menu.
'''

def user_operations_menu():
    global input_regex
    global name_regex
    global user_object_set
    while True:
        try:
            user_title_message = "\nUser Operations"
            print(user_title_message)
            user_menu_input = input("1. Add a new user\n2. View user details\n3. Display all users\n4. Return to main menu\nEnter choice here: ")
            if re.match(input_regex, user_menu_input):
                if user_menu_input == "1":
                    new_user_name = input("Please enter your name: ")
                    new_card_num = input("Please enter your new Library card number: ")
                    if new_card_num in fetch_card_numbers():
                        print("It appears a user with this library card has already been added to our database. Please try a new number.")
                    else:
                        if re.match(name_regex,new_user_name):
                            new_user_object = User(new_user_name, new_card_num)
                            new_user_object.add_user_to_table()
                            user_object_set_card_num_list = [user.get_card_number() for user in user_object_set]
                            if new_card_num not in user_object_set_card_num_list:
                                user_object_set.add(new_user_object)
                            else:
                                print("User object was already in temporary User set.")
                        else:
                            print("Please ensure a valid name was entered for the user.")
                elif user_menu_input == "2":
                    user_search_criteria = input("Please enter if you wish to search by 'Name' or 'Card Number': ").lower()
                    if user_search_criteria == 'name':
                        search_user_name = input("Please enter your name here: ")
                        if search_user_name in fetch_user_names():
                            if re.match(name_regex, search_user_name):
                                search_user_id_by_name = fetch_user_id_from_name(search_user_name)
                                display_name_user_object = get_user_object_from_table(search_user_id_by_name)
                                display_name_user_object.display_user_details()
                            else:
                                print("Please enter your name in valid first and last name format.")
                        else:
                            print("Please ensure user has first been added too database")
                    elif user_search_criteria == 'card number':
                            search_card_num = input("Please enter your card bumber here: ")
                            if search_card_num in fetch_card_numbers():
                                search_user_id_by_card_num = fetch_user_id_from_card_number(search_card_num)
                                display_card_num_user_object = get_user_object_from_table(search_user_id_by_card_num)
                                display_card_num_user_object.display_user_details()
                            else:
                                print("Please ensure a user with this card number has been entered into the database.")
                    else:
                        print("Invalid input please respond with 'Name' or 'Library ID'")
                elif user_menu_input == "3":
                    list_of_user_objects = []
                    for user_id in fetch_user_id_tup():
                        user_object = get_user_object_from_table(user_id)
                        list_of_user_objects.append(user_object)
                    for index, user in enumerate(list_of_user_objects, 1):
                        print(f"{str(index)}:"), user.display_user_details()
                elif user_menu_input == "4":
                    break
                else:
                    print("Invalid input, please enter a digit 1 to 4\n")
        except Exception as e:
            print(f"Error: {e}")
            
'''
The user operations menu uses the global user object set as well as the input_regex and name_regex variables. If the user chooses to add a new user they are prompted for inputs for  name and library card number.
We then verify that we are not entering a duplicate by using our fetch and check variables, and if its is a new card number we run regex verification on the name input.
We then instantiate a new User object to have access to the methods from the two inputs, then calling the .add_user_to_table() method on our new object. I then verify with a list comprehension
that our User object does not already have a duplicate in our user_object_set using the .get_card_number() method. If there is not duplicate we use the .add() method to add it to our local object set.
In option two we can search for a user by name or card number and then dispaly their details. Much like the book menu we use fetchers and regex to verify that our user's input is valid and once we do that 
we retrieve the auto-incremented ID by using our user's search criteria input. We then use that ID to call our get_user_object_from_table() function that unpacks a fetchall tuple into a User object.
We then call the .display_user_details method on our new object.
Option 3 instantiates a temporary list of user objects that we will populate by looping through all of our auto-incremented user ID's, using the get_user_object_from_table() fucntion on them and then appending those user_objects to the list.
Then we run another for loop, this time as an enumerate function where we run through the list we just populated starting at 1 and calling the .display_user_details() method on each object.
'''
def author_operations_menu():
    global input_regex
    global name_regex
    global date_regex
    global author_object_set
    while True:
        try:
            author_title_message = "\nAuthor Operations"
            print(author_title_message)
            author_menu_input = input("1. Add a new author\n2. View author bioraphy\n3. Display all author biographies\n4. Return to main menu\nEnter choice here: ")
            if re.match(input_regex, author_menu_input):
                if author_menu_input == "1":
                    new_author_name = input("Please enter the name of the author you wish to add to the system: ").title()
                    new_country_of_birth = input("Please enter the country of birth for this author: ").title()
                    new_author_dob = input("Please enter the date of brth for this author in YYYY-MM-DD format: ")
                    if (new_author_name, new_country_of_birth, new_author_dob) in fetch_author_list():
                        print("It appears this author has already been added to our database.")
                    else:
                        if re.match(name_regex, new_author_name) and re.match(date_regex, new_author_dob):
                            adding_author = Author(new_author_name, new_country_of_birth, new_author_dob)
                            adding_author.add_author_to_table()
                            author_set_object_list = [(author.get_author_name(), author.get_home_country(), author.get_date_of_birth()) for author in author_object_set]
                            if (adding_author.get_author_name(), adding_author.get_home_country(), adding_author.get_date_of_birth()) not in author_set_object_list:
                                author_object_set.add(adding_author)
                        else:
                            print("Please ensure valid name and date inputs were used.")
                elif author_menu_input == "2":
                    search_author_name = input("Please enter the name of the author you wish to view a biography of: ")
                    if re.match(name_regex, search_author_name):
                        if search_author_name in fetch_author_names():
                            search_author_id = fetch_author_id_name_only(search_author_name)
                            search_author_object = get_author_object_from_table(search_author_id)
                            search_author_object.display_biography()
                        else:
                            print("Please ensure the author you are searching for has been added to the database already.")
                    else:
                        print("Please ensure a valid name input was entered")
                elif author_menu_input == "3":
                    list_of_author_objects = []
                    for author_id in fetch_author_id_tup():
                        author_object = get_author_object_from_table(author_id)
                        list_of_author_objects.append(author_object)
                    for index, author in enumerate(list_of_author_objects, 1):
                        print(f"{str(index)}:"), author.display_biography()
                elif author_menu_input == "4":
                    break
                else:
                    print("Invalid input, please enter a digit 1 to 4\n")
        except Exception as e:
            print(f"Error: {e}")
        
'''
The author operations menu uses the global author object set as well as the input_regex, date regex, and name_regex variables. If the user chooses to add a new author they are prompted for inputs for name, home country and date of birth.
We then verify that we are not entering a duplicate by using our fetch and check functions, and if its is a new author we run regex verification on the name and date input.
We then instantiate a new Author object to have access to the methods from the three inputs, then calling the .add_author_to_table() method on our new object. I then verify with a list comprehension
that our Author object does not already have a duplicate in our author_object_set using a tuple and getter methods on each of its attributes. If there is no duplicate we use the .add() method to add it to our local object set.
In option two we can search for an author by name and then dispaly their biography. Much like the book and user menus we use fetchers and regex to verify that our user's input is valid and once we do that 
we retrieve the auto-incremented author ID that matches the user's name input. We then use that ID to call our get_author_object_from_table() function that unpacks a fetchall tuple into an Author object.
We then call the .display_biography method on our new object.
Option 3 instantiates a temporary list of author objects that we will populate by looping through all of our auto-incremented author ID's, using the get_author_object_from_table() fucntion on them and then appending those author_objects to the list.
Then we run another for loop, this time as an enumerate function where we run through the list we just populated starting at 1 and calling the .display_biography() method on each object.

'''

def genre_operations_menu():
    global input_regex
    global genre_object_set
    global genre_regex
    global fiction_regex
    while True:
        try:
            genre_title_message = "\nGenre Operations"
            print(genre_title_message)
            genre_menu_input = input("1. Add a new genre\n2. Edit description of a genre\n3. View genre details\n4. Display all genres\n5. Return to main menu\nEnter choice here: ")
            if re.match(input_regex, genre_menu_input):
                if genre_menu_input == "1":
                    new_genre_name = input("Please enter the name of the genre you wish to add: ").title()
                    genre_fict_nonfict = input("Is this genre best classified as Fiction or Non-Fiction: ").title()
                    describe_genre = input("Please enter a brief description of this genre: ")
                    if re.match(genre_regex, new_genre_name) and re.match(fiction_regex, genre_fict_nonfict):
                        if new_genre_name in fetch_genre_names():
                            print("It appears this genre has already been added to the Genres table")
                        else:
                            adding_genre = Genre(new_genre_name, genre_fict_nonfict, describe_genre)
                            adding_genre.add_genre_to_table()
                            genre_object_set_name_list = [genre.get_genre_name() for genre in genre_object_set]
                            if new_genre_name not in genre_object_set_name_list:
                                genre_object_set.add(adding_genre)
                    else:
                        print("Please ensure a valid input for genre name and Fiction/Non-Fiction classification.")
                elif genre_menu_input == "2":
                    genre_input_descript = input("For which genre do you wish to update its description: ").title()
                    if re.match(genre_regex, genre_input_descript):
                        if genre_input_descript in fetch_genre_names():
                            new_description = input("Please enter your updated description here: ")
                            edit_genre_descript_id = fetch_genre_id(genre_input_descript)
                            edit_descript_genre_object = get_genre_object_from_table(edit_genre_descript_id)
                            edit_descript_genre_object.update_genre_description(edit_genre_descript_id, new_description)
                            print(f"The genre, {edit_descript_genre_object.get_genre_name()} has been updated to have the following description: {new_description}")
                        else:
                            print("Please ensure the genre you wish to update has been already added to the database")
                    else:
                        print("Please ensure valid formatting of genre inputs.")
                elif genre_menu_input == "3":
                    search_genre_name = input("For which genre do you wish to see its details: ").title()
                    if re.match(genre_regex, search_genre_name):
                        if search_genre_name in fetch_genre_names():
                            search_genre_id = fetch_genre_id(search_genre_name)
                            search_genre_object = get_genre_object_from_table(search_genre_id)
                            search_genre_object.display_genre_details()
                        else:
                            print("Please ensure the genre you are searching for has been added to the database already.")
                    else:
                        print("Please ensure valid input for genre name.")
                elif genre_menu_input == "4":
                    list_of_genre_objects = []
                    for genre_id in fetch_genre_id_tup():
                        genre_object = get_genre_object_from_table(genre_id)
                        list_of_genre_objects.append(genre_object)
                    for index, genre in enumerate(list_of_genre_objects, 1):
                        print(f"{str(index)}:"), genre.display_genre_details()
                elif genre_menu_input == "5":
                    break
                else:
                    print("Invalid input, please enter a digit 1 to 5\n")
        except Exception as e:
            print(f"Error: {e}")
'''
The genre operations menu uses the global genre object set as well as the input_regex, genre regex, and fiction regex variables. If the user chooses to add a new genre they are prompted for inputs for name, fiction or non-fiction and description.
We then verify that we are not entering a duplicate by using our fetch and check functions, and if its is a new genre we run regex verification on the name and fiction/non-fiction input.
We then instantiate a new Genre object to have access to the methods from the three inputs, then calling the .add_genre_to_table() method on our new object. I then verify with a list comprehension
that our Genre object does not already have a duplicate in our genre_object_set using the name getter method on each object in the set. If there is no duplicate we use the .add() method to add it to our local object set.
In option two I take an input to identify which genre we are updating. I then check that it pases regex verification and that this genre name is in our database. If it is I take an input for a new description, fetch the genre_id based off the name entered in the input
and retrieve the genre object from the table that matches the genre_id we fetched. With this object now instatiated locally I run the update_genre_description method using the genre_id input we retrieved and the new description entered into our input.
In option 3 we can search for a genre by name and then dispaly its details. Much like the book, author, and user menus we use fetchers and regex to verify that our user's input is valid and once we do that 
we retrieve the auto-incremented genre ID that matches the user's name input. We then use that ID to call our get_genre_object_from_table() function that unpacks a fetchall tuple into a genre object.
We then call the .display_genre_details method on our new object.
Option 3 instantiates a temporary list of genre objects that we will populate by looping through all of our auto-incremented genre ID's, using the get_genre_object_from_table() fucntion on them and then appending those genre_objects to the list.
Then we run another for loop, this time as an enumerate function where we run through the list we just populated starting at 1 and calling the .display_genre_details() method on each object.

'''



def main_menu():
    global input_regex
    welcome_message = "Welcome To The Library Management System!\n"
    print(welcome_message)
    while True:
        menu_input = input("\nMain Menu:\n1. Book Operations\n2. User Operations\n3. Author Operations\n4. Genre Operations\n5. Quit\nEnter choice here: ")
        if re.match(input_regex, menu_input):
            if menu_input == "1":
                print("\n")
                book_operations_menu()
            elif menu_input == "2":
                print("\n")
                user_operations_menu()
            elif menu_input == "3":
                print("\n")
                author_operations_menu()
            elif menu_input == "4":
                print("\n")
                genre_operations_menu()
            elif menu_input == "5":
                break
            else:
                print("Invalid input, please enter a digit 1 to 5\n")

main_menu()

'''
The overall main_menu structure uses regex to validate that the user is entering a valid digit input. It gives the user options 1-5 that allows them to navigate to Book Operations, User Operations, Author Operations, Genre Operations, or to quit
the program altogether. Options 1-4 call each specific menu's individual function and option 5 uses the break keyword to break this function's while loop and end the program.
'''