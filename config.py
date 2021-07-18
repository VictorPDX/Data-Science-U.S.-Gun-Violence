import os

db_name = "U.S. Gun Violence"
table_name = "'Gun Violence'"
data_path = 'data/stage3.csv'
db_path = os.path.realpath(f'db/{db_name}.db')
population_table_name = "population"
population_data_path = "data/population_by_state.csv"
