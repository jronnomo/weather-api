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
    if station_id < 10:
        station_str = '0' + str(station_id)
    else:
        station_str = str(station_id)
    for filepath in filepaths:
        if Path(filepath).stem == f"TG_STAID0000{station_str}":
            return filepath


if __name__ == "__main__":
    app.run(debug=True)
