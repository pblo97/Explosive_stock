"""
Technical Indicators Module
Calculates evidence-based indicators for penny stock detection
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class TechnicalIndicators:
    """Calculate technical indicators for stock analysis"""

    @staticmethod
    def calculate_rvol(current_volume: int, avg_volume: int) -> float:
        """
        Calculate Relative Volume (RVOL)
        RVOL = Current Volume / Average Volume

        > 2.0 is strong signal for penny stocks
        """
        if avg_volume == 0:
            return 0
        return current_volume / avg_volume

    @staticmethod
    def calculate_obv(df: pd.DataFrame) -> pd.Series:
        """
        Calculate On-Balance Volume (OBV)
        Most important volume indicator for penny stocks

        Returns: OBV series
        """
        if df.empty or 'close' not in df.columns or 'volume' not in df.columns:
            return pd.Series()

        obv = [0]
        for i in range(1, len(df)):
            if df['close'].iloc[i] > df['close'].iloc[i - 1]:
                obv.append(obv[-1] + df['volume'].iloc[i])
            elif df['close'].iloc[i] < df['close'].iloc[i - 1]:
                obv.append(obv[-1] - df['volume'].iloc[i])
            else:
                obv.append(obv[-1])

        return pd.Series(obv, index=df.index)

    @staticmethod
    def obv_trend(df: pd.DataFrame, periods: int = 5) -> str:
        """
        Determine OBV trend direction

        Returns: 'up', 'down', or 'neutral'
        """
        obv = TechnicalIndicators.calculate_obv(df)
        if len(obv) < periods + 1:
            return 'neutral'

        recent_obv = obv.iloc[-periods:]
        slope = np.polyfit(range(len(recent_obv)), recent_obv, 1)[0]

        if slope > 0:
            return 'up'
        elif slope < 0:
            return 'down'
        return 'neutral'

    @staticmethod
    def calculate_vwap(df: pd.DataFrame) -> float:
        """
        Calculate Volume-Weighted Average Price (VWAP)
        Almost every trader uses this for penny stocks

        Returns: VWAP value
        """
        if df.empty or 'close' not in df.columns or 'volume' not in df.columns:
            return 0

        if 'high' in df.columns and 'low' in df.columns:
            typical_price = (df['high'] + df['low'] + df['close']) / 3
        else:
            typical_price = df['close']

        vwap = (typical_price * df['volume']).sum() / df['volume'].sum()
        return vwap

    @staticmethod
    def calculate_rsi(df: pd.DataFrame, periods: int = 14) -> float:
        """
        Calculate Relative Strength Index (RSI)
        81% accuracy according to 2024 research

        Returns: RSI value (0-100)
        """
        if df.empty or len(df) < periods + 1:
            return 50

        closes = df['close'].values
        deltas = np.diff(closes)

        gains = deltas.copy()
        losses = deltas.copy()

        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = abs(losses)

        avg_gain = np.mean(gains[-periods:])
        avg_loss = np.mean(losses[-periods:])

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def calculate_volume_spike(current_volume: int, prev_volume: int) -> float:
        """
        Calculate volume spike vs previous day

        Returns: Percentage increase
        """
        if prev_volume == 0:
            return 0
        return ((current_volume - prev_volume) / prev_volume) * 100

    @staticmethod
    def calculate_price_change(df: pd.DataFrame, periods: int = 5) -> float:
        """
        Calculate price change percentage over period

        Returns: Percentage change
        """
        if df.empty or len(df) < periods + 1:
            return 0

        old_price = df['close'].iloc[-periods - 1]
        new_price = df['close'].iloc[-1]

        if old_price == 0:
            return 0

        return ((new_price - old_price) / old_price) * 100

    @staticmethod
    def is_gap_up(current_open: float, prev_close: float, threshold: float = 3.0) -> bool:
        """
        Detect gap up

        Args:
            threshold: Percentage gap (default 3%)

        Returns: True if gap up detected
        """
        if prev_close == 0:
            return False

        gap_percent = ((current_open - prev_close) / prev_close) * 100
        return gap_percent >= threshold

    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame, current_volume: int,
                                 avg_volume: int, current_price: float) -> Dict:
        """
        Calculate all indicators at once

        Returns: Dictionary with all indicator values
        """
        indicators = {}

        # Core volume indicators
        indicators['rvol'] = TechnicalIndicators.calculate_rvol(current_volume, avg_volume)
        indicators['obv_trend'] = TechnicalIndicators.obv_trend(df)

        # Price indicators
        indicators['vwap'] = TechnicalIndicators.calculate_vwap(df)
        indicators['price_above_vwap'] = current_price > indicators['vwap']
        indicators['rsi'] = TechnicalIndicators.calculate_rsi(df)

        # Volume metrics
        if len(df) >= 2:
            prev_volume = df['volume'].iloc[-2]
            indicators['volume_spike'] = TechnicalIndicators.calculate_volume_spike(
                current_volume, prev_volume
            )
        else:
            indicators['volume_spike'] = 0

        # Price momentum
        indicators['price_change_5d'] = TechnicalIndicators.calculate_price_change(df, 5)

        # Dollar volume
        indicators['dollar_volume'] = current_volume * current_price

        # Gap detection
        if len(df) >= 2 and 'open' in df.columns:
            current_open = df['open'].iloc[-1]
            prev_close = df['close'].iloc[-2]
            indicators['gap_up'] = TechnicalIndicators.is_gap_up(current_open, prev_close)
        else:
            indicators['gap_up'] = False

        return indicators
