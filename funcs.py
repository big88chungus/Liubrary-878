import mysql.connector
from math import factorial

mydb = mysql.connector.connect(host="localhost", user="root", password = "Peter2005", port = "3306", database = "library")
cursor = mydb.cursor()
action = ""


def make_log(user_id, book_id, action):
    cursor.execute(f"INSERT INTO library.log VALUES ({user_id}, {book_id}, NOW(), '{action}')")
    mydb.commit()


def add_user(id, name, grade, barcode, admin):
    cursor.execute(f"INSERT INTO library.users VALUES ({id, name, grade, barcode, admin})")
    mydb.commit()


def add_book(id, name, barcode):
    cursor.execute(f"INSERT INTO library.users VALUES ({id, name, barcode})")
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


def login_user():
    while True:
        first_barcode_user = input("Whats your barcode: ")

        try:
            barcode_user = int(first_barcode_user)
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
        book_barcode = input()
        try:
            book_barcode = int(book_barcode)
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
