import ast
import random
import sqlite3
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
from src.create_bd.database import create_db
from src.menu.main_menu import main_menu
import tkinter.font as tkFont


def fake_db(name_db, size):
    from faker import Faker
    fake = Faker('uk_UA')
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    data = []

    j = -1

    for i in range(size):
        j += 1

        if j >= size:
            break

        email = fake.email()
        cursor.execute("""
                  SELECT * FROM ЛЮДИНА
                  WHERE "email" = ?
              """, (str(email),))
        if cursor.fetchone():
            continue

        surname = fake.last_name()
        name = fake.first_name()
        patronymic = fake.middle_name()
        password = fake.password(length=8)
        phone = ''.join([str(fake.random_int(min=0, max=9)) for _ in range(12)])

        data.append((surname, name, patronymic, email, password, phone))


    cursor.executemany("""
    INSERT INTO ЛЮДИНА ("прізвище", "ім'я", "по-батьковi", "email", "пароль", "телефон") 
    VALUES (?, ?, ?, ?,?,?)
    """, data)

    conn.commit()


    data = []
    j = -1

    for i in range(size):
        j += 1

        if j >= size:
            break

        agency_name = fake.company()
        address = fake.address().replace("\n", ", ")


        cursor.execute("""
                         SELECT * FROM АГЕНТСТВО
                         WHERE "назва" = ? AND "адрес" = ?
                     """, (str(agency_name),str(address),))
        if cursor.fetchone():
            continue

        phone = ''.join([str(fake.random_int(min=0, max=9)) for _ in range(12)])
        rating = round(fake.random_number(digits=1) / 2, 2)

        data.append((agency_name, address, phone, rating))


    cursor.executemany("""
       INSERT INTO АГЕНТСТВО ("назва", "адрес", "контакт", "рейтинг") 
       VALUES (?, ?, ?, ?)
       """, data)

    conn.commit()

    cursor.execute("SELECT id FROM АГЕНТСТВО")
    agency_ids = cursor.fetchall()
    agency_ids = [str(agency[0]) for agency in agency_ids]

    data = []
    j = -1

    for i in range(size):
        j += 1

        if j >= size:
            break

        id = random.choice(agency_ids)
        name = fake.word()

        cursor.execute("""
                                SELECT * FROM ЕКСКУРСІЯ
                                WHERE "агентство_id" = ? AND "назва" = ?
                            """, (str(id), str(name),))
        if cursor.fetchone():
            continue

        agency_ids.remove(str(id))

        description = fake.text(max_nb_chars=200)
        start_time = fake.date_time_this_year()
        end_time = start_time + timedelta(hours=random.randint(1, 5))
        cost = random.uniform(100, 5000)

        data.append((str(id), str(name), str(description), str(start_time), str(end_time), round(float(cost),2)))

    cursor.executemany("""
          INSERT INTO ЕКСКУРСІЯ ("агентство_id", "назва", "опис", "дата_час_початку", "дата_час_кінця", "вартість_в_грн") 
          VALUES (?, ?, ?, ?, ?, ?)
          """, data)

    conn.commit()

    cursor.execute("SELECT id FROM ЛЮДИНА")
    person_ids = cursor.fetchall()
    person_ids = [str(person[0]) for person in person_ids]

    data = []

    for i in range(len(person_ids)):

        id = random.choice(person_ids)
        person_ids.remove(str(id))

        cursor.execute("""
        SELECT * FROM ТУРИСТ
        WHERE "людина_id" = ?
        """, (str(id),))

        if cursor.fetchone():
            continue

        if i % 2 == 0:
            sex = "Human"
        else:
            sex = "Woman"

        if i % 100<50:
            category = "Rest"
        else:
            if i % 50<25:
                category = "Cargo"
            else:
                category = "Kids"

        data.append((str(id), str(sex), str(category)))

    cursor.executemany("""
    INSERT INTO ТУРИСТ ("людина_id", "стать", "категорія") 
     VALUES (?, ?, ?)
     """, data)

    conn.commit()

    cursor.execute("SELECT id FROM ЛЮДИНА")
    person_ids = cursor.fetchall()
    person_ids = [str(person[0]) for person in person_ids]
    data = []
    for person_id in person_ids:
        cursor.execute("""
        SELECT категорія FROM ТУРИСТ
        WHERE "людина_id" = ?
        """, (str(person_id),))
        results = cursor.fetchall()
        results = [str(result[0]) for result in results]
        results = str(results[0])

        if results != "Kids":
            cursor.execute("""
                    SELECT * FROM ПАСПОРТ
                    WHERE "людина_id" = ?
                    """, (str(person_id),))
            if cursor.fetchone():
                continue

            id = str(person_id)

            today = datetime.today()
            eighteen_years_ago = today - timedelta(days=18 * 365)
            ninety_years_ago = today - timedelta(days=90 * 365)
            birth_date = fake.date_between_dates(
                date_start=ninety_years_ago.date(),
                date_end=eighteen_years_ago.date()
            )
            finish_date = fake.date_between_dates(
                date_start=ninety_years_ago.date(),
                date_end=eighteen_years_ago.date()
            )

            start_valid = datetime.strptime(str(birth_date), "%Y-%m-%d") + timedelta(days=14 * 365)

            finish_date = (start_valid + timedelta(days=fake.random_int(min=3650, max=7300))).date()

            data.append((str(id),str(birth_date),str(finish_date)))

    cursor.executemany("""
    INSERT INTO ПАСПОРТ ("людина_id", "дата_народження", "дійсний_до")
    VALUES (?, ?, ?)
    """, data)

    conn.commit()

    cursor.execute("SELECT id FROM ЛЮДИНА")
    person_ids = cursor.fetchall()
    person_ids = [str(person[0]) for person in person_ids]
    data = []
    for person_id in person_ids:
        cursor.execute("""
           SELECT категорія FROM ТУРИСТ
           WHERE "людина_id" = ?
           """, (str(person_id),))
        results = cursor.fetchall()
        results = [str(result[0]) for result in results]
        results = str(results[0])
        id = str(person_id)
        if results == "Kids":
            while True:
                person_id = random.choice(person_ids)
                cursor.execute("""
                           SELECT * FROM ТУРИСТ
                           WHERE "людина_id" = ?
                           """, (str(person_id),))
                results = cursor.fetchall()
                results = [str(result) for result in results]
                results = list(ast.literal_eval(results[0]))
                results = [str(result) for result in results]
                if results[len(results)-1] != "Kids":
                    cursor.execute("""
                              SELECT * FROM БАТЬКІВСТВО
                              WHERE "дитина_id" = ? AND "один_з_батькiв_id" = ?
                              """, (str(id),str(results[0]),))
                    if cursor.fetchall():
                        continue
                    data.append((str(id),str(results[0])))
                    break

    cursor.executemany("""
    INSERT INTO БАТЬКІВСТВО ("дитина_id", "один_з_батькiв_id")
     VALUES (?, ?)
     """, data)

    conn.commit()

    data = []

    j = -1

    for i in range(size):
        j += 1

        if j >= size:
            break

        name = fake.company() + " Hotel"
        address = fake.address().replace("\n", ", ")

        cursor.execute("""
                      SELECT * FROM ОТЕЛЬ
                      WHERE "назва" = ? AND "адрес" = ?
                  """, (str(name),str(address),))
        if cursor.fetchone():
            continue

        cost = random.uniform(100, 5000)

        data.append((str(name), str(address), round(float(cost),2)))

    cursor.executemany("""
        INSERT INTO ОТЕЛЬ ("назва", "адрес", "вартість_в_грн") 
        VALUES (?, ?, ?)
        """, data)

    conn.commit()


    cursor.execute("SELECT id FROM ОТЕЛЬ")
    hotel_ids = cursor.fetchall()
    hotel_ids = [str(result[0]) for result in hotel_ids]

    data = []

    for hotel_id in hotel_ids:
        for i in range(1,11):
            cursor.execute("""
            SELECT * FROM НОМЕР_У_ОТЕЛІ
            WHERE "отель_id" = ? AND "номер_кімнати" = ?
            """, (str(hotel_id), str(i),))

            if cursor.fetchone():
                continue


            max = int(random.uniform(1, 9))
            cost = round(float(random.uniform(100, 5000)),2)

            data.append((str(str(hotel_id)), str(i), str(max), str(cost)))

    cursor.executemany("""
             INSERT INTO НОМЕР_У_ОТЕЛІ ("отель_id", "номер_кімнати", "максимальна_кількість", "вартість_в_грн") 
             VALUES (?, ?, ?, ?)
             """, data)

    conn.commit()

    cursor.execute('SELECT id FROM "ТУРИСТ" WHERE "категорія" = ? OR "категорія" = ?', ('Rest', 'Cargo'))
    hotel_ids = cursor.fetchall()
    hotel_ids = [str(result[0]) for result in hotel_ids]
    data = []
    j = -1
    for hotel_id in hotel_ids:
        j+=1
        cursor.execute("""
                   SELECT * FROM VISA
                   WHERE "турист_id" = ?
                   """, (str(hotel_id),))
        if cursor.fetchone():
            continue

        card = ''.join([str(fake.random_int(min=1, max=9)) for _ in range(12)])
        today = datetime.today()
        eighteen_years_ago = today - timedelta(days=18 * 365)
        ninety_years_ago = today - timedelta(days=90 * 365)
        birth_date = fake.date_between_dates(
            date_start=ninety_years_ago.date(),
            date_end=eighteen_years_ago.date()
        )
        finish_date = fake.date_between_dates(
            date_start=ninety_years_ago.date(),
            date_end=eighteen_years_ago.date()
        )

        start_valid = datetime.strptime(str(birth_date), "%Y-%m-%d") + timedelta(days=14 * 365)

        finish_date = (start_valid + timedelta(days=fake.random_int(min=3650, max=7300))).date()

        if j % 2 == 0:
            status = "Active"
        else:
            status = "Block"

        data.append((str(hotel_id),str(card),str(birth_date),str(finish_date),str(status)))

    cursor.executemany("""
    INSERT INTO VISA ("турист_id", "номер_карти", "дата_видачі", "дата_кінця", "статус")
    VALUES (?, ?, ?, ?, ?)
    """, data)

    conn.commit()

    cursor.execute("SELECT id FROM ТУРИСТ")
    tourist_ids = cursor.fetchall()
    tourist_ids = [str(result[0]) for result in tourist_ids]

    cursor.execute("SELECT * FROM НОМЕР_У_ОТЕЛІ")
    hotels1 = cursor.fetchall()
    hotels1 = [str(result) for result in hotels1]
    hotels = []
    for hotel in hotels1:
        hotel = str(hotel).replace('(','').replace(')','').replace(',','').replace('  ','')
        hotels.append(hotel.split())

    data = []
    for tourist_id in tourist_ids:
        was = True
        while was is True:
            today = datetime.today()
            eighteen_years_ago = today - timedelta(days=1 * 365)
            ninety_years_ago = today - timedelta(days=90 * 365)
            birth_date = fake.date_between_dates(
                date_start=ninety_years_ago.date(),
                date_end=eighteen_years_ago.date()
            )
            finish_date = fake.date_between_dates(
                date_start=ninety_years_ago.date(),
                date_end=eighteen_years_ago.date()
            )

            start_valid = datetime.strptime(str(birth_date), "%Y-%m-%d") + timedelta(days=14 * 365)

            finish_date = (start_valid + timedelta(days=fake.random_int(min=3650, max=7300))).date()

            id = random.randint(0, len(hotels)-1)

            cursor.execute("""
                              SELECT * FROM ПРОЖИВАННЯ_У_ОТЕЛІ
                              WHERE "турист_id" = ?
                              AND "отель_id" = ?
                              AND "номер_у_отелі_id" = ?
                              AND "дата_час_початку" = ?
                              AND "дата_час_кінця" = ?
                              """, (str(tourist_id), str(hotels[id][1]), str(hotels[id][0]),
                                    str(birth_date),
                                    str(finish_date),))
            if cursor.fetchone():
                continue


            data.append((str(tourist_id),str(hotels[id][1]), str(hotels[id][0]),
                         str(hotels[id][3]),str(birth_date),
                                    str(finish_date),
                         str(hotels[id][4]),
                         str(int(random.uniform(1, 14)))

                         ))

            was = False

    cursor.executemany("""
       INSERT INTO ПРОЖИВАННЯ_У_ОТЕЛІ ("турист_id",
       "отель_id",
       "номер_у_отелі_id",
       "максимальна_кількість_людей",
       "дата_час_початку",
       "дата_час_кінця",
       "вартість_в_грн",
       "кількість_днів")
       VALUES (?, ?, ?, ?, ?,?,?,?)
       """, data)

    conn.commit()

    cursor.execute('SELECT id FROM "ТУРИСТ" WHERE "категорія" = ?', ('Cargo',))
    tourist_ids = cursor.fetchall()
    tourist_ids = [str(result[0]) for result in tourist_ids]
    data = []

    for tourist_id in tourist_ids:

        cursor.execute("""
                     SELECT * FROM ВАНТАЖ
                     WHERE "турист_id" = ?
                     """, (str(tourist_id),))
        if cursor.fetchone():
            continue


        type = str(fake.mime_type())
        size_cargo = int(random.uniform(1, 14))
        kg = round(float(random.uniform(1, 120)),2)
        costs = round(float(random.uniform(200, 5000)),2)
        insurance = round(float(random.uniform(200, 5000)), 2)
        total =  (costs+insurance)*size_cargo

        data.append((str(tourist_id),
                     str(type),
                     str(size_cargo),
                     str(kg),
                     str(costs),
                     str(insurance),
                     str(total)))

    cursor.executemany("""
      INSERT INTO ВАНТАЖ ("турист_id",
      "тип_вантажу",
      "кількість_місць",
      "вага_в_кг",
      "вартість_пакування_в_грн",
      "страховка_в_грн",
      "загальна_сума_в_грн")
      VALUES (?, ?, ?, ?, ?,?,?)
      """, data)

    conn.commit()

    cursor.execute('SELECT id FROM ТУРИСТ')
    tourist_ids = cursor.fetchall()
    tourist_ids = [str(result[0]) for result in tourist_ids]
    data = []

    for tourist_id in tourist_ids:

        while True:

            name = fake.city_name() + "-" + fake.city_name()
            costs = round(float(random.uniform(200, 5000)),2)
            today = datetime.today()
            eighteen_years_ago = today - timedelta(days=18 * 365)
            ninety_years_ago = today - timedelta(days=90 * 365)


            birth_date = fake.date_between_dates(
                date_start=ninety_years_ago.date(),
                date_end=eighteen_years_ago.date()
            )


            start_valid = datetime.combine(birth_date, fake.time_object()) + timedelta(days=14 * 365)


            finish_date = start_valid + timedelta(hours=fake.random_int(min=8, max=24))

            start_str = start_valid.strftime("%Y-%m-%d %H:%M:%S")
            finish_str = finish_date.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                               SELECT * FROM РЕЙС
                               WHERE "турист_id" = ?
                               AND "номер" = ?
                               AND "дата_час_початку" = ?
                               AND "дата_час_кінця" = ?
                               """, (str(tourist_id),
                                     str(name),
                                     str(start_str),
                                     str(finish_str),))
            if cursor.fetchall():
                continue

            data.append((str(tourist_id),
                                     str(name),
                         str(start_str),
                         str(finish_str),str(costs),
                         ))
            break

    cursor.executemany("""
        INSERT INTO РЕЙС ("турист_id",
        "номер",
        "дата_час_початку",
        "дата_час_кінця",
        "загальна_сума_в_грн")
        VALUES (?, ?, ?, ?, ?)
        """, data)

    conn.commit()

    cursor.execute('SELECT id FROM "ТУРИСТ"')
    tourist_ids = cursor.fetchall()
    tourist_ids = [str(result[0]) for result in tourist_ids]

    cursor.execute('SELECT id, агентство_id, вартість_в_грн   FROM ЕКСКУРСІЯ')
    results = cursor.fetchall()
    results = [str(result) for result in results]
    excursion_ids = []

    data = []

    for result in results:
        result = str(result).replace('(','').replace(')','').replace(',','').replace('  ','')
        result = result.split()
        excursion_ids.append(result)

    for tourist_id in tourist_ids:
        while True:
            id = int(random.uniform(0, len(excursion_ids)-1))
            cursor.execute("""
                SELECT * FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ
                WHERE "турист_id" = ?
                AND "екскурсія_id" = ?
                AND "агентство_id" = ?
            """, (str(tourist_id),str(excursion_ids[id][0]),str(excursion_ids[id][1]),))
            if cursor.fetchall():
                continue
            data.append((str(tourist_id),str(excursion_ids[id][0]),str(excursion_ids[id][1]),str(excursion_ids[id][2])))
            break

    cursor.executemany("""
    INSERT INTO ПРОВЕДЕННЯ_ЕКСКУРСІЇ (
    "турист_id",
    "екскурсія_id",
    "агентство_id",
    "загальна_сума_в_грн")
    VALUES (?, ?, ?, ?)
    """, data)

    conn.commit()

    cursor.execute('SELECT id FROM ТУРИСТ')
    tourist_ids = cursor.fetchall()
    tourist_ids = [str(result[0]) for result in tourist_ids]
    data = []

    for tourist_id in tourist_ids:
        while True:
            today = datetime.today()
            eighteen_years_ago = today - timedelta(days=1 * 365)
            ninety_years_ago = today - timedelta(days=120 * 365)

            start_date = fake.date_between_dates(
                date_start=ninety_years_ago.date(),
                date_end=eighteen_years_ago.date()
            )

            start_valid = datetime.combine(start_date, fake.time_object()) + timedelta(days=14 * 365)

            finish_date = start_valid + timedelta(days=fake.random_int(min=5, max=25))

            cursor.execute("""
                SELECT SUM(вартість_в_грн) FROM ПРОЖИВАННЯ_У_ОТЕЛІ
                WHERE "турист_id" = ?
                AND "дата_час_кінця" >= ?
                AND "дата_час_початку" <= ?
            """, (str(tourist_id), str(start_date), str(finish_date)))

            result = cursor.fetchone()

            sum = 0

            if result[0] is not None:
                sum += float(result[0])

            cursor.execute("""
                           SELECT SUM(загальна_сума_в_грн) FROM РЕЙС
                           WHERE "турист_id" = ?
                           AND "дата_час_кінця" >= ?
                           AND "дата_час_початку" <= ?
                       """, (str(tourist_id), str(start_date), str(finish_date)))

            result = cursor.fetchone()

            if result[0] is not None:
                sum += float(result[0])

            cursor.execute("""
            SELECT SUM(загальна_сума_в_грн) FROM ВАНТАЖ
            WHERE "турист_id" = ?
            """, (str(tourist_id),))

            result = cursor.fetchone()

            if result[0] is not None:
                sum += float(result[0])

            cursor.execute("""
            SELECT екскурсія_id FROM ПРОВЕДЕННЯ_ЕКСКУРСІЇ
            WHERE "турист_id" = ?
            """, (str(tourist_id),))

            results = cursor.fetchall()
            temp_ids = []
            if results:
                results = [str(result) for result in results]
                for result in results:
                    result = str(result).replace('(','').replace(')','').replace(',','').replace(' ','')
                    temp_ids.append(result)

            for temp_id in temp_ids:
                cursor.execute("""
                SELECT SUM(вартість_в_грн) FROM ЕКСКУРСІЯ
                WHERE id = ?
                AND "дата_час_кінця" >= ?
                AND "дата_час_початку" <= ?
                """, (str(temp_id), str(start_date), str(finish_date)))

                result = cursor.fetchone()

                if result[0] is not None:
                    sum += float(result[0])



            cursor.execute("""
                      SELECT людина_id FROM ТУРИСТ
                      WHERE id = ?
                      """, (str(tourist_id),))
            result = cursor.fetchone()

            data.append((str(result[0]), str(start_date), str(finish_date), sum, 0, -sum))

            break

    cursor.executemany("""
           INSERT INTO ФІНАНСОВИЙ_ЗВІТ ("людина_id",
           "дата_час_початку",
           "дата_час_кінця",
           "витрати",
           "доходи",
           "прибуток")
           VALUES (?, ?, ?, ?, ?,?)
           """, data)

    conn.commit()

    conn.close()


if __name__ == "__main__":

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

   # fake_db(name_db, 1000)
    main_menu(root, name_db)




# pyinstaller --onefile --windowed --icon=resources/img/icon/icon.ico main.py