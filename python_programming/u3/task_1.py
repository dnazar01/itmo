import pandas, sqlite3

excelDataDF = pandas.read_excel("vegetable.xlsx", sheet_name="summer")
# напечатать всё содержимое листа
print(excelDataDF)

# Попытаться открыть соединение к базе
try:
    # осуществить подключение к БД sqlitePy
    connection = sqlite3.connect("sqlitePy.db")
    # создать курсор для выполнения запросов
    cursor = connection.cursor()
    print("База данных создана и успешно подключена к SQLite")
    # вывести версию базы
    select_query = "select sqlite_version();"
    cursor.execute(select_query)
    # вернуть все строки в виде списка
    record = cursor.fetchall()
    print("Версия базы данных SQLite: ", record)
    # закрыть курсор
    cursor.close()
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    # закрыть соединение с базой
    if connection:
        connection.commit()
        connection.close()
        print("Соединение с SQLite закрыто")
