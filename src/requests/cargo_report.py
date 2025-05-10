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
                    SUM(ВАНТАЖ.кількість_місць),
                    SUM(ВАНТАЖ.вага_в_кг),
                    COUNT(DISTINCT РЕЙС.id),
                    COUNT(DISTINCT CASE WHEN ТУРИСТ.категорія = 'Cargo' THEN РЕЙС.id END),
                    COUNT(DISTINCT CASE WHEN ТУРИСТ.категорія != 'Cargo' THEN РЕЙС.id END)
                FROM ВАНТАЖ
                JOIN ТУРИСТ ON ВАНТАЖ.турист_id = ТУРИСТ.id
                JOIN РЕЙС ON РЕЙС.турист_id = ТУРИСТ.id
                WHERE РЕЙС.дата_час_початку BETWEEN ? AND ?

            """, (start_date, end_date))

    rows = cursor.fetchone()
    conn.close()

    tree_window = tk.Toplevel(root)
    tree_window.title("Hotels info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Counter cargos", "Cargos weight", "Counter fly cargo", "Counter fly cargo with tourist Cargo", "Counter fly cargo without tourist Cargo"))
    tree["show"] = "headings"
    tree.heading("#1", text="Counter cargos")
    tree.heading("#2", text="Cargos weight")
    tree.heading("#3", text="Counter fly cargo")
    tree.heading("#4", text="Counter fly cargo with tourist Cargo")
    tree.heading("#5", text="Counter fly cargo without tourist Cargo")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)


    tree.insert("", "end", values=rows)


def cargo_report(root, name_db):
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
