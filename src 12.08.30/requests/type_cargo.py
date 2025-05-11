# type_cargo


import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def type_cargo(root, name_db):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
                SELECT 
                    тип_вантажу,
                    SUM(вага_в_кг) AS загальна_вага_в_кг,
                    ROUND(SUM(вага_в_кг) * 100.0 / (SELECT SUM(вага_в_кг) FROM ВАНТАЖ), 2) AS питома_частка_у_відсотках
                FROM ВАНТАЖ
                GROUP BY тип_вантажу
            """)


    rows = cursor.fetchall()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Type cargo", "Weight cargo", "Weight %"))
    tree["show"] = "headings"
    tree.heading("#1", text="Type cargo")
    tree.heading("#2", text="Weight cargo")
    tree.heading("#3", text="Weight %")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

