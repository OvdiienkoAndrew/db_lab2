import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox, filedialog
from PIL import Image
import io

def passport_edit(root, name_db, entries, ID):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]
    print(values)

    values[0] = str(values[0]).replace('/', '.')
    start_date_str = f"{values[0]} {values[1]}:{values[2]}"
    start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

    if len(values[3])>0:
        with open(values[3], "rb") as file:
            image_blob = file.read()

        query = """
                   UPDATE ПАСПОРТ
                   SET
                       "дійсний_до" = ?,
                       "фото" = ?
                   WHERE id = ?;
                   """
        cursor.execute(query, (start_date,image_blob, ID))
        conn.commit()
    else:
        query = """
           UPDATE ПАСПОРТ
           SET
               "дійсний_до" = ? 
           WHERE id = ?;
           """
        cursor.execute(query, (start_date, ID))
        conn.commit()


    messagebox.showinfo("✓", "I updated this Passport!")
    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def passport(action, table_name,root, entries, name_db):
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


        values[2] = str(values[2]).replace('/', '.')
        start_date_str = f"{values[2]} {values[4]}:{values[5]}"
        start_date = datetime.strptime(start_date_str, "%m.%d.%Y %H:%M")
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

        values[3] = str(values[3]).replace('/', '.')
        end_date_str = f"{values[3]} {values[6]}:{values[7]}"
        end_date = datetime.strptime(end_date_str, "%m.%d.%Y %H:%M")
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

        if start_date > end_date:
            messagebox.showinfo("x", "The birth date and time is later than end date and time!")
            root.deiconify()
            return

        image_path = values[8]
        img_bytes = None

        if image_path:
            with open(image_path, "rb") as file:
                img_bytes = file.read()


        cursor.execute("""
                SELECT * FROM ПАСПОРТ 
                WHERE "людина_id" = ?
                """, (this_person[0],))

        if cursor.fetchone():
            messagebox.showinfo("x", "I know this Passport!")
            root.deiconify()
            return

        cursor.execute("""
        INSERT INTO ПАСПОРТ ("людина_id", "дата_народження", "дійсний_до", "фото") 
        VALUES (?, ?, ?, ?)
        """, (this_person[0], start_date, end_date, img_bytes))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new Passport!")

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
                             SELECT * FROM ПАСПОРТ 
                             WHERE "людина_id" = ?
                             """, (this_person[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Passport!")
            root.deiconify()
            return

        this_passport = [str(result) for result in results]

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

        ID = this_passport[0]

        hints = [f"Old end time: {this_passport[3]}.\tNew end time:",
                 f"New photo (if empty - save old):"]

        labels = []

        labels.append(tk.Label(root, text=hints[0]))
        labels.append(tk.Label(root, text=hints[1]))

        root.update()

        for label in labels:
            label.place(x=10, y=50)

        root.update()

        empty_height = root.winfo_height() - 20 - button_back.winfo_height()

        for label in labels:
            empty_height -= label.winfo_height()

        empty_height /= (4)

        helper_height = 20 + button_back.winfo_height()

        for i, label in enumerate(labels, start=1):
            label.place(x=10, y=helper_height + i * empty_height + (i - 1) * label.winfo_height())

        root.update()
        from tkcalendar import DateEntry

        end_date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                   date_pattern="mm/dd/yyyy")

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

        entries = [end_date_entry, end_hour_spinbox, end_minute_spinbox, entry_image, button]

        j = 0

        entries[0].place(x=10 + root.winfo_width() / 2,
                             y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())

        root.update()

        entries[1].place(x=10 + root.winfo_width() / 2+10+entries[0].winfo_width(),
                         y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())
        root.update()

        entries[2].place(x=10 + root.winfo_width() / 2 + 10 + entries[0].winfo_width() + 10 +entries[1].winfo_width(),
                         y=helper_height + 1 * empty_height + (1 - 1) * labels[0].winfo_height())
        root.update()

        entries[3].place(x=10 + root.winfo_width() / 2,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height())

        root.update()

        entries[4].place(x=10 + root.winfo_width() / 2 + entries[3].winfo_width() +10,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height() - (entries[4].winfo_height()-entries[3].winfo_height())/2)

        root.update()

        entries[4].place(x=10 + root.winfo_width() / 2 + entries[3].winfo_width() + 10,
                         y=helper_height + 2 * empty_height + (2 - 1) * labels[0].winfo_height() - (
                                     entries[4].winfo_height() - entries[3].winfo_height()) / 2)

        root.update()
        entries.pop()

        send_button = tk.Button(root, text=action, command=lambda: passport_edit(root, name_db, entries, ID))
        send_button.place(x=10,
                          y=helper_height + 3 * empty_height + (3 - 1) * labels[0].winfo_height())
        root.update()

        root.deiconify()
        conn.close()
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
                      SELECT * FROM ПАСПОРТ 
                      WHERE "людина_id" = ?
                      """, (this_person[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this Passport!")
            root.deiconify()
            return

        cursor.execute("""
                    DELETE FROM ПАСПОРТ
                        WHERE "людина_id" = ?
                    """, (this_person[0]))

        conn.commit()

        root.deiconify()
        conn.close()

        messagebox.showinfo("✓", "The passport has been removed!")
        admin_menu(root, name_db)




    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass

