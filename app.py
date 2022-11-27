from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_cors import CORS
from binance.client import Client
import config
import math
import numpy as np

#flask --app app --debug run
app = Flask(__name__)
CORS(app)

client = Client(config.API_KEY, config.API_SECRET)

lookback = config.lookback
expo = config.expo


# Exponentially Weighted Volatility
def ewma_volatility(source, period: float):
    final_values = []
    sqrt_annual = math.sqrt(365) * 100

    expo = period
    squared = np.power(source, 2)
    prev_vol = expo * squared[0] + (1.0 - expo) * squared[0]
    final_values.append(sqrt_annual * math.sqrt(prev_vol))

    for i in range(1, len(source)):
        prev_vol = expo * prev_vol + (1.0 - expo) * squared[i]
        final_values.append(sqrt_annual * math.sqrt(prev_vol))

    ewma_vol = final_values[-1]
    return ewma_vol


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/price_history')
def price_history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    final_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }
        final_candlesticks.append(candlestick)

    # print(len(final_candlesticks))

    return jsonify(final_candlesticks)


@app.route('/indicator_history')
def indicator_history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    indicator_data = []
    timestamp = []
    close = []

    for data in candlesticks:
        timestamp.append(float(data[0] / 1000))
        close.append(float(data[4]))

    timestamp = np.array(timestamp)
    close = np.array(close)
    logr = np.diff(np.log(close))
    timestamp = timestamp[1:]
    upR = np.copy(logr)
    downR = np.copy(logr)
    for i in range(len(upR)):
        if upR[i] < 0:
            upR[i] = 0
        if downR[i] > 0:
            downR[i] = 0

    z = []

    for i in range(len(logr)+1):
        if i >= lookback:
            if len(upR[i - lookback: i]) > 1:
                upSRC = ewma_volatility(upR[i - lookback: i], expo)
                downSRC = ewma_volatility(downR[i - lookback: i], expo)
                momentum = np.subtract(upSRC, downSRC)
                z.append(momentum)

                colour = '#00ff0a'
                if len(z) > 1:
                    if z[-1] > 0:
                        colour = '#00ff0a'
                    else:
                        colour = '#ff1100'

                indicator = {
                    "time": timestamp[i-1],
                    "value": z[-1],
                    "color": colour
                }
                indicator_data.append(indicator)

    return jsonify(indicator_data)
