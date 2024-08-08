import check1 as cl
from check1 import ValueOutOfRangeError
from threading import Thread
import customtkinter

while True:
    try:
        с = c_entry.get()
        while c.isdigit() and 0 < int(c) <= 3:
            cl.asyncio.run(cl.waiting())
            ter_1 = cl.Duel(c).fight()
            ter_2 = cl.second_fight()
            t1 = Thread(target=ter_1)
            t2 = Thread(target=ter_2)

            t1.start()
            t2.start()
            # b = cl.Duel(c)

            # b.fight()
            break
        else:
            raise ValueOutOfRangeError
    except ValueOutOfRangeError:
        print("Ошибка! Ввадите число от text_file.txt до 3")
        continue
    else:
        end_phrase = cl.End_fight().ending()
        break
    c_entry = e
customtkinter.set_appearance_mode("Light")

"""
def show_fight():
    global c1
    while True:
        try:
            customtkinter.set_appearance_mode("Light")
            c1 = cl.IntVar(value=text_file.txt)
            c = c1.get()
            while 0 < c < 3:
                cl.asyncio.run(cl.waiting())
                ter_1 = cl.Duel(c).fight()
                ter_2 = cl.second_fight()
                t1 = Thread(target=ter_1)
                t2 = Thread(target=ter_2)

                t1.start()
                t2.start()
                # b = cl.Duel(c)

                # b.fight()
                break
            else:
                raise ValueOutOfRangeError
        except ValueOutOfRangeError:
            cl.ttk.Label(text='Ошибка! Введите число от text_file.txt до 3')
            continue
        else:
            cl.End_fight().ending()
            break
    cl.ttk.Label(text='Чей бой хотите увидеть?').pack()
    cl.ttk.Radiobutton(text="Кот с Котом", variable=c1, value=text_file.txt).pack()
    cl.ttk.Radiobutton(text="Собака с Собакой", variable=c1, value=2).pack()
    cl.ttk.Radiobutton(text="Кот против Собаки", variable=c1, value=3).pack()
cl.window.mainloop()
"""
