import funcs as fu

while True:
    user_id, admin_rank = fu.login_user()
    while True:
        print("Please scan book")
        is_book_being_returned, book_id = fu.identify_book_status()
        if is_book_being_returned:
            print("You want to return the book!")
            fu.return_book(user_id, book_id)
        else:
            print("You want to rent this book!")
            fu.rent_book(user_id, book_id)

