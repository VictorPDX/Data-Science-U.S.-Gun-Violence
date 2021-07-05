import re
import pandas as pd
import sqlite3 as sql
import plotly.graph_objects as go
from config import *



with open("SQL queries/incidents in year.sql", 'r') as sql_file:
    query = sql_file.read()

YEAR = re.search('%\d+%', query).group(0)[1:-1]

# assumes db has been loaded
conn = sql.connect(db_path)
df = pd.read_sql(query, conn)


# drop rows where (cnt or notes) == Nan
df.dropna(axis=0, subset=['n_killed', 'n_injured', 'notes'], how='any', inplace=True)


df['cnt'] = df['n_killed'] + df['n_injured']
df['text'] = df['notes'] + ' ' + 'Victims: ' + df['cnt'].astype(str)


# https://plotly.com/python/scatter-plots-on-maps/
fig = go.Figure(data=go.Scattergeo(
                                lon = df['longitude'],
                                lat = df['latitude'],
                                text = df['text'],
                                mode = 'markers',
                                marker_color = df['cnt']
                                )
                )


fig.update_layout(
                title = f'Gun Violence {YEAR}<br />(Hover for incident and number of victims)',
                geo_scope='usa',
                )
fig.show()