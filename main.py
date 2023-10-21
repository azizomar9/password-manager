from tkinter import *
import sqlite3, hashlib
from functools import partial

#creating connection with a database

with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

#creates a table in the database to store master password
cursor.execute("""
CREATE TABLE IF NOT EXISTS master_password(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL
)
""")

#creates a table in the database to store website/username/password
cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL
)
""")

#function to hash the master password given by the user
def hash_master_password(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    print(hash)
    return hash

#function that will display only on the first use of the program which takes
# in a new master password from the user and stores it into the database
def first_run():
    def masterpass_clicked():

        #if else statement that checks whether both passwords match up and will either take the user to the next screen
        #or it will tell the user they dont match until the passwords entered eventually match.
        if master_password_entry.get() == master_password_rentry.get():
            hashed_password = hash_master_password(master_password_entry.get().encode('utf-8'))
            insert_password= """INSERT INTO master_password(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashed_password)])
            db.commit()

            master_login()

        else:
            error_label = Label(text="The passwords do not match. Try again.", font=("Arial", 10, "bold"))
            error_label.grid(column=1, row=6, columnspan=2)


    # Setting up the title, labels, canvas, and entries on the window.
    window.title("Password Manager Login")
    window.config(padx=60, pady=60)

    canvas = Canvas(height=200, width=200)
    # logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(column=1, row=0)

    master_password_label = Label(text="Master Password:", font=("Arial", 10, "bold"))
    master_password_label.grid(column=0, row=3)
    master_password_entry = Entry(width=30, show="*")
    master_password_entry.grid(column=1, row=3)

    master_password_label = Label(text="Re-Enter Master Password:", font=("Arial", 10, "bold"))
    master_password_label.grid(column=0, row=4)
    master_password_rentry = Entry(width=30, show="*")
    master_password_rentry.grid(column=1, row=4)

    save = Button(text="Login", command=masterpass_clicked, width=36)
    save.grid(column=1, row=5, columnspan=2)

#function to display the password vault
def vault_screen():
    #gets rid of all previous widgets in the window
    for widget in window.winfo_children():
        widget.destroy()


    window.config(padx=100, pady=100)
    window.resizable(height=None, width=None)
    lbl = Label(window, text="Saved Passwords", font=("Arial", 20, "bold"), fg='#f00')
    lbl.grid(column=1, row = 0)

    btn = Button(window, text="Add New Password", command=new_password)
    btn.grid(column=1, pady=15, row = 1)

    lbl = Label(window, text="Website", font=("Arial", 12 , "bold"))
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="Username", font=("Arial", 12 , "bold"))
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="Password", font=("Arial", 12 , "bold"))
    lbl.grid(row=2, column=2, padx=80)

    #this displays all previous values in the database if there are any
    cursor.execute('SELECT * FROM vault')
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute('SELECT * FROM vault')
            array = cursor.fetchall()

            if (len(array) == 0):
                break

            def copy_to_clipboard(text):
                window.clipboard_clear()
                window.clipboard_append(text)
                window.update()

            def delete_entry(text1, text2, text3):
                website = text1
                username = text2
                password = text3
                delete_query = """DELETE FROM vault WHERE website=? AND username=? AND password=?"""
                cursor.execute(delete_query, (website, username, password))
                db.commit()  # Commit the changes to the database

            #iterates through each value in the vault database and displays their information
            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl1.grid(column=0, row=(i + 3))
            lbl2 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl2.grid(column=1, row=(i + 3))
            lbl3 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl3.grid(column=2, row=(i + 3))

            copy_btn = Button(window, text="Copy", command=lambda text=(array[i][3]): copy_to_clipboard(text))
            copy_btn.grid(column=3, row=(i + 3))

            delete_btn = Button(window, text="Delete", command=lambda text1=(array[i][1]),text2=(array[i][2]), text3=(array[i][3]) : delete_entry(text1, text2, text3))
            delete_btn.grid(column=4, row=(i + 3))

            i = i + 1

            cursor.execute('SELECT * FROM vault')
            if (len(cursor.fetchall()) <= i):
                break



#function that displays after the master password has been officially set on the first run and every run after
def master_login():
    for widget in window.winfo_children():
        widget.destroy()

    #gets master password input from user and checks if it matches with the password in the database
    def get_master_password():
        check_hashed_password = hash_master_password(master_password_entry.get().encode('utf-8'))
        cursor.execute("Select * FROM master_password WHERE id = 1 and password = ?", [(check_hashed_password)])

        return cursor.fetchall()

    def check_master_password():
        match = get_master_password()

        if match:
            vault_screen()
        else:
            master_password_entry.delete(0, END)
            wrong_password_label = Label(text="Invalid Password. Try Again", font=("Arial", 12, "bold"))
            wrong_password_label.grid(column=1, row=6)

    def on_enter_key(event):
        check_master_password()

    window.bind('<Return>', on_enter_key)
    window.title("Password Manager")
    window.config(padx=60, pady=60)

    canvas = Canvas(height=200, width=200)
    # logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(column=1, row=0)

    master_password_label = Label(text="Master Password:", font=("Arial", 10, "bold"))
    master_password_label.grid(column=0, row=3)
    master_password_entry = Entry(width=30, show="*")
    master_password_entry.grid(column=1, row=3)
    master_password_entry.focus()

    save = Button(text="Login master", command=check_master_password, width=36)
    save.grid(column=1, row=5, columnspan=2)

def user_password_check(username, password):

    if username != password:
        return password





#function that displays when a new password is to be added to the database and returns a password
def new_password():
    for widget in window.winfo_children():
        widget.destroy()


    #function that runs once the save password button is clicked after a user inputs new information and stores all
    #the info in the database
    def button_clicked(password="hi12"):

        website = website_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        # running function that checks whether username and password are the same and returns password


        insert_password = """INSERT INTO vault(website, username, password)
                          VALUES(?, ?, ?) """
        user_values = (website, username, password)
        cursor.execute(insert_password, user_values)
        db.commit()


        # clearing data on entries
        website_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)

        website_entry.focus()

        vault_screen()

    def enter_key(event):
        button_clicked()

    window.title("Password Manager")
    window.bind('<Return>', enter_key)
    #window.config(padx=40, pady=40)

    canvas = Canvas(height=200, width=200)
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(column=1, row=0)

    my_label = Label(text="Website:", font=("Arial", 10, "bold"))
    my_label.grid(column=0, row=1)
    website_entry = Entry(width=40)
    website_entry.focus()
    website_entry.grid(column=1, row=1, columnspan=2)

    username_label = Label(text="Email/username:", font=("Arial", 10, "bold"))
    username_label.grid(column=0, row=2)
    username_entry = Entry(width=40)
    username_entry.grid(column=1, row=2, columnspan=2)

    password_label = Label(text="Password:", font=("Arial", 10, "bold"))
    password_label.grid(column=0, row=3)
    password_entry = Entry(width=40)
    password_entry.grid(column=1, row=3, columnspan=2)


    save = Button(text="Save Password", command=button_clicked, width=36)
    save.grid(column=1, row=4, columnspan=2)


#initialize the tkinter
window = Tk()
logo_img = PhotoImage(file="logo.png")


#checks whether or not the database has an entry for master password and if it does it go straight to the login
#if it doesn't then it will run the initial setup screen
cursor.execute("Select * from master_password")
if cursor.fetchall():
    master_login()
else:
    first_run()
window.mainloop()