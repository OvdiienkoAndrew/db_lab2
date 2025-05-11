import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk

from tkcalendar import DateEntry


def hotelaccommodation_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    print(values)

    try:
        if int(values[0])<=0:
            messagebox.showinfo("x", "Max people in the room is wrong!")
            root.deiconify()
            return

    except Exception:
        messagebox.showinfo("x", "Max people in the room is wrong!")
        root.deiconify()
        return

    values[1] = str(values[1]).replace('/', '.')
    start_date_str = f"{values[1]} {values[2]}:{values[3]}"
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

    values[4] = str(values[4]).replace('/', '.')
    end_date_str = f"{values[4]} {values[5]}:{values[6]}"
    end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

    if start_date > end_date:
        messagebox.showinfo("x", "Start date and time is later than end date and time!")
        root.deiconify()
        return

    try:
        if float(values[7]) < 0:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return

    except Exception:
        messagebox.showinfo("x", "Price is wrong!")
        root.deiconify()
        return

    try:
        if int(values[8]) <= 0:
            messagebox.showinfo("x", "Days counter is wrong!")
            root.deiconify()
            return

    except Exception:
        messagebox.showinfo("x", "Days counter is wrong!")
        root.deiconify()
        return

    query = """
       UPDATE ПРОЖИВАННЯ_У_ОТЕЛІ
       SET 
           максимальна_кількість_людей = ?, 
           дата_час_початку = ?, 
           дата_час_кінця = ?, 
           вартість_в_грн = ?,
           кількість_днів = ?
       WHERE id = ?;
       """
    cursor.execute(query, (values[0], start_date, end_date, values[7], values[8], ID))

    conn.commit()


    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    messagebox.showinfo("✓", "I updated this Accommodation!")

    admin_menu(root,name_db)


def hotelaccommodation(action, table_name,root, name_db, entries):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add" and str(table_name).lower().replace(' ','') == "hotelaccommodation":

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

        if values[2].lower().replace(' ','') == "choicehotelname":
            messagebox.showinfo("x", "I don't know this Hotel!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

        cursor.execute("""SELECT * FROM ОТЕЛЬ WHERE назва = ?""", (values[2],))

        results = cursor.fetchone()

        this_hotel = [str(result) for result in results]

        cursor.execute("""SELECT * FROM НОМЕР_У_ОТЕЛІ WHERE отель_id = ? AND номер_кімнати = ?""", (this_hotel[0], values[3],))

        results = cursor.fetchone()

        if results is None:
            messagebox.showinfo("x", f"I don't know this Number ({values[3]}) in the hotel: '{this_hotel[1]}'!")
            root.deiconify()
            return

        this_number_in_hotel = [str(result) for result in results]


        values[4] = str(values[4]).replace('/', '.')
        start_date_str = f"{values[4]} {values[5]}:{values[6]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

        values[7] = str(values[7]).replace('/', '.')
        end_date_str = f"{values[7]} {values[8]}:{values[9]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")


        if start_date > end_date:
            messagebox.showinfo("x", "Start date and time is later than end date and time!")
            root.deiconify()
            return


        try:
            if int(values[10]) <= 0:
                messagebox.showinfo("x", f"Max person in the room is wrong!")
                root.deiconify()
                return

        except Exception:
            messagebox.showinfo("x", f"Max people in the room is wrong!")
            root.deiconify()
            return

        try:
            if float(values[11]) < 0:
                messagebox.showinfo("x", f"Price is wrong!")
                root.deiconify()
                return

        except Exception:
            messagebox.showinfo("x", f"Price is wrong!")
            root.deiconify()
            return

        try:
            if int(values[12]) <= 0:
                messagebox.showinfo("x", f"Day's counter is wrong!")
                root.deiconify()
                return

        except Exception:
            messagebox.showinfo("x", f"Day's counter is wrong!")
            root.deiconify()
            return

        query = "SELECT * FROM ПРОЖИВАННЯ_У_ОТЕЛІ WHERE турист_id = ? AND отель_id = ? AND дата_час_початку = ? AND дата_час_кінця = ?"
        cursor.execute(query, (this_person[0],this_hotel[0], start_date, end_date))

        results = cursor.fetchone()

        if results:
            conn.close()
            messagebox.showinfo("x", "I know this accommodation!")
            root.deiconify()
            return

        cursor.execute("""
               INSERT INTO ПРОЖИВАННЯ_У_ОТЕЛІ ("турист_id", "отель_id", "номер_у_отелі_id", "дата_час_початку", "дата_час_кінця", "вартість_в_грн", "кількість_днів", "максимальна_кількість_людей") 
               VALUES (?, ?, ?, ?, ?, ?,?,?)
               """, (this_person[0], this_hotel[0], this_number_in_hotel[0], start_date, end_date, values[11], values[12], values[10]))
        conn.commit()

        root.deiconify()
        conn.close()
        messagebox.showinfo("x", "I knew the new accommodation!")
        return

    if str(action).lower().replace(' ', '') == "edit" and str(table_name).lower().replace(' ', '') == "hotelaccommodation":

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

        if values[2].lower().replace(' ', '') == "choicehotelname":
            messagebox.showinfo("x", "I don't know this Hotel!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

        cursor.execute("""SELECT * FROM ОТЕЛЬ WHERE назва = ?""", (values[2],))

        results = cursor.fetchone()

        this_hotel = [str(result) for result in results]

        cursor.execute("""SELECT * FROM НОМЕР_У_ОТЕЛІ WHERE отель_id = ? AND номер_кімнати = ?""",
                       (this_hotel[0], values[3],))

        results = cursor.fetchone()

        if results is None:
            messagebox.showinfo("x", f"I don't know this Number ({values[3]}) in the hotel: '{this_hotel[1]}'!")
            root.deiconify()
            return

        this_number_in_hotel = [str(result) for result in results]

        values[4] = str(values[4]).replace('/', '.')
        start_date_str = f"{values[4]} {values[5]}:{values[6]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

        values[7] = str(values[7]).replace('/', '.')
        end_date_str = f"{values[7]} {values[8]}:{values[9]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

        if start_date > end_date:
            messagebox.showinfo("x", "Start date and time is later than end date and time!")
            root.deiconify()
            return

        query = "SELECT * FROM ПРОЖИВАННЯ_У_ОТЕЛІ WHERE турист_id = ? AND отель_id = ? AND дата_час_початку = ? AND дата_час_кінця = ?"
        cursor.execute(query, (this_person[0], this_hotel[0], start_date, end_date))

        results = cursor.fetchone()

        if results is None:
            conn.close()
            messagebox.showinfo("x", "I don't know this accommodation!")
            root.deiconify()
            return

        results = [str(result) for result in results]

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

        ID = results[0]

        hints = [f"Old max people in the room ({results[4]})\tNew max people in the room:",
                 f"Old Start date ({results[5]})\tNew start date:",
                 f"Old End date ({results[6]})\tNew End date:",
                 f"Old price ({results[7]})\tNew price:",
                 f"Old days ({results[8]})\tNew days:",
                 ]

        labels = []

        for i in range(0, len(hints)):
            labels.append(tk.Label(root, text=hints[i]))

        root.update()

        for label in labels:
            label.place(x=10, y=50)

        root.update()

        empty_height = root.winfo_height() - 20 - button_back.winfo_height()

        for label in labels:
            empty_height -= label.winfo_height()

        empty_height /= (len(labels) + 2)

        helper_height = 20 + button_back.winfo_height()

        for i, label in enumerate(labels, start=1):
            label.place(x=10, y=helper_height + i * empty_height + (i - 1) * label.winfo_height())

        entry_max_people= tk.Entry(root)

        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

        start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        entry_price = tk.Entry(root)
        entry_days = tk.Entry(root)

        root.update()

        entries = [entry_max_people, start_date_entry, start_hour_spinbox, start_minute_spinbox,
                   end_date_entry, end_hour_spinbox, end_minute_spinbox,
                   entry_price, entry_days]

        root.update()


        entries[0].place(x=10 + root.winfo_width()/2, y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())
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

        for i in range(7,len(entries)):
            entries[i].place(x=10 + root.winfo_width()/2, y=helper_height + (i-3) * empty_height + (i-3 - 1) * labels[0].winfo_height())


        root.update()

        send_button = tk.Button(root, text=action, command=lambda: hotelaccommodation_edit(root, entries, name_db, ID))
        send_button.place(x=10,
                          y=helper_height + (len(labels)+1) * empty_height + ((len(labels)+1)- 1) * labels[0].winfo_height())
        root.update()


        try:
            root.deiconify()
        except Exception:
            pass

        try:
            conn.close()
        except Exception:
            pass
        return

    if str(action).lower().replace(' ', '') == "delete" and str(table_name).lower().replace(' ', '') == "hotelaccommodation":

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

        if values[2].lower().replace(' ', '') == "choicehotelname":
            messagebox.showinfo("x", "I don't know this Hotel!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

        cursor.execute("""SELECT * FROM ОТЕЛЬ WHERE назва = ?""", (values[2],))

        results = cursor.fetchone()

        this_hotel = [str(result) for result in results]

        cursor.execute("""SELECT * FROM НОМЕР_У_ОТЕЛІ WHERE отель_id = ? AND номер_кімнати = ?""",
                       (this_hotel[0], values[3],))

        results = cursor.fetchone()

        if results is None:
            messagebox.showinfo("x", f"I don't know this Number ({values[3]}) in the hotel: '{this_hotel[1]}'!")
            root.deiconify()
            return

        this_number_in_hotel = [str(result) for result in results]

        values[4] = str(values[4]).replace('/', '.')
        start_date_str = f"{values[4]} {values[5]}:{values[6]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

        values[7] = str(values[7]).replace('/', '.')
        end_date_str = f"{values[7]} {values[8]}:{values[9]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

        if start_date > end_date:
            messagebox.showinfo("x", "Start date and time is later than end date and time!")
            root.deiconify()
            return

        query = "SELECT * FROM ПРОЖИВАННЯ_У_ОТЕЛІ WHERE турист_id = ? AND отель_id = ? AND дата_час_початку = ? AND дата_час_кінця = ?"
        cursor.execute(query, (this_person[0], this_hotel[0], start_date, end_date))

        results = cursor.fetchone()

        if results is None:
            conn.close()
            messagebox.showinfo("x", "I don't know this accommodation!")
            root.deiconify()
            return

        results = [str(result) for result in results]

        query = "DELETE FROM ПРОЖИВАННЯ_У_ОТЕЛІ WHERE id = ?"
        cursor.execute(query, (results[0],))
        conn.commit()


        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass

        messagebox.showinfo("✓", "The accommodation has been removed!")
        admin_menu(root, name_db)

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

