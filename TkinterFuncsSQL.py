import mysql.connector
from math import factorial
import tabulate as tb
import pandas

mydb = mysql.connector.connect(host="localhost", user="root", password = "Peter2005", port = "3306", database = "library")
cursor = mydb.cursor()
action = ""

def give_account_rent(user_id):
    cursor.execute(f"SELECT b.name, bu.date_return, case when date_return < CURRENT_DATE() THEN 'Ja' ELSE '' END AS Verspätung FROM book_user bu JOIN books b ON bu.book_id = b.id WHERE bu.user_id = {user_id} ORDER BY date_return ")
    account = cursor.fetchall()
    account = pandas.DataFrame(account, columns=["Buch Name", "Abgabe", "Verspätung"])
    blankIndex = [''] * len(account)
    account.index = blankIndex
    account = tb.tabulate(account, headers='keys', tablefmt='grid', showindex=False, numalign="left", stralign="left")
    return account

def show_log(limit):
    cursor.execute(f"Select log.id, users.name, books.name, log.action, log.time FROM library.log JOIN users ON log.user_id = users.id JOIN books ON log.book_id = books.id ORDER BY time desc LIMIT {limit}")
    log_list = cursor.fetchall()
    df = pandas.DataFrame(log_list, columns=["id", "user", "book", "action", "time"])
    blankIndex = [''] * len(df)
    df.index = blankIndex
    return df


def make_log(user_id, book_id, action):
    cursor.execute(f"INSERT INTO library.log (user_id, book_id, time, action) VALUES ({user_id}, {book_id}, NOW(), '{action}')")
    mydb.commit()


def add_user(name, grade, barcode, admin):
    cursor.execute(f"INSERT INTO library.users (name, grade, barcode, admin) VALUES ('{name}', {grade}, {barcode}, {admin})")
    print("success")
    mydb.commit()


def add_book(name, barcode):
    cursor.execute(f"INSERT INTO library.books (name, barcode) VALUES ('{name}', {barcode})")
    print("success")
    mydb.commit()


def delete(list):
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


def login_user(barcode):
    while True:
        first_barcode_user = barcode

        try:
            barcode_user = int(first_barcode_user)
        except ValueError:
            print("ValueError, please try again! ")
            return -1, 1, 1
        logged_in, id_of_user, admin_rank1, username = find_user(barcode_user)
        if logged_in:
            print(f"You're logged in, {username}!")
            if admin_rank1 >= 2:
                print("Admin rights enabled")

            return id_of_user, admin_rank1, username
        else:
            print("User not found, please try again!")
            return -2, 0, 0


def book_name_and_status(book_id):

    cursor.execute(f"Select name From books Where books.id = {book_id}")
    book_name_list = cursor.fetchall()
    try:
        book_name = book_name_list[0][0]
    except IndexError:
        return False, False

    cursor.execute(f"SELECT * from book_user WHERE book_id = {book_id}")
    rent_or_return = cursor.fetchall()
    if len(rent_or_return) == 0:
        return book_name, "Ausleihen"
    else:
        return book_name, "Rückgabe"



def identify_book_status(user, book):

    book_barcode = book
    try:
        book_barcode = int(book_barcode)
    except ValueError:
        print("ValueError! Please try again! ")
        return -1, -1

    cursor.execute(f"SELECT id FROM books WHERE books.barcode = {book_barcode}")
    is_book_real = cursor.fetchall()

    if len(is_book_real) <= 0:
        return -2, -2

    cursor.execute(f"SELECT id FROM books b JOIN book_user bu ON b.id = bu.book_id WHERE b.barcode = {book_barcode}")
    book_status1 = cursor.fetchall()
    try:
        cursor.execute(f"SELECT * FROM book_user WHERE book_id = {book_status1[0][0]} AND user_id = {user}")
        staty2 = cursor.fetchall()
    except IndexError:
        print("hi")
    if len(book_status1) == 0:
        cursor.execute(f"SELECT id FROM books WHERE books.barcode = {book_barcode}")
        book_id1 = cursor.fetchall()
        return False, book_id1[0][0]

    elif len(staty2) == 0:
        return False, -3

    elif len(book_status1) == 1:
        return True, book_status1[0][0]



