import sqlite3
import tkinter as tk
from tkinter import messagebox


class Transport:
    def __init__(self, id, name, payload_capacity, is_booked, length, width, height):
        self.id = id
        self.name = name
        self.payload_capacity = payload_capacity
        self.is_booked = is_booked
        self.length = length
        self.width = width
        self.height = height


class TransportManager:
    def __init__(self):
        self.connection = sqlite3.connect("transport.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS freight_transport
                            (id INTEGER PRIMARY KEY, name TEXT, payload_capacity REAL, 
                            is_booked INTEGER, length REAL, width REAL, height REAL)"""
        )
        self.connection.commit()

    def add_transport(self, name, payload_capacity, length, width, height):
        self.cursor.execute(
            "INSERT INTO freight_transport (name, payload_capacity, is_booked, length, width, height) "
            "VALUES (?, ?, 0, ?, ?, ?)",
            (name, payload_capacity, length, width, height),
        )
        self.connection.commit()
        messagebox.showinfo(
            title="Уведомление", message="Грузовой транспорт успешно добавлен."
        )

    def delete_transport(self, transport_id):
        self.cursor.execute("DELETE FROM freight_transport WHERE id=?", (transport_id,))
        if self.cursor.rowcount == 0:
            return messagebox.showerror(
                title="Ошибка", message="Транспорт с указанным id не найден"
            )
        else:
            self.connection.commit()
            messagebox.showinfo(
                title="Уведомление", message="Грузовой транспорт успешно удален."
            )

    def view_all_transport(self):
        self.cursor.execute("SELECT * FROM freight_transport")
        transports = self.cursor.fetchall()
        transport_info = ""
        for transport in transports:
            transport_info += (
                f"ID: {transport[0]}, Название: {transport[1]}, Грузоподъемность: {transport[2]}, Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]},"
                f"Забронирован: {'Да' if transport[3] else 'Нет'}\n"
            )
        messagebox.showinfo(title="Грузовой транспорт", message=transport_info)

    def view_transport_by_capacity(self, payload_capacity):
        self.cursor.execute(
            "SELECT * FROM freight_transport WHERE payload_capacity >= ?",
            (payload_capacity,),
        )
        transports = self.cursor.fetchall()
        transport_info = ""
        for transport in transports:
            transport_info += (
                f"ID: {transport[0]}, Название: {transport[1]}, Грузоподъемность: {transport[2]}, Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]},"
                f"Забронирован: {'Да' if transport[3] else 'Нет'}\n"
            )
        messagebox.showinfo(title="Грузовой транспорт", message=transport_info)

    def view_available_transport(self):
        self.cursor.execute("SELECT * FROM freight_transport WHERE is_booked=0")
        transports = self.cursor.fetchall()
        transport_info = ""
        for transport in transports:
            transport_info += f"ID: {transport[0]}, Название: {transport[1]}, Грузоподъемность: {transport[2]}, Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]}\n"
        messagebox.showinfo(
            title="Свободный грузовой транспорт", message=transport_info
        )

    def make_booking(self, transport_id):
        self.cursor.execute(
            "UPDATE freight_transport SET is_booked=text_file.txt WHERE id=?", (transport_id,)
        )
        if self.cursor.rowcount == 0:
            return messagebox.showerror(
                title="Ошибка", message="Транспорт с указанным id не найден"
            )
        else:
            self.connection.commit()
            messagebox.showinfo(
                title="Уведомление", message="Транспорт успешно забронирован."
            )

    def view_booked_transport(self):
        self.cursor.execute("SELECT * FROM freight_transport WHERE is_booked=text_file.txt")
        transports = self.cursor.fetchall()
        transport_info = ""
        for transport in transports:
            transport_info += f"ID: {transport[0]}, Название: {transport[1]}, Грузоподъемность: {transport[2]}, Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]}\n"
        messagebox.showinfo(
            title="Забронированный грузовой транспорт", message=transport_info
        )

    def view_transport_by_dimensions(self, payload_capacity, length, width, height):
        self.cursor.execute(
            "SELECT * FROM freight_transport WHERE payload_capacity >= ? "
            "AND length >= ? AND width >= ? AND height >= ? AND is_booked=0",
            (payload_capacity, length, width, height),
        )
        transports = self.cursor.fetchall()
        transport_info = ""
        for transport in transports:
            transport_info += (
                f"ID: {transport[0]}, Название: {transport[1]}, Грузоподъемность: {transport[2]}, "
                f"Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]}, "
                f"Забронирован: {'Да' if transport[3] else 'Нет'}\n"
            )
        messagebox.showinfo(title="Грузовой транспорт", message=transport_info)

    def close(self):
        self.cursor.close()
        self.connection.close()


class MakeWindow:
    def __init__(self):
        self.manager = TransportManager()
        self.window = tk.Tk()
        self.window.resizable(height=False, width=False)
        self.window.title("Учет грузового транспорта")
        self.window.geometry("600x400")
        self.window["bg"] = "#00ffff"
        self.create_buttons()

    def create_buttons(self):
        self.clear_page()
        add_button = tk.Button(
            self.window,
            text="Добавить транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.add_transport_view,
        )
        add_button.pack(pady=5)

        view_all_button = tk.Button(
            self.window,
            text="Показать весь транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.view_all_transport,
        )
        view_all_button.pack(pady=5)

        view_capacity_button = tk.Button(
            self.window,
            text="Просмотреть транспорт по грузоподъемности",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.check_capacity,
        )
        view_capacity_button.pack(pady=5)

        view_available_button = tk.Button(
            self.window,
            text="Просмотреть свободный транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.view_available_transport,
        )
        view_available_button.pack(pady=5)

        view_booked_button = tk.Button(
            self.window,
            text="Просмотреть забронированный транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.view_booked_transport,
        )
        view_booked_button.pack(pady=5)

        view_dimensions_button = tk.Button(
            self.window,
            text="Просмотреть подходящий по габаритам транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.view_transport_by_dimensions,
        )
        view_dimensions_button.pack(pady=5)

        book_button = tk.Button(
            self.window,
            text="Забронировать транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.transport_booking,
        )
        book_button.pack(pady=5)

        delete_button = tk.Button(
            self.window,
            text="Удалить транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.transport_delete,
        )
        delete_button.pack(pady=5)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def clear_page(self):
        # Удаление всех виджетов
        for widget in self.window.winfo_children():
            widget.destroy()

    def view_transport_by_dimensions(self):
        self.clear_page()
        tk.Label(
            self.window, text="Грузоподъемность:", font="Comfortaa 12", bg="#00ffff"
        ).pack(pady=3)
        self.capacity_entry = tk.Entry(self.window, font="Comfortaa 12", bg="#DCDCDC")
        self.capacity_entry.pack(pady=3)

        tk.Label(self.window, text="Длина:", font="Comfortaa 12", bg="#00ffff").pack(
            pady=3
        )
        self.length_entry = tk.Entry(self.window, font="Comfortaa 12", bg="#DCDCDC")
        self.length_entry.pack(pady=3)

        tk.Label(self.window, text="Ширина:", font="Comfortaa 12", bg="#00ffff").pack(
            pady=3
        )
        self.width_entry = tk.Entry(self.window, font="Comfortaa 12", bg="#DCDCDC")
        self.width_entry.pack(pady=3)

        tk.Label(self.window, text="Высота:", font="Comfortaa 12", bg="#00ffff").pack(
            pady=3
        )
        self.height_entry = tk.Entry(self.window, font="Comfortaa 12", bg="#DCDCDC")
        self.height_entry.pack(pady=3)

        view_button = tk.Button(
            self.window,
            text="Подобрать транспорт",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.view_transport,
        )
        view_button.pack(pady=3)

        main_menu = tk.Button(
            self.window,
            text="Главное меню",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.create_buttons,
        )
        main_menu.pack(pady=3)

    def view_transport(self):
        capacity_str = self.capacity_entry.get()
        length_str = self.length_entry.get()
        width_str = self.width_entry.get()
        height_str = self.height_entry.get()

        if capacity_str and length_str and width_str and height_str:
            try:
                capacity = float(capacity_str)
                length = float(length_str)
                width = float(width_str)
                height = float(height_str)
                self.manager.view_transport_by_dimensions(
                    capacity, length, width, height
                )
            except ValueError:
                messagebox.showerror(
                    title="Ошибка",
                    message="Некорректные значения грузоподъемности или габаритов.",
                )
        else:
            messagebox.showerror(
                title="Ошибка", message="Введите значения грузоподъемности и габаритов."
            )

    def check_capacity(self):
        self.clear_page()
        tk.Label(
            self.window, text="Грузоподъемность:", font="Comfortaa 12", bg="#00ffff"
        ).pack(pady=3)
        self.capacity_entry = tk.Entry(self.window, font="Comfortaa 12", bg="#DCDCDC")
        self.capacity_entry.pack(pady=3)
        view_capacity_button = tk.Button(
            self.window,
            text="Просмотреть",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.view_transport_by_capacity,
        )
        view_capacity_button.pack(pady=3)
        add_button = tk.Button(
            self.window,
            text="Главное меню",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.create_buttons,
        )
        add_button.pack(pady=3)

    def transport_delete(self):
        self.clear_page()
        tk.Label(
            self.window,
            text="Введите ID транспорта:",
            font="Comfortaa 12",
            bg="#00ffff",
        ).pack(pady=3)
        self.delete_entry = tk.Entry(self.window, font="Comfortaa 12", bg="#DCDCDC")
        self.delete_entry.pack(pady=3)

        delete_button = tk.Button(
            self.window,
            text="Удалить",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.delete_transport,
        )
        delete_button.pack(pady=3)
        add_button = tk.Button(
            self.window,
            text="Главное меню",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.create_buttons,
        )
        add_button.pack(pady=3)

    def transport_booking(self):
        self.clear_page()
        tk.Label(
            self.window,
            text="Введите ID транспорта:",
            font="Comfortaa 12",
            bg="#00ffff",
        ).pack(pady=3)
        self.booking_entry = tk.Entry(self.window, font="Comfortaa 12", bg="#DCDCDC")
        self.booking_entry.pack(pady=3)
        book_button = tk.Button(
            self.window,
            text="Забронировать",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.make_booking,
        )
        book_button.pack(pady=3)
        add_button = tk.Button(
            self.window,
            text="Главное меню",
            font="Comfortaa 12",
            bg="#00ffff",
            command=self.create_buttons,
        )
        add_button.pack(pady=3)

    def check_entry(self, entry):
        value = entry.get()
        if not value:
            return False
        try:
            value = int(value)
            if value < 0:
                messagebox.showerror("Ошибка", "Значение не может быть отрицательным")
                return False
            elif value > 10:
                messagebox.showerror("Ошибка", "Значение не может быть больше 10")
                return False
            else:
                return True
        except ValueError:
            messagebox.showerror("Ошибка", "Значение должно быть числом")
            return False

    def add_transport_view(self):
        self.clear_page()
        tk.Label(self.window, text="Название:", bg="#00ffff", font="Comfortaa 12").pack(
            pady=3
        )
        self.name_entry = tk.Entry(self.window, bg="#DCDCDC")
        self.name_entry.pack(pady=3)

        tk.Label(
            self.window, text="Грузоподъемность:", bg="#00ffff", font="Comfortaa 12"
        ).pack(pady=3)
        self.capacity_entry = tk.Entry(self.window, bg="#DCDCDC")
        self.capacity_entry.pack(pady=3)

        tk.Label(self.window, text="Длина:", bg="#00ffff", font="Comfortaa 12").pack(
            pady=3
        )
        self.length_entry = tk.Entry(self.window, bg="#DCDCDC")
        self.length_entry.pack(pady=3)

        tk.Label(self.window, text="Ширина:", bg="#00ffff", font="Comfortaa 12").pack(
            pady=3
        )
        self.width_entry = tk.Entry(self.window, bg="#DCDCDC")
        self.width_entry.pack(pady=3)

        tk.Label(self.window, text="Высота:", bg="#00ffff", font="Comfortaa 12").pack(
            pady=3
        )
        self.height_entry = tk.Entry(self.window, bg="#DCDCDC")
        self.height_entry.pack(pady=3)

        add_button = tk.Button(
            self.window,
            font="Comfortaa 12",
            text="Добавить",
            bg="#00ffff",
            command=self.add_transport,
        )
        add_button.pack(pady=3)
        add_button = tk.Button(
            self.window, text="Главное меню", bg="#00ffff", command=self.create_buttons
        )
        add_button.pack(pady=3)

    def check_add_capacity(self):
        capacity_str = self.capacity_entry.get()
        if capacity_str:
            try:
                capacity = float(capacity_str)
                self.manager.view_transport_by_capacity(capacity)
            except ValueError:
                messagebox.showerror(
                    title="Ошибка", message="Некорректное значение грузоподъемности."
                )

    def on_closing(self):
        if messagebox.askokcancel(title="Выход", message="Вы точно хотите выйти?"):
            self.manager.close()
            self.window.destroy()

    def add_transport(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror(
                title="Ошибка", message="Поле 'Название' не может быть пустым"
            )
            return
        try:
            capacity = float(self.capacity_entry.get())
        except ValueError:
            messagebox.showerror(
                title="Ошибка",
                message="Некорректное значение в поле 'Грузоподъемность'",
            )
            return
        try:
            length = float(self.length_entry.get())
        except ValueError:
            messagebox.showerror(
                title="Ошибка", message="Некорректное значение в поле 'Длина'"
            )
            return
        try:
            width = float(self.width_entry.get())
        except ValueError:
            messagebox.showerror(
                title="Ошибка", message="Некорректное значение в поле 'Ширина'"
            )
            return
        try:
            height = float(self.height_entry.get())
        except ValueError:
            messagebox.showerror(
                title="Ошибка", message="Некорректное значение в поле 'Высота'"
            )
            return

        self.manager.add_transport(name, capacity, length, width, height)
        self.name_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.length_entry.delete(0, tk.END)
        self.width_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)

    def delete_transport(self):
        transport_id_str = self.delete_entry.get()
        if transport_id_str:
            try:
                transport_id = int(transport_id_str)
                self.manager.delete_transport(transport_id)
                self.delete_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror(
                    title="Ошибка", message="Некорректный идентификатор транспорта."
                )
        else:
            messagebox.showerror(
                title="Ошибка", message="Введите идентификатор транспорта."
            )

    def view_all_transport(self):
        self.manager.view_all_transport()

    def view_transport_by_capacity(self):
        capacity_str = self.capacity_entry.get()
        if capacity_str:
            try:
                capacity = float(capacity_str)
                self.manager.view_transport_by_capacity(capacity)
            except ValueError:
                messagebox.showerror(
                    title="Ошибка", message="Некорректное значение грузоподъемности."
                )
        else:
            messagebox.showerror(
                title="Ошибка", message="Введите значение грузоподъемности."
            )

    def view_available_transport(self):
        self.manager.view_available_transport()

    def view_booked_transport(self):
        self.manager.view_booked_transport()

    def make_booking(self):
        transport_id_str = self.booking_entry.get()
        if transport_id_str:
            try:
                transport_id = int(transport_id_str)
                self.manager.make_booking(transport_id)
                self.booking_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror(
                    title="Ошибка", message="Некорректный идентификатор транспорта."
                )
        else:
            messagebox.showerror(
                title="Ошибка", message="Введите идентификатор транспорта."
            )

    def close(self):
        self.manager.close()
        self.window.destroy()


if __name__ == "__main__":
    gui = MakeWindow()
    gui.create_buttons()
    tk.mainloop()
