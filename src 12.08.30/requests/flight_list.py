#flight_list


import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def request(entries,root, name_db):

    values = [str(entry.get()) for entry in entries]

    values[1] = str(values[1]).replace('/', '.')
    start_date_str = f"{values[1]} {values[2]}:{values[3]}"
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")


    print(start_date)
    print(values[0])

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    query = """SELECT 
    
        РЕЙС.номер AS дата_вильоту,
        РЕЙС.дата_час_початку AS дата_прильоту,
        РЕЙС.дата_час_кінця AS номер_рейсу,
        
        COUNT(РЕЙС.турист_id),
        
        SUM(ВАНТАЖ.кількість_місць),
        SUM(ВАНТАЖ.вага_в_кг)

        

    FROM ТУРИСТ
    LEFT JOIN РЕЙС ON РЕЙС.турист_id = ТУРИСТ.id
    LEFT JOIN ВАНТАЖ ON ВАНТАЖ.турист_id = ТУРИСТ.id
   

    WHERE РЕЙС.номер = ?
    """
    cursor.execute(query, (values[0],))
    rows = cursor.fetchall()
    conn.close()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Number", "Start date", "End date", "Counter tourists", "Sum cargos", "Sum cargo weight"))
    tree["show"] = "headings"
    tree.heading("#1", text="Number")
    tree.heading("#2", text="Start date")
    tree.heading("#3", text="End date")
    tree.heading("#4", text="Counter tourists")
    tree.heading("#5", text="Sum cargos")
    tree.heading("#6", text="Sum cargo weight")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)

def flight_list(root, name_db):
    from src.requests.requests import requests
    root.title("Flight list")
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: requests(root, name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""SELECT номер FROM РЕЙС""")

    rows = cursor.fetchall()
    name = []
    for row in rows:
        name.append(str(row[0]))

    conn.close()

    entry_name = ttk.Combobox(root, values=name, state="readonly")
    entry_name.config(width=33)
    entry_name.set("Choice number")
    root.update()

    start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                 date_pattern="mm/dd/yyyy")
    start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
    start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)


    entries = [entry_name, start_date_entry, start_hour_spinbox, start_minute_spinbox]


    button_request = tk.Button(root, text="Send", command=lambda: request(entries, root, name_db))

    root.update()

    empty_height = root.winfo_height()

    values = [entry_name, start_date_entry, start_hour_spinbox, start_minute_spinbox, button_request]

    for value in values:
        value.place(x=10, y=10)

    root.update()

    for i, value in enumerate(values, start=0):
        if i in [2, 3, 5 , 6]:
            continue
        empty_height -= value.winfo_height()

    empty_height /= (len(values) - 2 + 1)



    values[len(values) - 1].place(x=(root.winfo_width() - values[len(values) - 1].winfo_width()) / 2,
                                  y=empty_height * 3 + 2* values[0].winfo_height())

    values[0].place(x=(root.winfo_width() - values[0].winfo_width()) / 2,
                                  y=empty_height)

    root.update()

    values[1].place(
        x=(root.winfo_width() - (20 + values[1].winfo_width() + values[2].winfo_width() + values[3].winfo_width())) / 2,
        y=empty_height * 2 + values[0].winfo_height())
    values[2].place(x=(root.winfo_width() - (
                20 + values[1].winfo_width() + values[2].winfo_width() + values[3].winfo_width())) / 2 + 10 + values[
                          1].winfo_width(), y=empty_height * 2 + values[0].winfo_height())
    values[3].place(x=(root.winfo_width() - (
                20 + values[1].winfo_width() + values[2].winfo_width() + values[3].winfo_width())) / 2 + 20 + values[
                          1].winfo_width() + values[2].winfo_width(), y=empty_height * 2 + values[0].winfo_height())

    root.update()
