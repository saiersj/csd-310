import sys
import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

def show_menu():
    print("\n -- Main Menu -- \n")

    print(" 1. Show Books\n 2. View WhatABook Locations\n 3. View Account\n 4. Exit Program")

    try:
        choice = int(input(' Select an option from above: '))

        return choice
    except ValueError:
        print("\n  Invalid input, exiting program...\n")

        sys.exit(0)

def show_books(cursor):
    cursor.execute("SELECT book_id, book_name, author, details from book")

    books = cursor.fetchall()

    print("\n  -- DISPLAYING BOOK LISTING --")

    for book in books:
        print(" Book ID: {}\n Book Name: {}\n Author: {}\n Details: {}\n".format(book[0], book[1], book[2], book[3]))

def show_locations(cursor):
    cursor.execute("SELECT store_id, locale from store")

    locations = cursor.fetchall()

    print("\n  -- DISPLAYING STORE LOCATIONS --")

    for location in locations:
        print("Location: {}\n".format(location[1]))

def validate_user():

    try:
        user_id = int(
            input('\n Please Enter Your Customer ID Number: '))

        if user_id < 0 or user_id > 3:
            print("\n Invalid customer number, program terminated...\n")
            sys.exit(0)

        return user_id
    except ValueError:
        print("\n Invalid number, program terminated...\n")

        sys.exit(0)

def show_account_menu():

    try:
        print("\n -- Account Menu --\n")
        print(" 1. Wishlist\n 2. Add Book\n 3. Main Menu\n")
        account_option = int(
            input('Please select an option from above: '))

        return account_option
    except ValueError:
        print("\nInvalid input, exiting program...")

        sys.exit(0)

def show_wishlist(cursor, user_id):

    cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author FROM wishlist INNER JOIN user ON wishlist.user_id = user.user_id INNER JOIN book ON wishlist.book_id = book.book_id WHERE user.user_id = {}".format(user_id))

    wishlist = cursor.fetchall()

    print("\n-- DISPLAYING WISHLIST ITEMS --")

    for book in wishlist:
        print(" Book Name: {}\n Author: {}\n".format(book[4], book[5]))

def show_books_to_add(cursor, user_id):

    query = ("SELECT book_id, book_name, author, details FROM book WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(user_id))

    print(query)

    cursor.execute(query)

    books_to_add = cursor.fetchall()

    print("\n -- DISPLAYING AVAILABLE BOOKS --")

    for book in books_to_add:
        print("Book Id: {}\nBook Name: {}\nAuthor: {}\nDetails: {}\n".format(book[0], book[1], book[2], book[3]))

def add_book_to_wishlist(cursor, user_id, book_id):
    cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(
        user_id, book_id))

try:
    db = mysql.connector.connect(**config)

    cursor = db.cursor()
    print("\n  Welcome to the WhatABook Application! ")

    user_selection = show_menu()

    while user_selection != 4:

        if user_selection == 1:
            show_books(cursor)

        if user_selection == 2:
            show_locations(cursor)

        if user_selection == 3:
            my_user_id = validate_user()
            account_option = show_account_menu()

            while account_option != 3:

                if account_option == 1:
                    show_wishlist(cursor, my_user_id)

                if account_option == 2:

                    show_books_to_add(cursor, my_user_id)

                    book_id = int(
                        input("\nEnter the Book ID you would like to add to your wishlist: "))

                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    db.commit()

                    print("\nBook id: {} was added to your wishlist!".format(book_id))

                if account_option < 0 or account_option > 3:
                    print("\n Invalid input, please try again...")

                account_option = show_account_menu()

        if user_selection < 0 or user_selection > 4:
            print("\n Invalid input, please try again...")

        user_selection = show_menu()

    print("\n\n Exiting Program...")

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The username or password provided are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)

finally:
    db.close()