"""
Objective: create a decorator that automatically handles opening and closing database connections

Instructions:

Complete the script below by Implementing a decorator with_db_connection that opens a database connection, passes it to the function and closes it afterword

"""

import sqlite3
import functools


def with_db_connection(func):
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # conn = sqlite3.connection("my_db.db")
        cursor = args[0].cursor()
        try:
            return func(cursor, *args, **kwargs)
        finally:
            cursor.close()
            args[0].close()

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id: int) -> dict:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetch_one()


conn = sqlite3.connection("my_db.db")

user = get_user_by_id(conn, user_id=1)
