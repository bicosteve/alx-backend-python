import pymysql
import pymysql.cursors

"""
Objective: Simulte fetching paginated data from the users database using a generator to lazily load each page

Instructions:

    Implement a generator function lazypaginate(pagesize) that implements the paginate_users(page_size, offset) that will only fetch the next page when needed at an offset of 0.
        You must only use one loop
        Include the paginate_users function in your code
        You must use the yield generator
        Prototype:
        def lazy_paginate(page_size)


"""


def paginate_users(page_size, offset):
    """
    Makes connection to mysql db and gets the user data
    returns all the users according to page_size, and offset

    """
    connection = pymysql.connect(
        host="localhost",
        user="bix",
        password="",
        database="ALX_prodev",
        cursorclass=pymysql.cursors.DictCursor,
    )

    try:
        cursor = connection.cursor()

        query = """SELECT * FROM user_data LIMIT %s OFFSET %s"""
        cursor.execute(query, (page_size, offset))

        users = cursor.fetchall()
        return users
    except pymysql.Error as err:
        print(f"error occured {err}")
        return users
    finally:
        if connection:
            connection.close()


def lazypaginate(pagesize):
    """
    This functions lazily paginate user data
    pagesize is th enumber of user to fetch per page
    yields a lsit of user for the current page

    """
    offset = 0

    while True:
        users = paginate_users(pagesize, offset)
        if not users:
            break
        yield users
        offset += pagesize
