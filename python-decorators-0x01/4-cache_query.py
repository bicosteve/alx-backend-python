import time
import sqlite3
import functools


"""
4. Using decorators to cache Database Queries

Objective: create a decorator that caches the results of a database queries inorder to avoid redundant calls

Instructions:

Implement a decorator function 'cache_query(func)' that caches query results based on the SQL query string

"""

query_cache = {}


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        cursor = args[0].cursor()
        try:
            return func(cursor, *args, **kwargs)
        finally:
            cursor.close()
            args[0].close()

    return wrapper


def cache_query(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0]
        if query in query_cache:
            print(f"Returning cached result fro query", query)
            return query_cache[query]
        else:
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


users = fetch_users_with_cache(query="SELECT * FROM users")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
