import ast
import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry

def request(values,root, name_db):
    selected_category = str(values[0].get())
    if "Choice Category" == selected_category:
        messagebox.showinfo("x", "Choice the category!")
        root.deiconify()
        return
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    if selected_category != "All":

        query = """
         SELECT ЛЮДИНА."прізвище", ЛЮДИНА."ім'я", ЛЮДИНА."по-батьковi", ОТЕЛЬ."назва", ОТЕЛЬ."адрес"
            FROM ТУРИСТ
            JOIN ЛЮДИНА ON ТУРИСТ.людина_id = ЛЮДИНА.id
            JOIN ПРОЖИВАННЯ_У_ОТЕЛІ ON ТУРИСТ.id = ПРОЖИВАННЯ_У_ОТЕЛІ.турист_id
            JOIN ОТЕЛЬ ON ПРОЖИВАННЯ_У_ОТЕЛІ.отель_id = ОТЕЛЬ.id
            WHERE ТУРИСТ.категорія = ?
            ORDER BY ЛЮДИНА."прізвище" ASC;

        """
        # DESC
        cursor.execute(query, (selected_category,))

    else:
        query = """
                SELECT ЛЮДИНА."прізвище", ЛЮДИНА."ім'я", ЛЮДИНА."по-батьковi", ОТЕЛЬ."назва", ОТЕЛЬ."адрес"
            FROM ТУРИСТ
            JOIN ЛЮДИНА ON ТУРИСТ.людина_id = ЛЮДИНА.id
            JOIN ПРОЖИВАННЯ_У_ОТЕЛІ ON ТУРИСТ.id = ПРОЖИВАННЯ_У_ОТЕЛІ.турист_id
            JOIN ОТЕЛЬ ON ПРОЖИВАННЯ_У_ОТЕЛІ.отель_id = ОТЕЛЬ.id
            ORDER BY ЛЮДИНА."прізвище" ASC;

               """ # DESC
        cursor.execute(query,)


    results = cursor.fetchall()

    if not results:
        messagebox.showinfo("No Data", "No tourists found in this category.")
        return

    tree_window = tk.Toplevel(root)
    tree_window.title("Tourists Information")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Surname", "Name", "Patronymic", "Hotel", "Address"))
    tree["show"] = "headings"
    tree.heading("#1", text="Surname")
    tree.heading("#2", text="Name")
    tree.heading("#3", text="Patronymic")
    tree.heading("#4", text="Hotel")
    tree.heading("#5", text="Address")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for result in results:
        tree.insert("", "end", values=result)

    conn.close()


def request_hotel_list(root, name_db):
    from src.requests.requests import requests
    root.title("Person list")
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: requests(root, name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    options_category = ["Rest", "Cargo", "Kids", "All"]

    entry_category = ttk.Combobox(root, values=options_category, state="readonly")
    entry_category.set("Choice Category")
    root.update()
    entry_category.place(x=(root.winfo_width() - entry_category.winfo_width()) / 2,
                         y=(root.winfo_height() - entry_category.winfo_height()) / 2)
    root.update()
    entry_category.place(x=(root.winfo_width() - entry_category.winfo_width()) / 2,
                         y=(root.winfo_height() / 2 - entry_category.winfo_height()))
    root.update()

    values = [entry_category]

    button_request = tk.Button(root, text="Send", command=lambda: request(values, root, name_db))
    root.update()
    button_request.place(x=(root.winfo_width() - button_request.winfo_width()) / 2,
                         y=(root.winfo_height() - button_request.winfo_height()) / 2)
    root.update()
    button_request.place(x=(root.winfo_width() - button_request.winfo_width()) / 2,
                         y=(root.winfo_height() / 2 + button_request.winfo_height()))
    root.update()
