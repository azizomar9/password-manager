from tkinter import *


def login_page():


    # login button
    def login_clicked(password="hi12"):
        # from selenium import webdriver
        # driver = webdriver.Chrome()
        # print(driver.current_url)
        # changing label value once button is clicked

        password = password_entry.get()

        password = password_check(password);

    def password_check(password):
        var = IntVar()
        correct_password = "money"
        while correct_password != password:
            print("The password you have entered is invalid.")
            password_entry.delete(0, END)

            # button_clicked(password)
            save = Button(window, text="Login", command=lambda: var.set(1), width=36)
            save.grid(column=1, row=4, columnspan=2)
            save.wait_variable(var)
            password_entry.focus()
            password = password_entry.get()
            if correct_password == password:
                break;
            # button_clicked(password)

            # if username != password:
            #     break;
        print(password)
        print("hi")

        return


    window.title("Password Manager Login")
    window.config(padx=60, pady=60)

    canvas = Canvas(height=200, width=200)
    # logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(column=1, row=0)

    password_label = Label(text="Master Password:", font=("Arial", 10, "bold"))
    password_label.grid(column=0, row=3)
    password_entry = Entry(width=30)
    password_entry.grid(column=1, row=3)

    save = Button(text="Login", command=login_clicked, width=36)
    save.grid(column=1, row=4, columnspan=2)





def password_manager():
    for widget in window.winfo_children():
        widget.destroy()
    # ---------------------------- PASSWORD GENERATOR ------------------------------- #

    # ---------------------------- SAVE PASSWORD ------------------------------- #

    from csv import writer

    # function to make sure username and password are not the same for security reasons
    def userPassCheck(username, password):
        var = IntVar()

        while username == password:
            print("The username and password are the same and therefore this combination will not be secure.")
            password_entry.delete(0, END)

            # button_clicked(password)
            save = Button(window, text="Save Password", command=lambda: var.set(1), width=36)
            save.grid(column=1, row=4, columnspan=2)
            save.wait_variable(var)
            password_entry.focus()
            password = password_entry.get()
            if username != password:
                break;
            # button_clicked(password)
            print(username, password)
            # if username != password:
            #     break;
        print(password)
        return password

    def button_clicked(password="hi12"):
        # from selenium import webdriver
        # driver = webdriver.Chrome()
        # print(driver.current_url)
        # changing label value once button is clicked

        website = website_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        password = userPassCheck(username, password);

        # if username == password:
        #     print("The username and password are the same and therefore this combination will not be secure.")
        #     password_entry.delete(0, END)
        #
        #     website_entry.focus()

        # clearing data on entries
        website_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)

        website_entry.focus()

        with open('passwords.csv', 'a', ) as data_file:
            data_file.write(f"{website} , {username} , {password}\n")

    # ---------------------------- UI SETUP ------------------------------- #


    window.title("Password Manager")
    window.config(padx=40, pady=40)

    canvas = Canvas(height=200, width=200)
   #logo_img = PhotoImage(file="logo.png")
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
    password_entry = Entry(width=21)
    password_entry.grid(column=1, row=3)

    button = Button(text="Generate password", command=button_clicked, padx=5)
    button.grid(column=2, row=3)

    save = Button(text="Save Password", command=button_clicked, width=36)
    save.grid(column=1, row=4, columnspan=2)



window = Tk()
logo_img = PhotoImage(file="logo.png")
login_page()
password_manager()

window.mainloop()