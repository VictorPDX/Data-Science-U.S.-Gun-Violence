import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
from config import *


with open("SQL queries/avg dead per day.sql", 'r') as sql_file:
    query = sql_file.read()


conn = sql.connect(db_path)
DataFrame = pd.read_sql(query, conn)


DataFrame.plot(figsize=(20, 5), y='Avg Dead per Day', x="Date")
plt.show()
