import tkinter as tk
import sqlite3
from tkinter import messagebox

def person_edit(root, entries, name_db,ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    if len(values[0]) <= 2:
        messagebox.showinfo("x", "Surname is small(3 letters min)!")
        root.deiconify()
        return

    if len(values[1]) <= 2:
        messagebox.showinfo("x", "Name is small(3 letters min)!")
        root.deiconify()
        return

    if len(values[2]) <= 2:
        messagebox.showinfo("x", "Patronymic is small(3 letters min)!")
        root.deiconify()
        return

    if len(values[3].replace(' ', '')) > 0:
        try:

            values[3] = int(values[3].replace(' ', ''))

            if len(str(values[3])) != 12:
                messagebox.showinfo("x", "Phone is wrong!")
                root.deiconify()
                return

        except Exception:
            messagebox.showinfo("x", "Phone is wrong!")
            root.deiconify()
            return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ЛЮДИНА 
        SET "прізвище" = ?, "ім'я" = ?, "по-батьковi" = ?, "телефон" = ?
        WHERE id = ?
    """, (values[0], values[1], values[2],values[3],ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this Person!")
    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def person(action, table_name,root, entries, name_db):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add" and str(table_name).lower().replace(' ','') == "person":
        if len(values[0]) <= 2:
            messagebox.showinfo("x", "Surname is small(3 letters min)!")
            root.deiconify()
            return

        if len(values[1]) <= 2:
            messagebox.showinfo("x", "Name is small(3 letters min)!")
            root.deiconify()
            return

        if len(values[2]) <= 2:
            messagebox.showinfo("x", "Patronymic is small(3 letters min)!")
            root.deiconify()
            return

        if len(values[3]) <= 5 or '@' not in values[3]:
            messagebox.showinfo("x", "Email is wrong!")
            root.deiconify()
            return

        if len(values[4].replace(' ', '')) <= 7:
            messagebox.showinfo("x", "Password is small(8 arguments min)!")
            root.deiconify()
            return


        if len(values[5].replace(' ', '')) > 0:
            try:

                values[5] = int(values[5].replace(' ',''))

                if len(str(values[5])) != 12:
                    messagebox.showinfo("x", "Phone is wrong!")
                    root.deiconify()
                    return

            except Exception:
                messagebox.showinfo("x", "Phone is wrong!")
                root.deiconify()
                return



        cursor.execute("""
            SELECT * FROM ЛЮДИНА
            WHERE "email" = ?
        """, (values[3],))

        if cursor.fetchone():
            messagebox.showinfo("x", "I know this Person (email)!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
                INSERT INTO ЛЮДИНА ("прізвище", "ім'я", "по-батьковi", "email", "пароль", "телефон") 
                VALUES (?, ?, ?, ?,?,?)
            """, (values))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new Person!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit" and str(table_name).lower().replace(' ', '') == "person":

        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email is wrong!")
            root.deiconify()
            return

        if len(values[1].replace(' ', '')) <= 7:
            messagebox.showinfo("x", "Password is small(8 arguments min)!")
            root.deiconify()
            return

        cursor.execute("""SELECT * FROM ЛЮДИНА WHERE email = ? AND пароль = ?""",(values[0], values[1]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Person!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

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


        ID = this_person[0]

        hints = [f"Old surname: {this_person[1]}.\tNew surname:",
                 f"Old name: {this_person[2]}.\tNew name:",
                 f"Old patronymic: {this_person[3]}.\tNew patronymic:",
                 f"Old phone: {this_person[6]}.\tNew phone:"
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

        entries = []

        for i in range(len(labels)):
            entries.append(tk.Entry(root))

        for i, entry in enumerate(entries, start=1):
            entry.place(x=root.winfo_width() / 2 + 10,
                        y=helper_height + i * empty_height + (i - 1) * labels[i - 1].winfo_height(),
                        width=root.winfo_width() / 2 - 20)
            entry.insert(0, str(''))

        send_button = tk.Button(root, text=action,
                                command=lambda: person_edit(root, entries, name_db,ID))
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

    if str(action).lower().replace(' ', '') == "delete" and str(table_name).lower().replace(' ', '') == "person":
        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email is wrong!")
            root.deiconify()
            return

        if len(values[1].replace(' ', '')) <= 7:
            messagebox.showinfo("x", "Password is small(8 arguments min)!")
            root.deiconify()
            return

        cursor.execute("""
        SELECT * FROM ЛЮДИНА 
        WHERE "email" = ? AND "пароль" = ?
        """, (values[0],values[1],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Person!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]


        cursor.execute("""
            DELETE FROM ЛЮДИНА
                WHERE id = ?
            """, (this_person[0]))

        conn.commit()

        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass

        messagebox.showinfo("✓", "The person has been removed!")
        admin_menu(root, name_db)

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

