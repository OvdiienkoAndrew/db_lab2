from datetime import datetime

import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry


def excursion_edit(root, name_db,entries, ID):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()


    values = [str(entries[0].get().strip()), str(entries[1]), str(entries[2]),str(entries[3].get().strip())]
    print(values)

    values[1] = str(values[1]).replace('/', '.')
    start_date_str = values[1]
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

    values[2] = str(values[2]).replace('/', '.')
    end_date_str = values[2]
    end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

    if start_date > end_date:
        messagebox.showinfo("x", "Start date and time is later than end date and time!")
        root.deiconify()
        return

    try:
        if float(values[3]) < 0:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Price is wrong!")
        root.deiconify()
        return

    query = """
    UPDATE ЕКСКУРСІЯ
    SET 
        опис = ?, 
        дата_час_початку = ?, 
        дата_час_кінця = ?, 
        вартість_в_грн = ? 
    WHERE id = ?;
    """
    cursor.execute(query, (values[0], start_date, end_date, values[3], ID))

    conn.commit()
    messagebox.showinfo("✓", "I updated this Excursion!")

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def excursion(action, table_name, root, name_db, entries):

    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()


    values = [str(entry.get().strip()) for entry in entries]

    if str(action).lower().replace(' ','') == "add":


        print(values)
        if len(values[0]) <= 0 or values[0].lower().replace(' ', '') == 'none':
            messagebox.showinfo("x", "Name Agency is empty!")
            root.deiconify()
            return

        if len(values[1]) <= 7 or values[1].lower().replace(' ', '') == 'none':
            messagebox.showinfo("x", "Address Agency is small (3 letters min)!")
            root.deiconify()
            return

        query = "SELECT * FROM АГЕНТСТВО WHERE назва = ? AND адрес = ? LIMIT 1"
        cursor.execute(query, (values[0],values[1],))

        results = cursor.fetchone()


        if not results:
            conn.close()
            messagebox.showinfo("x", "I don't know this agency!")
            root.deiconify()
            return

        agency = [str(result) for result in results]


        if len(values[2]) <= 1:
            messagebox.showinfo("x", "Name is small(2 letters min)!")
            root.deiconify()
            return

        query = "SELECT * FROM ЕКСКУРСІЯ WHERE агентство_id = ? AND назва = ? LIMIT 1"
        cursor.execute(query, (agency[0],values[2],))

        results = cursor.fetchone()

        if results:
            conn.close()
            messagebox.showinfo("x", "I know this excursion!")
            root.deiconify()
            return

        values[4] = str(values[4]).replace('/','.')
        start_date_str = f"{values[4]} {values[5]}:{values[6]}"
        print(start_date_str)
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

        values[7] = str(values[7]).replace('/','.')
        end_date_str = f"{values[7]} {values[8]}:{values[9]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

        if start_date > end_date:
            messagebox.showinfo("x", "Start date and time is later than end date and time!")
            root.deiconify()
            return

        try:
            if float(values[10]) < 0:
                messagebox.showinfo("x", "Price is wrong!")
                root.deiconify()
                return
        except Exception:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return

        cursor.execute("""
        INSERT INTO ЕКСКУРСІЯ ("агентство_id", "назва", "опис", "дата_час_початку", "дата_час_кінця", "вартість_в_грн") 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (agency[0], values[2], values[3], start_date, end_date, values[10]))
        conn.commit()
        messagebox.showinfo("✓", "I know the new Excursion!")


        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit":
        if len(values[0]) <= 0 or values[0].lower().replace(' ', '') == 'none':
            messagebox.showinfo("x", "Name Agency is empty!")
            root.deiconify()
            return

        if len(values[1]) <= 7 or values[1].lower().replace(' ', '') == 'none':
            messagebox.showinfo("x", "Address Agency is small (3 letters min)!")
            root.deiconify()
            return

        query = "SELECT * FROM АГЕНТСТВО WHERE назва = ? AND адрес = ? LIMIT 1"
        cursor.execute(query, (values[0], values[1],))

        results = cursor.fetchone()

        if not results:
            conn.close()
            messagebox.showinfo("x", "I don't know this agency!")
            root.deiconify()
            return

        agency = [str(result) for result in results]

        if len(values[2]) <= 1:
            messagebox.showinfo("x", "Name is small(2 letters min)!")
            root.deiconify()
            return

        query = "SELECT * FROM ЕКСКУРСІЯ WHERE агентство_id = ? AND назва = ? LIMIT 1"
        cursor.execute(query, (agency[0], values[2],))

        results = cursor.fetchone()

        if not results:
            conn.close()
            messagebox.showinfo("x", "I don't know this excursion!")
            root.deiconify()
            return

        this_excursion = [str(result) for result in results]

        root.deiconify()

        root.title(action)
        for widget in root.winfo_children():
            widget.destroy()

        button_back = tk.Button(root, text="Back", command=lambda: admin_menu(root, name_db))
        root.update()
        button_back.place(x=10, y=10)
        root.update()
        button_back.place(x=10, y=10)
        root.update()

        ID = this_excursion[0]

        hint_description = "Old description: " + this_excursion[3] + ".\tNew description:"
        hint_date_start = "Old date and time start " + this_excursion[4] + ".\tNew date and time start:"
        hint_date_end = "Old date and time end " + this_excursion[5] + ".\tNew date and time end:"
        hint_price = "Old price " + this_excursion[6] + ".\tNew price:"

        labels = []

        labels.append(tk.Label(root, text=hint_description))
        labels.append(tk.Label(root, text=hint_date_start))
        labels.append(tk.Label(root, text=hint_date_end))
        labels.append(tk.Label(root, text=hint_price))

        root.update()

        for label in labels:
            label.place(x=10, y=50)

        root.update()

        empty_height = root.winfo_height() - 20 - button_back.winfo_height()

        for label in labels:
            empty_height -= label.winfo_height()

        empty_height /= (6 + 2)

        helper_height = 20 + button_back.winfo_height()

        for i, label in enumerate(labels, start=1):
            label.place(x=10, y=helper_height + i * empty_height + (i - 1) * label.winfo_height())

        root.update()

        entry_description = tk.Entry(root)
        entry_price = tk.Entry(root)

        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

        start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        root.update()

        entry_description.place(x=10 + root.winfo_width() / 2,
                                y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())

        root.update()

        start_date_entry.place(x=10 + root.winfo_width() / 2,
                               y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        start_hour_spinbox.place(x=10 + (root.winfo_width() / 2) + start_date_entry.winfo_width() + 10,
                                 y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        start_minute_spinbox.place(
            x=10 + (
                    root.winfo_width() / 2) + start_date_entry.winfo_width() + 10 + start_hour_spinbox.winfo_width() + 10,
            y=helper_height + 2 * empty_height + (
                    2 - 1) * labels[0].winfo_height())

        root.update()

        end_date_entry.place(x=10 + root.winfo_width() / 2,
                             y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        end_hour_spinbox.place(x=10 + (root.winfo_width() / 2) + end_date_entry.winfo_width() + 10,
                               y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        end_minute_spinbox.place(
            x=10 + (
                    root.winfo_width() / 2) + end_date_entry.winfo_width() + 10 + end_hour_spinbox.winfo_width() + 10,
            y=helper_height + 3 * empty_height + (
                    3 - 1) * labels[0].winfo_height())

        root.update()

        entry_price.place(x=10 + root.winfo_width() / 2,
                          y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        values = [entry_description, f"{start_date_entry.get().strip()} {start_hour_spinbox.get().strip()}:{start_minute_spinbox.get().strip()}", f"{end_date_entry.get().strip()} {end_hour_spinbox.get().strip()}:{end_minute_spinbox.get().strip()}", entry_price]

        send_button = tk.Button(root, text=action, command=lambda: excursion_edit(root, name_db,values, ID))
        send_button.place(x=10,
                          y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())
        root.update()



        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass
        return

    if str(action).lower().replace(' ', '') == "delete":
        if len(values[0]) <= 0 or values[0].lower().replace(' ', '') == 'none':
            messagebox.showinfo("x", "Name Agency is empty!")
            root.deiconify()
            return

        if len(values[1]) <= 7 or values[1].lower().replace(' ', '') == 'none':
            messagebox.showinfo("x", "Address Agency is small (3 letters min)!")
            root.deiconify()
            return

        query = "SELECT * FROM АГЕНТСТВО WHERE назва = ? AND адрес = ? LIMIT 1"
        cursor.execute(query, (values[0], values[1],))

        results = cursor.fetchone()

        if not results:
            conn.close()
            messagebox.showinfo("x", "I don't know this agency!")
            root.deiconify()
            return

        agency = [str(result) for result in results]

        if len(values[2]) <= 1:
            messagebox.showinfo("x", "Name is small(2 letters min)!")
            root.deiconify()
            return

        query = "SELECT * FROM ЕКСКУРСІЯ WHERE агентство_id = ? AND назва = ? LIMIT 1"
        cursor.execute(query, (agency[0], values[2],))

        results = cursor.fetchone()

        if not results:
            conn.close()
            messagebox.showinfo("x", "I don't know this excursion!")
            root.deiconify()
            return

        query = "DELETE FROM ЕКСКУРСІЯ WHERE агентство_id = ? AND назва = ?"
        cursor.execute(query, (agency[0], values[2],))
        conn.commit()

        messagebox.showinfo("✓", "The excursion has been removed!")
        admin_menu(root, name_db)

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

