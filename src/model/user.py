import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def user_input(root, name_db, input_username, input_password):
    from src.menu.user_menu import user_menu

    for widget in root.winfo_children():
        widget.destroy()

    input_username = str(input_username)
    input_password = str(input_password)

    if len(input_username) <= 5 or '@' not in input_username:
        messagebox.showinfo("x", "Email is wrong!")
        root.deiconify()
        user(root, name_db)

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM ЛЮДИНА WHERE email = ? AND пароль =?", (input_username, input_password))
    results = cursor.fetchone()
    if results:
        conn.close()
        id = str(results[0])
        user_menu(root,name_db,id)
    else:
        root.withdraw()
        messagebox.showinfo("Error", "Password is wrong!")
        root.deiconify()
        conn.close()
        user(root, name_db)




def user(root, name_db):
    root.title("Input user")
    from src.menu.main_menu import main_menu

    root.title("User menu")
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: main_menu(root, name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()


    label_username = tk.Label(root, text="Email")
    label_password = tk.Label(root, text="Password")

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

    options_email = []
    names = cursor.fetchall()

    if names:
        for name in names:
            options_email.append(str(name[0]))

    conn.close()

    entry_username = ttk.Combobox(root, values=options_email, state="readonly")
    entry_username.set("Choice Email")
    entry_password = tk.Entry(root, show = "*")


    button_back = tk.Button(root, text="Back", command=lambda: main_menu(root, name_db))
    button_entrance = tk.Button(root, text="Entrance",
                                command=lambda: user_input(root, name_db, entry_username.get(), entry_password.get()))

    root.update()

    button_back.place(x=10, y=10)

    label_username.place(x=0, y=0)
    label_password.place(x=0, y=0)

    entry_username.place(x=0, y=0)
    entry_password.place(x=0, y=0)


    button_entrance.place(x=0, y=0)

    root.update()

    button_back.place(x=10, y=10)

    empty_height = (
                               root.winfo_height() - label_username.winfo_height() - label_password.winfo_height() - button_entrance.winfo_height()) / 4
    label_username.place(x=root.winfo_width() / 2 - 10 - label_username.winfo_width(), y=empty_height)
    label_password.place(x=root.winfo_width() / 2 - 10 - label_password.winfo_width(),
                         y=2 * empty_height + label_username.winfo_height())
    entry_username.place(x=root.winfo_width() / 2 + 10, y=empty_height)
    entry_password.place(x=root.winfo_width() / 2 + 10, y=2 * empty_height + entry_username.winfo_height())

    button_entrance.place(x=(root.winfo_width() - button_entrance.winfo_width()) / 2,
                          y=root.winfo_height() - empty_height - button_entrance.winfo_height())

    root.update()



