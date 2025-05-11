
import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def task2(root, name_db):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
    ЛЮДИНА."прізвище",
    ЛЮДИНА."ім'я",
    ЛЮДИНА."по-батьковi",
    ЛЮДИНА."email",
    SUM(ВАНТАЖ."страховка_в_грн") AS "Сума страховки"
FROM ТУРИСТ
JOIN ЛЮДИНА ON ТУРИСТ."людина_id" = ЛЮДИНА.id
JOIN ВАНТАЖ ON ВАНТАЖ."турист_id" = ТУРИСТ.id
JOIN РЕЙС ON РЕЙС."турист_id" = ТУРИСТ.id
GROUP BY 
    ЛЮДИНА."прізвище", 
    ЛЮДИНА."ім'я", 
    ЛЮДИНА."по-батьковi", 
    ЛЮДИНА."email";

       """)

    rows = cursor.fetchall()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Surname", "Name", "Patronymic", "Email", "The amount of insured baggage"))
    tree["show"] = "headings"
    tree.heading("#1", text="Surname")
    tree.heading("#2", text="Name")
    tree.heading("#3", text="Patronymic")
    tree.heading("#4", text="Email")
    tree.heading("#5", text="The amount of insured baggage")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

