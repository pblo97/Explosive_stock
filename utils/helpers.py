"""
Helper Functions
Utility functions for formatting and display
"""

import pandas as pd


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with K, M, B suffixes"""
    if num >= 1_000_000_000:
        return f"${num/1_000_000_000:.{decimals}f}B"
    elif num >= 1_000_000:
        return f"${num/1_000_000:.{decimals}f}M"
    elif num >= 1_000:
        return f"${num/1_000:.{decimals}f}K"
    else:
        return f"${num:.{decimals}f}"


def format_volume(vol: int) -> str:
    """Format volume with K, M suffixes"""
    if vol >= 1_000_000:
        return f"{vol/1_000_000:.1f}M"
    elif vol >= 1_000:
        return f"{vol/1_000:.1f}K"
    else:
        return str(vol)


def format_percent(value: float, decimals: int = 2) -> str:
    """Format percentage with + or - sign"""
    sign = '+' if value > 0 else ''
    return f"{sign}{value:.{decimals}f}%"


def get_signal_emoji(signal: str) -> str:
    """Get emoji for signal strength"""
    emoji_map = {
        'STRONG': '🚀',
        'MODERATE': '📈',
        'WEAK': '📊',
        'AVOID': '⛔'
    }
    return emoji_map.get(signal, '❓')


def get_trend_emoji(trend: str) -> str:
    """Get emoji for trend direction"""
    emoji_map = {
        'up': '⬆️',
        'down': '⬇️',
        'neutral': '➡️'
    }
    return emoji_map.get(trend, '❓')


def color_score(score: float) -> str:
    """Get color for score"""
    if score >= 70:
        return 'green'
    elif score >= 50:
        return 'orange'
    elif score >= 30:
        return 'yellow'
    else:
        return 'red'


def create_score_bar(score: float, max_score: float = 100) -> str:
    """Create ASCII progress bar for score"""
    filled = int((score / max_score) * 20)
    bar = '█' * filled + '░' * (20 - filled)
    return f"{bar} {score:.1f}/{max_score}"
