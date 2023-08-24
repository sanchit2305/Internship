import pandas as pd
from sqlalchemy import create_engine


db_user = 'root'
db_password = '12345'
db_host = 'localhost'
db_name = 'recorder'

csv_file = 'banknifty_pcr_15.csv' 
df = pd.read_csv(csv_file)
db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"


engine = create_engine(db_uri)


df.to_sql('banknifty15pcr', engine, if_exists='replace', index=False)

engine.dispose()