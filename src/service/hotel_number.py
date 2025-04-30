import tkinter as tk
import sqlite3
from tkinter import messagebox

def hotel_number_edit(root, entries, name_db,ID):

    from src.menu.admin_menu import admin_menu
    values = [str(entry.get().strip()) for entry in entries]

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    try:
        if int(values[0]) <= 0:
            messagebox.showinfo("x", "Max amount is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Max amount is wrong!")
        root.deiconify()
        return


    try:
        if round(float(values[1]),2) < 0:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            return
    except Exception:
        messagebox.showinfo("x", "Price is wrong!")
        root.deiconify()
        return


    cursor.execute("""
        UPDATE НОМЕР_У_ОТЕЛІ 
        SET "максимальна_кількість" = ?, "вартість_в_грн"=?
        WHERE id = ?
    """, (values[0], values[1],ID))
    conn.commit()
    messagebox.showinfo("✓", "I updated this number in hotel!")
    try:
        try:
            root.deiconify()
        except Exception:
            pass

        conn.close()
    except Exception:
        pass
    admin_menu(root,name_db)


def hotel_number(action, table_name,root, entries, name_db):
    from src.menu.admin_menu import admin_menu
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    root.withdraw()

    values = [str(entry.get().strip()) for entry in entries]


    if str(action).lower().replace(' ','') == "add":
        if len(values[0]) <= 2:
            messagebox.showinfo("x", "Name hotel is small(3 letters min)!")
            root.deiconify()
            return

        cursor.execute("""
                   SELECT * FROM ОТЕЛЬ
                   WHERE "назва" = ?
                   LIMIT 1
               """, (values[0],))

        results =  cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this hotel!")
            root.deiconify()
            conn.close()
            return

        this_hotel = [str(result) for result in results]


        try:

            if int(values[1]) <= 0:
                messagebox.showinfo("x", "Number room is wrong!")
                root.deiconify()
                conn.close()
                return

        except Exception:
            messagebox.showinfo("x", "Number room is wrong!")
            root.deiconify()
            conn.close()
            return

        try:

            if int(values[2]) <= 0:
                messagebox.showinfo("x", "Max amount is wrong!")
                root.deiconify()
                conn.close()
                return

        except Exception:
            messagebox.showinfo("x", "Max amount is wrong!")
            root.deiconify()
            conn.close()
            return

        try:

            if int(values[3]) < 0:
                messagebox.showinfo("x", "Price is wrong!")
                root.deiconify()
                conn.close()
                return

        except Exception:
            messagebox.showinfo("x", "Price is wrong!")
            root.deiconify()
            conn.close()
            return


        print(f"{this_hotel[0]}\t{values[1]}")
        cursor.execute("""
            SELECT * FROM НОМЕР_У_ОТЕЛІ
            WHERE "отель_id" = ?
            AND "номер_кімнати" = ?
            LIMIT 1
        """, (this_hotel[0], values[1],))

        if cursor.fetchone():
            messagebox.showinfo("x", "I know this hotel and number connection!")
            root.deiconify()
            conn.close()
            return

        cursor.execute("""
                INSERT INTO НОМЕР_У_ОТЕЛІ ("отель_id", "номер_кімнати", "максимальна_кількість", "вартість_в_грн") 
                VALUES (?, ?, ?, ?)
            """, (this_hotel[0], values[1], values[2], values[3]))
        conn.commit()
        messagebox.showinfo("✓", "I knew the new connection in the room and the hotel!")

        root.deiconify()
        conn.close()
        return

    if str(action).lower().replace(' ', '') == "edit":

        if len(values[0]) <= 2:
            messagebox.showinfo("x", "Name hotel is small(3 letters min)!")
            root.deiconify()
            return

        cursor.execute("""
                          SELECT * FROM ОТЕЛЬ
                          WHERE "назва" = ?
                          LIMIT 1
                      """, (values[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this hotel!")
            root.deiconify()
            conn.close()
            return

        this_hotel = [str(result) for result in results]

        cursor.execute("""
        SELECT * FROM НОМЕР_У_ОТЕЛІ
        WHERE "отель_id" = ?
        AND "номер_кімнати" = ?
        LIMIT 1
         """, (this_hotel[0],values[1]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this number in hotel!")
            root.deiconify()
            conn.close()
            return

        this_hotel_number = [str(result) for result in results]
        

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


        ID = this_hotel_number[0]

        hints = [f"Old Max amount: {this_hotel_number[3]}.\nNew Max amount:",
                 f"Old Price: {this_hotel_number[4]}.\nNew Price:"]


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
                                command=lambda: hotel_number_edit(root, entries, name_db, ID))
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
            messagebox.showinfo("x", "Name hotel is small(3 letters min)!")
            root.deiconify()
            return

        cursor.execute("""
                          SELECT * FROM ОТЕЛЬ
                          WHERE "назва" = ?
                          LIMIT 1
                      """, (values[0],))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this hotel!")
            root.deiconify()
            conn.close()
            return

        this_hotel = [str(result) for result in results]


        try:
            if int(values[1]) <0:
                messagebox.showinfo("x", "Hotel number is wrong!")
                root.deiconify()
                conn.close()
                return
        except Exception:
            messagebox.showinfo("x", "Hotel number is wrong!")
            root.deiconify()
            conn.close()
            return


        cursor.execute("""
        SELECT * FROM НОМЕР_У_ОТЕЛІ
        WHERE "отель_id" = ?
        AND "номер_кімнати" = ?
        LIMIT 1
         """, (this_hotel[0],values[1]))

        results = cursor.fetchone()

        if not results:
            messagebox.showinfo("x", "I don't know this number in hotel!")
            root.deiconify()
            conn.close()
            return

        this_hotel_number = [str(result) for result in results]
        

        cursor.execute("""
                DELETE FROM НОМЕР_У_ОТЕЛІ
                WHERE "отель_id" = ?
                AND "номер_кімнати" = ?
            """, (this_hotel[0],this_hotel_number[2]))
        messagebox.showinfo("✓", "The number in hotel has been removed!")

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