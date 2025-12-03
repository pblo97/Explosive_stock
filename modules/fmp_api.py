"""
FMP API Client
Handles all interactions with Financial Modeling Prep API
"""

import requests
import pandas as pd
from typing import List, Dict, Optional
import time


class FMPClient:
    BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request with error handling"""
        if params is None:
            params = {}
        params['apikey'] = self.api_key

        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def get_stock_screener(self,
                          min_price: float = 0.50,
                          max_price: float = 10.0,
                          min_volume: int = 100000,
                          max_market_cap: int = 300000000,
                          exchange: str = None) -> pd.DataFrame:
        """
        Get stocks matching penny stock criteria
        """
        params = {
            'priceMoreThan': min_price,
            'priceLowerThan': max_price,
            'volumeMoreThan': min_volume,
            'marketCapLowerThan': max_market_cap,
            'limit': 1000
        }

        if exchange:
            params['exchange'] = exchange

        data = self._make_request('stock-screener', params)

        if data:
            return pd.DataFrame(data)
        return pd.DataFrame()

    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote for a symbol"""
        data = self._make_request(f'quote/{symbol}')
        return data[0] if data else None

    def get_historical_data(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Get historical price data"""
        data = self._make_request(f'historical-price-full/{symbol}',
                                  {'timeseries': days})

        if data and 'historical' in data:
            df = pd.DataFrame(data['historical'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        return pd.DataFrame()

    def get_profile(self, symbol: str) -> Optional[Dict]:
        """Get company profile including float"""
        data = self._make_request(f'profile/{symbol}')
        return data[0] if data else None

    def get_key_metrics(self, symbol: str) -> Optional[Dict]:
        """Get key metrics"""
        data = self._make_request(f'key-metrics/{symbol}', {'limit': 1})
        return data[0] if data else None

    def get_intraday_data(self, symbol: str, interval: str = '5min') -> pd.DataFrame:
        """Get intraday data for volume analysis"""
        data = self._make_request(f'historical-chart/{interval}/{symbol}')

        if data:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            return df.sort_values('date')
        return pd.DataFrame()

    def get_market_cap(self, symbol: str) -> Optional[float]:
        """Get market capitalization"""
        quote = self.get_quote(symbol)
        return quote.get('marketCap') if quote else None

    def get_avg_volume(self, symbol: str) -> Optional[int]:
        """Get average volume"""
        quote = self.get_quote(symbol)
        return quote.get('avgVolume') if quote else None

    def batch_quotes(self, symbols: List[str]) -> pd.DataFrame:
        """Get quotes for multiple symbols"""
        symbols_str = ','.join(symbols[:100])  # API limit
        data = self._make_request(f'quote/{symbols_str}')

        if data:
            return pd.DataFrame(data)
        return pd.DataFrame()
