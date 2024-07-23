import re
from Book import Book
from User import User
from Author import Author
from Genre import Genre
from fetch_and_check import fetch_genre_names, fetch_isbn_numbers, fetch_author_id, fetch_genre_id, fetch_author_list, fetch_book_id_from_isbn, get_book_object_from_table, fetch_card_numbers, fetch_user_id_from_card_number, fetch_rental_id, fetch_book_id_from_title, fetch_book_id_tup, fetch_user_id_from_name, get_user_object_from_table, fetch_user_names, fetch_user_id_tup

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
                        author_name_country_list = [(author.get_author_name(), author.get_home_country()) for author in author_object_set]
                        if (new_author.get_author_name(), new_author.get_home_country()) not in author_name_country_list:
                            author_object_set.add(new_author)
                        if (new_author.get_author_name(), new_author.get_home_country()) not in fetch_author_list():
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
#Start from here
def author_operations_menu():
    global input_regex
    global name_regex
    global date_regex
    global author_list
    global library_dictionary
    while True:
        try:
            author_title_message = "\nAuthor Operations"
            print(author_title_message)
            author_menu_input = input("1. Add a new author\n2. View author bioraphy\n3. Display all author biographies\n4. Return to main menu\nEnter choice here: ")
            if re.match(input_regex, author_menu_input):
                if author_menu_input == "1":
                    new_author_name = input("Please enter the name of the author you wish to add to the system: ").title()
                    new_country_of_birth = input("Please enter the country of birth for this author: ")
                    new_author_dob = input("Please enter the date of brth for this author in MM-DD-YYYY format: ")
                    if re.match(name_regex, new_author_name) and re.match(date_regex, new_author_dob):
                        adding_author = Author(new_author_name, new_country_of_birth, new_author_dob)
                        if adding_author not in author_list:
                            author_list.append(adding_author)
                            print(f"{new_author_name} has been added to the author list.")
                        elif adding_author in author_list:
                            print(f"{new_author_name} is already in the author list and a duplicate entry has not been added.")
                elif author_menu_input == "2":
                    search_author_name = input("Please enter the name of the author you wish to view a biography of: ")
                    if re.match(name_regex, search_author_name):
                        try:
                            for author in author_list:
                                if author.get_author_name() == search_author_name:
                                    print("\n")
                                    author.display_biography()
                        except IndexError:
                            print("Please ensure author with this name has already been added to the author list before attempting to view details.")
                elif author_menu_input == "3":
                    for index, author in enumerate(author_list, 1):
                        print(f"\n{index}:"), author.display_biography()
                elif author_menu_input == "4":
                    break
                else:
                    print("Invalid input, please enter a digit 1 to 4\n")
        except Exception as e:
            print(f"Error: {e}")
        
'''
The author_operations_menu is a while loop with options 1-4 that allows the user to add author objects to the author list, display details for individual authors, or display details for each author. If the user chooses option 
1 they can add an author and are prompted to input the new authors name. At this point we convert their input to titlecase and run a regex to validate their input. We then prompt the user for a country of birth and date of birth and once this information is stored and the date is validated to be in proper format
We create the adding_author variable to store an Author class object witht he user inputs. If that object is not already in the global author list, we append it to the list. I also included logic to print a statement saying if the uathor is already in the list.
Option 2 prompts the user for a name to searh for a specific author's biographical information. Once this input is validated via regex we try to loop through the author list and use the .get_author_name method on each object looking for a match with the user input.
If there is a match we run the .display_biography method on that Author object, and I have an exception built in for an IndexError in case the user searches for an author not in the list, much like my earlier KeyError exceptions that handled searches for missing dictionary entries.
Option 3 uses the enumerate function to loop through the entire list and numbers each biographical entry in our list. Option 4 returns the user to the main menu.
'''

def genre_operations_menu():
    global input_regex
    global genre_list
    global genre_regex
    global fiction_regex
    global library_dictionary
    while True:
        try:
            genre_title_message = "\nGenre Operations"
            print(genre_title_message)
            genre_menu_input = input("1. Add a new genre\n2. Edit description of a genre\n3. View genre details\n4. Display all genres\n5. Return to main menu\nEnter choice here: ")
            if re.match(input_regex, genre_menu_input):
                if genre_menu_input == "1":
                    new_genre_name = input("Please enter the name of the genre you wish to add: ").title()
                    genre_name_list = [genre.get_genre_name() for genre in genre_list]
                    if new_genre_name not in genre_name_list:
                        genre_fict_nonfict = input("Is this genre best classified as Fiction or Non-Fiction: ").title()
                        describe_genre = input("Please enter a brief description of this genre: ")
                        if re.match(genre_regex, new_genre_name) and re.match(fiction_regex, genre_fict_nonfict):
                            adding_genre = Genre(new_genre_name, genre_fict_nonfict, describe_genre)
                            genre_list.append(adding_genre)
                            print(f"{new_genre_name} has been added to the genre list.")
                    elif new_genre_name in genre_name_list:
                        print("This genre has already been added to our genre list. Please choose options 2 or 3 to read more about it.")
                elif genre_menu_input == "2":
                    genre_input_descript = input("For which genre do you wish to update its description: ").title()
                    if re.match(genre_regex, genre_input_descript):
                        try:
                            for genre in genre_list:
                                if genre_input_descript == genre.get_genre_name():
                                    new_description = input("Please enter your updated description here: ")
                                    genre.set_description(new_description)
                                    print(f"The genre, {genre.get_genre_name()} has been updated to have the following description: {new_description}")
                                else:
                                    print("Please ensure the genre you wish to update has been already added to the list")
                        except IndexError:
                            print("Please ensure this genre has been added to the genre list before attempting to edit its description")
                elif genre_menu_input == "3":
                    search_genre_name = input("For which genre do you wish to see its details: ").title()
                    if re.match(genre_regex, search_genre_name):
                        try:
                            for genre in genre_list:
                                if search_genre_name == genre.get_genre_name():
                                    print("\n")
                                    genre.display_genre_details()
                        except IndexError:
                            print("Please ensure genre you are searching for has already been added to the genre list")
                elif genre_menu_input == "4":
                    for index, genre in enumerate(genre_list, 1):
                        print(f"\n{index}:"), genre.display_genre_details()
                elif genre_menu_input == "5":
                    break
                else:
                    print("Invalid input, please enter a digit 1 to 5\n")
        except Exception as e:
            print(f"Error: {e}")
'''
The genre_operations_menu() function is a while loop with 5 choices, the first which is to add a new genre. This works by asking for a new genre name input which we convert to title case. After validating this input
via regex I use a list comprehension to store a list of each genre name using the .get_genre_name() method. If the user input is not in this list comprehension, we then take an input for fiction vs. non fiction and  validat ethat input via regex.
I then take an input for the genre's description and use those three inputs to instaniate a Genre class object stored at adding_genre variable. We then append that variable to the global genre list.
I also include logic to return a print statement if the user tries to add the same genre more than once. In option 2 the user can update the genre's description by first entering which genre they wish to edit.
After validating that input via regex and starting a try block we loop through the genre list and try to find a match for the user input to a genre object's .get_genre_name() method. If there is a match we prompt the user to enter in their new edited description, and then use the set_description setter method to update
that object. The result is printed in the terminal and ane else statement, as well as an IndexError exception handle any attempt to edit a genre that is not found in our list. Option 3 prompts the user for a genre name for which they are searching for to display its details.
After validating that input via regex in a try block, we once again loop through the genre list and try to match the user input to the genre class's name getter method. Once there is a match we run the .display_genre_details() method on it and if there is not match we have an exception
for an IndexError prompting the user to ensure that they are searching for a Genre object that has already been added to the list. Option 4 once again uses the enumerate function to loop through the entire list, numbeirng it while running the display_genre_details() method on each object.
Option 5 breaks this while loop and returns the user to the main menu.
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