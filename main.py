import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import ttk
from src.create_bd.database import create_db
from src.menu.main_menu import main_menu
import tkinter.font as tkFont

if __name__=="__main__":

    name_db = "src/resources/database/my.db"
    create_db(name_db)

    root = Tk()
    root.title("Туристична фірма")
    root.geometry("1500x900")
    root.option_add("*Font", tkFont.Font(family="Times New Roman", size=32))
    root.resizable(False, False)


    try:
        root.iconbitmap(r'src/resources/img/icon/icon.ico')
    except Exception:
       print("Didn't find icon.ico in folder \"src/resources/img/icon/icon.ico\"")

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    for i in range(100):
        cursor.execute("""
                  SELECT * FROM ЛЮДИНА
                  WHERE "email" = ?
              """, (f"email{int(100-i)}@gmail.com",))
        if cursor.fetchone():
            continue

        cursor.execute("""
                       INSERT INTO ЛЮДИНА ("прізвище", "ім'я", "по-батьковi", "email", "пароль", "телефон") 
                       VALUES (?, ?, ?, ?,?,?)
                   """, (f"Surname{i}",f"Name{i}", f"Pantronymic{i}", f"email{int(100-i)}@gmail.com", "12345678","380987654321" ))

    conn.commit()

    for i in range(1,101):
        cursor.execute("""
                     SELECT * FROM ТУРИСТ
                     WHERE "людина_id" = ?
                 """, (f"{i}",))
        if cursor.fetchone():
            continue

        cursor.execute("""
                          INSERT INTO ТУРИСТ ("людина_id", "стать", "категорія") 
                          VALUES (?, ?, ?)
                      """, (
        f"{i}", f"Human", f"Kids"))



    conn.commit()

    for i in range(1, 101):
        cursor.execute("""
                      SELECT * FROM ОТЕЛЬ
                      WHERE "назва" = ?
                  """, (f"name{i}",))
        if cursor.fetchone():
            continue

        cursor.execute("""
                           INSERT INTO ОТЕЛЬ ("назва", "адрес", "вартість_в_грн") 
                           VALUES (?, ?, ?)
                       """, (
            f"name{i}", f"address{i}", float(i*i)))


    conn.commit()

    for i in range(1, 11):
        for j in range(1, 11):
            cursor.execute("""
                             SELECT * FROM НОМЕР_У_ОТЕЛІ
                             WHERE "отель_id" = ? AND "номер_кімнати" = ?
                         """, (f"name{i}",int(j)))
            if cursor.fetchone():
                continue

            cursor.execute("""
                                  INSERT INTO НОМЕР_У_ОТЕЛІ ("отель_id", "номер_кімнати", "максимальна_кількість", "вартість_в_грн")
                                  VALUES (?, ?, ?, ?)
                              """, (
                i, j, int(j+10), float(i*j)))

    conn.commit()


    for i in range(1, 101):
            cursor.execute("""
                             SELECT * FROM ВАНТАЖ
                             WHERE "турист_id" = ? 
                         """, (str(i),))
            if cursor.fetchone():
                continue

            cursor.execute("""
                                  INSERT INTO ВАНТАЖ ("турист_id", "тип_вантажу", "кількість_місць", "вага_в_кг", "вартість_пакування_в_грн", "страховка_в_грн", "загальна_сума_в_грн")
                                  VALUES (?, ?, ?, ?,?,?,?)
                              """, (
                i,f"Cargo{i}",int(i*2+10), float(666), float(125), float(i*0.8), round((( float(125)+float(i*0.8))*int(i*2+10)),2)))

    conn.commit()

    for i in range(1, 101):
        cursor.execute("""
                                SELECT * FROM АГЕНТСТВО
                                WHERE "назва" = ? 
                            """, (f"Agency{i}",))
        if cursor.fetchone():
            continue

        cursor.execute("""
                                     INSERT INTO АГЕНТСТВО ("назва", "адрес", "контакт", "рейтинг")
                                     VALUES (?, ?, ?, ?)
                                 """, (
            f"Agency{i}", f"Adress{i}", "+380998765432", float(i%5)))

    conn.commit()

    start_date_str = "12/31/2025 14:30"


    start_date = datetime.strptime(start_date_str, "%m/%d/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")

    for i in range(1, 101):
        for j in range(1, 11):
            cursor.execute("""
                               SELECT * FROM ЕКСКУРСІЯ WHERE агентство_id = ? AND назва = ?
                           """, (i, f"Excursion{j}"))
            if cursor.fetchone():
                continue

            cursor.execute("""
                                    INSERT INTO ЕКСКУРСІЯ ("агентство_id", "назва", "опис", "дата_час_початку", "дата_час_кінця", "вартість_в_грн")
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (
                i, f"Excursion{j}","Description", start_date,start_date,float(j*i+10)))

    conn.commit()

    for i in range(1, 101):
        for j in range(1, 11):
            cursor.execute("""
                                  SELECT * FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ WHERE id = ? AND турист_id = ?
                              """, (i, f"Excursion{j}"))
            if cursor.fetchone():
                continue

            cursor.execute("""
                                       INSERT INTO ПРОВЕДЕННЯ_ЕКСКУРСІЇ ("турист_id", "екскурсія_id", "агентство_id", "загальна_сума_в_грн")
                                       VALUES (?, ?, ?, ?)
                                   """, (
                i, j, i, round(float(i*j+10),2)))

    conn.commit()

    conn.close()

    main_menu(root, name_db)

# pyinstaller --onefile --windowed --icon=resources/img/icon/icon.ico main.py