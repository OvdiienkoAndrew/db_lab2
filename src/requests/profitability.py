# profitability


import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def profitability(root, name_db):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
SELECT 
    (SELECT SUM(доходи) FROM ФІНАНСОВИЙ_ЗВІТ) AS загальний_дохід,
    SUM(ЕКСКУРСІЯ.вартість_в_грн) + 
    SUM(ПРОЖИВАННЯ_У_ОТЕЛІ.вартість_в_грн) + 
    SUM(ВАНТАЖ.загальна_сума_в_грн) + 
    SUM(РЕЙС.загальна_сума_в_грн) AS загальні_витрати,
    (SELECT SUM(доходи) FROM ФІНАНСОВИЙ_ЗВІТ) - (
        SUM(ЕКСКУРСІЯ.вартість_в_грн) + 
        SUM(ПРОЖИВАННЯ_У_ОТЕЛІ.вартість_в_грн) + 
        SUM(ВАНТАЖ.загальна_сума_в_грн) + 
        SUM(РЕЙС.загальна_сума_в_грн)
    ) AS рентабельність
FROM ЛЮДИНА
JOIN ТУРИСТ ON ЛЮДИНА.id = ТУРИСТ.людина_id
JOIN РЕЙС ON РЕЙС.турист_id = ТУРИСТ.id
JOIN ВАНТАЖ ON ВАНТАЖ.турист_id = ТУРИСТ.id
JOIN ПРОЖИВАННЯ_У_ОТЕЛІ ON ПРОЖИВАННЯ_У_ОТЕЛІ.турист_id = ТУРИСТ.id
JOIN ПРОВЕДЕННЯ_ЕКСКУРСІЇ ON ПРОВЕДЕННЯ_ЕКСКУРСІЇ.турист_id = ТУРИСТ.id
JOIN ЕКСКУРСІЯ ON ЕКСКУРСІЯ.id = ПРОВЕДЕННЯ_ЕКСКУРСІЇ.екскурсія_id;

    """)

    rows = cursor.fetchall()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Income", "Costs", "Profit"))
    tree["show"] = "headings"
    tree.heading("#1", text="Income")
    tree.heading("#2", text="Costs")
    tree.heading("#3", text="Profit")

    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

