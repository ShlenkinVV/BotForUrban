import sqlite3

connection = sqlite3.connect('telegram.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    connection.commit()


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    return products


# cursor.execute('INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?);',
#                (1, 'Клавиатура', 'описание 1', 1000))
# cursor.execute('INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?);',
#                (2, 'Мышь', 'описание 2', 2000))
# cursor.execute('INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?);',
#                (3, 'Коврик', 'описание 3', 3000,))
# cursor.execute('INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?);',
#                (4, 'Наушники', 'описание 4', 4000))

# connection.commit()
# connection.close()
