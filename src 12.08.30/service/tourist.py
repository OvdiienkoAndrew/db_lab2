import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk


def tourist_edit(root, entries, name_db, ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    if str(values[0]).lower().replace(' ', '') == "choicesex":
        messagebox.showinfo("x", "You didn't choice sex!")
        root.deiconify()
        return

    if str(values[1]).lower().replace(' ', '') == "choicecategory":
        messagebox.showinfo("x", "You didn't choice Category!")
        root.deiconify()
        return

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ТУРИСТ 
        SET "стать" = ?, "категорія" = ?
        WHERE id = ?
    """, (values[0], values[1],ID))
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


def tourist(action, table_name,root, entries, name_db):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add" and str(table_name).lower().replace(' ','') == "tourist":
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

        if cursor.fetchone():
            messagebox.showinfo("x", "I bag your pardon. I know this tourist!")
            root.deiconify()
            return

        if str(values[2]).lower().replace(' ','') == "choicesex":
            messagebox.showinfo("x", "You didn't choice sex!")
            root.deiconify()
            return

        if str(values[3]).lower().replace(' ', '') == "choicecategory":
            messagebox.showinfo("x", "You didn't choice Category!")
            root.deiconify()
            return

        cursor.execute("""
               INSERT INTO ТУРИСТ ("людина_id", "стать", "категорія") 
               VALUES (?, ?, ?)
               """, (this_person[0], values[2], values[3]))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new Tourist!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit" and str(table_name).lower().replace(' ', '') == "tourist":

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
               """, (values[0], values[1],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Person!")
            root.deiconify()
            return

        this_person = [str(result) for result in results]

        cursor.execute("""
                       SELECT * FROM ТУРИСТ 
                       WHERE "людина_id" = ?
                       """, (this_person[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Tourist!")
            root.deiconify()
            return

        this_tourist = [str(result) for result in results]

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


        ID = this_tourist[0]

        hints = [
                 f"Old sex: {this_tourist[2]}.\tNew sex:",
                 f"Old category: {this_tourist[3]}.\tNew category:"
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

        root.update()

        options_sex = ["Human", "Woman"]

        entry_sex = ttk.Combobox(root, values=options_sex, state="readonly")
        entry_sex.set("Choice Sex")

        options_category = ["Rest", "Cargo", "Kids"]

        entry_category = ttk.Combobox(root, values=options_category, state="readonly")
        entry_category.set("Choice Category")

        root.update()
        entries = [entry_sex, entry_category]

        root.update()

        for i, entry in enumerate(entries, start=1):
            entry.place(x=10 + root.winfo_width() / 2,
                        y=helper_height + i * empty_height + (i - 1) * labels[0].winfo_height())

        root.update()



        send_button = tk.Button(root, text=action,
                                command=lambda: tourist_edit(root, entries, name_db, ID))
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

    if str(action).lower().replace(' ', '') == "delete" and str(table_name).lower().replace(' ', '') == "tourist":
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
                SELECT * FROM ТУРИСТ 
                WHERE "людина_id" = ?
                """, (this_person[0],))

        if not results:
            messagebox.showinfo("x", "I don't know this Tourist!")
            root.deiconify()
            return


        cursor.execute("""
            DELETE FROM ТУРИСТ
                WHERE людина_id = ?
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

        messagebox.showinfo("✓", "The tourist has been removed!")
        admin_menu(root, name_db)

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

