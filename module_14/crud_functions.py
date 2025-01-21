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
    cursor.execute('''

    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT_NULL
    )
    ''')
    connection.commit()


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    return products


def add_user(username, email, age, balance=1000):
    cursor.execute(f'''
        INSERT INTO Users (username, email, age, balance) VALUES('{username}', '{email}', '{age}', '{balance}')
    ''')
    connection.commit()


def is_included(username):
    user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if user.fetchone() is None:
        return False
    else:
        return True

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
