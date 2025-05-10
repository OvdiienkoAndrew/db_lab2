# full_finance_report

import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def request(entries,root, name_db):
    values = []
    for entry in entries:
        values.append(str(entry.get()))

    values[0] = str(values[0]).replace('/', '.')
    start_date_str = f"{values[0]} {values[1]}:{values[2]}"
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")

    values[3] = str(values[3]).replace('/', '.')
    end_date_str = f"{values[3]} {values[4]}:{values[5]}"
    end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            l.email,
            SUM(p.вартість_в_грн) AS загальна_вартість_в_отелі,
            SUM(e.загальна_сума_в_грн) AS загальна_сума_екскурсій,
            SUM(r.загальна_сума_в_грн) AS загальна_сума_рейсів,
            SUM(CASE WHEN v.статус = 'Active' THEN 1 ELSE 0 END) AS кількість_активних_віз
        FROM ФІНАНСОВИЙ_ЗВІТ AS f

        LEFT JOIN ЛЮДИНА AS l ON l.id = f.людина_id
        LEFT JOIN ТУРИСТ AS t ON t.людина_id = l.id

        LEFT JOIN ПРОЖИВАННЯ_У_ОТЕЛІ AS p ON p.турист_id = t.id
        LEFT JOIN ПРОВЕДЕННЯ_ЕКСКУРСІЇ AS e ON e.турист_id = t.id
        LEFT JOIN РЕЙС AS r ON r.турист_id = t.id
        LEFT JOIN VISA AS v ON v.турист_id = t.id

        LEFT JOIN ЕКСКУРСІЯ AS x ON x.id = e.екскурсія_id 
        AND x.агентство_id = e.агентство_id

        WHERE f.дата_час_початку BETWEEN ? AND ?
        AND p.дата_час_початку BETWEEN ? AND ?
        AND x.дата_час_початку BETWEEN ? AND ?
        AND f.дата_час_кінця BETWEEN ? AND ?
        AND p.дата_час_кінця BETWEEN ? AND ?
        AND x.дата_час_кінця BETWEEN ? AND ?

        GROUP BY l.email
    """, (start_date, end_date, start_date, end_date, start_date, end_date,
          start_date, end_date, start_date, end_date, start_date, end_date))

    rows = cursor.fetchall()
    conn.close()

    tree_window = tk.Toplevel(root)
    tree_window.title("Hotels info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Emails", "Hotel costs", "Excursion costs", "Fly costs","Visa status"))
    tree["show"] = "headings"
    tree.heading("#1", text="Emails")
    tree.heading("#2", text="Hotel costs")
    tree.heading("#3", text="Excursion costs")
    tree.heading("#4", text="Fly costs")
    tree.heading("#5", text="Visa status")



    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)


def full_finance_report(root, name_db):
    from src.requests.requests import requests
    root.title("Cargo report")
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: requests(root, name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                 date_pattern="mm/dd/yyyy")
    start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
    start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

    end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                               date_pattern="mm/dd/yyyy")
    end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
    end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

    entries = [start_date_entry, start_hour_spinbox, start_minute_spinbox, end_date_entry,
               end_hour_spinbox, end_minute_spinbox]



    button_request = tk.Button(root, text="Send", command=lambda: request(entries, root, name_db))

    root.update()

    empty_height = root.winfo_height()

    values = [start_date_entry, start_hour_spinbox, start_minute_spinbox, end_date_entry,
              end_hour_spinbox, end_minute_spinbox, button_request]

    for value in values:
        value.place(x=10, y=10)

    root.update()

    for i, value in enumerate(values, start=0):
        if i in [2, 3, 5, 6]:
            continue
        empty_height -= value.winfo_height()

    empty_height /= (len(values) - 4 + 1)



    values[len(values) - 1].place(x=(root.winfo_width() - values[len(values) - 1].winfo_width()) / 2,
                                  y=empty_height * 3 + 3 * values[0].winfo_height())

    root.update()

    values[0].place(
        x=(root.winfo_width() - (20 + values[0].winfo_width() + values[1].winfo_width() + values[2].winfo_width())) / 2,
        y=empty_height * 1 + values[0].winfo_height())
    values[1].place(x=(root.winfo_width() - (
                20 + values[0].winfo_width() + values[1].winfo_width() + values[2].winfo_width())) / 2 + 10 + values[
                          0].winfo_width(), y=empty_height * 1 + values[0].winfo_height())
    values[2].place(x=(root.winfo_width() - (
                20 + values[0].winfo_width() + values[1].winfo_width() + values[2].winfo_width())) / 2 + 20 + values[
                          0].winfo_width() + values[1].winfo_width(), y=empty_height * 1 + values[0].winfo_height())

    root.update()

    values[3].place(
        x=(root.winfo_width() - (20 + values[3].winfo_width() + values[4].winfo_width() + values[5].winfo_width())) / 2,
        y=empty_height * 2 + 2 * values[0].winfo_height())
    values[4].place(x=(root.winfo_width() - (
            20 + values[3].winfo_width() + values[4].winfo_width() + values[5].winfo_width())) / 2 + 10 + values[
                          3].winfo_width(), y=empty_height * 2 + 2 * values[0].winfo_height())
    values[5].place(x=(root.winfo_width() - (
            20 + values[3].winfo_width() + values[4].winfo_width() + values[5].winfo_width())) / 2 + 20 + values[
                          3].winfo_width() + values[4].winfo_width(), y=empty_height * 2 + 2 * values[0].winfo_height())

    root.update()
