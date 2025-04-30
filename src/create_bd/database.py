import sqlite3

def create_db(name):
    with sqlite3.connect(name) as db:
        cursor = db.cursor()

        АГЕНТСТВО = """
        CREATE TABLE IF NOT EXISTS АГЕНТСТВО (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "назва" TEXT NOT NULL, 
            "адрес" TEXT NOT NULL,
            "контакт" TEXT NOT NULL,
            "рейтинг" REAL NOT NULL CHECK(рейтинг BETWEEN 0 AND 5)
         )
        """

        ЕКСКУРСІЯ = """
        CREATE TABLE IF NOT EXISTS ЕКСКУРСІЯ (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "агентство_id" INTEGER NOT NULL,
            "назва" TEXT NOT NULL, 
            "опис" TEXT NOT NULL,
            "дата_час_початку" DATETIME NOT NULL,
            "дата_час_кінця" DATETIME NOT NULL,
            "вартість_в_грн" REAL NOT NULL CHECK("вартість_в_грн" >= 0),

            FOREIGN KEY ("агентство_id") REFERENCES АГЕНТСТВО (id) ON DELETE CASCADE
        )
        """

        ЛЮДИНА = """
        CREATE TABLE IF NOT EXISTS ЛЮДИНА (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "прізвище" TEXT NOT NULL, 
            "ім'я" TEXT NOT NULL,
            "по-батьковi" TEXT NOT NULL,
            "email" TEXT NOT NULL,
            "пароль" TEXT NOT NULL,
            "телефон" TEXT DEFAULT NULL
         )
        """

        БАТЬКІВСТВО = """
               CREATE TABLE IF NOT EXISTS БАТЬКІВСТВО (
                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   "дитина_id" INTEGER NOT NULL,
                   "один_з_батькiв_id" INTEGER NOT NULL,
                  
                   FOREIGN KEY ("дитина_id") REFERENCES ЛЮДИНА (id) ON DELETE CASCADE,
                   FOREIGN KEY ("один_з_батькiв_id") REFERENCES ЛЮДИНА (id) ON DELETE CASCADE
                )
               """

        ОТЕЛЬ = """
        CREATE TABLE IF NOT EXISTS ОТЕЛЬ (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "назва" TEXT NOT NULL, 
            "адрес" TEXT NOT NULL,
            "вартість_в_грн" REAL NOT NULL CHECK("вартість_в_грн" >= 0)
         )
        """

        НОМЕР_У_ОТЕЛІ = """
                CREATE TABLE IF NOT EXISTS НОМЕР_У_ОТЕЛІ (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    "отель_id" INTEGER NOT NULL,
                    "номер_кімнати" INTEGER NOT NULL CHECK("номер_кімнати" > 0), 
                    "максимальна_кількість" INTEGER NOT NULL CHECK("номер_кімнати" > 0), 
                    "вартість_в_грн" REAL NOT NULL CHECK("вартість_в_грн" >= 0),
                
                    FOREIGN KEY ("отель_id") REFERENCES ОТЕЛЬ (id) ON DELETE CASCADE
                 )
                """

        ФІНАНСОВИЙ_ЗВІТ  = """
                CREATE TABLE IF NOT EXISTS ФІНАНСОВИЙ_ЗВІТ (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    "людина_id" INTEGER NOT NULL,
                   
                    "дата_час_початку" DATETIME NOT NULL,
                    "дата_час_кінця" DATETIME NOT NULL,
                    
                    "витрати" REAL NOT NULL CHECK("витрати" >= 0),
                    "доходи" REAL NOT NULL CHECK("доходи" >= 0),
                    "прибуток" REAL NOT NULL,
                    
                    
                    FOREIGN KEY ("людина_id") REFERENCES ЛЮДИНА (id) ON DELETE CASCADE
                 )
                """

        ПАСПОРТ = """
                        CREATE TABLE IF NOT EXISTS ПАСПОРТ (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "людина_id" INTEGER NOT NULL,

                            "дата_народження" DATE NOT NULL,
                            "дійсний_до" DATE NOT NULL,

                            "фото" BLOB DEFAULT NULL,

                            FOREIGN KEY ("людина_id") REFERENCES ЛЮДИНА (id) ON DELETE CASCADE
                         )
                        """

        ТУРИСТ = """
                        CREATE TABLE IF NOT EXISTS ТУРИСТ (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "людина_id" INTEGER NOT NULL,

                            "стать" TEXT CHECK(стать IN ('Human','Woman')) NOT NULL,
                           
                           "категорія" TEXT CHECK(категорія IN ('Rest','Cargo','Kids')) NOT NULL,

                            FOREIGN KEY ("людина_id") REFERENCES ЛЮДИНА (id) ON DELETE CASCADE
                         )
                        """

        VISA =  """
                        CREATE TABLE IF NOT EXISTS VISA (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "турист_id" INTEGER NOT NULL,
                            "номер_карти" TEXT NOT NULL,

                           "дата_видачі" DATE NOT NULL,
                            "дата_кінця" DATE NOT NULL,
                           "статус" TEXT CHECK(статус IN ('Active','Block')) NOT NULL,

                            FOREIGN KEY ("турист_id") REFERENCES ТУРИСТ (id) ON DELETE CASCADE
                         )
                        """

        ПРОЖИВАННЯ_У_ОТЕЛІ = """
                              CREATE TABLE IF NOT EXISTS ПРОЖИВАННЯ_У_ОТЕЛІ (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  
                                  "турист_id" INTEGER NOT NULL,
                                  "отель_id" INTEGER NOT NULL,
                                  "номер_у_отелі_id" INTEGER NOT NULL,
                                  "максимальна_кількість_людей" INTEGER NOT NULL,
                                  "дата_час_початку" DATETIME NOT NULL,
                                  "дата_час_кінця" DATETIME NOT NULL,
                                  "вартість_в_грн" REAL NOT NULL,
                                  "кількість_днів" REAL NOT NULL,

                                  FOREIGN KEY ("турист_id") REFERENCES ТУРИСТ (id) ON DELETE CASCADE,
                                  FOREIGN KEY ("отель_id") REFERENCES ОТЕЛЬ (id) ON DELETE CASCADE,
                                  FOREIGN KEY ("номер_у_отелі_id") REFERENCES НОМЕР_У_ОТЕЛІ (id) ON DELETE CASCADE
                               )
                              """

        ВАНТАЖ = """
                                      CREATE TABLE IF NOT EXISTS ВАНТАЖ (
                                          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                          "турист_id" INTEGER NOT NULL,
                                          "тип_вантажу" TEXT NOT NULL,
                                          "кількість_місць" INTEGER NOT NULL,
                                          "вага_в_кг" REAL NOT NULL,
                                          "вартість_пакування_в_грн" REAL NOT NULL,
                                         "страховка_в_грн" REAL NOT NULL,
                                         "загальна_сума_в_грн" REAL NOT NULL,
                                          FOREIGN KEY ("турист_id") REFERENCES ТУРИСТ (id) ON DELETE CASCADE
                                          
                                       )
                                      """
        РЕЙС = """
                                      CREATE TABLE IF NOT EXISTS РЕЙС (
                                          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                          "турист_id" INTEGER NOT NULL,
                                          
                                          "номер" TEXT NOT NULL,
                                          "дата_час_початку" DATETIME NOT NULL,
                                          "дата_час_кінця" DATETIME NOT NULL,
                                          
                                          
                                          "загальна_сума_в_грн" REAL NOT NULL,
                                          FOREIGN KEY ("турист_id") REFERENCES ТУРИСТ (id) ON DELETE CASCADE
                                    )
                                      """

        ПРОВЕДЕННЯ_ЕКСКУРСІЇ = """
                                              CREATE TABLE IF NOT EXISTS ПРОВЕДЕННЯ_ЕКСКУРСІЇ (
                                                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                  "турист_id" INTEGER NOT NULL,
                                                  "екскурсія_id" INTEGER NOT NULL,
                                                  "агентство_id" INTEGER NOT NULL,
                                                  "загальна_сума_в_грн" REAL NOT NULL,
                                                  FOREIGN KEY ("турист_id") REFERENCES ТУРИСТ (id) ON DELETE CASCADE,
                                                  FOREIGN KEY ("агентство_id") REFERENCES АГЕНТСТВО (id) ON DELETE CASCADE,
                                                   FOREIGN KEY ("екскурсія_id") REFERENCES ЕКСКУРСІЯ (id) ON DELETE CASCADE
                                               )
                                              """

        АДМІНІСТРАТОР = """
        CREATE TABLE IF NOT EXISTS АДМІНІСТРАТОР (
         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         username TEXT NOT NULL,
         password TEXT NOT NULL)
        """

        cursor.execute(АГЕНТСТВО)
        cursor.execute(ЕКСКУРСІЯ)
        cursor.execute(ЛЮДИНА)
        cursor.execute(БАТЬКІВСТВО)
        cursor.execute(ОТЕЛЬ)
        cursor.execute(НОМЕР_У_ОТЕЛІ)
        cursor.execute(ФІНАНСОВИЙ_ЗВІТ)
        cursor.execute(ПАСПОРТ)
        cursor.execute(ТУРИСТ)
        cursor.execute(VISA)
        cursor.execute(ПРОЖИВАННЯ_У_ОТЕЛІ)
        cursor.execute(ВАНТАЖ)
        cursor.execute(РЕЙС)
        cursor.execute(ПРОВЕДЕННЯ_ЕКСКУРСІЇ)
        cursor.execute(АДМІНІСТРАТОР)

        db.commit()