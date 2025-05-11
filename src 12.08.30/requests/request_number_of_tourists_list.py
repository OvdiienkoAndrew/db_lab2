import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry

def request(entries,root, name_db, empty_height):
    values = []
    for entry in entries:
        values.append(str(entry.get()))

    if "Choice Category" == values[0]:
        messagebox.showinfo("x", "Choice the category!")
        root.deiconify()
        return

    values[1] = str(values[1]).replace('/', '.')
    start_date_str = f"{values[1]} {values[2]}:{values[3]}"
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")

    values[4] = str(values[4]).replace('/', '.')
    end_date_str = f"{values[4]} {values[5]}:{values[6]}"
    end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    query = """
        SELECT COUNT(DISTINCT ТУРИСТ.id)
        FROM ТУРИСТ
        JOIN ПРОЖИВАННЯ_У_ОТЕЛІ ON ТУРИСТ.id = ПРОЖИВАННЯ_У_ОТЕЛІ.турист_id
        WHERE 
                ПРОЖИВАННЯ_У_ОТЕЛІ.дата_час_початку >= ?
                AND ПРОЖИВАННЯ_У_ОТЕЛІ.дата_час_кінця <= ?
            
    """

    params = [start_date, end_date]

    if values[0] != "All":
         query += " AND ТУРИСТ.категорія = ?"
         params.append(values[0])

    cursor.execute(query, params)
    results = cursor.fetchone()[0]


    label = tk.Label(root, text=str(results))
    root.update()
    label.pack(pady=10)
    root.update()
    label.place(x=(root.winfo_width()-label.winfo_width())/2,y=root.winfo_height()-empty_height/2)
    root.update()

    conn.close()


def request_number_of_tourists_list(root, name_db):
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

    start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                 date_pattern="mm/dd/yyyy")
    start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
    start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

    end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                               date_pattern="mm/dd/yyyy")
    end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
    end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)


    entries = [entry_category, start_date_entry, start_hour_spinbox, start_minute_spinbox, end_date_entry, end_hour_spinbox, end_minute_spinbox]

    empty_height = root.winfo_height()

    button_request = tk.Button(root, text="Send", command=lambda: request(entries, root, name_db, empty_height))

    root.update()

    values = [entry_category, start_date_entry, start_hour_spinbox, start_minute_spinbox, end_date_entry, end_hour_spinbox, end_minute_spinbox,button_request]



    for value in values:
        value.place(x=10, y=10)

    root.update()

    for i,value in enumerate(values, start=0):
        if i in [2,3,5,6]:
            continue
        empty_height-=value.winfo_height()

    empty_height /= (len(values)-4+1)


    values[0].place(x=(root.winfo_width()-values[0].winfo_width())/2, y = empty_height)

    values[len(values)-1].place(x=(root.winfo_width() - values[len(values)-1].winfo_width()) / 2, y=empty_height * 4 + 3* values[0].winfo_height())

    root.update()

    values[1].place(x=(root.winfo_width() - (20+values[1].winfo_width()+values[2].winfo_width()+values[3].winfo_width()))/2, y=empty_height*2+values[0].winfo_height())
    values[2].place(x=(root.winfo_width() - (20+values[1].winfo_width()+values[2].winfo_width()+values[3].winfo_width()))/2 + 10+values[1].winfo_width(), y=empty_height*2+values[0].winfo_height())
    values[3].place(x=(root.winfo_width() - (20+values[1].winfo_width()+values[2].winfo_width()+values[3].winfo_width()))/2 + 20+values[1].winfo_width()+values[2].winfo_width(), y=empty_height*2+values[0].winfo_height())

    root.update()

    values[4].place(
        x=(root.winfo_width() - (20 + values[4].winfo_width() + values[5].winfo_width() + values[6].winfo_width())) / 2,
        y=empty_height * 3 + 2* values[0].winfo_height())
    values[5].place(x=(root.winfo_width() - (
                20 + values[4].winfo_width() + values[5].winfo_width() + values[6].winfo_width())) / 2 + 10 + values[
                          4].winfo_width(), y=empty_height * 3 + 2* values[0].winfo_height())
    values[6].place(x=(root.winfo_width() - (
                20 + values[4].winfo_width() + values[5].winfo_width() + values[6].winfo_width())) / 2 + 20 + values[
                          4].winfo_width() + values[5].winfo_width(), y=empty_height * 3 + 2* values[0].winfo_height())

    root.update()