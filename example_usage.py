#!/usr/bin/env python3
"""
Example CLI Usage
Quick examples of how to use the screener programmatically
"""

import config
from modules.screener import PennyStockScreener


def example_market_scan():
    """Example: Full market scan"""
    print("=" * 60)
    print("EXAMPLE 1: Full Market Scan")
    print("=" * 60)

    # Initialize screener
    screener = PennyStockScreener(config.FMP_API_KEY)

    # Scan NASDAQ for top 20 stocks, minimum score 50
    results = screener.scan_market(
        exchange="NASDAQ",
        max_stocks=20,
        min_score=50
    )

    if not results.empty:
        print(f"\n✅ Found {len(results)} explosive candidates!\n")

        # Show top 5
        for idx, row in results.head(5).iterrows():
            print(f"{row['symbol']:6} | Score: {row['total_score']:5.1f} | "
                  f"Signal: {row['signal_strength']:8} | "
                  f"RVOL: {row['rvol']:4.2f}x | "
                  f"OBV: {row['obv_trend']:8} | "
                  f"Price: ${row['price']:.2f}")

        print(f"\n💡 Top Pick: {results.iloc[0]['symbol']} with score {results.iloc[0]['total_score']:.1f}")
    else:
        print("\n❌ No stocks found matching criteria")


def example_analyze_symbol():
    """Example: Analyze specific symbol"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Analyze Specific Symbol")
    print("=" * 60)

    screener = PennyStockScreener(config.FMP_API_KEY)

    # Analyze a specific symbol
    symbol = "AAPL"  # Change this to any symbol
    result = screener.watch_symbol(symbol)

    if not result.get('error'):
        print(f"\n📊 Analysis for {symbol}:")
        print(f"   Name: {result['name']}")
        print(f"   Price: ${result['price']:.2f}")
        print(f"   Score: {result['total_score']:.1f}/100")
        print(f"   Signal: {result['signal_strength']}")
        print(f"\n   Key Metrics:")
        print(f"   - RVOL: {result['rvol']:.2f}x")
        print(f"   - OBV Trend: {result['obv_trend']}")
        print(f"   - RSI: {result['rsi']:.1f}")
        print(f"   - VWAP: ${result['vwap']:.2f}")
        print(f"   - Float: {result['float']:,.0f} shares")

        print(f"\n   Score Breakdown:")
        breakdown = result['score_breakdown']
        print(f"   Tier 1 (Critical): {result['tier1_score']:.1f}/60")
        print(f"     • RVOL: {breakdown['rvol']}/25")
        print(f"     • OBV: {breakdown['obv']}/20")
        print(f"     • Float: {breakdown['float']}/15")
        print(f"   Tier 2 (Important): {result['tier2_score']:.1f}/30")
        print(f"   Tier 3 (Complement): {result['tier3_score']:.1f}/10")

        if result['risk_flags']:
            print(f"\n   ⚠️  Risk Warnings:")
            for flag in result['risk_flags']:
                print(f"   {flag}")
    else:
        print(f"\n❌ Error: {result['error']}")


def example_top_picks():
    """Example: Get top 10 picks"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Get Top 10 Explosive Picks")
    print("=" * 60)

    screener = PennyStockScreener(config.FMP_API_KEY)

    # Get top 10 picks (automatically filters out high-risk pumps)
    top_picks = screener.get_top_picks(n=10, exchange="NASDAQ")

    if not top_picks.empty:
        print(f"\n🚀 Top {len(top_picks)} Explosive Stock Picks:\n")

        print(f"{'Rank':<5} {'Symbol':<8} {'Score':<8} {'Signal':<12} {'RVOL':<8} {'Price':<10}")
        print("-" * 60)

        for idx, (_, row) in enumerate(top_picks.iterrows(), 1):
            print(f"{idx:<5} {row['symbol']:<8} {row['total_score']:<8.1f} "
                  f"{row['signal_strength']:<12} {row['rvol']:<8.2f}x ${row['price']:<10.2f}")

        # Show detailed analysis of #1 pick
        print(f"\n{'='*60}")
        print(f"🎯 DETAILED ANALYSIS - #1 PICK: {top_picks.iloc[0]['symbol']}")
        print(f"{'='*60}")

        pick = top_picks.iloc[0]
        print(f"\nCompany: {pick['name']}")
        print(f"Price: ${pick['price']:.2f} ({pick['change_percent']:+.2f}%)")
        print(f"Market Cap: ${pick['market_cap']:,.0f}")
        print(f"\nWhy This Stock:")

        # Explain the score
        if pick['rvol'] >= 2.0:
            print(f"  ✅ Strong volume: {pick['rvol']:.2f}x normal (institutional interest)")
        if pick['obv_trend'] == 'up':
            print(f"  ✅ OBV trending UP (accumulation phase)")
        if pick['rsi'] >= 40 and pick['rsi'] <= 70:
            print(f"  ✅ RSI in healthy range: {pick['rsi']:.1f} (not overbought)")
        if pick['price'] > pick['vwap']:
            print(f"  ✅ Price above VWAP (${pick['vwap']:.2f}) - institutional support")

        if pick['risk_flags']:
            print(f"\n⚠️  Warnings:")
            for flag in pick['risk_flags']:
                print(f"  {flag}")
        else:
            print(f"\n✅ No major risk flags detected")

    else:
        print("\n❌ No top picks found today")


def example_custom_scan():
    """Example: Custom scan with specific criteria"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom Scan - RVOL >3x, Score >60")
    print("=" * 60)

    screener = PennyStockScreener(config.FMP_API_KEY)

    # Get all results
    results = screener.scan_market(exchange="NASDAQ", max_stocks=50, min_score=40)

    if not results.empty:
        # Custom filter: RVOL > 3x AND Score > 60 AND no pump risks
        filtered = results[
            (results['rvol'] > 3.0) &
            (results['total_score'] > 60) &
            (results['risk_flags'].apply(lambda x: 'PUMP RISK' not in str(x)))
        ]

        print(f"\n✅ Found {len(filtered)} stocks matching custom criteria\n")

        for _, row in filtered.head(10).iterrows():
            print(f"{row['symbol']:6} | Score: {row['total_score']:5.1f} | "
                  f"RVOL: {row['rvol']:5.2f}x | "
                  f"OBV: {row['obv_trend']:8} | "
                  f"RSI: {row['rsi']:5.1f}")
    else:
        print("\n❌ No results found")


if __name__ == "__main__":
    print("\n🚀 EXPLOSIVE PENNY STOCK DETECTOR - CLI Examples\n")

    if config.FMP_API_KEY == "your_api_key_here":
        print("❌ ERROR: Please set your FMP API key in config.py")
        print("Get your API key at: https://financialmodelingprep.com")
        exit(1)

    # Run examples
    # Uncomment the ones you want to try:

    # example_market_scan()
    # example_analyze_symbol()
    # example_top_picks()
    # example_custom_scan()

    print("\n💡 TIP: Uncomment the examples you want to run in example_usage.py")
    print("\nOr run the Streamlit app for full interface:")
    print("  streamlit run app.py\n")
