from flask import Flask, render_template
import pandas as pd
import glob
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/<station>/<date>')
def data(station, date):
    filepaths = glob.glob('./data/data_small/TG_*')
    station_df = pd.read_csv("data/data_small/stations.txt", skiprows=17)
    stations_list = station_df[:100][["STAID", "STANAME                                 "]]
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
            "Station Name": f"{station_name.strip(' ')}"
        }
    except TypeError:
        return "Invalid Date"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
