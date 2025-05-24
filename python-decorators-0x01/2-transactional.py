import sqlite3
import functools


"""
Objective: create a decorator that manages database transactions by automatically committing or rolling back changes

Instructions:

Complete the script below by writing a decorator transactional(func) that ensures a function running a database operation is wrapped inside a transaction.If the function raises an error, rollback; otherwise commit the transaction.

Copy the with_db_connection created in the previous task into the script

"""


def with_db_connection(func):
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cursor = args[0].cursor()
        try:
            return func(cursor, *args, **kwargs)
        finally:
            cursor.close()
            args[0].close()

    return wrapper


def transactional(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, *kwargs)
            args[0].commit()
            return result
        except Exception as e:
            args[0].rollback()
            print(f"Transaction not successfull : {e}")
        finally:
            args[0].cursor().close()
            args[0].close()

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
