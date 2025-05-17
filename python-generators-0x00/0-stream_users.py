import mysql.connector


def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="bix",
        password="",
        database="ALX_prodev",
    )

    query = """SELECT * FROM user_data"""

    cursor = connection.execute(query)
    for index, row in enumerate(cursor):
        if index >= 6:
            break
        yield row

    connection.close()


for users in stream_users():
    print(users)
