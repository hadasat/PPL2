
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from flask import Flask
from flask import jsonify
from flask import request
from flask import request
import sqlite3

# return data frame represent the data set from the db
def getDataSet():
    conn = sqlite3.connect('bikeShare.db')
    df = pd.read_sql_query("SELECT * FROM bikeShareTable", conn)
    return df


app = Flask(__name__)

# parameters: list of tuples contains [station: string, probability: int] and number k
# return the k tuples with the heighest probability
def getKMostProbability(tuples, k):
    sortedTuples = sorted(tuples, key=lambda x: x[1], reverse=True)
    return sortedTuples[:k]

# get k recommandations. this method build the dt model with the given data.
# id there is no k results, the function try again with depth -1
def getKRecommendations(dataset,k, x_input, initDepth=15):
    clf = tree.DecisionTreeClassifier(max_depth=initDepth)
    features = ["TripDurationinmin", "StartStationID", "BirthYear", "Gender"]
    X = dataset[features]
    y = dataset["EndStationName"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    dt = clf.fit(X_train, y_train)
    y_pred = dt.predict_proba([x_input])
    results = list(zip(dt.classes_, y_pred[0]))
    kMostProbability = getKMostProbability(results, k)
    lastElement = kMostProbability[-1]
    if abs(lastElement[1]) == 0:
        print(initDepth, " not good")
        return getKRecommendations(dataset,k, x_input, initDepth - 1)
    onlyClassesName = [item[0] for item in kMostProbability]

    return onlyClassesName

# return id of stations by station name
def getIdOfStation(stationName,dataset):
    x = dataset[["StartStationID", "StartStationName"]]
    list_stations = x.values.tolist()
    for value in list_stations:
        if value[1] == stationName:
            return value[0]
    return "error"

# returns  k recommandations with given parameters.
def getRecommandations(k, TripDurationinmin, StartStation, BirthYear, Gender):
    dataset = getDataSet()
    station_id = getIdOfStation(StartStation,dataset)
    if station_id == "error":
        return "error: station not found"
    input_array_data = [TripDurationinmin, station_id, BirthYear, Gender];
    return getKRecommendations(dataset,k, input_array_data)


@app.route("/",methods=['GET'])
def home():
    args = request.args
    try:
        if "number" in args:
            number_of_recommendations = int(args["number"])

        if "time" in args:
            trip_duration_min = int(args.get("time"))

        if "station" in args:
            start_station = args["station"]

        if "year" in request.args:
            birth_year = int(args.get("year"))
        if "gender" in request.args:
            gender = int(args.get("gender"))
    except:
        return jsonify("Invalid Input")

    try:
        recommendations = getRecommandations(number_of_recommendations, trip_duration_min, start_station, birth_year, gender)
        print(recommendations)
        return jsonify(recommendations)
    except:
        return jsonify("Some error occurred :(")


if __name__ == "__main__":
    app.run(debug=True)
