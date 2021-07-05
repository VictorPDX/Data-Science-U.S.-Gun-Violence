import re
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np
from config import *


with open("SQL queries/participant.sql", 'r') as sql_file:
    query = sql_file.read()


conn = sql.connect(db_path)
DataFrame = pd.read_sql(query, conn)

DataFrame.dropna(axis=0, subset=['Age', 'Sex', 'Type'], how='any', inplace=True)


# Frequency counters
males = np.zeros(110, dtype=int)
females = np.zeros(110, dtype=int)

for row in DataFrame.itertuples():
    Sex, Age, Type =  row[1:]
    sexes = re.split(r"\|\||\|", Sex)
    ages  = re.split(r"\|\||\|", Age)
    types = re.split(r"\|\||\|", Type)
    for s, a, t in zip(sexes, ages, types):
        age = int(re.split("::|:", a)[1])
        if age > 110:
            continue
        elif re.split("::|:", s)[1].lower() == "male":
            males[age] += 1
        else:
            females[age] += 1


# Plot
plt.style.use('seaborn-whitegrid')
plt.title("Gun Incidents by Age")
plt.xlabel("Age")
plt.ylabel("Incidents")
plt.plot(males)
plt.plot(females)
plt.legend(['Males', "Females"])
plt.show()
