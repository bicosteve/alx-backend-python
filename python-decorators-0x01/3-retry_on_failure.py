import time
import sqlite3
import functools


"""
3 .


Objective: create a decorator that retries database operations if they fail due to transient errors

Instructions:

Complete the script below by implementing a retry_on_failure(retries=3, delay=2) decorator that retries the function of a certain number of times if it raises an exception

"""


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        cursor = args[0].cursor()
        try:
            return func(cursor, *args, **kwargs)
        finally:
            cursor.close()
            args[0].close()

    return wrapper


def retry_on_failure(retries, delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attemp in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempts {attemp + 1} failed : {e}")
                    if attemp < retries - 1:
                        time.sleep(delay)
                    else:
                        print("All attempts failed")

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=2)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


users = fetch_users_with_retry(sqlite3.connection("my_db.db"))
print(users)
