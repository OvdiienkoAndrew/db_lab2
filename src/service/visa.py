import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk

from tkcalendar import DateEntry


def visa_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    import re

    values[0] = ''.join(re.findall(r'\d', values[0]))

    if len(values[0]) != 12:
        messagebox.showinfo("x", "Card number is wrong!")
        root.deiconify()
        return

    values[1] = str(values[1]).replace('/', '.')
    start_date_str = f"{values[1]} 00:00"
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d")

    values[2] = str(values[2]).replace('/', '.')
    end_date_str = f"{values[2]} 23:59"
    end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
    end_date = end_date.strftime("%Y-%m-%d")

    if start_date > end_date:
        messagebox.showinfo("x", "Start date is later than end date!")
        root.deiconify()
        return

    if str(values[3]).lower().replace(' ', '') == "choicestatus":
        messagebox.showinfo("x", "You didn't choice Status!")
        root.deiconify()
        return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE VISA 
        SET "номер_карти" = ?, "дата_видачі" = ?, "дата_кінця" = ?, "статус" = ?
        WHERE id = ?
    """, (values[0], start_date, end_date, values[3],ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this Tourist!")

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def visa(action, table_name,root, name_db, entries):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add" and str(table_name).lower().replace(' ','') == "visa":
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

        cursor.execute("""SELECT * FROM Visa WHERE турист_id = ?""", (this_tourist[0]))

        if cursor.fetchone():
            messagebox.showinfo("x", "I bag your pardon. I know this Visa!")
            root.deiconify()
            return

        import re

        values[2] = ''.join(re.findall(r'\d', values[2]))

        if len(values[2]) != 12:
            messagebox.showinfo("x", "Card number is wrong!")
            root.deiconify()
            return

        values[3] = str(values[3]).replace('/', '.')
        start_date_str = f"{values[3]} 00:00"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d")

        values[4] = str(values[4]).replace('/', '.')
        end_date_str = f"{values[4]} 23:59"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d")


        if start_date > end_date:
            messagebox.showinfo("x", "Start date is later than end date!")
            root.deiconify()
            return

        if str(values[5]).lower().replace(' ','') == "choicestatus":
            messagebox.showinfo("x", "You didn't choice status!")
            root.deiconify()
            return



        cursor.execute("""
                INSERT INTO Visa ("турист_id", "номер_карти", "дата_видачі", "дата_кінця", "статус")
                VALUES (?, ?, ?,?, ?)
                """, (this_tourist[0], values[2], start_date, end_date, values[5]))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new Visa!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit" and str(table_name).lower().replace(' ', '') == "visa":

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

        cursor.execute("""SELECT * FROM ТУРИСТ WHERE людина_id = ?""", (this_person[0]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this tourist!")
            root.deiconify()
            return

        this_tourist = [str(result) for result in results]

        cursor.execute("""SELECT * FROM Visa WHERE турист_id = ?""", (this_tourist[0]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this Visa!")
            root.deiconify()
            return

        this_visa = [str(result) for result in results]

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

        ID = this_visa[0]

        hints = [
                 f"Old card number: {this_visa[2]}.\tNew card number:",
                 f"Old start date: {this_visa[3]}.\tNew start date:",
                 f"Old end date: {this_visa[4]}.\tNew end date:",
                 f"Old status: {this_visa[5]}.\tNew status:"
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



        entry_card_number = tk.Entry(root)

        start_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="mm/dd/yyyy")
        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

        options_sex = ["Active", "Block"]

        entry_sex = ttk.Combobox(root, values=options_sex, state="readonly")
        entry_sex.set("Choice status")

        entries = [entry_card_number, start_date_entry, end_date_entry, entry_sex]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10+root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()



        send_button = tk.Button(root, text=action,
                                command=lambda: visa_edit(root, entries, name_db, ID))
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

    if str(action).lower().replace(' ', '') == "delete" and str(table_name).lower().replace(' ', '') == "visa":

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

        cursor.execute("""SELECT * FROM Visa WHERE турист_id = ?""", (this_tourist[0]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this Visa!")
            root.deiconify()
            return

        this_visa = [str(result) for result in results]

        cursor.execute("""
            DELETE FROM Visa
                WHERE id = ?
            """, (this_visa[0]))

        conn.commit()

        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass

        messagebox.showinfo("✓", "The visa has been removed!")
        admin_menu(root, name_db)

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

