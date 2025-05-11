import tkinter as tk
import sqlite3
from tkinter import messagebox


def agency_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]


    values[0] = ''.join(filter(str.isdigit, values[0]))

    if len(values[0]) != 12:
        messagebox.showinfo("x", "Phone is wrong!")
        root.deiconify()
        return

    values[len(values) - 1] = values[len(values) - 1].replace(',', '.').replace('..', '.')
    try:

        if len(str(values[len(values) - 1]).replace(' ', '')) <= 0:
            messagebox.showinfo("x", "Rating is wrong [0;5]!")
            root.deiconify()
            return
        if not (0 <= float(values[len(values) - 1]) <= 5):
            messagebox.showinfo("x", "Rating is wrong [0;5]!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Rating is wrong [0;5]!")
        root.deiconify()
        return
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE АГЕНТСТВО 
        SET контакт = ?, рейтинг = ?
        WHERE id = ?
    """, (values[0], values[1],ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this Agency!")
    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def agency(action, table_name,root, entries, name_db):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add":

        if len(values[0])<=1:
            messagebox.showinfo("x", "Name is small(2 letters min)!")
            root.deiconify()
            conn.close()
            return

        if len(values[1]) < 8:
            messagebox.showinfo("x", "Address is small(8 letters min)!")
            root.deiconify()
            conn.close()
            return


        values[2] = ''.join(filter(str.isdigit, values[2]))

        if len(values[2]) != 12:
            messagebox.showinfo("x", "Phone is wrong!")
            root.deiconify()
            conn.close()
            return

        values[len(values) - 1] = values[len(values)-1].replace(',','.').replace('..','.')
        try:

            if len(str(values[len(values)-1]).replace(' ',''))<=0:
                messagebox.showinfo("x", "Rating is wrong [0;5]!")
                root.deiconify()
                conn.close()
                return
            if not (0<=float(values[len(values) - 1])<=5):
                messagebox.showinfo("x", "Rating is wrong [0;5]!")
                root.deiconify()
                conn.close()
                return
        except Exception:
            messagebox.showinfo("x", "Rating is wrong [0;5]!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
            SELECT 1 FROM АГЕНТСТВО 
            WHERE назва = ? AND адрес = ?
            LIMIT 1
        """, (values[0],values[1],))

        if cursor.fetchone():
            messagebox.showinfo("x", "I know this Agency!")
        else:
            cursor.execute("""
                INSERT INTO АГЕНТСТВО (назва, адрес, контакт, рейтинг) 
                VALUES (?, ?, ?, ?)
            """, values)
            conn.commit()
            messagebox.showinfo("✓", "I know the new Agency!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit":
        if len(values[0]) <= 2:
            messagebox.showinfo("x", "Name is small(3 letters min)!")
            root.deiconify()
            conn.close()
            return

        if len(values[1]) <= 8:
            messagebox.showinfo("x", "Address is small(8 letters min)!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
            SELECT * FROM АГЕНТСТВО 
            WHERE назва = ?
            AND
             адрес = ?
        """, (values[0],values[1],))

        row = cursor.fetchone()


        if row:
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

            hints = [str(value) for value in row]
            ID = hints[0]
            hints.pop(0)
            hints[0] = "Old name: "+hints[0]+".\tNew name:"
            hints[1] = "Old address: " + hints[1] + ".\tNew address:"
            hints[2] = "Old contact: " + hints[2] + ".\tNew contact:"
            hints[3] = "Old rating: " + hints[3] + ".\tNew rating:"
            hints.pop(0)
            hints.pop(0)

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
                                    command=lambda: agency_edit(root, entries, name_db,ID))
            send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
                0].winfo_height())
        else:

            messagebox.showinfo("x", "I don't know this Agency!")
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
        if len(values[0]) <= 2:
            messagebox.showinfo("x", "Name is small(3 letters min)!")
            root.deiconify()
            conn.close()
            return

        if len(values[1]) <= 8:
            messagebox.showinfo("x", "Address is small(8 letters min)!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
            SELECT * FROM АГЕНТСТВО
            WHERE назва = ? AND адрес=?
        """, (values[0],values[1]))

        if cursor.fetchone():
            cursor.execute("""
                DELETE FROM АГЕНТСТВО
                WHERE назва = ? AND адрес=?
            """, (values[0],values[1]))

            conn.commit()
            try:
                try:
                    root.deiconify()
                except Exception:
                    pass

                conn.close()
            except Exception:
                pass
            messagebox.showinfo("✓", "The agency has been removed!")
            admin_menu(root, name_db)

        else:
            messagebox.showinfo("x", "I don't know this agency!")



    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

