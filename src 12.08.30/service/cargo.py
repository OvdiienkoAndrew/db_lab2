import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk

from tkcalendar import DateEntry


def cargo_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    if len(values[0].replace(' ', '')) <= 3:
        messagebox.showinfo("x", "Cargo type is small(4 arguments min)!")
        root.deiconify()
        return

    try:
        if int(values[1]) <= 0:
            messagebox.showinfo("x", "Number of luggage compartments is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Number of luggage compartments is wrong!")
        root.deiconify()
        return

    try:
        if float(values[2]) <= 0:
            messagebox.showinfo("x", "Weight in kg is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Weight in kg is wrong!")
        root.deiconify()
        return

    try:
        if float(values[3]) <= 0:
            messagebox.showinfo("x", "Price (one place) is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Price (one place) is wrong!")
        root.deiconify()
        return

    try:
        if float(values[4]) <= 0:
            messagebox.showinfo("x", "Insurance is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Insurance is wrong!")
        root.deiconify()
        return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ВАНТАЖ 
        SET "тип_вантажу" = ?, "кількість_місць" = ?, "вага_в_кг" = ?, "вартість_пакування_в_грн" = ?, "страховка_в_грн" = ?, "загальна_сума_в_грн" = ?
        WHERE id = ?
    """, (str(values[0]), round(float(values[1]),2), round(float(values[2]),2), round(float(values[3]),2), round(float(values[4]),2),  round(float(round(float(values[1]),2)*(round(float(values[3]),2)+round(float(values[4]),2))),2), ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this Cargo!")



    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def cargo(action, table_name,root, name_db, entries):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add" and str(table_name).lower().replace(' ','') == "cargo":
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

        if len(values[2].replace(' ', '')) <= 3:
            messagebox.showinfo("x", "Cargo type is small(4 arguments min)!")
            root.deiconify()
            return

        try:
            if int(values[3])<=0:
                messagebox.showinfo("x", "Number of luggage compartments is wrong!")
                root.deiconify()
                return
        except Exception:
            messagebox.showinfo("x", "Number of luggage compartments is wrong!")
            root.deiconify()
            return


        try:
            if float(values[4])<=0:
                messagebox.showinfo("x", "Weight in kg is wrong!")
                root.deiconify()
                return
        except Exception:
            messagebox.showinfo("x", "Weight in kg is wrong!")
            root.deiconify()
            return

        try:
            if float(values[5]) <= 0:
                messagebox.showinfo("x", "Price (one place) is wrong!")
                root.deiconify()
                return
        except Exception:
            messagebox.showinfo("x", "Price (one place) is wrong!")
            root.deiconify()
            return

        try:
            if float(values[6]) <= 0:
                messagebox.showinfo("x", "Insurance is wrong!")
                root.deiconify()
                return
        except Exception:
            messagebox.showinfo("x", "Insurance is wrong!")
            root.deiconify()
            return

        cursor.execute("SELECT 1 FROM ВАНТАЖ WHERE турист_id = ? LIMIT 1", (this_tourist[0],))


        if cursor.fetchone():
            conn.close()
            messagebox.showinfo("x", "I know this tourist with cargo!")
            root.deiconify()
            return

        cursor.execute("""
                INSERT INTO ВАНТАЖ ("турист_id", "тип_вантажу", "кількість_місць", "вага_в_кг", "вартість_пакування_в_грн", "страховка_в_грн", "загальна_сума_в_грн")
                VALUES (?, ?, ?,?, ?,?,?)
                """, (this_tourist[0], values[2], round(float(values[3]),2), round(float(values[4]),2), round(float(values[5]),2), round(float(values[6]),2), round(float((float(values[5]) + float(values[6]))* float(values[3])),2)))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new Cargo!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit" and str(table_name).lower().replace(' ', '') == "cargo":

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
            messagebox.showinfo("x", "Password is wrong!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]
        print(this_person)

        cursor.execute("""SELECT * FROM ТУРИСТ WHERE людина_id = ?""", (this_person[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this tourist!")
            root.deiconify()
            return

        this_tourist = [str(result) for result in results]
        print(this_tourist)

        cursor.execute("SELECT * FROM ВАНТАЖ WHERE турист_id = ? LIMIT 1", (this_tourist[0],))

        results = cursor.fetchone()

        if not results:
            conn.close()
            messagebox.showinfo("x", "I don't know this tourist with cargo!")
            root.deiconify()
            return

        this_cargo = [str(result) for result in results]
        print(this_cargo)

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

        ID = this_cargo[0]

        hints = [
                 f"The old cargo type: {this_cargo[2]}.\tThe new cargo type:",
                 f"The old number of luggage compartments: {this_cargo[3]}.\tThe new number of luggage compartments:",
                 f"The old weight in kg: {this_cargo[4]}.\tThe new weight in kg:",
                 f"The old price (one place): {this_cargo[5]}.\tThe new price (one place):",
                 f"The old insurance: {this_cargo[5]}.\tThe new pinsurance:"
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

        entries=[]

        for label in labels:
            entries.append(tk.Entry(root))



        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10+root.winfo_width()/2 + ((1/4)*root.winfo_width()), y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()



        send_button = tk.Button(root, text=action,
                                command=lambda: cargo_edit(root, entries, name_db, ID))
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

    if str(action).lower().replace(' ', '') == "delete" and str(table_name).lower().replace(' ', '') == "cargo":

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
            messagebox.showinfo("x", "Password is wrong!")
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

        cursor.execute("SELECT 1 FROM ВАНТАЖ WHERE турист_id = ? LIMIT 1", (this_tourist[0],))

        if cursor.fetchone() is None:
            conn.close()
            messagebox.showinfo("x", "I don't know this tourist with cargo!")
            root.deiconify()
            return

        query = "DELETE FROM ВАНТАЖ WHERE турист_id = ?"
        cursor.execute(query, (this_tourist[0],))
        conn.commit()

        messagebox.showinfo("✓", "The cargo has been removed!")
        admin_menu(root, name_db)


    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

