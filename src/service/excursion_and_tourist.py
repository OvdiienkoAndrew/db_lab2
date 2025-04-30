import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk

from tkcalendar import DateEntry


def excursion_and_tourist_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    try:
        if float(values[0]) < 0:
            messagebox.showinfo("x", "The Price is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "The Price is wrong!")
        root.deiconify()
        return

    cursor.execute("""
           UPDATE ПРОВЕДЕННЯ_ЕКСКУРСІЇ 
           SET "загальна_сума_в_грн" = ?
           WHERE id = ?
       """, (values[0], ID))
    conn.commit()

    messagebox.showinfo("✓", "I updated this accommodation!")

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def excursion_and_tourist(action, table_name,root, name_db, entries):
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

        cursor.execute("""SELECT * FROM ЕКСКУРСІЯ WHERE назва = ?""", (str(values[2]),))
        results = cursor.fetchall()
        for result in results:
            this_excursions = [str(result1) for result1 in result]
            cursor.execute("""SELECT * FROM АГЕНТСТВО WHERE id = ?""", (str(this_excursions[1]),))
            res = cursor.fetchone()
            if res:
                this_agency = [str(v) for v in res]

                cursor.execute("""SELECT 1 FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ WHERE турист_id = ? AND екскурсія_id = ? AND агентство_id = ?""",
                               (str(this_tourist[0]),str(this_excursions[0]),str(this_agency[0]),))

                if cursor.fetchone():
                    messagebox.showinfo("x", "I bag your pardon. I know this accommodation!")
                    root.deiconify()
                    return

                cursor.execute("""
                INSERT INTO ПРОВЕДЕННЯ_ЕКСКУРСІЇ ("турист_id", "екскурсія_id", "агентство_id", "загальна_сума_в_грн")
                VALUES (?, ?, ?,?)
                """, (str(this_tourist[0]),str(this_excursions[0]),str(this_agency[0]), round(float(str(this_excursions[6])),2)))
                conn.commit()
                messagebox.showinfo("✓", "I knew the new accommodation!")
                root.deiconify()
                conn.close()
                return

        messagebox.showinfo("x", "I bag your pardon. This agency doesn't pass this excursion!")
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

        cursor.execute("""SELECT * FROM ЕКСКУРСІЯ WHERE назва = ?""", (str(values[2]),))
        results = cursor.fetchall()

        was = False
        this_table = []
        for result in results:
            this_excursions = [str(result1) for result1 in result]
            cursor.execute("""SELECT * FROM АГЕНТСТВО WHERE id = ?""", (str(this_excursions[1]),))
            res = cursor.fetchone()
            if res:
                this_agency = [str(v) for v in res]

                cursor.execute(
                    """SELECT * FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ WHERE турист_id = ? AND екскурсія_id = ? AND агентство_id = ?""",
                    (str(this_tourist[0]), str(this_excursions[0]), str(this_agency[0]),))

                re = cursor.fetchone()

                if re:
                    was = True
                    this_table = [str(v) for v in re]


        if was is False:
            messagebox.showinfo("x", "I bag your pardon. I don't know this accommodation!")
            root.deiconify()
            return


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

        ID = this_table[0]

        hints = [
                 f"The old price: {this_table[4]}.\tThe new price:"
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

        entry_price = tk.Entry(root)

        entries = [entry_price]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10+root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()



        send_button = tk.Button(root, text=action,
                                command=lambda: excursion_and_tourist_edit(root, entries, name_db, ID))
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

        cursor.execute("""SELECT * FROM ЕКСКУРСІЯ WHERE назва = ?""", (str(values[2]),))
        results = cursor.fetchall()
        for result in results:
            this_excursions = [str(result1) for result1 in result]
            cursor.execute("""SELECT * FROM АГЕНТСТВО WHERE id = ?""", (str(this_excursions[1]),))
            res = cursor.fetchone()
            if res:
                this_agency = [str(v) for v in res]

                cursor.execute(
                    """SELECT * FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ WHERE турист_id = ? AND екскурсія_id = ? AND агентство_id = ?""",
                    (str(this_tourist[0]), str(this_excursions[0]), str(this_agency[0]),))

                re = cursor.fetchone()

                if re:
                    this_result = [str(v) for v in re]
                    cursor.execute("""
                    DELETE FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ
                    WHERE id = ?
                    """, (this_result[0]))
                    messagebox.showinfo("✓", "The accommodation has been removed!")
                    admin_menu(root, name_db)



        conn.commit()
        messagebox.showinfo("x", "I bag your pardon. I don't know this accommodation!")

        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass


    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

