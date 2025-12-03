# FMP API Configuration
# Rename this file to config.py and add your API key

FMP_API_KEY = "your_fmp_api_key_here"

# Screening parameters
MIN_PRICE = 0.50
MAX_PRICE = 10.0
MAX_MARKET_CAP = 300_000_000  # $300M
MIN_VOLUME = 100_000

# Scoring weights (total = 100)
WEIGHTS = {
    'rvol': 25,           # Relative Volume
    'obv': 20,            # On-Balance Volume
    'float': 15,          # Float size
    'vwap': 15,           # Price above VWAP
    'volume_spike': 10,   # Volume spike
    'dollar_volume': 5,   # Dollar volume
    'rsi': 7,             # RSI
    'price_momentum': 3   # Price change
}

# Alert thresholds
HIGH_SCORE_THRESHOLD = 70
MEDIUM_SCORE_THRESHOLD = 50
