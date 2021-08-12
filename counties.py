import pandas as pd
import numpy as np
import numbers
import plotly
from plotly.offline import init_notebook_mode, iplot
import plotly as py
import plotly.graph_objs as go
from plotly import tools
import folium
from config import *
from tqdm import tqdm
# from folium import plugins

# init_notebook_mode(connected=True)

fields = ['state', 'city_or_county', 'n_killed', 'n_injured']
DataFrame = pd.read_csv(data_path, usecols=fields)
cities_df = pd.read_csv("./data/us cities/uscities.csv")

states = cities_df['state_name'].unique()
states.sort()
counties = cities_df['city'].unique()
counties.sort()

columns = ["city", 'population', 'injured', 'killed']
res = pd.DataFrame(columns=DataFrame.columns)
res_counter = 0

for s in tqdm(states):
    s_counties = cities_df[cities_df['state_name']== s]['city'].unique()
    s_counties.sort()
    for c in s_counties:
        temp = DataFrame[(DataFrame['city_or_county'] == c) & (DataFrame['state'] == s)]
        temp = temp.drop(columns=['city_or_county'])
        sums = temp.sum(axis = 0, skipna = True)
        sums['population'] = cities_df[(cities_df['city'] == c) & (cities_df['state_name'] == s)]['population'].values[0]
        sums['state'] = s
        sums['city'] = c
        res = res.append(sums, ignore_index=True)
        x = 1


res.to_csv("counties count.csv")