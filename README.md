# Bitcoin Custom Indicator Chart - Flask Web App

Bitcoin price and custom EWMA momentum indicator values will update in real time. 

You can define the desired amount of price/indicator chart history.

Green Colour = Buy Signal

Red Colour = Sell Signal

A signal would be acted upon at the open of the candle immediately after it.
### Getting Started

Install the python dependencies using:
```pip install -r requirements.txt```


### Launching the app

use the command:```flask --app app --debug run``` this launches the webapp in debug mode.

![Alt text](screenshot.jpg?raw=true "Optional Title")