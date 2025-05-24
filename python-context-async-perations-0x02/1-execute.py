import sqlite3

"""
1. Reusable Query Context Manager

Objective: create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution

Instructions:

Implement a class based custom context manager ExecuteQuery that takes the query: ”SELECT * FROM users WHERE age > ?” and the parameter 25 and returns the result of the query

Ensure to use the__enter__() and the __exit__() methods

"""


class ExecuteQuery:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.query = "SELECT * FROM users WHERE age > ?"
        self.param = (25,)

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        result = self.cursor.execute(self.query, self.param)
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


with ExecuteQuery("my_db.db") as result:
    for row in result:
        print(row)
