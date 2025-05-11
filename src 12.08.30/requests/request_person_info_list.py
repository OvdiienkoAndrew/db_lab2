import ast
import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry


def request(value,root, name_db):
    value = str(value.get())
    if value == "Choice Email":
       messagebox.showinfo("x", "Choice the Email!")
       root.deiconify()
       return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    query = """SELECT 
    ЛЮДИНА.email,
    ТУРИСТ.стать,
    ТУРИСТ.категорія,

    РЕЙС.дата_час_початку AS дата_вильоту,
    РЕЙС.дата_час_кінця AS дата_прильоту,
    РЕЙС.номер AS номер_рейсу,

    ОТЕЛЬ.назва AS готель,
    ОТЕЛЬ.адрес AS адреса_готелю,
    ПРОЖИВАННЯ_У_ОТЕЛІ.дата_час_початку AS заїзд,
    ПРОЖИВАННЯ_У_ОТЕЛІ.дата_час_кінця AS виїзд,

    ЕКСКУРСІЯ.назва AS екскурсія,
    АГЕНТСТВО.назва AS агентство,

    ВАНТАЖ.тип_вантажу,
    ВАНТАЖ.вага_в_кг,
    ВАНТАЖ.загальна_сума_в_грн

FROM ТУРИСТ
JOIN ЛЮДИНА ON ЛЮДИНА.id = ТУРИСТ.людина_id
LEFT JOIN РЕЙС ON РЕЙС.турист_id = ТУРИСТ.id
LEFT JOIN ПРОЖИВАННЯ_У_ОТЕЛІ ON ПРОЖИВАННЯ_У_ОТЕЛІ.турист_id = ТУРИСТ.id
LEFT JOIN ОТЕЛЬ ON ОТЕЛЬ.id = ПРОЖИВАННЯ_У_ОТЕЛІ.отель_id
LEFT JOIN ПРОВЕДЕННЯ_ЕКСКУРСІЇ ON ПРОВЕДЕННЯ_ЕКСКУРСІЇ.турист_id = ТУРИСТ.id
LEFT JOIN ЕКСКУРСІЯ ON ЕКСКУРСІЯ.id = ПРОВЕДЕННЯ_ЕКСКУРСІЇ.екскурсія_id
LEFT JOIN АГЕНТСТВО ON АГЕНТСТВО.id = ПРОВЕДЕННЯ_ЕКСКУРСІЇ.агентство_id
LEFT JOIN ВАНТАЖ ON ВАНТАЖ.турист_id = ТУРИСТ.id

WHERE ЛЮДИНА.email = ?
"""
    cursor.execute(query, (value,))
    rows = cursor.fetchall()

    if not rows:
        messagebox.showinfo("Немає даних", "За вказаним email турист не знайдений.")
        return

    window = tk.Toplevel(root)
    window.title("Інформація про туриста")
    text = tk.Text(window, wrap=tk.WORD, width=100, height=30)
    text.pack(padx=10, pady=10)

    i=0
    for row in rows:
            i+=1
            text.insert(tk.END, f"Email: {row[0]}\n")
            text.insert(tk.END, f"Sex: {row[1]}, Category: {row[2]}\n")
            text.insert(tk.END, f"Flight number: {row[5]}, Start: {row[3]}, End: {row[4]}\n")
            text.insert(tk.END, f"Hotel: {row[6]}, Address: {row[7]}, Start date: {row[8]}, End date: {row[9]}\n")
            text.insert(tk.END, f"Excursion: {row[10]}, Agency: {row[11]}\n")
            text.insert(tk.END, f"Type Cargo: {row[12]}, Weight: {row[13]} kg, Price: {row[14]} grn\n")
            text.insert(tk.END, "\n" + "-" * 80 + "\n\n")


    text.insert(tk.END, f"\n\nCounter: {i}\n\n")
    conn.close()

def request_person_info_list(root, name_db):
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


    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ЛЮДИНА.email
        FROM ТУРИСТ
        JOIN ЛЮДИНА ON ТУРИСТ.людина_id = ЛЮДИНА.id
        ORDER BY ЛЮДИНА.email ASC
    """)

    options_email = []
    names = cursor.fetchall()

    if names:
        for name in names:
            options_email.append(str(name[0]))

    conn.close()

    entry_username = ttk.Combobox(root, values=options_email, state="readonly")
    entry_username.set("Choice Email")


    button_request = tk.Button(root, text="Send", command=lambda: request(entry_username, root, name_db))
    root.update()

    values = [entry_username, button_request]

    empty_height = root.winfo_height()

    for value in values:
        value.place(x=10,y=10)
        root.update()
        empty_height -= value.winfo_height()

    empty_height /= (len(values)+1)

    for i,value in enumerate(values,start=1):
        value.place(x=(root.winfo_width()-value.winfo_width())/2, y=i*empty_height+(i-1)*values[0].winfo_height())
        root.update()






