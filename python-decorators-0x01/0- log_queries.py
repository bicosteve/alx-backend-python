"""
Objective: create a decorator that logs database queries executed by any function

Instructions:

Complete the code below by writing a decorator log_queries that logs the SQL query before executing it.

Prototype: def log_queries()

"""

import sqlite3
import functools
import logging
from datetime import datetime


def log_queries(original_func):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
    logger = logging.getLogger(__name__)

    def wrapper(*args, **kwargs):
        query = args[0]
        logging.info(f"query ran {query}")
        return original_func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


users = fetch_all_users("SELECT * FROM users")
