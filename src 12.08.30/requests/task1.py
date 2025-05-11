
import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def task1(root, name_db):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
           SELECT 
               ОТЕЛЬ."назва" AS "Готель",
               ОТЕЛЬ."адрес" AS "Адреса",
               COUNT(DISTINCT ПРОЖИВАННЯ_У_ОТЕЛІ."турист_id") AS "Кількість туристів",
               SUM(ПРОЖИВАННЯ_У_ОТЕЛІ."кількість_днів") AS "Сумарно днів"
           FROM ПРОЖИВАННЯ_У_ОТЕЛІ
           JOIN ОТЕЛЬ ON ПРОЖИВАННЯ_У_ОТЕЛІ."отель_id" = ОТЕЛЬ.id
           JOIN ТУРИСТ ON ПРОЖИВАННЯ_У_ОТЕЛІ."турист_id" = ТУРИСТ.id
           GROUP BY ОТЕЛЬ."назва", ОТЕЛЬ."адрес"
       """)

    rows = cursor.fetchall()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Name", "Address", "Count tourists", "Count days"))
    tree["show"] = "headings"
    tree.heading("#1", text="Name")
    tree.heading("#2", text="Address")
    tree.heading("#3", text="Count tourists")
    tree.heading("#4", text="Count day")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

