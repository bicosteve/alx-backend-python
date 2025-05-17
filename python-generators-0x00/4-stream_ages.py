import pymysql


"""
Objective: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

Instruction:

    Implement a generator stream_user_ages() that yields user ages one by one.

    Use the generator in a different function to calculate the average age without loading the entire dataset into memory

    Your script should print Average age of users: average age

    You must use no more than two loops in your script

    You are not allowed to use the SQL AVERAGE
"""


def stream_user_ages():
    """
    Streams user ages from the database on at a time.
    """

    try:
        connection = pymysql.connect(
            host="localhost", user="bix", password="", database="ALX_prodev"
        )

        with connection.cursor() as cursor:
            """
            Fetch ages one at a time to minimize memory usage

            """
            cursor.execute("SELECT age FROM user_data")
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row[0]  # yeild row[0] yield only the age not the whole row

    except pymysql.Error as er:
        print(f"An error occurred while connecting to db {er}")
        return
    finally:
        if connection:
            connection.close()


def calculate_average_age():
    """Calculates the average age of users using the stream_user_ages generator"""
    age_stream = stream_user_ages()
    count = 0
    total = 0

    for age in age_stream:
        total += age
        count += 1

    if count == 0:
        print("the average age is 0")
    print(f"the average age is {total/count}")
