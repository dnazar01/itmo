import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import asyncio
from pizza import PepperoniPizza, BBQPizza, SeafoodPizza
from order import Order


class PizzaOrderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PizzaModel OrderModel")
        self.root.geometry("400x300")
        self.order = Order()

        self.create_widgets()

    async def run(self):
        self.root.mainloop()

    def create_widgets(self):
        self.menu_label = tk.Label(self.root, text="Выберите пиццу:")
        self.menu_label.grid(row=0, column=0, padx=10, pady=5)

        self.pizza_var = tk.StringVar()
        self.pizza_combobox = ttk.Combobox(self.root, textvariable=self.pizza_var, state="readonly")
        self.pizza_combobox["values"] = ["Пепперони", "Барбекю", "Дары моря"]
        self.pizza_combobox.grid(row=0, column=1, padx=10, pady=5)

        self.quantity_label = tk.Label(self.root, text="Количество:")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=5)

        self.quantity_spinbox = tk.Spinbox(self.root, from_=1, to=10)
        self.quantity_spinbox.grid(row=1, column=1, padx=10, pady=5)

        self.add_button = tk.Button(self.root, text="Добавить в заказ", command=self.add_to_order)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.confirm_button = tk.Button(self.root, text="Текущий заказ", command=self.confirm_order)
        self.confirm_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.exit_button = tk.Button(self.root, text="Выход", command=self.root.quit)
        self.exit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def add_to_order(self):
        pizza_choice = self.pizza_var.get()
        quantity = int(self.quantity_spinbox.get())
        if quantity > 3:
            messagebox.showinfo("Ошибка", f"Больше 3 {pizza_choice} нельзя заказать")
        else:
            if pizza_choice == "Пепперони":
                self.order.add_pizza(PepperoniPizza, quantity)
            elif pizza_choice == "Барбекю":
                self.order.add_pizza(BBQPizza, quantity)
            elif pizza_choice == "Дары моря":
                self.order.add_pizza(SeafoodPizza, quantity)
            messagebox.showinfo("Успех", f"{quantity} пицц(ы) {pizza_choice} добавлены в заказ.")

    def confirm_order(self):
        if self.order.get_pizzas():
            # Создаем новое окно для подтверждения заказа
            self.confirm_window = tk.Toplevel(self.root)
            self.confirm_window.title("Подтверждение заказа")

            # Создаем метку для отображения заказанных пицц
            order_label = tk.Label(self.confirm_window, text="Ваш заказ:")
            order_label.pack()

            # Получаем список пицц в заказе и отображаем их на метке
            pizzas = self.order.get_pizzas()
            for pizza in pizzas:
                pizza_label = tk.Label(self.confirm_window, text=f"- {pizza.name}")
                pizza_label.pack()

            # Создаем метку для отображения общей стоимости заказа
            total_cost_label = tk.Label(self.confirm_window,
                                        text=f"Общая стоимость заказа: {self.order.calculate_total()} рублей")
            total_cost_label.pack()

            # Создаем кнопку для подтверждения заказа
            confirm_button = tk.Button(self.confirm_window, text="Подтвердить", command=self.confirmation)
            confirm_button.pack()
            # Создаем кнопку для подтверждения заказа
            decline_button = tk.Button(self.confirm_window, text="Отклонить", command=self.decline)
            decline_button.pack()
        else:
            messagebox.showwarning("Предупреждение", "Вы еще не добавили ни одной пиццы в заказ.")

    def confirmation(self):
        self.order.save()
        self.confirm_window.destroy()

    def decline(self):
        self.order.clear()
        self.confirm_window.destroy()


async def main():
    gui = PizzaOrderGUI()
    await gui.run()


if __name__ == "__main__":
    asyncio.run(main())
