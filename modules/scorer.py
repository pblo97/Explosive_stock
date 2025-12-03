"""
Scoring System
Evidence-based scoring for penny stock explosive potential
"""

from typing import Dict


class StockScorer:
    """Score stocks based on explosive potential indicators"""

    @staticmethod
    def score_rvol(rvol: float) -> float:
        """
        Score Relative Volume (25 points max)
        RVOL 2-4x is ideal - professional day traders prefer this range
        """
        if rvol >= 5.0:
            return 10  # Too high - possible pump & dump
        elif rvol >= 3.0:
            return 25  # Perfect range
        elif rvol >= 2.0:
            return 22  # Good signal
        elif rvol >= 1.5:
            return 15  # Moderate
        elif rvol >= 1.0:
            return 5   # Low interest
        else:
            return 0

    @staticmethod
    def score_obv(obv_trend: str, price_change: float) -> float:
        """
        Score On-Balance Volume (20 points max)
        OBV trending up before price = strong signal
        """
        if obv_trend == 'up':
            if price_change < 5:
                return 20  # OBV up, price not yet - best signal
            elif price_change < 15:
                return 17  # OBV confirming price move
            else:
                return 10  # Might be late
        elif obv_trend == 'neutral':
            return 5
        else:
            return 0  # OBV down - avoid

    @staticmethod
    def score_float(float_shares: float) -> float:
        """
        Score Float size (15 points max)
        Lower float = easier to move price
        """
        if float_shares == 0:
            return 0

        float_millions = float_shares / 1_000_000

        if float_millions < 10:
            return 10  # Very low - high risk of pump & dump
        elif float_millions < 20:
            return 15  # Perfect range
        elif float_millions < 50:
            return 12  # Good
        elif float_millions < 100:
            return 7   # Moderate
        else:
            return 2   # High float - harder to move

    @staticmethod
    def score_vwap(price: float, vwap: float) -> float:
        """
        Score VWAP position (15 points max)
        Price above VWAP = institutional support
        """
        if vwap == 0:
            return 0

        diff_percent = ((price - vwap) / vwap) * 100

        if 0 < diff_percent <= 5:
            return 15  # Just above VWAP - ideal entry
        elif 5 < diff_percent <= 10:
            return 12  # Above but not extended
        elif 10 < diff_percent <= 20:
            return 7   # Getting extended
        elif diff_percent > 20:
            return 2   # Too far from VWAP
        else:
            return 5   # Below VWAP - caution

    @staticmethod
    def score_volume_spike(spike_percent: float) -> float:
        """
        Score Volume Spike (10 points max)
        Sudden volume increase
        """
        if spike_percent >= 500:
            return 5   # Extreme - might be manipulation
        elif spike_percent >= 300:
            return 10  # Strong spike
        elif spike_percent >= 200:
            return 9   # Good spike
        elif spike_percent >= 100:
            return 7   # Moderate spike
        elif spike_percent >= 50:
            return 4   # Small spike
        else:
            return 0

    @staticmethod
    def score_dollar_volume(dollar_volume: float) -> float:
        """
        Score Dollar Volume (5 points max)
        Real liquidity measure
        """
        if dollar_volume >= 5_000_000:
            return 5   # High liquidity
        elif dollar_volume >= 2_000_000:
            return 4
        elif dollar_volume >= 1_000_000:
            return 3
        elif dollar_volume >= 500_000:
            return 2
        else:
            return 0   # Too illiquid

    @staticmethod
    def score_rsi(rsi: float) -> float:
        """
        Score RSI (7 points max)
        81% accuracy - use to avoid overbought
        """
        if 40 <= rsi <= 60:
            return 7   # Neutral zone - best for entry
        elif 30 <= rsi < 40:
            return 6   # Slightly oversold - good
        elif 60 < rsi <= 70:
            return 5   # Slightly overbought - caution
        elif 70 < rsi <= 80:
            return 2   # Overbought - risky
        elif rsi > 80:
            return 0   # Extremely overbought - avoid
        else:
            return 3   # Oversold

    @staticmethod
    def score_price_momentum(price_change: float) -> float:
        """
        Score Price Momentum (3 points max)
        Recent price action
        """
        if 5 <= price_change <= 20:
            return 3   # Good momentum, not parabolic
        elif 20 < price_change <= 35:
            return 2   # Strong but extended
        elif 0 <= price_change < 5:
            return 1   # Slight move
        else:
            return 0   # Down or too extended

    @staticmethod
    def calculate_total_score(indicators: Dict, float_shares: float = 0) -> Dict:
        """
        Calculate total score and breakdown

        Returns: Dictionary with score and breakdown
        """
        scores = {}

        # Tier 1 - Critical (60%)
        scores['rvol'] = StockScorer.score_rvol(indicators.get('rvol', 0))
        scores['obv'] = StockScorer.score_obv(
            indicators.get('obv_trend', 'neutral'),
            indicators.get('price_change_5d', 0)
        )
        scores['float'] = StockScorer.score_float(float_shares)

        # Tier 2 - Important (30%)
        scores['vwap'] = StockScorer.score_vwap(
            indicators.get('current_price', 0),
            indicators.get('vwap', 0)
        )
        scores['volume_spike'] = StockScorer.score_volume_spike(
            indicators.get('volume_spike', 0)
        )
        scores['dollar_volume'] = StockScorer.score_dollar_volume(
            indicators.get('dollar_volume', 0)
        )

        # Tier 3 - Complementary (10%)
        scores['rsi'] = StockScorer.score_rsi(indicators.get('rsi', 50))
        scores['price_momentum'] = StockScorer.score_price_momentum(
            indicators.get('price_change_5d', 0)
        )

        # Calculate total
        total = sum(scores.values())

        return {
            'total_score': round(total, 2),
            'breakdown': scores,
            'tier1_score': scores['rvol'] + scores['obv'] + scores['float'],
            'tier2_score': scores['vwap'] + scores['volume_spike'] + scores['dollar_volume'],
            'tier3_score': scores['rsi'] + scores['price_momentum']
        }

    @staticmethod
    def get_signal_strength(score: float) -> str:
        """
        Get signal strength based on score

        Returns: 'STRONG', 'MODERATE', 'WEAK', or 'AVOID'
        """
        if score >= 70:  # HIGH_SCORE_THRESHOLD
            return 'STRONG'
        elif score >= 50:  # MEDIUM_SCORE_THRESHOLD
            return 'MODERATE'
        elif score >= 30:
            return 'WEAK'
        else:
            return 'AVOID'

    @staticmethod
    def get_risk_flags(indicators: Dict, float_shares: float, rvol: float) -> list:
        """
        Identify risk flags (pump & dump warning signs)

        Returns: List of risk warnings
        """
        flags = []

        # Float < 10M + RVOL > 5x = pump & dump risk
        float_millions = float_shares / 1_000_000 if float_shares > 0 else 0
        if float_millions < 10 and rvol > 5:
            flags.append('⚠️ PUMP RISK: Ultra low float + extreme volume')

        # Price spike > 50% in one day
        if indicators.get('price_change_5d', 0) > 50:
            flags.append('⚠️ Parabolic move - might be too late')

        # RSI > 80
        if indicators.get('rsi', 50) > 80:
            flags.append('⚠️ Extremely overbought')

        # OBV down while price up
        if indicators.get('obv_trend') == 'down' and indicators.get('price_change_5d', 0) > 5:
            flags.append('⚠️ Divergence: Price up but OBV down')

        # Low dollar volume
        if indicators.get('dollar_volume', 0) < 500_000:
            flags.append('⚠️ Low liquidity - hard to exit')

        return flags
