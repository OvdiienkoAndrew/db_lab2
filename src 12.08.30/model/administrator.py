import tkinter as tk
import sqlite3
from tkinter import messagebox




def admin_input(root, name_db, input_username, input_password):
    from src.menu.admin_menu import admin_menu

    for widget in root.winfo_children():
        widget.destroy()

    input_username = str(input_username)
    input_password = str(input_password)

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM АДМІНІСТРАТОР WHERE username = ? AND password =?", (input_username, input_password))

    if cursor.fetchone():
        conn.close()
        admin_menu(root,name_db)
    else:
        root.withdraw()
        messagebox.showinfo("Error", "I don't know this admin!")
        root.deiconify()
        conn.close()
        administrator(root, name_db)



def administrator(root, name_db):

    root.title("Input admin")

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    username = "admin"
    password = "root"

    cursor.execute("SELECT 1 FROM АДМІНІСТРАТОР WHERE username = ? AND password =?", (username, password))



    if cursor.fetchone():
        pass
    else:
        cursor.execute(f"INSERT INTO АДМІНІСТРАТОР (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    conn.close()


    from src.menu.main_menu import main_menu

    for widget in root.winfo_children():
        widget.destroy()

    label_username = tk.Label(root, text="Username")
    label_password = tk.Label(root, text="Password")

    entry_username = tk.Entry(root, show = "*")
    entry_password = tk.Entry(root, show = "*")

    button_back = tk.Button(root, text="Back", command=lambda: main_menu(root, name_db))
    button_entrance = tk.Button(root, text="Entrance",command=lambda: admin_input(root, name_db, entry_username.get(), entry_password.get()))

    root.update()

    button_back.place(x=10, y=10)

    label_username.place(x=0, y=0)
    label_password.place(x=0, y=0)
    entry_username.place(x=0, y=0)
    entry_password.place(x=0, y=0)
    button_entrance.place(x=0, y=0)

    root.update()

    button_back.place(x=10, y=10)

    empty_height = (root.winfo_height() - label_username.winfo_height() - label_password.winfo_height() - button_entrance.winfo_height()) / 4
    label_username.place(x=root.winfo_width() / 2 - 10 - label_username.winfo_width(), y=empty_height)
    label_password.place(x=root.winfo_width() / 2 - 10 - label_password.winfo_width(), y=2 * empty_height + label_username.winfo_height())
    entry_username.place(x=root.winfo_width() / 2 + 10, y=empty_height)
    entry_password.place(x=root.winfo_width() / 2 + 10, y=2 * empty_height + entry_username.winfo_height())

    button_entrance.place(x=(root.winfo_width() - button_entrance.winfo_width()) / 2, y=root.winfo_height() - empty_height - button_entrance.winfo_height())

    root.update()

