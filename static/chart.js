var chart = LightweightCharts.createChart(document.body, {
  width: 2500,
  height: 1200,
	layout: {
		backgroundColor: '#131722',
		textColor: '#d1d4dc',
	},
	grid: {
		vertLines: {
			color: 'rgba(42, 46, 57, 0)',
		},
		horzLines: {
			color: 'rgba(42, 46, 57, 0.6)',
		},
	},
	priceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
		secondsVisible: true,
	},
});

chart.applyOptions({
    rightPriceScale: {
        visible: true,
    },
    leftPriceScale: {
        visible: true,
    },
    crosshair: {
        mode: 1, // CrosshairMode.Magnet
    },
});

var candleSeries = chart.addCandlestickSeries({
	upColor: '#26a69a',
	downColor: '#ef5350',
	borderDownColor: '#ef5350',
	borderUpColor: '#26a69a',
	wickDownColor: '#ef5350',
	wickUpColor: '#26a69a',
	priceScaleId: 'right',
});

const leftSeries = chart.addHistogramSeries({
	color: '#2196f3',
	lineWidth: 2,
	priceFormat: {
		type: 'price',
	},
    priceScaleId: 'left',
});

chart.priceScale('right').applyOptions({
    scaleMargins: {
        top: 0.03,
        bottom: 0.3,
    },
});

chart.priceScale('left').applyOptions({
    scaleMargins: {
        top: 0.7,
        bottom: 0.03,
    },
});

fetch('http://127.0.0.1:5000/price_history')
	.then((r) => r.json())
	.then((response) => {
        candleSeries.setData(response);
	})

fetch('http://127.0.0.1:5000/indicator_history')
	.then((r) => r.json())
	.then((response) => {
        leftSeries.setData(response);
	})

var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_1m");

binanceSocket.onmessage = function (event) {
	var message = JSON.parse(event.data);
	var candlestick = message.k;
	console.log(candlestick)
	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})

    fetch('http://127.0.0.1:5000/indicator_history')
	    .then((r) => r.json())
	    .then((response) => {
        leftSeries.setData(response);
	    })

	    document.title = "BTCUSDT " + Math.round(candlestick.c);

}