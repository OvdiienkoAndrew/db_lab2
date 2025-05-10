
import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def request(entries, root, name_db):
    values = [str(entry.get()) for entry in entries]


    value = values[0]

    if value == "Choice number":
        messagebox.showinfo("x", "Choice the number!")
        root.deiconify()
        return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            "ЛЮДИНА"."прізвище", 
            "ЛЮДИНА"."ім'я",
            "ЛЮДИНА"."по-батьковi",
            "ЛЮДИНА"."email",
            "ВАНТАЖ"."тип_вантажу",
            "ОТЕЛЬ"."назва" AS "готель",
            "ОТЕЛЬ"."адрес" AS "готель",
            "НОМЕР_У_ОТЕЛІ"."номер_кімнати",
            "ПРОЖИВАННЯ_У_ОТЕЛІ"."кількість_днів",
            "ВАНТАЖ"."тип_вантажу",
            "ВАНТАЖ"."вага_в_кг",
            "ВАНТАЖ"."загальна_сума_в_грн" AS "вартість_вантажу",
            "ВАНТАЖ"."кількість_місць",
            "ВАНТАЖ"."страховка_в_грн" AS "страхування"
        FROM "РЕЙС"
        JOIN "ТУРИСТ" ON "РЕЙС"."турист_id" = "ТУРИСТ"."id"
        JOIN "ЛЮДИНА" ON "ЛЮДИНА"."id" = "ТУРИСТ"."людина_id"
        LEFT JOIN "ПРОЖИВАННЯ_У_ОТЕЛІ" ON "ПРОЖИВАННЯ_У_ОТЕЛІ"."турист_id" = "ТУРИСТ"."id"
        LEFT JOIN "ОТЕЛЬ" ON "ОТЕЛЬ"."id" = "ПРОЖИВАННЯ_У_ОТЕЛІ"."отель_id"
        LEFT JOIN "НОМЕР_У_ОТЕЛІ" ON "НОМЕР_У_ОТЕЛІ"."id" = "ПРОЖИВАННЯ_У_ОТЕЛІ"."номер_у_отелі_id"
        LEFT JOIN "ВАНТАЖ" ON "ВАНТАЖ"."турист_id" = "ТУРИСТ"."id"
        WHERE "РЕЙС"."номер" = ?
    """, (value,))

    rows = cursor.fetchall()
    conn.close()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=(
    "Surname", "Name", "Patronymic", "Email", "Cargo category", "Hotel name", "Hotel address", "Hotel number", "Counter days", "Cargo type", "Weight",
    "Cargo price", "Cargo size", "Cargo insurance"))
    tree["show"] = "headings"
    tree.heading("#1", text="Surname")
    tree.heading("#2", text="Name")
    tree.heading("#3", text="Patronymic")
    tree.heading("#4", text="Email")
    tree.heading("#5", text="Cargo category")
    tree.heading("#6", text="Hotel name")

    tree.heading("#7", text="Hotel address")
    tree.heading("#8", text="Hotel number")
    tree.heading("#9", text="Counter days")
    tree.heading("#10", text="Cargo type")
    tree.heading("#11", text="Weight")
    tree.heading("#12", text="Cargo price")
    tree.heading("#13", text="Cargo size")
    tree.heading("#14", text="Cargo insurance")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)


def from_fly(root, name_db):
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

    cursor.execute("SELECT номер FROM РЕЙС ORDER BY номер ASC")

    rows = cursor.fetchall()
    name = []
    for row in rows:
        name.append(str(row[0]))

    conn.close()

    entry_name = ttk.Combobox(root, values=name, state="readonly")
    entry_name.config(width=33)
    entry_name.set("Choice number")
    root.update()

    entries = [entry_name]

    button_request = tk.Button(root, text="Send", command=lambda: request(entries, root, name_db))

    root.update()

    empty_height = root.winfo_height()

    values = [entry_name, button_request]

    for value in values:
        value.place(x=10, y=10)

    root.update()

    for i, value in enumerate(values, start=0):
        empty_height -= value.winfo_height()

    empty_height /= (len(values) + 1)

    values[len(values) - 1].place(x=(root.winfo_width() - values[len(values) - 1].winfo_width()) / 2,
                                  y=empty_height * 2 + 1 * values[0].winfo_height())

    values[0].place(x=(root.winfo_width() - values[0].winfo_width()) / 2,
                    y=empty_height)
    root.update()
