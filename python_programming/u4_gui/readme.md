Урок 6. GUI
Указания: Программу реализовать с использованием ООП: классы, методы и объекты.
Используя стандартную библиотеку tkinter, реализовать графические возможности на
языке Python.

Задание 1. Создать приложение Графический калькулятор для расчетов с двумя
аргументами простых операций сложения/вычитания/умножения/деления, либо
произвести расчеты площади/периметра для прямоугольника. Предусмотреть
отлов возможных ошибок ввода данных, результаты вычислений округлить до
сотых. По желанию: задать размеры, цвет, заголовок окна; изменить цвет/шрифт
виджетов. Необходимо использовать следующие элементы управления:

Две радио кнопки (класс RadioButton) с подписями Калькулятор/Прямоугольник
(понадобиться для Задания 3). Значение по умолчанию Калькулятор. Если
выбрано значение Прямоугольник в текстовые поля аргументов нельзя вводить
отрицательные значения;
Текстовые поля (класс Entry) – предназначены для ввода аргументов. Аргументы
могут быть положительные/отрицательные, целые/дробные;
Множественный выбор (класс Checkbutton) – выполнение вычислений и
отображение результатов. Если выбран переключатель Калькулятор, то
отображаются результаты суммы/разности/произведения/частного. Если
выбран переключатель Прямоугольник, вычисляются и отображаются только
Периметр и Площадь;
Метки (класс Label) статические для подписи Текстовых полей и динамические
для отображения результатов вычислений;
Кнопки (класс Button) выполняют операции Поменять местами аргументы,
Очистить форму, и Выход из приложения.
Задание 2. Расширить функционал приложения Графический Калькулятор, создав
пункты меню. Добавить три главных пункта: Файл, Операции, Справка.

Меню Файл содержит команду Выход;
Меню Операции содержит возможность Очистить данные и выбор выполнения
операции суммы/разности/произведения/частного и визуализацию того, что
выбрано;
Меню Справка отображает окно диалога с информацией о программе.
Задание 3. Расширить функционал приложения Графический Калькулятор, добавив
создание графического прямоугольника (виджет Canvas и create_rectangle()) внизу
формы. Длина/Ширина прямоугольника – это аргументы, введенные в текстовые
поля. Цвет, заливку сделать по желанию.

This is a offline tool, your data stays locally and is not send to any server!
