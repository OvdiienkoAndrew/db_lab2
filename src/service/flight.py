import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox

from tkcalendar import DateEntry


def flight_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]


    try:

        if float(values[0])<0:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return

    except Exception:

        messagebox.showinfo("x", "Price is wrong!")
        root.deiconify()
        return


    values[1] = str(values[1]).replace('/', '.')
    start_date_str = f"{values[1]} {values[2]}:{values[3]}"
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")

    values[4] = str(values[4]).replace('/', '.')
    end_date_str = f"{values[4]} {values[5]}:{values[6]}"
    end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M")

    if start_date > end_date:
        messagebox.showinfo("x", "Start date is later than end date!")
        root.deiconify()
        return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE РЕЙС 
        SET "загальна_сума_в_грн" = ?, "дата_час_початку" = ?, "дата_час_кінця" = ?
        WHERE id = ?
    """, (values[0], start_date, end_date,ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this Flight!")

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def flight(action, table_name,root, name_db, entries):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add":
        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email is wrong!")
            root.deiconify()
            return

        if len(values[1].replace(' ', '')) <= 7:
            messagebox.showinfo("x", "Password is small(8 arguments min)!")
            root.deiconify()
            return

        cursor.execute("""SELECT * FROM ЛЮДИНА WHERE email = ? AND пароль = ?""", (values[0], values[1]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Person!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

        cursor.execute("""SELECT * FROM ТУРИСТ WHERE людина_id = ?""", (this_person[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this tourist!")
            root.deiconify()
            return

        this_tourist = [str(result) for result in results]

        if len(str(values[2]).replace(' ','')) <= 7:
            messagebox.showinfo("x", "Number flight is small (8 symbols min)!")
            root.deiconify()
            return

        cursor.execute("""SELECT * FROM РЕЙС WHERE турист_id = ? AND номер = ?""", (this_tourist[0], str(values[2]).replace(' ','')))

        if cursor.fetchone():
            messagebox.showinfo("x", "I bag your pardon. I know this flight with this person!")
            root.deiconify()
            return

        values[3] = str(values[3]).replace('/', '.')
        start_date_str = f"{values[3]} {values[4]}:{values[5]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M")

        values[6] = str(values[6]).replace('/', '.')
        end_date_str = f"{values[6]} {values[7]}:{values[8]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M")


        if start_date > end_date:
            messagebox.showinfo("x", "Start date is later than end date!")
            root.deiconify()
            return


        try:
            if float(values[9])<0:
                messagebox.showinfo("x", "Price is wrong!")
                root.deiconify()
                return
        except Exception:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return


        cursor.execute("""
                INSERT INTO РЕЙС ("турист_id", "номер", "дата_час_початку", "дата_час_кінця", "загальна_сума_в_грн")
                VALUES (?, ?, ?,?, ?)
                """, (this_tourist[0], values[2], start_date, end_date, values[9]))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new Flight!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit":
        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email is wrong!")
            root.deiconify()
            return

        if len(values[1].replace(' ', '')) <= 7:
            messagebox.showinfo("x", "Password is small(8 arguments min)!")
            root.deiconify()
            return

        cursor.execute("""SELECT * FROM ЛЮДИНА WHERE email = ? AND пароль = ?""", (values[0], values[1]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Person!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

        cursor.execute("""SELECT * FROM ТУРИСТ WHERE людина_id = ?""", (this_person[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this tourist!")
            root.deiconify()
            return

        this_tourist = [str(result) for result in results]

        cursor.execute("""SELECT * FROM РЕЙС WHERE турист_id = ? AND номер = ?""", (this_tourist[0], values[2]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this flight!")
            root.deiconify()
            return

        this_flight = [str(result) for result in results]

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

        ID = this_flight[0]

        hints = [
            f"The old price: {this_flight[5]}.\tThe new price:",
                 f"The old start date and time: {this_flight[3]}.\tThe new start date and time:",
                 f"The old end date and time: {this_flight[4]}.\tThe new end date and time:"

                 ]

        labels = []

        for hint in hints:
            labels.append(tk.Label(root, text=hint))

        root.update()

        for label in labels:
            label.place(x=10, y=50)

        root.update()

        empty_height = root.winfo_height() - 20 - button_back.winfo_height()

        for label in labels:
            empty_height -= label.winfo_height()

        empty_height /= (len(hints) + 2)

        helper_height = 20 + button_back.winfo_height()

        for i, label in enumerate(labels, start=1):
            label.place(x=10, y=helper_height + i * empty_height + (i - 1) * label.winfo_height())

        root.update()

        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")
        end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        entry_price = tk.Entry(root)

        root.update()

        entries = [
            entry_price,
            start_date_entry, start_hour_spinbox, start_minute_spinbox,
            end_date_entry, end_hour_spinbox, end_minute_spinbox

        ]

        root.update()

        entries[0].place(x=10+root.winfo_width()/2, y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())

        root.update()

        entries[1].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        entries[2].place(x=20 + root.winfo_width() / 2 + entries[1].winfo_width(),
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        entries[3].place(x=30 + root.winfo_width() / 2 + entries[1].winfo_width() + entries[2].winfo_width(),
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        entries[4].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[5].place(x=20 + root.winfo_width() / 2 + entries[4].winfo_width(),
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[6].place(x=30 + root.winfo_width() / 2 + entries[4].winfo_width() + entries[5].winfo_width(),
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: flight_edit(root, entries, name_db, ID))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

        try:
            root.deiconify()
        except Exception:
            pass

        try:
            conn.close()
        except Exception:
            pass
        return

    if str(action).lower().replace(' ', '') == "delete":

        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email is wrong!")
            root.deiconify()
            return

        if len(values[1].replace(' ', '')) <= 7:
            messagebox.showinfo("x", "Password is small(8 arguments min)!")
            root.deiconify()
            return

        cursor.execute("""SELECT * FROM ЛЮДИНА WHERE email = ? AND пароль = ?""", (values[0], values[1]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Person!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

        cursor.execute("""SELECT * FROM ТУРИСТ WHERE людина_id = ?""", (this_person[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this tourist!")
            root.deiconify()
            return

        this_tourist = [str(result) for result in results]

        cursor.execute("""SELECT * FROM РЕЙС WHERE турист_id = ? AND номер = ?""", (this_tourist[0], values[2]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this flight!")
            root.deiconify()
            return

        this_flight= [str(result) for result in results]

        cursor.execute("""
            DELETE FROM РЕЙС
                WHERE id = ?
            """, (this_flight[0]))

        conn.commit()

        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass

        messagebox.showinfo("✓", "The flight has been removed!")
        admin_menu(root, name_db)

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

