""" 
    book_name: whatabook.py
    Author: Alexander Taylor
    Date: 3/01/2023
    Description: Whatabook program
"""

#imports
import sys
import mysql.connector
from mysql.connector import errorcode

#database config
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}


#Method for the main menu
def show_menu():
    while True:
        print("\n  -- Main Menu --")
        print("    1. View Books\n    2. View Store Locations\n    3. My Account\n    4. Exit Program")
        try:
            choice = int(input('      <Example enter: 1 for book listing>: '))
            if choice < 1 or choice > 4:
                print("\n  Invalid number, please try again...")
            elif choice == 4:
                print("\n  Exiting program...")
                sys.exit(0)
            else:
                return choice
        except ValueError:
            print("\n  Invalid number, please try again...")


#Method to grab all books currently on database
def show_books(_cursor):
    _cursor.execute("SELECT book_id, book_name, author, details FROM book")
    books = _cursor.fetchall()
    print("\n  -- BOOK INFORMATION --")   
    for book in books:
        print("  Book ID: {}\n  Book Name: {}\n  Author: {}\n  Details: {}\n".format(book[0], book[1], book[2], book[3]))


#Method to grab location from database
def show_locations(_cursor):
    _cursor.execute("SELECT store_id, locale FROM store")
    locations = _cursor.fetchall()
    print("\n  -- DISPLAYING STORE LOCATIONS --")
    for location in locations:
        print("  Locale: {}\n".format(location[1]))


#Method to validate user input with what is in the database
def validate_user(_cursor):
    _cursor.execute("SELECT user_id FROM user")
    valid_choices = [row[0] for row in _cursor.fetchall()]
    while True:
        print("\n  -- user SELECTION MENU --")
        try:
            choice = int(input('      ENTER user ID NUMBER: '))
            if choice not in valid_choices:
                print("\n  Invalid value, please try again...")
            else:
                return choice
        except ValueError:
            print("\n  Invalid value, please try again...")


#Method to show account and get user input
def show_account_menu():
    while True:
        print("\n      -- user Menu --")
        print("        1. Wishlist\n        2. Add Book\n        3. Main Menu\n        4. Exit")
        try:
            choose_account = int(input('      <Example enter: 1 for book listing>: '))
            if choose_account < 1 or choose_account > 4:
                print("\n  Invalid value, please try again...")
            elif choose_account == 4:
                print("\n  Exiting program...")
                sys.exit(0)
            else:
                return choose_account
        except ValueError:
            print("\n  Invalid value, please try again...")


#Method to show wishlist based on user
def show_wishlist(_cursor, _user_id):
    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))
    wishlist = _cursor.fetchall()
    print("\n        -- DISPLAYING WISHLIST  --")
    for book in wishlist:
        print("        Book Name: {}\n        Author: {}\n".format(book[4], book[5]))


#Method to show available books to add to a wishlist
def show_books_to_add(_cursor, _user_id):
    _cursor.execute("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))
    books_to_add = _cursor.fetchall()
    print("\n        -- DISPLAYING AVAILABLE BOOKS --")
    for book in books_to_add:
        print("        Book Id: {}\n        Book book_name: {}\n".format(book[0], book[1]))


# Method to add books to wishlist
def add_book_to_wishlist(_cursor, _user_id, _book_id):
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))


# Beginning of Main Program
try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print("\n  Welcome to WhatABook! ")
    user_selection = show_menu()

    #Main Menu
    while user_selection != 4:
        if user_selection == 1:         
            show_books(cursor)
        if user_selection == 2:         
            show_locations(cursor)
        if user_selection == 3:         
            my_user_id = validate_user(cursor)
            account_option = show_account_menu()

            #User Menu
            while account_option != 3:
                if account_option == 1:
                    show_wishlist(cursor, my_user_id)
                if account_option == 2:
                    show_books_to_add(cursor, my_user_id)
                    book_id = int(input("\n        Enter the id of the book you want to add: "))
                    add_book_to_wishlist(cursor, my_user_id, book_id)
                    db.commit()
                    print("\n        Book id: {} was added to your wishlist!".format(book_id))

                #End User Menu
                account_option = show_account_menu() 

        #End Main Menu
        user_selection = show_menu() 

    print("\n\n  End program...")


# handle any errors
except mysql.connector.errors.ProgrammingError as err:
    print(f"An error occurred: {err.msg}")

# finally block to close database
finally:

    db.close()