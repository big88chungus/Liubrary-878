import funcs as fu

while True:
    print("Please scan ID")
    user_id, admin_rank = fu.login_user()
    print("Please scan book")
    while True:
        
        try:
            
            is_book_being_returned, book_id = fu.identify_book_status()
            if is_book_being_returned:
                print("You want to return the book!")
                fu.return_book(user_id, book_id)
            else:
                print("You want to rent this book!")
                fu.rent_book(user_id, book_id)
        except TypeError:
            continue
        print("Please scan book")


