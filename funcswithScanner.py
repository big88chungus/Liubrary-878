from __future__ import print_function
import mysql.connector
from math import factorial

import de2120_barcode_scanner
import time
import sys
import serial

mydb = mysql.connector.connect(host="localhost", user="root", password = "123", port = "3306", database = "library")
cursor = mydb.cursor()
action = ""
my_scanner = de2120_barcode_scanner.DE2120BarcodeScanner()


def make_log(user_id, book_id, action):
    cursor.execute(f"INSERT INTO library.log (user_id, book_id, time, action) VALUES ({user_id}, {book_id}, NOW(), '{action}')")
    mydb.commit()

def show_log(limit):
    cursor.execute(f"SELECT * from library.log ORDER BY id DESC LIMIT {limit}")
    log = cursor.fetchall()
    print(log)


def add_user():
    print("Please scan barcode")
    barcode = ""

    while not barcode:
        try:
            my_scanner.start_scan()
            barcode = my_scanner.read_barcode()
            time.sleep(0.02)
        except TypeError:
            continue
    print(str(barcode))
    barcode_new = str(barcode)[-9:]
    print(barcode_new)
    time.sleep(1.5)
    u_id = int(input("What's your id? "))
    name = input("What's your name? ")
    grade = int(input("what's your grade? "))
    admin = int(input("What is the admin status? "))
    cursor.execute(f"INSERT INTO library.users VALUES ({u_id}, '{name}', {grade}, {barcode_new}, {admin})")
    mydb.commit()
    barcode = ""


def add_book():
    print("Please scan book barcode")
    barcode = ""
    while not barcode:
        try:
            my_scanner.start_scan()
            barcode = my_scanner.read_barcode()
            time.sleep(0.02)
        except TypeError:
            continue
    print(barcode)
    new_barcode = barcode[-9:]
    print(new_barcode)
    b_id = int(input("What is the book id? "))
    name = input("What is the name of the book? ")
    cursor.execute(f"INSERT INTO library.books VALUES ({b_id}, '{name}', {new_barcode})")
    mydb.commit()
    barcode = ""

def delete_data():
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("DELETE FROM books")
    cursor.execute("DELETE FROM users")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    mydb.commit()


def delete(list):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    list_to_delete = ["", ""]
    if list == 0:
        list_to_delete[0] = "DELETE FROM log"
    elif list == 1:
        list_to_delete[0] = "DELETE FROM book_user"
    elif list == 2:
        list_to_delete[0] = "DELETE FROM book_user"
        list_to_delete[1] = "DELETE FROM log"
    for i in range(factorial(list)):
        cursor.execute(f"{list_to_delete[i]}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    mydb.commit()


def rent_book(user_id, book_id):
    cursor.execute(f"INSERT INTO library.book_user VALUES ({book_id}, {user_id}, CURRENT_DATE() + INTERVAL 10 DAY)")
    mydb.commit()

    cursor.execute(f"SELECT u.name, b.name, bu.date_return FROM book_user bu JOIN users u ON bu.user_id = u.id JOIN books b ON bu.book_id = b.id WHERE bu.book_id = {book_id}")
    user_data = cursor.fetchall()
    for user in user_data:
        print(user[0], user[1], user[2])
    make_log(user_id, book_id, "rent")


def late_keepers():
    cursor.execute("SELECT u.name FROM book_user bu JOIN users u ON bu.user_id = u.id WHERE bu.date_return < curdate();")
    late_keepers = cursor.fetchall()
    for late in late_keepers:
        print(late)


def return_book(user_id, book_id):
    cursor.execute(f"DELETE from book_user WHERE user_id={user_id} AND book_id = {book_id}")
    mydb.commit()
    make_log(user_id, book_id, "return")


def complete_list():
    cursor.execute("Select * from library.book_user")
    complete_list = cursor.fetchall()
    for row in complete_list:
        print(row)


def find_user(user_barcode):
    cursor.execute(f"SELECT id, admin, name FROM library.users WHERE barcode={user_barcode}")
    found_user = cursor.fetchall()
    if len(found_user) <= 0:
        return False, -1, -1, -1
    else:
        return True, found_user[0][0], found_user[0][1], found_user[0][2]


def login_user():
    while True:
        barcode = ""
        while not barcode:
            try:
                my_scanner.start_scan()
                barcode = my_scanner.read_barcode()
                time.sleep(0.02)
            except TypeError:
                continue

        try:
            barcode_user = int(barcode[-9:])
        except ValueError:
            print("ValueError, please try again! ")
            continue
        logged_in, id_of_user, admin_rank1, username = find_user(barcode_user)
        if logged_in:
            print(f"You're logged in, {username}!")
            if admin_rank1 >= 2:
                print("Admin rights enabled")

            return id_of_user, admin_rank1
        else:
            print("User not found, please try again!")
            continue


def identify_book_status():

    while True:
        barcode = ""
        while not barcode:
            try:
                my_scanner.start_scan()

                barcode = my_scanner.read_barcode()
                time.sleep(0.02)
            except ValueError:
                continue

        try:
            book_barcode = int(barcode[-9:])
        except ValueError:
            print("ValueError! Please try again! ")
            continue

        cursor.execute(f"SELECT id FROM books WHERE books.barcode = {book_barcode}")
        is_book_real = cursor.fetchall()
        if len(is_book_real) >= 1:
            break
        elif len(is_book_real) <= 0:
            print("Book not found, please try again! ")

    cursor.execute(f"SELECT id FROM books b JOIN book_user bu ON b.id = bu.book_id WHERE b.barcode = {book_barcode}")
    book_status1 = cursor.fetchall()
    if len(book_status1) == 1:
        return True, book_status1[0][0]
    else:
        cursor.execute(f"SELECT id FROM books WHERE books.barcode = {book_barcode}")
        book_id1 = cursor.fetchall()
        return False, book_id1[0][0]
