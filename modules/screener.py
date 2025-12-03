"""
Stock Screener
Main screening logic combining all indicators and scoring
"""

import pandas as pd
from typing import List, Dict
import time
from modules.fmp_api import FMPClient
from modules.indicators import TechnicalIndicators
from modules.scorer import StockScorer
import config


class PennyStockScreener:
    """Main screener class for detecting explosive penny stocks"""

    def __init__(self, api_key: str):
        self.client = FMPClient(api_key)
        self.indicators = TechnicalIndicators()
        self.scorer = StockScorer()

    def get_candidate_stocks(self, exchange: str = None) -> pd.DataFrame:
        """
        Get initial list of penny stock candidates

        Args:
            exchange: Optional filter by exchange (NASDAQ, NYSE, etc)

        Returns: DataFrame of candidate stocks
        """
        print("🔍 Scanning for penny stock candidates...")

        df = self.client.get_stock_screener(
            min_price=config.MIN_PRICE,
            max_price=config.MAX_PRICE,
            min_volume=config.MIN_VOLUME,
            max_market_cap=config.MAX_MARKET_CAP,
            exchange=exchange
        )

        print(f"✓ Found {len(df)} candidates matching basic criteria")
        return df

    def analyze_stock(self, symbol: str) -> Dict:
        """
        Deep analysis of a single stock

        Returns: Dictionary with all metrics and score
        """
        result = {
            'symbol': symbol,
            'error': None
        }

        try:
            # Get quote data
            quote = self.client.get_quote(symbol)
            if not quote:
                result['error'] = 'No quote data'
                return result

            # Get historical data
            historical = self.client.get_historical_data(symbol, days=30)
            if historical.empty:
                result['error'] = 'No historical data'
                return result

            # Get profile for float
            profile = self.client.get_profile(symbol)
            float_shares = profile.get('sharesOutstanding', 0) if profile else 0

            # Current metrics
            current_price = quote['price']
            current_volume = quote['volume']
            avg_volume = quote['avgVolume']
            market_cap = quote.get('marketCap', 0)

            # Calculate all indicators
            indicators = self.indicators.calculate_all_indicators(
                historical,
                current_volume,
                avg_volume,
                current_price
            )

            # Add current price for scoring
            indicators['current_price'] = current_price

            # Calculate score
            score_data = self.scorer.calculate_total_score(indicators, float_shares)

            # Get risk flags
            risk_flags = self.scorer.get_risk_flags(
                indicators,
                float_shares,
                indicators['rvol']
            )

            # Build result
            result.update({
                'name': quote.get('name', symbol),
                'price': current_price,
                'change_percent': quote.get('changesPercentage', 0),
                'volume': current_volume,
                'avg_volume': avg_volume,
                'market_cap': market_cap,
                'float': float_shares,
                'rvol': indicators['rvol'],
                'obv_trend': indicators['obv_trend'],
                'vwap': indicators['vwap'],
                'rsi': indicators['rsi'],
                'volume_spike': indicators['volume_spike'],
                'price_change_5d': indicators['price_change_5d'],
                'dollar_volume': indicators['dollar_volume'],
                'gap_up': indicators['gap_up'],
                'total_score': score_data['total_score'],
                'score_breakdown': score_data['breakdown'],
                'tier1_score': score_data['tier1_score'],
                'tier2_score': score_data['tier2_score'],
                'tier3_score': score_data['tier3_score'],
                'signal_strength': self.scorer.get_signal_strength(score_data['total_score']),
                'risk_flags': risk_flags
            })

        except Exception as e:
            result['error'] = str(e)

        return result

    def scan_market(self, exchange: str = None, max_stocks: int = 50,
                   min_score: float = 30) -> pd.DataFrame:
        """
        Full market scan with analysis

        Args:
            exchange: Filter by exchange
            max_stocks: Maximum number of stocks to analyze
            min_score: Minimum score to include in results

        Returns: DataFrame of analyzed stocks sorted by score
        """
        # Get candidates
        candidates = self.get_candidate_stocks(exchange)

        if candidates.empty:
            print("❌ No candidates found")
            return pd.DataFrame()

        # Limit number to analyze
        symbols = candidates['symbol'].head(max_stocks).tolist()
        print(f"\n📊 Analyzing top {len(symbols)} stocks...")

        results = []
        for i, symbol in enumerate(symbols, 1):
            print(f"  [{i}/{len(symbols)}] Analyzing {symbol}...", end='\r')

            result = self.analyze_stock(symbol)

            if not result.get('error') and result.get('total_score', 0) >= min_score:
                results.append(result)

            # Rate limiting
            time.sleep(0.3)

        print(f"\n✓ Analysis complete! Found {len(results)} stocks above score {min_score}")

        if not results:
            return pd.DataFrame()

        # Convert to DataFrame and sort
        df = pd.DataFrame(results)
        df = df.sort_values('total_score', ascending=False)

        return df

    def get_top_picks(self, n: int = 10, exchange: str = None) -> pd.DataFrame:
        """
        Get top N explosive stock picks

        Args:
            n: Number of top picks
            exchange: Optional exchange filter

        Returns: DataFrame of top picks
        """
        df = self.scan_market(exchange=exchange, max_stocks=100, min_score=40)

        if df.empty:
            return df

        # Filter out high-risk pumps
        df = df[~df['risk_flags'].apply(lambda x: any('PUMP RISK' in flag for flag in x))]

        return df.head(n)

    def watch_symbol(self, symbol: str) -> Dict:
        """
        Quick analysis for a specific symbol

        Returns: Analysis dictionary
        """
        print(f"🔍 Analyzing {symbol}...")
        result = self.analyze_stock(symbol)

        if result.get('error'):
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✓ Score: {result['total_score']}/100 - {result['signal_strength']}")

        return result
