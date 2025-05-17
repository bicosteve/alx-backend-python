# Create a generator that streams rows from an SQL database one by one.


from database.db import Database


db = Database("ALX_prodev", "localhost", "bix", "")


# Connecting to dabase
db.connect_db()


# Creating database
db.create_database()

# Connectiong to prodev
db.connect_to_prodev()

# Creating table
is_created = db.create_table()


# Inserting data
db.insert_data("./data/data.csv")
