# sql functions
import os
import sqlite3

from dotenv import load_dotenv


read = load_dotenv('.env')

database = os.getenv('FILE_DATABASE')


# add to the database
def add_to_database(user_id: int, username: str) -> None:
    with sqlite3.connect(database) as cursor:
        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, username, 0, 0))


# checking availability user_id in the database
def check_user_id(user_id: int) -> bool:
    with sqlite3.connect(database) as cursor:
        data = cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return data is not None


# checking ban status of user
def is_banned(user_id: int) -> bool:
    with sqlite3.connect(database) as cursor:
        data = cursor.execute('SELECT ban FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if data is not None:
        return data[0]


# checking for admin status of user
def is_admin(user_id: int) -> bool:
    with sqlite3.connect(database) as cursor:
        data = cursor.execute('SELECT admin FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if data is not None:
        return data[0]


# change ban status
def change_ban_status(username: str, ban: bool) -> None:
    with sqlite3.connect(database) as cursor:
        data = cursor.execute('SELECT ban FROM users WHERE username = ?', (username,)).fetchone()
        if data is not None:
            if data[0] != ban:
                cursor.execute('UPDATE users SET ban = ? WHERE username = ?', (ban, username))
                return True
        else:
            return False
