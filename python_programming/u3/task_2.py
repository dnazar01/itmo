import sqlite3

# Создание соединения с базой данных
conn = sqlite3.connect("country.db")

# Создание курсора для выполнения операций с базой данных
cur = conn.cursor()

# Создание таблицы tCountry
cur.execute(
    """CREATE TABLE IF NOT EXISTS tCountry (
                id INTEGER PRIMARY KEY,
                country_name TEXT
            )"""
)

# Заполнение таблицы произвольными значениями
countries = [("USA",), ("Canada",), ("Germany",), ("Japan",), ("Australia",)]

# Использование executemany()
cur.executemany("INSERT INTO tCountry (country_name) VALUES (?)", countries)

# Сохранение изменений
conn.commit()

# Выполнение запросов для выборки данных
cur.execute("SELECT * FROM tCountry")

# Использование fetchone()
print("fetchone():", cur.fetchone())

# Использование fetchmany()
print("fetchmany(2):", cur.fetchmany(2))

# Использование fetchall()
print("fetchall():", cur.fetchall())

# Закрытие курсора и соединения
cur.close()
conn.close()
