import csv
import uuid
import mysql.connector


class Database:
    def __init__(self, db_name, host, username, password):
        self.db_name = db_name
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def connect_db(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.db_name,
            )

            if self.connection.is_connnected():
                print(f"Connection success to {self.db_name} db")
                return self.connection()
            else:
                print(f"Failed to connect to database: {self.db_name}")
                return None

        except mysql.connector.Error as err:
            print(f"error connecting to db {err}")
            return None

    def create_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.db_name,
            )

            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            connection.commit()
            connection.close()

            return self.connect_db()

        except mysql.connector.Error as err:
            print(f"error creating database: {err}")
            return None

    def connect_to_prodev(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.db_name,
            )

            if connection.is_connected():
                return connection
            else:
                return None
        except mysql.connector.Error as err:
            print(f'Error connecting to "prodev" database {err}')
            return None

    def create_table(self, table_name):
        if not self.connection:
            print("No db connection")
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}")
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            return False

    def insert_data(self, data):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.db_name,
            )

            cursor = connection.cursor()

            with open(data, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                user_data = []

                for row in reader:
                    user_id = str(uuid.uuid4())
                    name = row["name"]
                    email = row["email"]
                    age = row["age"]

                    user_data.append(user_id, name, email, age)

            insert_query = """
                INSERT INTO user_data (user_id,name, email, age)
                VALUES (%s,%s,%s,%s)
            """

            cursor.execute(insert_query, user_data)
        except mysql.connector.Error as err:
            print(f"Error {err}")
