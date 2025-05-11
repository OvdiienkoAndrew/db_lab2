import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk

from tkcalendar import DateEntry


def financialreport_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    try:
       if (float(values[0] ))<0:
        messagebox.showinfo("x", "The costs is wrong!")
        root.deiconify()
        return
    except Exception:
        messagebox.showinfo("x", "The costs is wrong!")
        root.deiconify()
        return

    try:
        if (float(values[1])) < 0:
            messagebox.showinfo("x", "The profit is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "The profit is wrong!")
        root.deiconify()
        return


    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ФІНАНСОВИЙ_ЗВІТ 
        SET "витрати" = ?, "доходи" = ?, "прибуток" = ?
        WHERE id = ?
    """, (round(float(values[0]),2), round(float(values[1]),2), round(float(round(float(values[1]),2)-round(float(values[0]),2)),2),ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this Order!")

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def financialreport(action, table_name,root, name_db, entries):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]
    print(values)


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



        values[2] = str(values[2]).replace('/', '.')
        start_date_str = f"{values[2]} {values[3]}:{values[4]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M")

        values[5] = str(values[5]).replace('/', '.')
        end_date_str = f"{values[5]} {values[6]}:{values[7]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M")


        if start_date > end_date:
            messagebox.showinfo("x", "Start date is later than end date!")
            root.deiconify()
            return

        cursor.execute("""SELECT * FROM ФІНАНСОВИЙ_ЗВІТ WHERE людина_id = ? AND дата_час_початку = ? AND дата_час_кінця = ?""", (this_person[0],start_date,end_date, ))

        if cursor.fetchone():
            messagebox.showinfo("x", "I bag your pardon. I know this Report!")
            root.deiconify()
            return

        try:
            
            if float(values[8]) != float(str(values[8])):
                messagebox.showinfo("x", "The profit is wrong!")
                root.deiconify()
                return
        except Exception:
            messagebox.showinfo("x", "The profit is wrong!")
            root.deiconify()
            return

        costs = 0

        cursor.execute("SELECT загальна_сума_в_грн FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ WHERE турист_id = ?", (this_tourist[0],))


        result = cursor.fetchall()

        if result:
            for results in result:
                costs += float(results[0])

        cursor.execute("SELECT загальна_сума_в_грн FROM РЕЙС WHERE турист_id = ?", (this_tourist[0],))

        result = cursor.fetchall()

        if result:
            for results in result:
                costs += float(results[0])

        cursor.execute("SELECT загальна_сума_в_грн FROM ВАНТАЖ WHERE турист_id = ?", (this_tourist[0],))

        result = cursor.fetchall()

        if result:
            for results in result:
                costs += float(results[0])

        cursor.execute("SELECT вартість_в_грн, кількість_днів  FROM ПРОЖИВАННЯ_У_ОТЕЛІ WHERE турист_id = ?", (this_tourist[0],))

        result = cursor.fetchall()

        if result:
            for results in result:
                costs += (float(results[0])*int(result[1]))

        costs = round(float(costs),2)


        cursor.execute("""
                INSERT INTO ФІНАНСОВИЙ_ЗВІТ ("людина_id", "дата_час_початку", "дата_час_кінця", "витрати", "доходи", "прибуток")
                VALUES (?, ?, ?,?, ?,?)
                """, (this_person[0], start_date, end_date, costs, round(float(values[8]),2), round(float(round(float(values[8]),2)-costs),2)))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new Report!")

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

        values[2] = str(values[2]).replace('/', '.')
        start_date_str = f"{values[2]} {values[3]}:{values[4]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M")

        values[5] = str(values[5]).replace('/', '.')
        end_date_str = f"{values[5]} {values[6]}:{values[7]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M")

        if start_date > end_date:
            messagebox.showinfo("x", "Start date is later than end date!")
            root.deiconify()
            return

        cursor.execute(
            """SELECT * FROM ФІНАНСОВИЙ_ЗВІТ WHERE людина_id = ? AND дата_час_початку = ? AND дата_час_кінця = ?""",
            (this_person[0], start_date, end_date,))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I bag your pardon. I don't know this Report!")
            root.deiconify()
            return

        this_order = [str(result) for result in results]

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

        ID = this_order[0]

        hints = [
                 f"The old costs: {this_order[4]}.\tThe new costs:",
                 f"The old profit: {this_order[5]}.\tThe new profit:"
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



        entry_costs = tk.Entry(root)
        entry_profit = tk.Entry(root)


        entries = [entry_costs, entry_profit]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10+root.winfo_width()/2, y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()



        send_button = tk.Button(root, text=action,
                                command=lambda: financialreport_edit(root, entries, name_db, ID))
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

        values[2] = str(values[2]).replace('/', '.')
        start_date_str = f"{values[2]} {values[3]}:{values[4]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M")

        values[5] = str(values[5]).replace('/', '.')
        end_date_str = f"{values[5]} {values[6]}:{values[7]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M")

        if start_date > end_date:
            messagebox.showinfo("x", "Start date is later than end date!")
            root.deiconify()
            return

        try:
            cursor.execute("""
                DELETE FROM ФІНАНСОВИЙ_ЗВІТ
                    WHERE людина_id = ?
                    AND дата_час_початку = ?
                    AND дата_час_кінця = ?
                """, (this_person[0], start_date, end_date))
        except Exception:
            messagebox.showinfo("x", "I don't know this order!")
            root.deiconify()
            return

        conn.commit()

        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass

        messagebox.showinfo("✓", "The order has been removed!")
        admin_menu(root, name_db)

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

