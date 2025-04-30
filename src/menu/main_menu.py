import tkinter as tk


def main_menu(root,name_db):
    for widget in root.winfo_children():
        widget.destroy()

    from src.model.administrator import administrator
    from src.model.user import user

    administrator_menu = tk.Button(root, text="Administrator", command=lambda: administrator(root, name_db))
    user_menu = tk.Button(root, text="User", command=lambda: user(root, name_db))

    root.update()
    administrator_menu.place(x=0, y=0)
    user_menu.place(x=0, y=0)
    root.update()

    empty_height = (root.winfo_height()-administrator_menu.winfo_height()-user_menu.winfo_height())/3

    administrator_menu.place(x=(root.winfo_width()-administrator_menu.winfo_width())/2, y=empty_height)
    user_menu.place(x=(root.winfo_width()-user_menu.winfo_width())/2, y=root.winfo_height()-empty_height-user_menu.winfo_height())
    root.update()


    root.mainloop()