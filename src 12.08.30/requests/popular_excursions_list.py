import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def popular_excursions_list(root, name_db,title_name):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()


    cursor.execute("""
       SELECT
    ЕКСКУРСІЯ.назва AS екскурсія,
    АГЕНТСТВО.назва AS агентство,
    АГЕНТСТВО.рейтинг AS рейтинг,
    COUNT(ПРОВЕДЕННЯ_ЕКСКУРСІЇ.турист_id) AS кількість_туристів
FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ
JOIN ЕКСКУРСІЯ ON ПРОВЕДЕННЯ_ЕКСКУРСІЇ.екскурсія_id = ЕКСКУРСІЯ.id
JOIN АГЕНТСТВО ON ПРОВЕДЕННЯ_ЕКСКУРСІЇ.агентство_id = АГЕНТСТВО.id
GROUP BY ЕКСКУРСІЯ.назва, АГЕНТСТВО.назва, АГЕНТСТВО.рейтинг
ORDER BY кількість_туристів DESC, рейтинг DESC
LIMIT 5

    """)


    rows = cursor.fetchall()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Excursion name", "Agency name", "Agency points", "Counter tourists"))
    tree["show"] = "headings"
    tree.heading("#1", text="Excursion name")
    tree.heading("#2", text="Agency name")
    tree.heading("#3", text="Agency points")
    tree.heading("#4", text="Counter tourists")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()




