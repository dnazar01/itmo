import tkinter as tk
from tkinter import messagebox
import tkinter.colorchooser as colorchooser

font_large = ("Arial", 14)
font_small = ("Arial", 12)



def choose_rectangle_color():
    color = colorchooser.askcolor(title="Выберите цвет прямоугольника")
    if color[1]:  # Если цвет выбран
        rectangle_color.set(color[1])  # Установим выбранный цвет
        draw_centered_rectangle(float(entry1.get()), float(entry2.get()), outline_color=rectangle_color.get(),fill_color=rectangle_color.get())
        calculate()

def calculate(event=None):
    try:
        arg1 = float(entry1.get())
        arg2 = float(entry2.get())
        sum_label.config(text='Сложение:')
        div_label.config(text='Деление:')
        dif_label.config(text='Вычитание:')
        mult_label.config(text='Умножение:')
        perimeter_label.config(text='Периметр:')
        area_label.config(text='Площадь:')

        if choice.get() == "Калькулятор":
            if sum_checkbox_var.get():
                sum_label.config(text='Сложение: ' + str(round(arg1 + arg2, 2)))
            if difference_checkbox_var.get():
                dif_label.config(text='Вычитание: ' + str(round(arg1 - arg2, 2)))
            if division_checkbox_var.get():
                if arg2 == 0:
                    div_label.config(text="Деление: Ошибка!")
                else:
                    div_label.config(text='Деление: ' + str(round(arg1 / arg2, 2)))
            if multiplication_checkbox_var.get():
                mult_label.config(text='Умножение: ' + str(round(arg1 * arg2, 2)))
        else:
            if perimeter_checkbox_var.get():
                if arg1 >= 0 and arg2 >= 0:
                    perimeter_label.config(text='Периметр: ' + str(round((arg1 + arg2) * 2, 2)))
                    canvas.delete("rect")
                    draw_centered_rectangle(arg1, arg2, outline_color=rectangle_color.get(),fill_color=rectangle_color.get())  # Вызываем функцию для рисования прямоугольника с выбранным цветом
                else:
                    perimeter_label.config(text='Периметр: Ошибка!')
            if area_checkbox_var.get():
                if arg1 >= 0 and arg2 >= 0:
                    area_label.config(text='Площадь: ' + str(round(arg1 * arg2, 2)))
                    canvas.delete("rect")
                    draw_centered_rectangle(arg1, arg2, outline_color=rectangle_color.get(),fill_color=rectangle_color.get())  # Вызываем функцию для рисования прямоугольника с выбранным цветом
                else:
                    area_label.config(text='Площадь: Ошибка!')
    except Exception as e:
        pass

def update():
    calculate()

def draw_centered_rectangle(width, height, outline_color="black", fill_color="green"):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    rect_width = width * 10
    rect_height = height * 10
    x1 = (canvas_width - rect_width) / 2
    y1 = (canvas_height - rect_height) / 2
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color, tags="rect")

def show_help():
    messagebox.showinfo("Справка", "Графический калькулятор v1.3\nАвтор: Назар Данилов К3121")

def swap():
    temp = entry1.get()
    entry1.delete(0, tk.END)
    entry1.insert(0, entry2.get())
    entry2.delete(0, tk.END)
    entry2.insert(0, temp)

def clear():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    sum_label.config(text="")
    dif_label.config(text="")
    div_label.config(text="")
    mult_label.config(text="")
    perimeter_label.config(text="")
    area_label.config(text="")
    canvas.delete("rect")

def exit_app():
    root.destroy()

def show_calculator_options():
    sum_checkbox.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    difference_checkbox.grid(row=5, column=1, padx=5, pady=5, sticky="w")
    multiplication_checkbox.grid(row=6, column=0, padx=5, pady=5, sticky="w")
    division_checkbox.grid(row=6, column=1, padx=5, pady=5, sticky="w")

    area_checkbox.grid_forget()
    perimeter_checkbox.grid_forget()
    area_label.grid_forget()
    perimeter_label.grid_forget()
    sum_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    dif_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    div_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    mult_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    update()

def show_square_options():
    area_checkbox.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    perimeter_checkbox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    sum_checkbox.grid_forget()
    difference_checkbox.grid_forget()
    multiplication_checkbox.grid_forget()
    division_checkbox.grid_forget()
    area_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    perimeter_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    sum_label.grid_forget()
    dif_label.grid_forget()
    div_label.grid_forget()
    mult_label.grid_forget()
    update()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root = tk.Tk()
root.title('Графический калькулятор')
root.geometry('600x600')
root.resizable(False, False)

center_window(root)

button_frame = tk.Frame(root, bg="#F0F0F0")  # Light gray background
button_frame.pack(pady=10)

arg1 = tk.StringVar()
arg2 = tk.StringVar()

entry1 = tk.Entry(button_frame, textvariable=arg1, font=font_large, width=10, justify='center', bd=2)  # Border width 2
entry2 = tk.Entry(button_frame, textvariable=arg2, font=font_large, width=10, justify='center', bd=2)

entry1.grid(row=4, column=0, padx=5)
entry2.grid(row=4, column=1, padx=5)

entry1.bind("<KeyRelease>", calculate)
entry2.bind("<KeyRelease>", calculate)

label1 = tk.Label(button_frame, text="Аргумент 1", font=font_small, bg="#F0F0F0") # Light gray background
label2 = tk.Label(button_frame, text="Аргумент 2", font=font_small, bg="#F0F0F0") # Light gray background
label1.grid(row=3, column=0, padx=5)
label2.grid(row=3, column=1, padx=5)

#Styling the checkboxes
checkbox_style = {"font": font_small, "bg": "#F0F0F0"} # Light gray background

sum_checkbox_var = tk.BooleanVar()
difference_checkbox_var = tk.BooleanVar()
multiplication_checkbox_var = tk.BooleanVar()
division_checkbox_var = tk.BooleanVar()
area_checkbox_var = tk.BooleanVar()
perimeter_checkbox_var = tk.BooleanVar()

sum_checkbox = tk.Checkbutton(button_frame, text="Сложение", variable=sum_checkbox_var, command=update, **checkbox_style)
difference_checkbox = tk.Checkbutton(button_frame, text="Вычитание", variable=difference_checkbox_var, command=update, **checkbox_style)
multiplication_checkbox = tk.Checkbutton(button_frame, text="Умножение", variable=multiplication_checkbox_var, command=update, **checkbox_style)
division_checkbox = tk.Checkbutton(button_frame, text="Деление", variable=division_checkbox_var, command=update, **checkbox_style)
area_checkbox = tk.Checkbutton(button_frame, text="Площадь", variable=area_checkbox_var, command=update, **checkbox_style)
perimeter_checkbox = tk.Checkbutton(button_frame, text="Периметр", variable=perimeter_checkbox_var, command=update, **checkbox_style)

swap_button = tk.Button(button_frame, text="Поменять местами", command=swap)
clear_button = tk.Button(button_frame, text="Очистить", command=clear)
exit_button = tk.Button(button_frame, text="Выход", command=exit_app)

swap_button.grid(row=7, column=0, padx=5)
clear_button.grid(row=7, column=1, padx=5)
exit_button.grid(row=9, column=0, padx=5,columnspan=2)

choice = tk.StringVar()
choice.set("Калькулятор")

calc_button = tk.Radiobutton(button_frame, text="Калькулятор", variable=choice, value="Калькулятор", font=font_large, command=show_calculator_options, bg="#F0F0F0")  # Light gray background
square_button = tk.Radiobutton(button_frame, text="Прямоугольник", variable=choice, value="Прямоугольник", font=font_large, command=show_square_options, bg="#F0F0F0")  # Light gray background

calc_button.grid(row=2, column=0, padx=5)
square_button.grid(row=2, column=1, padx=5)

sum_label = tk.Label(button_frame, text="Сложение:", font=font_small, bg="#F0F0F0")  # Light gray background
div_label = tk.Label(button_frame, text="Деление:", font=font_small, bg="#F0F0F0")  # Light gray background
dif_label = tk.Label(button_frame, text="Вычитание:", font=font_small, bg="#F0F0F0")  # Light gray background
mult_label = tk.Label(button_frame, text="Умножение:", font=font_small, bg="#F0F0F0")  # Light gray background
area_label = tk.Label(button_frame, text="Площадь:", font=font_small, bg="#F0F0F0")  # Light gray background
perimeter_label = tk.Label(button_frame, text="Периметр:", font=font_small, bg="#F0F0F0")  # Light gray background

show_calculator_options()



menu_bar = tk.Menu(button_frame)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Выход", command=exit_app)
menu_bar.add_cascade(label="Файл", menu=file_menu)

operations_menu = tk.Menu(menu_bar, tearoff=0)
operations_menu.add_command(label="Очистить данные", command=clear)
operations_menu.add_separator()
operation_submenu = tk.Menu(operations_menu, tearoff=0)
operation_submenu.add_radiobutton(label="Сложение", variable=sum_checkbox_var, value=1)
operation_submenu.add_radiobutton(label="Вычитание", variable=difference_checkbox_var, value=1)
operation_submenu.add_radiobutton(label="Умножение", variable=multiplication_checkbox_var, value=1)
operation_submenu.add_radiobutton(label="Деление", variable=division_checkbox_var, value=1)
operations_menu.add_cascade(label="Операции", menu=operation_submenu)
menu_bar.add_cascade(label="Операции", menu=operations_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="О программе", command=show_help)
menu_bar.add_cascade(label="Справка", menu=help_menu)

root.config(menu=menu_bar)

canvas = tk.Canvas(root, width=300, height=300, bg="#FFFFFF", bd=2, relief=tk.SOLID)  # White canvas background, solid border
canvas.pack()

rectangle_color = tk.StringVar()

color_button = tk.Button(button_frame, text="Выбрать цвет прямоугольника", command=choose_rectangle_color)
color_button.grid(row=8, column=0, columnspan=2, pady=5)

root.mainloop()