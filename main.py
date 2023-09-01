from flask import Flask, render_template
import pandas as pd
import numpy as np
import glob
from pathlib import Path

app = Flask(__name__)

stations_df = pd.read_csv("data/data_small/stations.txt", skiprows=17)
stations = stations_df[:100][["STAID", "STANAME                                 "]]


@app.route('/')
def home():
    return render_template('home.html', data=stations.to_html())


@app.route('/api/<station_id>')
def station_api(station_id):
    station_id = str(station_id).zfill(6)
    datafile = f"./data/data_small/TG_STAID{station_id}.txt"
    station_data_df = pd.read_csv(datafile, skiprows=20, parse_dates=["    DATE"])
    # station_data = station_data_df["   TG"].mask(station_data_df["   TG"] == -9999, np.nan)
    station_data = station_data_df.to_dict(orient="records")

    return station_data


@app.route('/api/<station_id>/<year>')
def station_year_api(station_id, year):
    station_id = str(station_id).zfill(6)
    datafile = f"./data/data_small/TG_STAID{station_id}.txt"
    station_data_df = pd.read_csv(datafile, skiprows=20)
    station_data_df["    DATE"] = station_data_df["    DATE"].astype(str)
    station_data = station_data_df[station_data_df["    DATE"].str.startswith(str(year))]

    return station_data.to_dict(orient="records")


@app.route('/api/<station>/<date>')
def data(station, date):
    stations_list = stations_df[:100][["STAID", "STANAME                                 "]]
    station_id = stations_list.loc[stations_list["STAID"] == int(station)]["STAID"].squeeze()
    station_name = stations_list.loc[stations_list["STAID"] == int(station)]["STANAME                                 "].squeeze()
    station_id = str(station_id).zfill(6)
    datafile = f"./data/data_small/TG_STAID{station_id}.txt"
    df = pd.read_csv(datafile, skiprows=20, parse_dates=["    DATE"])
    try:
        temp = df.loc[df["    DATE"] == date]['   TG'].squeeze()
        temp = temp / 10 * (9/5) + 32
        return {
            "Temp": f"{int(temp)}F",
            "Station ID": f"{station_id}",
            "Station Name": f"{station_name.strip(' ')}",
            "Date": f"{date}"
        }
    except TypeError:
        return "Invalid Date"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
