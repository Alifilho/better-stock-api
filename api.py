import flask
import yfinance as yf
from flask import jsonify

from stockAnalysis import analysis

app = flask.Flask("Stocks API")
# app.config["DEBUG"] = True


@app.route('/api/stock', methods=['POST'])
def home():
    stocks = list()
    best_stocks = analysis()
    for stock in best_stocks:
        stocks.append(yf.Ticker(stock))

    return jsonify(stocks)


app.run()
