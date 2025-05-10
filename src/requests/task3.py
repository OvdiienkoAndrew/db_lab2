
import ast
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def task3(root, name_db):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
WITH Агентства_Сума AS (
    SELECT 
        АГЕНТСТВО."назва" AS "Агентство",
        SUM(ПРОВЕДЕННЯ_ЕКСКУРСІЇ."загальна_сума_в_грн") AS "Загальний_дохід"
    FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ
    JOIN АГЕНТСТВО ON ПРОВЕДЕННЯ_ЕКСКУРСІЇ."агентство_id" = АГЕНТСТВО.id
    GROUP BY АГЕНТСТВО."назва"
),
Сума_Загальна AS (
    SELECT SUM("Загальний_дохід") AS Всього FROM Агентства_Сума
)
SELECT 
    Агентство,
    Загальний_дохід,
    ROUND(100.0 * Загальний_дохід / Всього, 2) AS "Відсоток_від_всього"
FROM Агентства_Сума, Сума_Загальна;
 

       """)

    rows = cursor.fetchall()

    tree_window = tk.Toplevel(root)
    tree_window.title("Excursion info")

    frame = tk.Frame(tree_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Agency", "Total Income", "Percentage of Total"))
    tree["show"] = "headings"
    tree.heading("#1", text="Agency")
    tree.heading("#2", text="Total Income")
    tree.heading("#3", text="Percentage of Total")


    tree.pack(side="left", fill="both", expand=True)
    tree["show"] = "headings"

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

