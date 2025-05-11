import tkinter as tk
import sqlite3
from tkinter import messagebox

def parents_edit(root, entries, name_db, ID):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    from src.menu.admin_menu import admin_menu

    values = [str(entry.get().strip()) for entry in entries]

    if len(values[0]) <= 5 or '@' not in values[0]:
        messagebox.showinfo("x", "Email (child) is wrong!")
        root.deiconify()
        return

    if len(values[1]) <= 5 or '@' not in values[0]:
        messagebox.showinfo("x", "Email (guardian) is wrong!")
        root.deiconify()
        return

    cursor.execute("""
               SELECT * FROM ЛЮДИНА
               WHERE "email" = ?
           """, (values[0],))

    results = cursor.fetchone()

    if not results:
        messagebox.showinfo("x", "I don't know this child!")
        root.deiconify()
        conn.close()
        return

    child = [str(result) for result in results]

    cursor.execute("""
                      SELECT * FROM ЛЮДИНА
                      WHERE "email" = ?
                  """, (values[1],))

    results = cursor.fetchone()

    if not results:
        messagebox.showinfo("x", "I don't know this guardian!")
        root.deiconify()
        conn.close()
        return

    guardian = [str(result) for result in results]

    if child == guardian:
        messagebox.showinfo("x", "It's one person!")
        root.deiconify()
        conn.close()
        return


    cursor.execute("""
        UPDATE БАТЬКІВСТВО 
        SET дитина_id = ?, один_з_батькiв_id = ?
        WHERE id = ?
    """, (child[0], guardian[0],ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this connection!")
    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def parents(action, table_name,root, entries, name_db):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add":

        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email (child) is wrong!")
            root.deiconify()
            return

        if len(values[1]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email (guardian) is wrong!")
            root.deiconify()
            return


        cursor.execute("""
            SELECT * FROM ЛЮДИНА
            WHERE "email" = ?
        """, (values[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this child!")
            root.deiconify()
            conn.close()
            return

        child = [str(result) for result in results]

        cursor.execute("""
                   SELECT * FROM ЛЮДИНА
                   WHERE "email" = ?
               """, (values[1],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this guardian!")
            root.deiconify()
            conn.close()
            return

        guardian = [str(result) for result in results]


        if child == guardian:
            messagebox.showinfo("x", "It's one person!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
        SELECT * FROM БАТЬКІВСТВО
        WHERE "дитина_id" = ? AND "один_з_батькiв_id" = ?
        """, (child[0], guardian[0],))

        results = cursor.fetchone()

        if results:
            messagebox.showinfo("x", "I know this connection!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
              SELECT * FROM БАТЬКІВСТВО
              WHERE "дитина_id" = ? AND "один_з_батькiв_id" = ?
              """, (guardian[0], child[0],))

        results = cursor.fetchone()

        if results:
            messagebox.showinfo("x", "I know this connection!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
            INSERT INTO БАТЬКІВСТВО (дитина_id, один_з_батькiв_id)
            VALUES (?, ?)
        """, (child[0], guardian[0]))
        conn.commit()

        messagebox.showinfo("x", "I knew the new connection!")
        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "delete":

        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email (child) is wrong!")
            root.deiconify()
            return

        if len(values[1]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email (guardian) is wrong!")
            root.deiconify()
            return

        cursor.execute("""
                   SELECT * FROM ЛЮДИНА
                   WHERE "email" = ?
               """, (values[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this child!")
            root.deiconify()
            conn.close()
            return

        child = [str(result) for result in results]

        cursor.execute("""
                          SELECT * FROM ЛЮДИНА
                          WHERE "email" = ?
                      """, (values[1],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this guardian!")
            root.deiconify()
            conn.close()
            return

        guardian = [str(result) for result in results]

        if child == guardian:
            messagebox.showinfo("x", "It's one person!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
               SELECT * FROM БАТЬКІВСТВО
               WHERE "дитина_id" = ? AND "один_з_батькiв_id" = ?
               """, (child[0], guardian[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this connection!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
        DELETE FROM БАТЬКІВСТВО
        WHERE "дитина_id" = ? AND "один_з_батькiв_id" = ?
        """, (child[0], guardian[0],))
        conn.commit()

        messagebox.showinfo("x", "The сonnection has been removed!")
        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit":

        if len(values[0]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email (child) is wrong!")
            root.deiconify()
            return

        if len(values[1]) <= 5 or '@' not in values[0]:
            messagebox.showinfo("x", "Email (guardian) is wrong!")
            root.deiconify()
            return

        cursor.execute("""
                   SELECT * FROM ЛЮДИНА
                   WHERE "email" = ?
               """, (values[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this child!")
            root.deiconify()
            conn.close()
            return

        child = [str(result) for result in results]

        cursor.execute("""
                          SELECT * FROM ЛЮДИНА
                          WHERE "email" = ?
                      """, (values[1],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this guardian!")
            root.deiconify()
            conn.close()
            return

        guardian = [str(result) for result in results]

        if child == guardian:
            messagebox.showinfo("x", "It's one person!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
               SELECT * FROM БАТЬКІВСТВО
               WHERE "дитина_id" = ? AND "один_з_батькiв_id" = ?
               """, (child[0], guardian[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this connection!")
            root.deiconify()
            conn.close()
            return

        this_parents = [str(result) for result in results]

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

        ID = this_parents[0]

        hints = [f"Old email (child): {child[4]}. New email (child):",
                 f"Old email (guardian): {guardian[4]}. New email (guardian):"]



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
                                command=lambda: parents_edit(root, entries, name_db, ID))
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

    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

