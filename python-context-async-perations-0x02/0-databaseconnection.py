import sqlite3

"""
0. custom class based context manager for Database connection.

Objective: create a class based context manager to handle opening and closing database connections automatically

Instructions:

Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.

"""


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connection(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()


with DatabaseConnection("my_db.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    for row in results:
        print(row)
