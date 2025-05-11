import ast
import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry




def request(index,root, name_db):
    from src.requests.request_person_list import request_person_list
    from src.requests.request_hotel_list import request_hotel_list
    from src.requests.request_number_of_tourists_list import request_number_of_tourists_list
    from src.requests.request_person_info_list import request_person_info_list
    from src.requests.request_hotel_number_list import request_hotel_number_list
    from src.requests.excursion_with_tourist_list import excursion_with_tourist_list
    from src.requests.popular_excursions_list import popular_excursions_list
    from src.requests.flight_list import flight_list
    from src.requests.financial_report import financial_report
    from src.requests.cargo_report import cargo_report
    from src.requests.full_finance_report import full_finance_report
    from src.requests.type_cargo import type_cargo
    from src.requests.profitability import profitability
    from src.requests.rest_plus_kids_divide_shop import rest_plus_kids_divide_shop
    from src.requests.from_fly import from_fly
    from src.requests.task1 import task1
    from src.requests.task2 import task2
    from src.requests.task3 import task3

    index = int(str(index))

    if index == 1:
        request_person_list(root, name_db)
    elif index == 2:
        request_hotel_list(root, name_db)
    elif index == 3:
        request_number_of_tourists_list(root, name_db)
    elif index == 4:
        request_person_info_list(root, name_db)
    elif index == 5:
        request_hotel_number_list(root, name_db)
    elif index == 6:
        excursion_with_tourist_list(root, name_db)
    elif index == 7:
        popular_excursions_list(root, name_db, "Popular Excursions list")
    elif index == 8:
        flight_list(root, name_db)
    elif index == 9:
        financial_report(root, name_db)
    elif index == 10:
        cargo_report(root, name_db)
    elif index == 11:
        full_finance_report(root, name_db)
    elif index == 12:
        type_cargo(root, name_db)
    elif index == 13:
        profitability(root, name_db)
    elif index == 14:
        rest_plus_kids_divide_shop(root, name_db)
    elif index == 15:
        from_fly(root, name_db)
    elif index == 16:
        task1(root, name_db)
    elif index == 17:
         task2(root, name_db)
    elif index == 18:
         task3(root, name_db)


def requests(root, name_db):
    from src.menu.admin_menu import admin_menu
    root.title("Requests")
    for widget in root.winfo_children():
        widget.destroy()

    button_back = tk.Button(root, text="Back", command=lambda: admin_menu(root,name_db))
    root.update()
    button_back.place(x=10, y=10)
    root.update()
    button_back.place(x=10, y=10)
    root.update()

    hints = ["Person list", "Hotel list", "Number of tourists list", "Person info", "Hotels number list",
             "Excursion with tourist list", "Popular Excursions list", "Flight list","Finance report",
             "Cargo report", "Full Finance report", "Type cargo",
             "Profitability", "(Rest+Kids)/Cargo", "From Fly",
             "How many tourists lived in each hotel and how many days in total",
             "The amount of baggage insurance for each tourist who has a flight",
             "Percentage of agency income from agency tours"]

    buttons = []

    for i in range(0, len(hints)):
        buttons.append(tk.Button(root, text=hints[i], command=lambda j=i + 1: request(j,root, name_db)))

    root.update()

    for button in buttons:
        button.place(x=10, y=50)

    root.update()

    empty_height = root.winfo_height()

    for button in buttons:
        empty_height -= button.winfo_height()

    empty_height /= (len(buttons) + 2)

    root.update()

    for i, button in enumerate(buttons, start=1):
        button.place(x=(root.winfo_width() - button.winfo_width()) / 2,
                     y=i * empty_height + (i - 1) * button.winfo_height())

    root.update()