import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   ('User'+str(i), 'example'+str(i)+'@gmail.com', i*10, 1000))



cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()

for i in range(1, len(users)+1):
    if i%2 != 0:
        cursor.execute('UPDATE Users SET balance = ? WHERE username = ?', (500, 'User'+str(i)))

for i in range(1, len(users)+1):
    if i%3 == 1:
        cursor.execute('DELETE FROM Users WHERE username = ?', ('User'+str(i),))



cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
users = cursor.fetchall()

for user in users:
    res = ''
    res+=f'Имя: {user[0]} | '
    res+=f'Почта: {user[1]} | '
    res+=f'Возраст: {user[2]} | '
    res+=f'Баланс: {user[3]} '
    print(res)



connection.commit()
connection.close()

