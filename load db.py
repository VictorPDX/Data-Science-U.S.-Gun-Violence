import csv
import pandas as pd
import sqlite3 as sql
from config import *


# VS Code: To view Table in Database, install SQLite extension, watch GIF examples


# Load Gun Violence data
try:
    # load from Database
    conn = sql.connect(db_path)
    DataFrame = pd.read_sql(f'SELECT * FROM "{table_name}"', conn)
except (sql.OperationalError, pd.io.sql.DatabaseError):
    #  No table. Create the table, and get DataFrame representation
    DataFrame = pd.read_csv(data_path)
    conn = sql.connect(db_path)
    DataFrame.to_sql(table_name, conn)
finally:
    conn.close()

# Load state population data
try:
    conn = sql.connect(db_path)
    cursor = conn.cursor()

    # Recreate population table
    cursor.execute(f"DROP TABLE IF EXISTS {population_table_name};")
    print(f"Dropped table '{population_table_name}'.")
    cursor.execute(f"""CREATE TABLE {population_table_name}(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    year INTEGER NOT NULL,
    POP INTEGER NOT NULL
    )""")
    print(f"Created table '{population_table_name}'.")

    # Load data from csv
    count = 0
    input_file = csv.DictReader(open(population_data_path), delimiter=',')
    for row in input_file:
        # print(row)
        for year in range(2010, 2020):
            cursor.execute(f"""INSERT INTO {population_table_name}(state, year, pop)
    VALUES("{row['state']}", {year}, {row[str(year)]})
    """)
            count += 1
    print(f"Inserted {count} rows.")
except Exception as ex:
    print("Exception:", ex)
finally:
    conn.commit()
    conn.close()

print("DONE")
