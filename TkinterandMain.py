import tabulate
import funcyyys as fu
import tkinter as tk
import tabulate as tb


tabulate.PRESERVE_WHITESPACE = True


class LibraryGUI:
    def __init__(self, master):
        self.len_of_book_id_list = 0
        self.book_user_adder_turn = 0
        self.counter = 1
        self.book_barcodes = []
        self.copy_book_barcodes = []
        self.make_admin = 1
        self.log_shown_bool = False
        self.book_list_is_shown = False
        self.log_is_shown = False
        self.admin_mode = False
        self.count_changes = 0
        self.master = master
        self.userBool = False
        master.title("Library GUI")
        self.master.geometry("1920x1080")
        self.user_id_label = tk.Label(master, text="Please scan user ID", font=("Arial", 20))
        self.user_id_label.place(relx=0.5, rely=0.4, height=200, width=2000, anchor="center")
        self.user_id_entry = tk.Entry(master, font=("Arial", 14))
        self.user_id_entry.place(height=80, width=500, relx=0.5, rely=0.5, anchor="center")
        self.user_id_entry.focus_set()
        self.user_id_entry.bind("<Return>", self.show_book_id_screen)
        self.book_ids = []
        self.book_ids_copy = []
        self.user_id = 0
        self.child_window_bookshow = tk.Toplevel(self.master)

    def show_book_id_screen(self, event=None):
        self.user_id_entry.focus_set()
        user_barcode = self.user_id_entry.get()

        self.user_id_global, admin_rank, username = fu.login_user(user_barcode)
        user_id = self.user_id_global
        if user_id != -1 and user_id != -2:
            self.user_id = user_id
            self.user_id_label.place_forget()
            self.user_id_entry.place_forget()

            if admin_rank == 2:
                self.show_admin_id_screen()

            self.account = tk.Label(self.master, text=fu.give_account_rent(user_id), font=("Courier", 13), relief="groove")
            self.account.place(relx=0.7, rely=0.5, height=450, width=500, anchor="nw")


            self.greeting_label = tk.Label(self.master, text=f"Hello, {username}!", font=("Arial", 20))
            self.greeting_label.place(height=80, width=500, relx=0.5, rely=0.1, anchor="center")
            self.book_id_label = tk.Label(self.master, text="Please enter book ID", font=("Arial", 23))
            self.book_id_label.place(relx=0.5, rely=0.4, height=200, width=500, anchor="center")

            self.book_id_entry = tk.Entry(self.master, font=("Arial", 14))
            self.book_id_entry.place(height=80, width=500, relx=0.5, rely=0.5, anchor="center")
            self.book_id_entry.focus_set()
            self.book_id_entry.bind("<Return>", self.store_book_id)

            self.done_button = tk.Button(self.master, text="I'm done!", command=self.show_user_id_screen, bg="blue", fg="white", font=("Arial", 15))
            self.done_button.place(relx=0.5, rely=0.6, height=60, width=200, anchor="center")
            if self.counter == 1:
                self.show_your_books()
                self.counter += 1
        else:
            error_message = tk.Label(self.master, text="User not found, please scan again!", font=("Arial", 16))
            error_message.place(relx=0.5, rely=0.7, height=60, width=2000, anchor="center")
            self.user_id_entry.delete(0, tk.END)
            root.after(1000, error_message.destroy)

    def show_admin_id_screen(self):
        self.admin_mode = True
        self.show_log_button = tk.Button(self.master, text="show log", command=self.show_log, bg="brown", fg="white")
        self.show_log_button.place(relx=0.475, rely=0.73, height=50, width=100)
        self.show_booklist_button = tk.Button(self.master, text="show book list", command=self.show_your_books,
                                              bg='red', fg='#ffffff')
        self.show_booklist_button.place(relx=0.475, rely=0.65, height=50, width=100)

        self.Var1 = tk.IntVar()
        self.radiobutton_add_user = tk.Radiobutton(self.master, text="Nutzer hinzufügen", font=("Arial", 13),variable=self.Var1, value=1, command=self.add_user_screen)
        self.radiobutton_add_book = tk.Radiobutton(self.master, text="Buch hinzufügen", variable=self.Var1, value=2, font=("Arial", 13), command=self.add_book_screen)
        self.radiobutton_add_user.place(relx=0.07, rely=0.08, width=200, height=100)
        self.radiobutton_add_book.place(relx=0.07, rely=0.14, width=200, height=100)

    def make_admin_equals_two(self):
        self.make_admin = 2

    def add_user_screen(self):
            # name,  barcode, admin, grade fertig button

        if self.book_user_adder_turn != 2:
            print(self.book_user_adder_turn)
            self.name_entry = tk.Entry(self.master, font=("Arial", 14))
            self.name_entry.place(relx=0.075, rely=0.4, width=200, height=60)
            self.grade_entry = tk.Entry(self.master, font=("Arial", 14))
            self.grade_entry.place(relx=0.075, rely=0.5, width=200, height=60)
            self.barcode_entry = tk.Entry(self.master, font=("Arial", 14))
            self.barcode_entry.place(relx=0.075, rely=0.6, width=200, height=60)
            self.admin_check_button = tk.Checkbutton(self.master, font=("Arial", 14), text="Benutzer Admin?", width=20, command=self.make_admin_equals_two)
            self.admin_check_button.place(relx=0.075, rely=0.7, width=200, height=100)
            self.adding_done_button = tk.Button(self.master, text="Add user", bg="blue", fg="white", command=self.make_new_user_data)
            self.adding_done_button.place(relx=0.075, rely=0.8, width=150, height=70)
            self.ask_grade_label = tk.Label(self.master, text="Klasse")
            self.ask_grade_label.place(relx=0.075, rely=0.565)
            self.name_label_user = tk.Label(self.master, text="Name")
            self.name_label_user.place(relx=0.075, rely=0.375)
            self.barcode_user_label = tk.Label(self.master, text="barcode")
            self.barcode_user_label.place(relx=0.075, rely=0.480)
            if not self.userBool and self.count_changes != 0:
                self.book_name_entry.place_forget()
                self.book_barcode_entry.place_forget()
                self.adding_done_button_book.place_forget()
                self.name_label_book.place_forget()
                self.barcode_book_label.place_forget()
            self.userBool = True
            self.count_changes = 1
        self.book_user_adder_turn = 2

    def add_book_screen(self):
        print(self.book_user_adder_turn)
        #name, barcode
        if self.book_user_adder_turn != 1:
            self.book_name_entry = tk.Entry(self.master, font=("Arial", 14))
            self.book_name_entry.place(relx=0.075, rely=0.4, width=200, height=60)
            self.book_barcode_entry = tk.Entry(self.master, font=("Arial", 14))
            self.book_barcode_entry.place(relx=0.075, rely=0.5, width=200, height=60)
            self.adding_done_button_book = tk.Button(self.master, text="Add Book", bg="blue", fg="white", command=self.make_book_new_data)
            self.adding_done_button_book.place(relx=0.075, rely=0.6, width=100, height=60)
            self.name_label_book = tk.Label(self.master, text="Name")
            self.name_label_book.place(relx=0.075, rely=0.375)
            self.barcode_book_label = tk.Label(self.master, text="barcode")
            self.barcode_book_label.place(relx=0.075, rely=0.480)
            if self.userBool and self.count_changes != 0:
                self.name_entry.place_forget()
                self.grade_entry.place_forget()
                self.barcode_entry.place_forget()
                self.admin_check_button.place_forget()
                self.adding_done_button.place_forget()
                self.ask_grade_label.place_forget()
                self.name_label_user.place_forget()
                self.barcode_user_label.place_forget()
            self.userBool = False
            self.count_changes = 1
        self.book_user_adder_turn = 1

    def make_new_user_data(self):
        name = self.name_entry.get()
        grade = self.grade_entry.get()
        barcode = self.barcode_entry.get()
        admin = self.make_admin
        if name and grade and barcode:
            try:
                fu.add_user(name, barcode, grade, admin)
                self.barcode_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.grade_entry.delete(0, tk.END)
                self.admin_check_button.destroy()
                self.admin_check_button = tk.Checkbutton(self.master, font=("Arial", 14), text="Benutzer Admin?", width=20,
                                                         command=self.make_admin_equals_two)
                self.admin_check_button.place(relx=0.075, rely=0.7, width=200, height=100)
                self.make_admin = 1
                self.hurrah_widget = tk.Label(self.master, text="Nutzer hinzugefügt")
                self.hurrah_widget.place(relx=0.075, rely=0.7)
                root.after(2000, self.hurrah_widget.destroy)
            except:
                self.barcode_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.grade_entry.delete(0, tk.END)
                self.admin_check_button.destroy()
                self.admin_check_button = tk.Checkbutton(self.master, font=("Arial", 14), text="Benutzer Admin?",
                                                         width=20,
                                                         command=self.make_admin_equals_two)
                self.admin_check_button.place(relx=0.075, rely=0.7, width=200, height=100)
                self.make_admin = 1
                self.hurrah_widget = tk.Label(self.master, text="Etwas ist schiefgelaufen! Bitte versuche es erneut")
                self.hurrah_widget.place(relx=0.075, rely=0.7)
                root.after(2000, self.hurrah_widget.destroy)
        else:
            self.barcode_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
            self.hurrah_widget = tk.Label(self.master, text="Etwas ist schiefgelaufen! Bitte versuche es erneut")
            self.hurrah_widget.place(relx=0.075, rely=0.7)
            root.after(2000, self.hurrah_widget.destroy)
    def make_book_new_data(self):
        name = self.book_name_entry.get()
        code = self.book_barcode_entry.get()
        if name and code:
            try:
                fu.add_book(name, code)
                self.book_barcode_entry.delete(0, tk.END)
                self.book_name_entry.delete(0, tk.END)
                self.hurrah_widget = tk.Label(self.master, text="Buch hinzugefügt")
                self.hurrah_widget.place(relx=0.075, rely=0.57)
                root.after(2000, self.hurrah_widget.destroy)
            except:
                self.book_barcode_entry.delete(0, tk.END)
                self.book_name_entry.delete(0, tk.END)
                self.hurrah_widget = tk.Label(self.master, text="Etwas ist schiefgelaufen! Bitte versuche es erneut")
                self.hurrah_widget.place(relx=0.075, rely=0.57)
                root.after(2000, self.hurrah_widget.destroy)
        else:
            self.book_barcode_entry.delete(0, tk.END)
            self.book_name_entry.delete(0, tk.END)
            self.hurrah_widget = tk.Label(self.master, text="Etwas ist schiefgelaufen! Bitte versuche es erneut")
            self.hurrah_widget.place(relx=0.075, rely=0.57)
            root.after(2000, self.hurrah_widget.destroy)
    def show_log(self):

        df = fu.show_log(25)
        table = tb.tabulate(df, headers='keys', tablefmt='grid', showindex=False, numalign="left", stralign="left")
        self.log_shown_bool = True
        try:
            self.child_is_closed = self.child_window_bookshow.state()
        except:
            self.log_is_shown = False

        if not self.log_is_shown:
            self.child_window_bookshow = tk.Toplevel(self.master)
            self.child_window_bookshow.geometry("610x1000")
            self.child_window_bookshow.wm_transient(self.master)
            self.label_show_log = tk.Label(self.child_window_bookshow, text=table, font=("Courier", 11), relief="groove")
            self.label_show_log.pack()
            self.log_is_shown = True
            self.show_log_button["text"] = "hide log"


        elif self.log_is_shown:
            self.child_window_bookshow.withdraw()
            self.show_log_button["text"] = "show log"
            self.log_is_shown = False
        print(self.log_is_shown)

    def books_to_base(self):
        if len(self.book_barcodes) != 0:
            for book in self.book_barcodes:
                is_book_being_returned, book_id = fu.identify_book_status(self.user_id_global, book)
                if book_id == -3:
                    self.book_id_label.configure(text="Bereits ausgeliehen!")
                    root.after(3000, self.change_book_label)
                elif is_book_being_returned:
                    print("You want to return the book!")
                    fu.return_book(self.user_id, book_id)
                else:
                    print("You want to rent this book!")
                    fu.rent_book(self.user_id, book_id)
        self.book_barcodes = []
        self.book_ids = []

    def change_book_label(self):
        self.book_id_label.configure(text="Please scan Barcode!")

    def store_book_id(self, event=None):

        book_barcode = self.book_id_entry.get()
        useless_bool, book_id = fu.identify_book_status(self.user_id_global, book_barcode)
        if book_id == -2 or book_id == -1 or book_barcode in self.copy_book_barcodes:
            self.book_id_label.config(text="Book ID wrong / already scanned")
            self.book_id_entry.delete(0, tk.END)
            root.after(1500, self.change_book_label)
        else:
            self.book_namez, self.book_status = fu.book_name_and_status(book_id)
            self.book_ids.append(book_id)
            self.book_ids_copy.append(book_id)
            self.book_barcodes.append(book_barcode)
            self.copy_book_barcodes.append(book_barcode)
            self.book_id_entry.delete(0, tk.END)
            if self.book_namez:
                self.book_listbox.insert(0, f"{self.book_namez} --> {self.book_status}")
                self.len_of_book_id_list += 1
            self.book_list["text"] = f"{self.len_of_book_id_list} Bücher gescanned"
            self.account.destroy()
            self.books_to_base()
            self.account = tk.Label(self.master, text=fu.give_account_rent(self.user_id_global), font=("Courier", 13),
                                    relief="groove")
            self.account.place(relx=0.7, rely=0.5, height=450, width=500, anchor="nw")

    def show_your_books(self):
        self.len_of_book_id_list = len(self.book_ids_copy)
        if not self.book_list_is_shown:

            self.book_list = tk.Label(self.master, text=f"{self.len_of_book_id_list} Bücher gescanned", font=("Arial", 15))
            self.book_listbox = tk.Listbox(self.master)

            self.book_listbox.place(height=400, width=200, relx=0.8, rely=0.25, anchor="center")
            self.book_list.place(relx=0.8, rely=0.04, height=200, width=200, anchor="center")
            self.book_list_is_shown = True
            if self.admin_mode == True:
                self.show_booklist_button["text"] = "Hide book list"
            for index, book in enumerate(self.book_ids_copy):
                book_name, book_status = fu.book_name_and_status(book)
                if book_name != "False":
                    self.book_listbox.insert(index, f"{book_name} --> {book_status}")


        elif self.book_list_is_shown:
            self.book_list.place_forget()
            self.book_list_is_shown = False
            self.show_booklist_button["text"] = "Show book list"
            self.book_listbox.destroy()
            #self.child_window_bookshow.withdraw()


    def show_user_id_screen(self):

        self.books_to_base()
        if self.admin_mode:
            self.show_log_button.place_forget()
            self.show_booklist_button.place_forget()
            self.child_window_bookshow.destroy()

            self.radiobutton_add_user.place_forget()
            self.radiobutton_add_book.place_forget()


            if self.book_user_adder_turn == 2 or self.book_user_adder_turn == 0:
                try:
                    self.name_entry.place_forget()
                    self.grade_entry.place_forget()
                    self.barcode_entry.place_forget()
                    self.admin_check_button.place_forget()
                    self.adding_done_button.place_forget()
                    self.ask_grade_label.place_forget()
                    self.name_label_user.place_forget()
                    self.barcode_user_label.destroy()
                except:
                    print("other")

            elif self.book_user_adder_turn == 1 or self.book_user_adder_turn == 0:
                try:
                    self.book_name_entry.place_forget()
                    self.book_barcode_entry.place_forget()
                    self.adding_done_button_book.place_forget()
                    self.name_label_book.place_forget()
                    self.barcode_book_label.destroy()
                except:
                    print("hi")
        self.book_user_adder_turn = 0
        self.book_list.destroy()
        self.book_listbox.destroy()
        self.greeting_label.place_forget()
        self.book_id_label.place_forget()
        self.user_id_entry.delete(0, "end")
        self.book_id_entry.place_forget()
        self.done_button.place_forget()
        self.account.destroy()

        self.counter = 1
        self.book_ids = []
        self.book_ids_copy = []
        self.user_id_global = ""

        self.book_barcodes = []
        self.copy_book_barcodes = []
        self.make_admin = 1
        self.log_shown_bool = False
        self.book_list_is_shown = False
        self.log_is_shown = False
        self.admin_mode = False
        self.count_changes = 0
        self.userBool = False
        self.len_of_book_id_list = 0


        self.user_id_label.config(text="Please enter user ID")
        self.user_id_entry.place(height=80, width=500, relx=0.5, rely=0.5, anchor="center")
        self.user_id_label.place(relx=0.5, rely=0.4, height=200, width=2000, anchor="center")
        self.user_id_entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    LibraryGUI(root)

    root.mainloop()
