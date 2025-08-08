# Introduction to Quantitative Trading

A comprehensive Python project demonstrating real-time and historical cryptocurrency data aggregation, analysis, and visualization for quantitative trading applications.

## 🚀 Features

- **Real-time Data Streaming**: Connect to BitMEX WebSocket for live tick and orderbook data
- **Historical Data Analysis**: Process CSV files with date range filtering
- **Multiple Aggregation Methods**:
  - **OHLCV Candlesticks**: Open, High, Low, Close, Volume data
  - **VWAP**: Volume Weighted Average Price calculations
  - **Volume Buckets**: Aggregated trades based on volume thresholds
  - **Order Flow Analysis**: Buy/sell volume, net flow, and imbalance ratios
  - **Summary Statistics**: Comprehensive tick data metrics
- **Data Visualization**: Beautiful charts using matplotlib and seaborn
- **Modular Architecture**: Clean, focused classes for each aggregation type
- **Teaching Materials**: Simple examples for learning quantitative concepts

## 📁 Project Structure

```
Intro to quant/
├── aggregations_examples/     # Example scripts for each aggregator
├── data/                      # Historical CSV data files
├── data_aggregator/           # Individual aggregation classes
├── exchange/                  # Exchange connectivity modules
├── tick_queue_module/         # Real-time tick data queue
├── visualization/             # Data visualization functions
├── main.py                    # Main entry point
└── requirements.txt           # Python dependencies
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:FarhanKardan/intoToQuant.git
   cd intoToQuant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Data Aggregation Types

### 1. OHLCV Aggregator
Generates traditional candlestick data with open, high, low, close, and volume information.

```python
from data_aggregator.ohlcv_aggregator import OHLCVAggregator

agg = OHLCVAggregator("BTCUSDT")
agg.add_ticks(tick_data)
ohlcv_data = agg.generate_ohlcv('5min')
```

### 2. VWAP Aggregator
Calculates Volume Weighted Average Price for accurate price analysis.

```python
from data_aggregator.vwap_aggregator import VWAPAggregator

agg = VWAPAggregator("BTCUSDT")
agg.add_ticks(tick_data)
vwap_data = agg.generate_vwap('5min')
```

### 3. Volume Bucket Aggregator
Groups trades into volume-based buckets for large trade analysis.

```python
from data_aggregator.volume_bucket_aggregator import VolumeBucketAggregator

agg = VolumeBucketAggregator("BTCUSDT")
agg.add_ticks(tick_data)
buckets = agg.generate_volume_buckets(bucket_size=1000.0)
```

### 4. Order Flow Aggregator
Analyzes buy/sell pressure and market microstructure.

```python
from data_aggregator.order_flow_aggregator import OrderFlowAggregator

agg = OrderFlowAggregator("BTCUSDT")
agg.add_ticks(tick_data)
orderflow = agg.generate_order_flow('5min')
```

### 5. Statistics Aggregator
Provides comprehensive summary statistics for tick data.

```python
from data_aggregator.stats_aggregator import StatsAggregator

agg = StatsAggregator("BTCUSDT")
agg.add_ticks(tick_data)
stats = agg.get_summary_stats()
```

## 🎯 Usage Examples

### Real-time Data Streaming
```bash
python main.py
```

### Run Individual Aggregation Examples
```bash
# OHLCV Example
python aggregations_examples/ohlcv_example.py

# VWAP Example
python aggregations_examples/vwap_example.py

# Volume Buckets Example
python aggregations_examples/volume_buckets_example.py

# Order Flow Example
python aggregations_examples/order_flow_example.py

# Order Flow / Volume Profile Example
python aggregations_examples/volume_profile_example.py --timeframe 1H --limit 10000 --style classic
```

### Run All Examples
```bash
python aggregations_examples/run_all_examples.py
```

### Real-time Tick Queue
```bash
python tick_queue_module/main.py
```

## 📈 Visualization

The project includes comprehensive visualization capabilities:

```python
from visualization.visualization import plot_ohlcv, plot_vwap, plot_volume_buckets

# Plot OHLCV candlesticks
plot_ohlcv(ohlcv_data, "BTCUSDT OHLCV Analysis")

# Plot VWAP analysis
plot_vwap(vwap_data, "BTCUSDT VWAP Analysis")

# Plot volume buckets
plot_volume_buckets(bucket_data, "BTCUSDT Volume Buckets")
```

## 🔧 Configuration

### WebSocket Configuration
- **Testnet**: Set `testnet=True` in BitmexWebSocket for testing
- **Production**: Use `testnet=False` for live data

### Data Sources
- **Real-time**: BitMEX WebSocket API
- **Historical**: CSV files in the `data/` directory

## 📋 Requirements

- Python 3.8+
- pandas==2.0.3
- pyarrow==12.0.0
- websockets==12.0
- matplotlib==3.7.2
- seaborn==0.12.2

## 🎓 Learning Objectives

This project is designed to teach:

1. **Real-time Data Processing**: Handling live market data streams
2. **Data Aggregation**: Converting tick data into meaningful time series
3. **Market Microstructure**: Understanding order flow and volume analysis
4. **Technical Analysis**: OHLCV and VWAP calculations
5. **Data Visualization**: Creating professional trading charts
6. **Modular Design**: Building maintainable, focused components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please ensure compliance with BitMEX API terms of service when using live data.

## ⚠️ Disclaimer

This software is for educational purposes only. It is not financial advice. Trading cryptocurrencies involves substantial risk of loss. Always do your own research and consider consulting with a financial advisor.

## 🔗 Links

- [BitMEX API Documentation](https://www.bitmex.com/app/apiOverview)
- [GitHub Repository](https://github.com/FarhanKardan/intoToQuant) 