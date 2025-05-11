def user_menu(root, name_db, id):
    import ast
    import tkinter as tk
    import sqlite3
    from tkinter import messagebox, ttk, filedialog
    from tkcalendar import DateEntry
    from src.model.user import user

    labelse = []

    root.title("User menu")
    for widget in root.winfo_children():
       widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: user(root, name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ЛЮДИНА WHERE id = ?", (id,))
    this_people = cursor.fetchall()


    text = ""
    for name in this_people:
        text+= name[1] + " " +  name[2] + " " +  name[3]

    TEXT = tk.Label(root, text=text)
    root.update()
    labelse.append(TEXT)
    root.update()

    options = []
    cursor.execute("SELECT один_з_батькiв_id FROM БАТЬКІВСТВО WHERE дитина_id = ?", (id,))
    results = cursor.fetchall()
    if results:
        for result in results:
            options.append(str(result))

    options2 = []
    for option in options:
        option = str(option).replace('(','').replace(')','').replace(',','').replace(' ','')

        cursor.execute("SELECT * FROM ЛЮДИНА WHERE id = ?", (str(option),))
        results = cursor.fetchall()

        if results:
            for result in results:
                options2.append(f"{result[1]} {result[2]} {result[3]}")

    entry_email = ttk.Combobox(root, values=options2, state="readonly")
    entry_email.config(width=33)
    entry_email.set("Looks Guardian")
    root.update()
    labelse.append(entry_email)
    root.update()

    options = []
    cursor.execute("SELECT дитина_id FROM БАТЬКІВСТВО WHERE один_з_батькiв_id = ?", (id,))
    results = cursor.fetchall()
    if results:
        for result in results:
            options.append(str(result))

    options2 = []
    for option in options:
        option = str(option).replace('(', '').replace(')', '').replace(',', '').replace(' ', '')

        cursor.execute("SELECT * FROM ЛЮДИНА WHERE id = ?", (str(option),))
        results = cursor.fetchall()

        if results:
            for result in results:
                options2.append(f"{result[1]} {result[2]} {result[3]}")

    entry_email2 = ttk.Combobox(root, values=options2, state="readonly")
    entry_email2.config(width=33)
    entry_email2.set("Looks Kids")
    root.update()
    labelse.append(entry_email2)
    root.update()

    cursor.execute("SELECT * FROM ПАСПОРТ WHERE людина_id = ? LIMIT 1", (id,))
    results = cursor.fetchone()

    if results:
        label_date_time = tk.Label(root, text=f"The date and time of birthday: {results[2]}")
        label_date_time_end = tk.Label(root, text=f"The last date of legality: {results[3]}")
        root.update()
        label_date_time.place(x=10, y=10)
        label_date_time_end.place(x=10, y=10)
        root.update()
        label_date_time.place(x=10 + root.winfo_width()/2, y=100)
        root.update()
        label_date_time_end.place(x=10 + root.winfo_width()/2, y=150)
        root.update()
        from PIL import Image, ImageTk
        import io
        import tkinter as tk

        image_data = io.BytesIO(results[4])
        image = Image.open(image_data)

        image_resized = image.resize((400, 600))

        tk_image = ImageTk.PhotoImage(image_resized)

        label_image = tk.Label(root, image=tk_image)
        label_image.place(x=10 + root.winfo_width() // 2, y=200)

        label_image.image = tk_image
        root.update()

    cursor.execute("SELECT * FROM ТУРИСТ WHERE людина_id = ? LIMIT 1", (id,))
    results = cursor.fetchone()

    label_sex = tk.Label(root, text=f"The sex: {results[2]}")
    label_category= tk.Label(root, text=f"The category: {results[3]}")
    root.update()
    labelse.append(label_sex)
    labelse.append(label_category)
    root.update()

    turist_id = int(str(results[0]))

    cursor.execute("SELECT * FROM ФІНАНСОВИЙ_ЗВІТ WHERE людина_id = ? LIMIT 1", (id,))
    results = cursor.fetchone()
    if results:
        label_1= tk.Label(root, text=f"The start date and time: {results[2]}")
        label_2 = tk.Label(root, text=f"The start date and time: {results[3]}")
        label_3 = tk.Label(root, text=f"The total profit : {results[6]}")
        root.update()
        labelse.append(label_1)
        labelse.append(label_2)
        labelse.append(label_3)
        root.update()

    cursor.execute("SELECT * FROM ПРОЖИВАННЯ_У_ОТЕЛІ WHERE турист_id = ?", (turist_id,))
    results = cursor.fetchall()
    hotel_id = []
    if results:
        for result in results:
            result = [str(result1) for result1 in result]
            hotel_id.append(result[2])

    options = []

    for hotel_id1 in hotel_id:

        cursor.execute("SELECT * FROM ОТЕЛЬ WHERE id = ? LIMIT 1", (str(hotel_id1),))

        results = cursor.fetchone()
        if results:
            results = [str(result) for result in results]
            options.append(f"Name: {results[1]}, Address: {results[2]}")

    hotels = ttk.Combobox(root, values=options, state="readonly")
    hotels.config(width=33)
    hotels.set("Looks Hotels")

    root.update()
    labelse.append(hotels)
    root.update()

    cursor.execute("SELECT DISTINCT екскурсія_id, агентство_id FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ WHERE турист_id = ?", (str(turist_id),))
    results = cursor.fetchall()
    excursion_id = []
    agency_id = []

    if results:
        for result in results:
            result = [str(result1) for result1 in result]
            excursion_id.append(result[0])
            agency_id.append(result[1])
            #print(f"{result[2]} {result[3]}")

    options = []

    for i in range(0, len(excursion_id)):

        cursor.execute("SELECT * FROM ЕКСКУРСІЯ WHERE id = ? LIMIT 1", (str(excursion_id[i]),))
        results = cursor.fetchone()

        excursion1 = [str(result) for result in results]

        cursor.execute("SELECT * FROM АГЕНТСТВО WHERE id = ? LIMIT 1", (str(agency_id[i]),))
        results = cursor.fetchone()

        agency1 = [str(result) for result in results]


        options.append(f"Name (agency): {agency1[1]}, Address (agency): {agency1[2]}, Excursion: {excursion1[2]}")

    hotels = ttk.Combobox(root, values=options, state="readonly")
    hotels.config(width=50)
    hotels.set("Looks Excursions")

    root.update()
    labelse.append(hotels)
    root.update()

    i = 50
    for label in labelse:
        label.place(x=10,y=i+50)
        i+=50
    root.update()

    i = 50
    for label in labelse:
        label.place(x=10, y=i + 50)
        i += 50
    root.update()

    # TEXT.place(x=(root.winfo_width()/2 - TEXT.winfo_width() )/2, y=(root.winfo_height() - button_back.winfo_height() - 20 - TEXT.winfo_height())/2)



