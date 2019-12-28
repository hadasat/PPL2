

import pandas as pd
import requests
import sqlite3


conn = sqlite3.connect('bikeShare.db')
cur = conn.cursor()

try:
    df = pd.read_csv(r"/Users/ofirb/Desktop/University/עקרונות שפות תכנות/Assignments/HW2/BikeShare.csv")
    df.to_sql("bikeShareTable", conn, if_exists='fail', index=False)
except:
    print("db already exist")


def getRecommandations(number_of_recommendations, trip_duration_min, start_station, birth_year, gender):
    c = requests.get('http://127.0.0.1:5000/',params={'number': number_of_recommendations, "time": trip_duration_min,'station': start_station, 'year' : birth_year, 'gender': gender},)
    return c.json()

