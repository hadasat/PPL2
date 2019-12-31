

import pandas as pd
import requests
import sqlite3
import os

# get the csv and insert it to the db
current_directory = os.getcwd()
csv_file_name = "BikeShare.csv"
csv_path = current_directory + "/" + csv_file_name

conn = sqlite3.connect('bikeShare.db')
cur = conn.cursor()

print(csv_path)
try:
    df = pd.read_csv(csv_path)
    df.to_sql("bikeShareTable", conn, if_exists='fail', index=False)
except:
    print("db already exist")


# get recommandations using webServices.
# return list of stations. If error returns right message
def getRecommandations(number_of_recommendations, trip_duration_min, start_station, birth_year, gender):
    c = requests.get('http://127.0.0.1:5000/',params={'number': number_of_recommendations, "time": trip_duration_min,'station': start_station, 'year' : birth_year, 'gender': gender},)
    return c.json()

