import ast
import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry




def table(action,table_name,root,name_db):

    from src.service.agency import agency
    from src.service.excursion import excursion
    from src.service.person import person
    from src.service.parents import parents
    from src.service.hotel import hotel
    from src.service.hotel_number import hotel_number
    from src.service.passport import passport
    from src.service.tourist import tourist
    from src.service.visa import visa
    from src.service.hotelaccommodation import hotelaccommodation
    from src.service.cargo import cargo
    from src.service.flight import flight
    from src.service.excursion_and_tourist import excursion_and_tourist
    from src.service.financialreport import financialreport


    root.title(f"{action}/{table_name}")
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: actions(action,root, name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    if str(action).lower().replace(' ','')==str("add") and str(table_name).lower().replace(' ','')==str("agency"):
            hints = ["Name","Address","Contact without +","Rating"]

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

            entries = []

            for i in range(len(labels)):
                entries.append(tk.Entry(root))

            for i, entry in enumerate(entries, start=1):
                entry.place(x=root.winfo_width() / 2 + 10,
                            y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                            width=root.winfo_width() / 2 - 20)
                entry.insert(0, str(''))

            send_button = tk.Button(root, text=action, command=lambda: agency(action, table_name,root, entries, name_db))
            send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
                0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str("delete")) and str(table_name).lower().replace(' ', '') == str("agency"):

        hints = ["Name", "Address"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: agency(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str("excursion"):
        hints = ["Name Agency", "Address Agency","Name","Description","Start date and time (YYYY-MM-DD HH:MM)","End date and time (YYYY-MM-DD HH:MM)","Price "]

        label_name_agency = tk.Label(root, text=hints[0])
        label_address_agency = tk.Label(root, text=hints[1])
        label_name = tk.Label(root, text=hints[2])
        label_description = tk.Label(root, text=hints[3])
        label_start = tk.Label(root, text=hints[4])
        label_end = tk.Label(root, text=hints[5])
        label_price = tk.Label(root, text=hints[6])

        root.update()

        label_name_agency.place(x=10, y=50)
        label_address_agency.place(x=10, y=50)
        label_name.place(x=10, y=50)
        label_description.place(x=10, y=50)
        label_start.place(x=10, y=50)
        label_end.place(x=10, y=50)
        label_price.place(x=10, y=50)

        root.update()

        empty_height = root.winfo_height() - 20 - button_back.winfo_height()


        empty_height = empty_height - label_name_agency.winfo_height() -label_name.winfo_height()-label_address_agency.winfo_height()-label_description.winfo_height()-label_start.winfo_height()-label_end.winfo_height()-label_price.winfo_height()

        empty_height /= (len(hints) + 2)

        helper_height = 20 + button_back.winfo_height()

        label_name_agency.place(x=10, y=helper_height + 1 * empty_height + (1 - 1) * label_name_agency.winfo_height())
        label_address_agency.place(x=10, y=helper_height + 2 * empty_height + (2 - 1) * label_name_agency.winfo_height())
        label_name.place(x=10, y=helper_height + 3 * empty_height + (3 - 1) * label_name_agency.winfo_height())
        label_description.place(x=10, y=helper_height + 4 * empty_height + (4 - 1) * label_name_agency.winfo_height())
        label_start.place(x=10,y=helper_height + 5 * empty_height + (5 - 1) * label_name_agency.winfo_height())
        label_end.place(x=10, y=helper_height + 6 * empty_height + (6 - 1) * label_name_agency.winfo_height())
        label_price.place(x=10,y=helper_height + 7 * empty_height + (7 - 1) * label_name_agency.winfo_height())

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT  назва, адрес  FROM АГЕНТСТВО ORDER BY назва ASC")

        options_name = []
        options_address = []
        results = cursor.fetchall()

        if results:
            for result in results:
                options_name.append(str(result[0]))
                options_address.append(str(result[1]))


        conn.close()

        entry_name_agency = ttk.Combobox(root, values=options_name, state="readonly")
        entry_name_agency.set("Choice name agency")

        entry_address_agency = ttk.Combobox(root, values=options_address, state="readonly")
        entry_address_agency.set("Choice address agency")


        entry_name = tk.Entry(root)
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


        entry_name_agency.place(x=10+root.winfo_width()/2,
                                y=helper_height + 1 * empty_height + (1-1) * label_name_agency.winfo_height())

        root.update()

        entry_address_agency.place(x=10 + root.winfo_width() / 2,
                                y=helper_height + 2 * empty_height + (2 - 1) * label_name_agency.winfo_height())

        root.update()

        entry_name.place(x=10 + root.winfo_width() / 2,
                                y=helper_height + 3 * empty_height + (3 - 1) * label_name_agency.winfo_height())

        root.update()

        entry_description.place(x=10 + root.winfo_width() / 2,
                                y=helper_height + 4 * empty_height + (4 - 1) * label_name_agency.winfo_height())

        root.update()

        start_date_entry.place(x=10 + root.winfo_width() / 2,
                               y=helper_height + 5 * empty_height + (5 - 1) * label_name_agency.winfo_height())

        root.update()

        start_hour_spinbox.place(x=10 + (root.winfo_width() / 2) + start_date_entry.winfo_width() + 10,
                                 y=helper_height + 5 * empty_height + (5 - 1) * label_name_agency.winfo_height())

        root.update()

        start_minute_spinbox.place(
            x=10 + (
                        root.winfo_width() / 2) + start_date_entry.winfo_width() + 10 + start_hour_spinbox.winfo_width() + 10,
            y=helper_height + 5 * empty_height + (
                    5 - 1) * label_name_agency.winfo_height())

        root.update()

        end_date_entry.place(x=10 + root.winfo_width() / 2,
                               y=helper_height + 6 * empty_height + (6 - 1) * label_name_agency.winfo_height())

        root.update()

        end_hour_spinbox.place(x=10 + (root.winfo_width() / 2) + end_date_entry.winfo_width() + 10,
                                 y=helper_height + 6 * empty_height + (6 - 1) * label_name_agency.winfo_height())

        root.update()

        end_minute_spinbox.place(
            x=10 + (
                    root.winfo_width() / 2) + end_date_entry.winfo_width() + 10 + end_hour_spinbox.winfo_width() + 10,
            y=helper_height + 6 * empty_height + (
                    6 - 1) * label_name_agency.winfo_height())

        root.update()

        entry_price.place(x=10 + root.winfo_width() / 2,
                                y=helper_height + 7 * empty_height + (7 - 1) * label_name_agency.winfo_height())

        root.update()


        values = [entry_name_agency,entry_address_agency,entry_name,entry_description,start_date_entry,start_hour_spinbox,start_minute_spinbox,end_date_entry,end_hour_spinbox,end_minute_spinbox,entry_price]

        send_button = tk.Button(root, text=action, command=lambda: excursion(action, table_name, root, name_db,values))
        send_button.place(x=10,
                          y=helper_height + 8 * empty_height + (8 - 1) * label_name_agency.winfo_height())
        root.update()

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("excursion"):

        hints = ["Name Agency", "Address Agency","Name"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: excursion(action, table_name, root, name_db, entries))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str("person"):
        hints = ["Surname", "Name", "Patronymic", "Email","Password","Phone (not necessarily)"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action, command=lambda: person(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str("delete")) and str(table_name).lower().replace(' ', '') == str("person"):

        hints = ["Email","Password"]

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



        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        entries = [entry_email, entry_password]

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: person(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str("parent(onlyforthekid)"):
        hints = ["Email (child)", "Email (guardian)"]

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

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        entry_email1 = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email1.set("Choice Email")


        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email2 = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email2.set("Choice Email")


        entries = [entry_email1, entry_email2]


        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action, command=lambda: parents(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("parent(onlyforthekid)"):

        hints = ["Email (child)", "Email (guardian)"]

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



        options_email1 = []

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        query = """SELECT дитина_id FROM БАТЬКІВСТВО"""
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for result in results:
                query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                cursor.execute(query, (str(result[0]),))
                temps = cursor.fetchone()
                if temps:
                    options_email1.append(str(temps[4]))

        root.update()
        entry_email1 = ttk.Combobox(root, values=options_email1, state="readonly")
        entry_email1.set("Choice Email")

        query = """SELECT один_з_батькiв_id FROM БАТЬКІВСТВО"""
        cursor.execute(query)
        results = cursor.fetchall()
        options_email = []

        if results:
            for result in results:
                query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                cursor.execute(query, (str(result[0]),))
                temps = cursor.fetchone()
                if temps:
                    options_email.append(str(temps[4]))

        root.update()
        entry_email2 = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email2.set("Choice Email")

        entries = [entry_email1, entry_email2]

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: parents(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "hotel"):
        hints = ["Name", "Address", "Price"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action, command=lambda: hotel(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("hotel"):

        hints = ["Name"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: hotel(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "hotel'snumber"):
        hints = ["Name hotel", "Number room", "Max amount", "Price"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action, command=lambda: hotel_number(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("hotel'snumber"):

        hints = ["Name hotel", "Number room"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: hotel_number(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "passport"):
        hints = ["Email", "Password", "Date of Birthday", "End date","Photo"]

        label_email= tk.Label(root, text=hints[0])
        label_password = tk.Label(root, text=hints[1])
        label_start_date = tk.Label(root, text=hints[2])
        label_end_date = tk.Label(root, text=hints[3])
        label_photo = tk.Label(root, text=hints[4])

        labels = [label_email,label_password,label_start_date,label_end_date,label_photo]

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

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)


        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

        start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        def choose_photo(entry_widget):
            filepath = filedialog.askopenfilename(
                title="Выберите изображение",
                filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if filepath:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, filepath)

        entry_image = tk.Entry(root)

        button = tk.Button(root, text="Choice photo", command=lambda: choose_photo(entry_image))


        root.update()

        entries = [entry_email,entry_password,start_date_entry,end_date_entry,start_hour_spinbox,start_minute_spinbox,end_hour_spinbox,end_minute_spinbox,entry_image,button]

        j=0

        for i, label in enumerate(labels, start=1,):
            entries[j].place(x=10+root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * label.winfo_height())
            j+=1
            if i>=4:
                break

        root.update()

        entries[j].place(x=10 + root.winfo_width() / 2 + 10 + entries[j-1].winfo_width() ,
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        j+=1

        root.update()

        entries[j].place(x=10 + root.winfo_width() / 2 + 10 + entries[j - 2].winfo_width() + 10 + entries[j - 1].winfo_width(),
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        j += 1
        root.update()

        entries[j].place(x=10 + root.winfo_width() / 2 + 10 + entries[j - 1-2].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        j += 1

        root.update()

        entries[j].place(x=10 + root.winfo_width() / 2 + 20 + entries[3].winfo_width() + entries[5].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        j += 1

        root.update()

        entries[j].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        j += 1

        root.update()

        entries[j].place(x=10 + root.winfo_width() / 2 + 10 + entries[j-1].winfo_width(),
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height()-(entries[j].winfo_height()-entries[j-1].winfo_height())/2)

        root.update()

        entries[j].place(x=10 + root.winfo_width() / 2 + 10 + entries[j - 1].winfo_width(),
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height() - (
                                     entries[j].winfo_height() - entries[j - 1].winfo_height()) / 2)

        root.update()

        entries.pop()

        send_button = tk.Button(root, text=action, command=lambda: passport(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("passport"):

        hints = ["Email", "Password"]

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

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT людина_id FROM ПАСПОРТ")

        options_email = []
        names = cursor.fetchall()

        if names:
            for name in names:
                #cursor.execute("SELECT * FROM ЛЮДИНА WHERE id = ?")
                cursor.execute("SELECT email FROM ЛЮДИНА WHERE id = ?", (str(name[0]),))
                emails = cursor.fetchall()

                options_email.append(str(emails[0][0]))

        options_email = sorted(options_email)


        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        root.update()

        entries = [entry_email, entry_password]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))
            root.update()

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: passport(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())
        root.update()

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "tourist"):
        hints = ["Email", "Password", "Sex", "Category"]

        label_email = tk.Label(root, text=hints[0])
        label_password = tk.Label(root, text=hints[1])
        label_sex = tk.Label(root, text=hints[2])
        label_category = tk.Label(root, text=hints[3])

        labels = [label_email, label_password, label_sex, label_category]

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

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        options_sex = ["Human", "Woman"]

        entry_sex = ttk.Combobox(root, values=options_sex, state="readonly")
        entry_sex.set("Choice Sex")

        options_category = ["Rest", "Cargo", "Kids"]

        entry_category = ttk.Combobox(root, values=options_category, state="readonly")
        entry_category.set("Choice Category")



        root.update()
        entries = [entry_email, entry_password, entry_sex, entry_category]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10 + root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action, command=lambda: tourist(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("tourist"):

        hints = ["Email", "Password"]

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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: tourist(action, table_name, root, entries, name_db))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str("visa"):
        hints = ["Email", "Password","Card number","Start date and time (YYYY-MM-DD HH:MM)","End date and time (YYYY-MM-DD HH:MM)","Status "]

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
        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)
        entry_card_number = tk.Entry(root)



        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

        options_sex = ["Active", "Block"]

        entry_sex = ttk.Combobox(root, values=options_sex, state="readonly")
        entry_sex.set("Choice status")

        entries = [entry_email, entry_password, entry_card_number, start_date_entry, end_date_entry, entry_sex]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10+root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()




        send_button = tk.Button(root, text=action, command=lambda: visa(action, table_name, root, name_db,entries))
        send_button.place(x=10,
                          y=helper_height + (1+len(labels)) * empty_height + ((1+len(labels)) - 1) * labels[0].winfo_height())
        root.update()

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("visa"):

        hints = ["Email", "Password"]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        options_email = []

        query = """SELECT * FROM VISA"""
        cursor.execute(query)
        results = cursor.fetchall()
        results = [str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '') for
                   result in results]

        if results is not None:
            cargoes = [str(result) for result in results]
            for cargo1 in cargoes:
                cargo1 = cargo1.split()
                query = """SELECT * FROM ТУРИСТ Where id = ?"""
                cursor.execute(query, (str(cargo1[1]),))
                results = cursor.fetchall()
                results = [str(result) for result in results]
                results = [
                    str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '')
                    for result in results]
                results = [str(result).split() for result in results]

                for result in results:
                    query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                    cursor.execute(query, (str(result[1]),))
                    user = cursor.fetchall()
                    user = [
                        str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ',
                                                                                                                '') for
                        result in user]

                    user = [str(result) for result in user]
                    user = user[0].split()
                    options_email.append(str(user[4]))
                    print(user[4])

        conn.close()
        root.update()
        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)
        root.update()
        entries = [entry_email, entry_password]
        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: visa(action, table_name, root, name_db,entries))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "hotelaccommodation"):
        hints = ["Email", "Password", "Name Hotel", "Number in the hotel", "Start date and time (YYYY-MM-DD HH:MM)",
                 "End date and time (YYYY-MM-DD HH:MM)","Max people", "Price ", "Day's counter"]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT назва FROM ОТЕЛЬ")

        options_name_hotel = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_name_hotel.append(str(name[0]))


        conn.close()



        entry_name_hotel = ttk.Combobox(root, values=options_name_hotel, state="readonly")
        entry_name_hotel.set("Choice hotel name")

        entry_number_hotel = tk.Entry(root)
        entry_max_people= tk.Entry(root)
        entry_price = tk.Entry(root)
        entry_day_counter = tk.Entry(root)


        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

        start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        root.update()


        entries = [entry_email, entry_password, entry_name_hotel, entry_number_hotel,
                   start_date_entry, start_hour_spinbox, start_minute_spinbox,
                   end_date_entry, end_hour_spinbox, end_minute_spinbox,
                   entry_max_people, entry_price, entry_day_counter
                   ]

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10+root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()

        entries[5].place(x=20+root.winfo_width()/2 + entries[4].winfo_width(), y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        entries[6].place(x=30 + root.winfo_width() / 2 + entries[4].winfo_width() + entries[5].winfo_width(),
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        entries[7].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 6 * empty_height + (6 - 1) * labels[0].winfo_height())

        root.update()

        entries[8].place(x=20 + root.winfo_width() / 2 + entries[7].winfo_width(),
                         y=helper_height + 6 * empty_height + (6 - 1) * labels[0].winfo_height())

        root.update()

        entries[9].place(x=30 + root.winfo_width() / 2 + entries[7].winfo_width() + entries[8].winfo_width(),
                         y=helper_height + 6 * empty_height + (6 - 1) * labels[0].winfo_height())

        root.update()

        root.update()

        entries[10].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 7 * empty_height + (7 - 1) * labels[0].winfo_height())

        root.update()

        entries[11].place(x=10 + root.winfo_width() / 2,
                          y=helper_height + 8 * empty_height + (8 - 1) * labels[0].winfo_height())

        root.update()

        entries[12].place(x=10 + root.winfo_width() / 2,
                          y=helper_height + 9 * empty_height + (9 - 1) * labels[0].winfo_height())

        root.update()





        send_button = tk.Button(root, text=action, command=lambda: hotelaccommodation(action, table_name, root, name_db, entries))
        send_button.place(x=10,
                          y=helper_height + (len(labels)+1) * empty_height + ((len(labels)+1) - 1) * labels[0].winfo_height())
        root.update()

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("hotelaccommodation"):

        hints = ["Email", "Password", "Name Hotel", "Number in the hotel", "Start date and time (YYYY-MM-DD HH:MM)",
                 "End date and time (YYYY-MM-DD HH:MM)"]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        options_email = []

        query = """SELECT * FROM ПРОЖИВАННЯ_У_ОТЕЛІ"""
        cursor.execute(query)
        results = cursor.fetchall()
        results = [str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '') for
                   result in results]

        if results is not None:
            cargoes = [str(result) for result in results]
            for cargo1 in cargoes:
                cargo1 = cargo1.split()
                query = """SELECT * FROM ТУРИСТ Where id = ?"""
                cursor.execute(query, (str(cargo1[1]),))
                results = cursor.fetchall()
                results = [str(result) for result in results]
                results = [
                    str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '')
                    for result in results]
                results = [str(result).split() for result in results]

                for result in results:
                    query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                    cursor.execute(query, (str(result[1]),))
                    user = cursor.fetchall()
                    user = [
                        str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ',
                                                                                                                '') for
                        result in user]

                    user = [str(result) for result in user]
                    user = user[0].split()
                    options_email.append(str(user[4]))
                    print(user[4])


        root.update()
        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        cursor.execute("SELECT назва FROM ОТЕЛЬ")

        options_name_hotel = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_name_hotel.append(str(name[0]))

        conn.close()

        entry_name_hotel = ttk.Combobox(root, values=options_name_hotel, state="readonly")
        entry_name_hotel.set("Choice hotel name")

        entry_number_hotel = tk.Entry(root)

        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

        start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        root.update()

        entries = [entry_email, entry_password, entry_name_hotel, entry_number_hotel,
                   start_date_entry, start_hour_spinbox, start_minute_spinbox,
                   end_date_entry, end_hour_spinbox, end_minute_spinbox
                   ]

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10 + root.winfo_width() / 2,
                        y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()

        entries[5].place(x=20 + root.winfo_width() / 2 + entries[4].winfo_width(),
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        entries[6].place(x=30 + root.winfo_width() / 2 + entries[4].winfo_width() + entries[5].winfo_width(),
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        entries[7].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 6 * empty_height + (6 - 1) * labels[0].winfo_height())

        root.update()

        entries[8].place(x=20 + root.winfo_width() / 2 + entries[7].winfo_width(),
                         y=helper_height + 6 * empty_height + (6 - 1) * labels[0].winfo_height())

        root.update()

        entries[9].place(x=30 + root.winfo_width() / 2 + entries[7].winfo_width() + entries[8].winfo_width(),
                         y=helper_height + 6 * empty_height + (6 - 1) * labels[0].winfo_height())

        root.update()


        send_button = tk.Button(root, text=action,
                                command=lambda: hotelaccommodation(action, table_name, root, name_db, entries))
        send_button.place(x=10,
                          y=helper_height + (len(labels) + 1) * empty_height + ((len(labels) + 1) - 1) * labels[
                              0].winfo_height())
        root.update()

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "cargo"):
        hints = ["Email", "Password", "Cargo type", "Number of luggage compartments", "Weight in kg", "Price (one place)", "Insurance"]

        labels = []

        for i,hint in enumerate(hints,start=0):
            labels.append(tk.Label(root, text=hints[i]))


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

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")

        entry_password = tk.Entry(root)

        entry_cargo_type = tk.Entry(root)
        entry_number_of_luggage_compartments = tk.Entry(root)
        entry_weight_in_kg = tk.Entry(root)
        entry_price_one_place = tk.Entry(root)
        entry_insurance = tk.Entry(root)

        root.update()
        entries = [entry_email, entry_password, entry_cargo_type,entry_number_of_luggage_compartments,
                   entry_weight_in_kg, entry_price_one_place, entry_insurance]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10 + root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action, command=lambda: cargo(action, table_name,root, name_db, entries))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("cargo"):

        hints = ["Email", "Password"]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        options_email = []

        query = """SELECT * FROM ВАНТАЖ"""
        cursor.execute(query)
        results = cursor.fetchall()
        results = [str(result).replace(')','').replace('(','').replace(',','').replace("'",'').replace('  ','') for result in results]


        if results is not None:
             cargoes = [str(result) for result in results]
             for cargo1 in cargoes:
                cargo1 = cargo1.split()
                query = """SELECT * FROM ТУРИСТ Where id = ?"""
                cursor.execute(query, (str(cargo1[1]),))
                results = cursor.fetchall()
                results = [str(result) for result in results]
                results = [
                    str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '')
                    for result in results]
                results = [str(result).split() for result in results]

                for result in results:

                    query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                    cursor.execute(query, (str(result[1]),))
                    user = cursor.fetchall()
                    user = [
                        str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ',
                                                                                                                '') for
                        result in user]

                    user = [str(result) for result in user]
                    user = user[0].split()
                    options_email.append(str(user[4]))
                    print(user[4])


        conn.close()
        root.update()
        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)
        root.update()
        entries = [entry_email, entry_password]
        root.update()

        entries[0].place(x=10+root.winfo_width()/2,y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())
        entries[1].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: cargo(action, table_name,root, name_db, entries))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

        root.update()

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "flight"):
        hints = ["Email", "Password", "Number flight", "Start date and time (YYYY-MM-DD HH:MM)",
                 "End date and time (YYYY-MM-DD HH:MM)", "Price "]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        entry_number = tk.Entry(root)

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
            entry_email, entry_password, entry_number,
            start_date_entry, start_hour_spinbox, start_minute_spinbox,
            end_date_entry, end_hour_spinbox, end_minute_spinbox,
            entry_price
        ]

        root.update()

        entries[0].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())

        root.update()

        entries[1].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        entries[2].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[3].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        entries[4].place(x=20 + root.winfo_width() / 2 + entries[3].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        root.update()

        entries[5].place(x=30 + root.winfo_width() / 2 + entries[3].winfo_width() + entries[4].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        entries[6].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        entries[7].place(x=20 + root.winfo_width() / 2 + entries[6].winfo_width(),
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        root.update()

        entries[8].place(x=30 + root.winfo_width() / 2 + entries[6].winfo_width() + entries[7].winfo_width(),
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        entries[9].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 6 * empty_height + (6 - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: flight(action, table_name, root, name_db, entries))
        send_button.place(x=10,
                          y=helper_height + (len(labels) + 1) * empty_height + ((len(labels) + 1) - 1) * labels[
                              0].winfo_height())
        root.update()

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str("flight"):

        hints = ["Email", "Password", "Number flight"]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        options_email = []

        query = """SELECT * FROM РЕЙС"""
        cursor.execute(query)
        results = cursor.fetchall()
        results = [str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '') for
                   result in results]

        if results is not None:
            cargoes = [str(result) for result in results]
            for cargo1 in cargoes:
                cargo1 = cargo1.split()
                query = """SELECT * FROM ТУРИСТ Where id = ?"""
                cursor.execute(query, (str(cargo1[1]),))
                results = cursor.fetchall()
                results = [str(result) for result in results]
                results = [
                    str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '')
                    for result in results]
                results = [str(result).split() for result in results]

                for result in results:
                    query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                    cursor.execute(query, (str(result[1]),))
                    user = cursor.fetchall()
                    user = [
                        str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ',
                                                                                                                '') for
                        result in user]

                    user = [str(result) for result in user]
                    user = user[0].split()
                    options_email.append(str(user[4]))



        root.update()
        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        cursor.execute("""
            SELECT DISTINCT номер FROM РЕЙС
            ORDER BY номер ASC
        """)

        results = cursor.fetchall()
        results = [str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '') for
                   result in results]
        options_number = []
        if results is not None:
            results = [str(result) for result in results]
            for result in results:
                result = str(result.split()).replace('[','').replace(']','').replace("'",'')
                print(result)
                options_number.append(result)

        root.update()
        entry_number = ttk.Combobox(root, values=options_number, state="readonly")
        entry_number.set("Choice Number")
        root.update()
        entries = [entry_email, entry_password, entry_number]
        root.update()

        for i, entry in enumerate(entries,start=1):
            entry.place(x=10 + root.winfo_width() / 2,
                         y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: flight(action, table_name, root, name_db, entries))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

        root.update()

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "сonductinganexcursion"):
        hints = ["Email", "Password", "Name excursion", "Agency"]

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


        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))



        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        cursor.execute("SELECT DISTINCT назва FROM ЕКСКУРСІЯ ORDER BY назва ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))


        entry_excursion = ttk.Combobox(root, values=options_email, state="readonly")
        entry_excursion.set("Choice Excursion")

        root.update()



        options_agency = []

        cursor.execute("SELECT DISTINCT назва FROM АГЕНТСТВО ORDER BY назва ASC")

        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_agency.append(str(name[0]))

        entry_agency = ttk.Combobox(root, values=options_agency, state="readonly")
        entry_agency.set("Choice Agency")

        entries = [
            entry_email, entry_password, entry_excursion, entry_agency
        ]

        root.update()

        for i, entry in enumerate(entries,start=1):
            entry.place(x=10 + root.winfo_width() / 2,
                         y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: excursion_and_tourist(action, table_name, root, name_db, entries))
        send_button.place(x=10,
                          y=helper_height + (len(labels) + 1) * empty_height + ((len(labels) + 1) - 1) * labels[
                              0].winfo_height())
        root.update()

    if (str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete")) and str(table_name).lower().replace(' ', '') == str(
            "сonductinganexcursion"):
        hints = ["Email", "Password", "Name excursion", "Agency"]

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

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        options_email = []

        query = """SELECT DISTINCT турист_id FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ"""
        cursor.execute(query)
        results = cursor.fetchall()


        if results:

            for result in results:

                query = """SELECT людина_id FROM ТУРИСТ Where id = ?"""
                cursor.execute(query, (str(result[0]),))
                results1 = cursor.fetchall()

                # results = [str(result) for result in results]
                # results = [
                #     str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ', '')
                #     for result in results]
                # results = [str(result).split() for result in results]

                for result1 in results1:

                    query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                    cursor.execute(query, (str(result1[0]),))
                    user = cursor.fetchall()
                    # user = [
                    #     str(result).replace(')', '').replace('(', '').replace(',', '').replace("'", '').replace('  ',
                    #                                                                                             '') for
                    #     result in user]
                    for result2 in user:

                    #     user = [str(result[0]) for result in user]
                    # # user = user[0].split()
                        options_email.append(str(result2[4]))


      #  options_email = list(set(options_email))

        options_email = sorted(options_email)
        root.update()
        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

        cursor.execute("SELECT DISTINCT назва FROM ЕКСКУРСІЯ ORDER BY назва ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        entry_excursion = ttk.Combobox(root, values=options_email, state="readonly")
        entry_excursion.set("Choice Excursion")

        root.update()

        options_agency = []

        cursor.execute("SELECT DISTINCT назва FROM АГЕНТСТВО ORDER BY назва ASC")

        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_agency.append(str(name[0]))

        entry_agency = ttk.Combobox(root, values=options_agency, state="readonly")
        entry_agency.set("Choice Agency")

        entries = [
            entry_email, entry_password, entry_excursion, entry_agency
        ]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10 + root.winfo_width() / 2,
                        y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: excursion_and_tourist(action, table_name, root, name_db, entries))
        send_button.place(x=10,
                          y=helper_height + (len(labels) + 1) * empty_height + ((len(labels) + 1) - 1) * labels[
                              0].winfo_height())
        root.update()

    if str(action).lower().replace(' ', '') == str("add") and str(table_name).lower().replace(' ', '') == str(
            "financialreport"):
        hints = ["Email", "Password", "Start date and time (YYYY-MM-DD HH:MM)",
                 "End date and time (YYYY-MM-DD HH:MM)", "Profit "]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))

        conn.close()

        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)

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
            entry_email, entry_password,
            start_date_entry, start_hour_spinbox, start_minute_spinbox,
            end_date_entry, end_hour_spinbox, end_minute_spinbox,
            entry_price
        ]

        root.update()

        entries[0].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())

        root.update()

        entries[1].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        entries[2].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[3].place(x=20 + root.winfo_width() / 2 + entries[2].winfo_width(),
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())


        root.update()

        entries[4].place(x=30 + root.winfo_width() / 2 + entries[3].winfo_width() + entries[2].winfo_width(),
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[5].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        entries[6].place(x=20 + root.winfo_width() / 2 + entries[5].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        entries[7].place(x=30 + root.winfo_width() / 2 + entries[5].winfo_width() + entries[6].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        entries[8].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 5 * empty_height + (5 - 1) * labels[0].winfo_height())

        root.update()

        send_button = tk.Button(root, text=action,
                                command=lambda: financialreport(action, table_name, root, name_db, entries))
        send_button.place(x=10,
                          y=helper_height + (len(labels) + 1) * empty_height + ((len(labels) + 1) - 1) * labels[
                              0].winfo_height())
        root.update()

    if(str(action).lower().replace(' ', '') == str("edit") or str(action).lower().replace(' ', '') == str(
            "delete"))  and str(table_name).lower().replace(' ', '') == str(
            "financialreport"):
        hints = ["Email", "Password", "Start date and time (YYYY-MM-DD HH:MM)",
                 "End date and time (YYYY-MM-DD HH:MM)"]

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

        root.update()

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM ЛЮДИНА ORDER BY email ASC")

        options_email = []
        names = cursor.fetchall()

        if names is not None:
            for name in names:
                options_email.append(str(name[0]))


        options_email = []

        query = """SELECT DISTINCT людина_id FROM ФІНАНСОВИЙ_ЗВІТ"""
        cursor.execute(query)
        results = cursor.fetchall()


        if results:
            for result in results:
                query = """SELECT * FROM ЛЮДИНА Where id = ?"""
                cursor.execute(query, (str(result[0]),))
                temps = cursor.fetchone()
                if temps:
                    options_email.append(str(temps[4]))

        root.update()
        entry_email = ttk.Combobox(root, values=options_email, state="readonly")
        entry_email.set("Choice Email")
        entry_password = tk.Entry(root)


        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        start_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        start_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")
        end_hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=2, format="%02.0f", wrap=True)
        end_minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=2, format="%02.0f", wrap=True)

        root.update()

        entries = [
            entry_email, entry_password,
            start_date_entry, start_hour_spinbox, start_minute_spinbox,
            end_date_entry, end_hour_spinbox, end_minute_spinbox,
        ]

        root.update()

        entries[0].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())

        root.update()

        entries[1].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        entries[2].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[3].place(x=20 + root.winfo_width() / 2 + entries[2].winfo_width(),
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[4].place(x=30 + root.winfo_width() / 2 + entries[3].winfo_width() + entries[2].winfo_width(),
                         y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())

        root.update()

        entries[5].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        entries[6].place(x=20 + root.winfo_width() / 2 + entries[5].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()

        entries[7].place(x=30 + root.winfo_width() / 2 + entries[5].winfo_width() + entries[6].winfo_width(),
                         y=helper_height + 4 * empty_height + (4 - 1) * labels[0].winfo_height())

        root.update()


        send_button = tk.Button(root, text=action,
                                command=lambda: financialreport(action, table_name, root, name_db, entries))
        send_button.place(x=10,
                          y=helper_height + (len(labels) + 1) * empty_height + ((len(labels) + 1) - 1) * labels[
                              0].winfo_height())
        root.update()


def actions(action, root, name_db):
    root.title(action)
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: admin_menu(root,name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    hints = ["Agency", "Excursion", "Person", "Parent (only for the kid)","Hotel","Hotel's number","Financial report","Passport","Tourist","Visa","Hotel accommodation","Cargo","Flight","Сonducting an excursion"]

    buttons = []

    for i in range(0, len(hints)):
        buttons.append(tk.Button(root, text=hints[i], command=lambda j=i + 1: table(action,hints[j - 1], root, name_db)))

    root.update()

    for button in buttons:
        button.place(x=10, y=50)

    root.update()

    empty_height = root.winfo_height() - 20 - button_back.winfo_height()

    for button in buttons:
        empty_height -= button.winfo_height()

    empty_height /= (len(buttons) + 2)

    helper_height = 20 + button_back.winfo_height()

    root.update()

    for i, button in enumerate(buttons, start=1):
        button.place(x=(root.winfo_width() - button.winfo_width()) / 2,
                     y=helper_height + i * empty_height + (i - 1) * button.winfo_height())

    root.update()

def admin_menu(root,name_db):
    from src.model.administrator import administrator

    root.title("Admin menu")
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: administrator(root, name_db))
    root.update()
    button_back.place(x=10,y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    hints = ["Add","Edit","Delete"]


    buttons = []

    for i in range(0,len(hints)):
        buttons.append(tk.Button(root, text=hints[i], command=lambda j=i+1: actions(hints[j-1],root,name_db)))

    root.update()

    for button in buttons:
        button.place(x=10, y=50)

    root.update()

    empty_height = root.winfo_height() - 20 - button_back.winfo_height()

    for button in buttons:
        empty_height -= button.winfo_height()

    empty_height /= (len(buttons) + 2)

    helper_height = 20 + button_back.winfo_height()

    root.update()

    for i, button in enumerate(buttons, start=1):
        button.place(x=(root.winfo_width()-button.winfo_width())/2, y=helper_height + i * empty_height + (i - 1) * button.winfo_height())

    root.update()
   # button_add_person = tk.Button(root, text="Add person", command=lambda: add_person(root, name_db))



