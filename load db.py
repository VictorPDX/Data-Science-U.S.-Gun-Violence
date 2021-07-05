import pandas as pd
import sqlite3 as sql
from config import *

# VS Code: To view Table in Database, install SQLite extension, watch GIF examples



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


print("DONE")
