import tkinter as tk
import sqlite3
from tkinter import messagebox

def hotel_edit(root, entries, name_db,ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    if len(values[0]) <= 7:
        messagebox.showinfo("x", "Address is small(8 letters min)!")
        root.deiconify()
        return

    try:

        if float(values[1]) < 0:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return

    except Exception:
        messagebox.showinfo("x", "Price is wrong!")
        root.deiconify()
        return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ОТЕЛЬ 
        SET "адрес" = ?, "вартість_в_грн"=?
        WHERE id = ?
    """, (values[0], values[1],ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this hotel!")
    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def hotel(action, table_name,root, entries, name_db):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add":
        if len(values[0]) <= 2:
            messagebox.showinfo("x", "Surname is small(3 letters min)!")
            root.deiconify()
            return

        if len(values[1]) <= 7:
            messagebox.showinfo("x", "Address is small(8 letters min)!")
            root.deiconify()
            return

        try:

            if float(values[2]) < 0:
                messagebox.showinfo("x", "Price is wrong!")
                root.deiconify()
                return

        except Exception:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return



        cursor.execute("""
            SELECT 1 FROM ОТЕЛЬ
            WHERE "назва" = ?
            LIMIT 1
        """, (values[0],))

        if cursor.fetchone():
            messagebox.showinfo("x", "I know this hotel!")
        else:
            cursor.execute("""
                INSERT INTO ОТЕЛЬ ("назва", "адрес", "вартість_в_грн") 
                VALUES (?, ?, ?)
            """, values)
            conn.commit()
            messagebox.showinfo("✓", "I knew the new hotel!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit":
        if len(values[0]) <= 2:
            messagebox.showinfo("x", "Name is small(3 letters min)!")
            root.deiconify()
            return

        cursor.execute("""
                SELECT * FROM ОТЕЛЬ
                WHERE "назва" = ?
                """, (values[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this hotel!")
            root.deiconify()
            conn.close()
            return

        this_hotel = [str(result) for result in results]


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


        ID = this_hotel[0]

        hints = [f"Old Address: {this_hotel[2]}.\nNew Address:",
                 f"Old Price: {this_hotel[3]}.\nNew Price:"]


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
                                command=lambda: hotel_edit(root, entries, name_db, ID))
        send_button.place(x=10, y=helper_height + (len(labels) + 1) * empty_height + (len(labels)) * labels[
            0].winfo_height())

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
            return

        cursor.execute("""
                SELECT * FROM ОТЕЛЬ
                WHERE "назва" = ?
                """, (values[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this hotel!")
            root.deiconify()
            conn.close()
            return


        cursor.execute("""
                DELETE FROM ОТЕЛЬ
                WHERE "назва" = ?
            """, (values[0],))
        messagebox.showinfo("✓", "The hotel has been removed!")

        conn.commit()
        try:
            try:
                root.deiconify()
            except Exception:
                pass

            conn.close()
        except Exception:
            pass

        return




    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

    return