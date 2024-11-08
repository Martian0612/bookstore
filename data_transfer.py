import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

# Loading the environment variables
load_dotenv()

# Creating a connection to sqlite database
sqlite_conn = sqlite3.connect("C:\\Users\\Lenovo\\Desktop\\coding stuff\\api project assignment\\BookBuddyHub\\db.sqlite3"
)
# Creating a cursor object for executing all commands
sqlite_cursor= sqlite_conn.cursor()

# Creating a connection to postgresql database
pg_conn = psycopg2.connect(
    dbname = "BookBuddyHub_db",
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host = "127.0.0.1",
    port = "5432"
)

# Creating a postgre cursor
pg_cursor = pg_conn.cursor()

# Fetch data from auth_user table in SQLite
sqlite_cursor.execute("SELECT * FROM auth_user")
rows = sqlite_cursor.fetchall()
print(rows)

# Get column names from the auth_user table in SQLite
sqlite_cursor.execute("PRAGMA table_info(auth_user)")
print("pragma data ",sqlite_cursor.execute("PRAGMA table_info(auth_user)"))
columns = [column[1] for column in sqlite_cursor.fetchall()]
sqlite_cursor.execute("SELECT * FROM auth_user")
sqlite_cursor.execute("PRAGMA table_info(auth_user)")
columns2 = [column for column in sqlite_cursor.fetchall()]
sqlite_cursor.execute("SELECT * FROM auth_user")
sqlite_cursor.execute("PRAGMA table_info(auth_user)")
columns3 = [column[2] for column in sqlite_cursor.fetchall()]
print(columns,"columns")
print("checing")
print(columns2)
print("checking again")
print(columns3)
column_names = ", ".join(columns)
# column_names2 = ", ".join(columns2)
column_names3 = ", ".join(columns3)
print("column names", column_names)
# print("column names2", column_names2)
print("column names3", column_names3)
placeholders = ", ".join(["%s"] * len(columns))
print("placeholders ", placeholders)

# Function to convert data types based on PostgreSQL column types
def convert_types(row, column_types):
    converted_row = []
    for value, col_type in zip(row, column_types):
        if col_type == 'boolean':
            print(" i am bool")
            converted_row.append(bool(value)) # Convert integer to boolean values.
        else:
            print("i am not bool")
            converted_row.append(value) # keep the original value for other types
        return converted_row
    
# Get the column types from teh PostgreSQL auth_user table
results = pg_cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'auth_user'")
print(results," results")
if results:

    column_types = [col[1] for col in pg_cursor.fetchall()]


    # Insert data into PostgreSQL auth_user table
    for row in rows:
        converted_row = convert_types(row, column_types)
        pg_cursor.execute(
            f"INSERT INTO auth_user ({column_names}) VALUES ({placeholders})",
            converted_row
        )
else:
    print("No data found")
# Commit the changes and close the connections
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()