"""
	author: Mario Calderon
	date: 23-Feb-2023
	class: CYBR410-308H Data/Database Security
    version 1.0
    description: Application that interacts with a MySQL database 
"""

# Modules required for this program
import mysql.connector, prettytable, sys
from mysql.connector import Error
from prettytable import PrettyTable

# Configuration to connect to the WhatABook Database
config = {
    'host': 'localhost',
    'user': 'whatabook_user',
    'password': 'MySQL8IsGreat!',
    'database': 'whatabook',
    'raise_on_warnings': True
}

    # Initial menu presented when the application launches
def show_menu():
    print()
    print('-------------------')
    print('     Main Menu     ')
    print('-------------------')
    print('1. View Books')
    print('2. View Store Locations')
    print('3. My Account')
    print('4. Exit')
    print('-------------------')

def show_books(cursor):
    # Query for all books from the database
    cursor.execute('SELECT book_id, book_name, author, details FROM book')
    books = cursor.fetchall()
    # Print the list of available books with book id, name, author, and details
    print('Available Books:')
    table = PrettyTable()
    table.field_names = ["ID", "Book Name", "Author", "Details"]
    for book in books:
        table.add_row([book[0], book[1], book[2], book[3]])
    print(table)

def show_locations(cursor):
    # Query to retrive all store locations from the database
    cursor.execute('SELECT store_id, locale FROM store')
    locations = cursor.fetchall()
    # Print the list of store locations in a tabular format
    if locations:
        table = PrettyTable()
        table.field_names = ["Store ID", "Locale"]
        for location in locations:
            table.add_row([location[0], location[1]])
        print("Store Locations:")
        print(table)
    else:
        print("No store locations found.")

def validate_user(cursor):
    """
    This function takes in a cursor and user_id, and checks if the user exists in the database
    It returns True if the user exists, and False otherwise
    """
    user_id = input('Enter your user ID: ')
    cursor.execute('SELECT user_id FROM user WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()
    if user:
        return user_id
    else:
        print('Please enter a valid user ID.')
        return False

def show_account_menu():
    # Menu selections that are displayed once a valid user is selected
    print('My Account Menu')
    print('1. Wishlist')
    print('2. Add Book')
    print('3. Main Menu')

def show_wishlist(cursor, user_id):
    # Query for books from the wishlist for the given user
    cursor.execute('''
        SELECT book.book_id, book.book_name, book.author, book.details
        FROM book
        INNER JOIN wishlist ON book.book_id = wishlist.book_id
        INNER JOIN user ON wishlist.user_id = user.user_id
        WHERE user.user_id = %s
    ''', (user_id,))
    books = cursor.fetchall()
    # Print the list of books in the wishlist for the given user
    if books:
        table = PrettyTable()
        table.field_names = ["ID", "Book Name", "Author", "Details"]
        for book in books:
            table.add_row([book[0], book[1], book[2], book[3]])
        print('Your Wishlist:')
        print(table)
    else:
        print('Your Wishlist is empty')

def show_books_to_add(cursor, user_id):
    # Query for books that are not already in the user's wishlist
    cursor.execute("""
        SELECT book_id, book_name, author, details
        FROM book
        WHERE book_id NOT IN (
            SELECT book_id FROM wishlist WHERE user_id = %s
        )
    """, (user_id,))
    books = cursor.fetchall()
    # Print the list of available books and prompt the user to add a book to their wishlist
    if books:
        table = PrettyTable()
        table.field_names = ["ID", "Book Name", "Author", "Details"]
        for book in books:
            table.add_row([book[0], book[1], book[2], book[3]])
        print("Available Books:")
        print(table)
    else:
        print("No books are currently available to add to your wishlist.")
    print()
    
    book_id = input("Enter the ID of the book you want to add to your wishlist, or press Enter to go back: ")
    if book_id:
        add_book_to_wishlist(cursor, user_id, book_id)

def add_book_to_wishlist(cursor, user_id, book_id):
    try:
        # execute INSERT statement to add book to wishlist
        cursor.execute("INSERT INTO wishlist (user_id, book_id) VALUES (%s, %s)", (user_id, book_id))

        # commit changes to the database
        db.commit()

        print("Book added to wishlist!")

    except mysql.connector.Error as err:
        # if there's an error, rollback changes and print error message
        print("Error adding book to wishlist:", err)
        db.rollback()

    except Exception as e:
        # if there's any other error, print the error message and rollback changes
        print("An error occurred while adding book to wishlist:", e)
        db.rollback()

try:
    # connect to the database
    db = mysql.connector.connect(**config)

    # create a cursor
    cursor = db.cursor()

    print("\n  Welcome to the WhatABook Used Book Store Application! ")

    # show the main menu to the user
    show_menu()

    # get user input for menu choice
    user_choice = int(input("Enter your choice: "))

    # loop until user exits
    while user_choice != 4:
        # view books
        if user_choice == 1:
            show_books(cursor)

        # view store locations
        elif user_choice == 2:
            show_locations(cursor)

        # view account menu
        elif user_choice == 3:
            # validate user and get their user_id
            user_id = validate_user(cursor)

            # if user is not valid, return to main menu
            if not user_id:
                show_menu()
                continue

            # show the account menu to the user
            show_account_menu()

            # get user input for account menu choice
            account_choice = int(input("Enter your choice: "))

            # loop until user goes back to main menu
            while account_choice != 3:
                # view wishlist
                if account_choice == 1:
                    show_wishlist(cursor, user_id)

                # add book to wishlist
                elif account_choice == 2:
                    show_books_to_add(cursor, user_id)

                # invalid input
                else:
                    print("Invalid input. Please enter a number between 1 and 3.")

                # show account menu to user again
                show_account_menu()

                # get user input for account menu choice again
                account_choice = int(input("Enter your choice: "))

        # invalid input
        else:
            print("Invalid input. Please enter a number between 1 and 4.")

        # show main menu to user again
        show_menu()

        # get user input for menu choice again
        user_choice = int(input("Enter your choice: "))
  
    # close the cursor and database connection
    cursor.close()
    db.close()

    # exit program
    print("Exiting program.")
finally:
    exit()