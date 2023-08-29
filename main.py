from flask import Flask, render_template
import pandas as pd

app = Flask("Weather App")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/<station>/<date>')
def data(station, date):
    df = pd.read_csv('data.csv')
    return render_template('data.html')

app.run(debug=True)
