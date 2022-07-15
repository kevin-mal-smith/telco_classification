import pandas as pd
import numpy as np
import os
from env import host, username, password

# this function acquires the telco data from the SQL server utilizing the host, username, and password from the env.py file
def new_telco_data():
   
    sql_query = """
                select * from customers
                join contract_types using (contract_type_id)
                join internet_service_types using (internet_service_type_id)
                join payment_types using (payment_type_id)
                """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('telco_churn'))

    return df
# this function checks for a cached csv file first, then uses the new_telco_data function to acquire it if it doesnt exist locally
def get_telco_data():
    
    if os.path.isfile('telco.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('telco.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_telco_data()
        
        # Cache data
        df.to_csv('telco.csv')
        
    return df