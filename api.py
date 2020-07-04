import flask
import yfinance as yf
from flask import jsonify

app = flask.Flask("Stocks API")
app.config["DEBUG"] = True


@app.route('/api/stock', methods=['POST'])
def home():
    msft = yf.Ticker("RRC")
    return jsonify(msft.info)


app.run()
