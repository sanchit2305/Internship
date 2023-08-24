import pandas as pd
from sqlalchemy import create_engine


db_user = 'root'
db_password = '12345'
db_host = 'localhost'
db_name = 'combined'

csv_file = 'nifty_banknifty_finnifty_combined.csv' 
df = pd.read_csv(csv_file)
db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"


engine = create_engine(db_uri)


df.to_sql('combined', engine, if_exists='replace', index=False)

engine.dispose()


