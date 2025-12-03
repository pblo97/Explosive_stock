"""
Explosive Penny Stock Detector
Streamlit App - Evidence-based penny stock screening
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config
from modules.screener import PennyStockScreener
from modules.fmp_api import FMPClient
from utils.helpers import (
    format_number, format_volume, format_percent,
    get_signal_emoji, get_trend_emoji, color_score
)

# Page config
st.set_page_config(
    page_title="Explosive Penny Stock Detector",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_screener(api_key):
    """Initialize screener with caching"""
    return PennyStockScreener(api_key)


def plot_stock_chart(symbol: str, api_key: str):
    """Create price + volume chart"""
    client = FMPClient(api_key)
    df = client.get_historical_data(symbol, days=30)

    if df.empty:
        st.warning("No chart data available")
        return

    # Create subplot with secondary y-axis
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{symbol} Price', 'Volume')
    )

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ),
        row=1, col=1
    )

    # Volume bars
    colors = ['red' if df['close'].iloc[i] < df['open'].iloc[i] else 'green'
              for i in range(len(df))]

    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker_color=colors
        ),
        row=2, col=1
    )

    fig.update_layout(
        height=600,
        showlegend=False,
        xaxis_rangeslider_visible=False
    )

    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)


def display_stock_details(stock_data: dict):
    """Display detailed analysis for a stock"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Score",
            f"{stock_data['total_score']}/100",
            f"{stock_data['signal_strength']}"
        )

    with col2:
        st.metric(
            "Price",
            f"${stock_data['price']:.2f}",
            format_percent(stock_data['change_percent'])
        )

    with col3:
        st.metric(
            "RVOL",
            f"{stock_data['rvol']:.2f}x",
            "Volume"
        )

    with col4:
        st.metric(
            "RSI",
            f"{stock_data['rsi']:.1f}",
            stock_data['obv_trend'].upper()
        )

    # Score breakdown
    st.subheader("📊 Score Breakdown")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Tier 1 - Critical (60 pts)**")
        breakdown = stock_data['score_breakdown']
        st.write(f"• RVOL: {breakdown['rvol']}/25")
        st.write(f"• OBV: {breakdown['obv']}/20")
        st.write(f"• Float: {breakdown['float']}/15")
        st.write(f"**Total: {stock_data['tier1_score']:.1f}/60**")

    with col2:
        st.write("**Tier 2 - Important (30 pts)**")
        st.write(f"• VWAP: {breakdown['vwap']}/15")
        st.write(f"• Vol Spike: {breakdown['volume_spike']}/10")
        st.write(f"• $ Volume: {breakdown['dollar_volume']}/5")
        st.write(f"**Total: {stock_data['tier2_score']:.1f}/30**")

    with col3:
        st.write("**Tier 3 - Complement (10 pts)**")
        st.write(f"• RSI: {breakdown['rsi']}/7")
        st.write(f"• Momentum: {breakdown['price_momentum']}/3")
        st.write(f"**Total: {stock_data['tier3_score']:.1f}/10**")

    # Key metrics
    st.subheader("📈 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write(f"**Volume:** {format_volume(stock_data['volume'])}")
        st.write(f"**Avg Volume:** {format_volume(stock_data['avg_volume'])}")
        st.write(f"**RVOL:** {stock_data['rvol']:.2f}x")

    with col2:
        st.write(f"**Market Cap:** {format_number(stock_data['market_cap'])}")
        st.write(f"**Float:** {format_volume(stock_data['float'])} shares")
        st.write(f"**$ Volume:** {format_number(stock_data['dollar_volume'])}")

    with col3:
        st.write(f"**VWAP:** ${stock_data['vwap']:.2f}")
        st.write(f"**RSI:** {stock_data['rsi']:.1f}")
        st.write(f"**OBV Trend:** {get_trend_emoji(stock_data['obv_trend'])} {stock_data['obv_trend'].upper()}")

    with col4:
        st.write(f"**5D Change:** {format_percent(stock_data['price_change_5d'])}")
        st.write(f"**Vol Spike:** {format_percent(stock_data['volume_spike'])}")
        st.write(f"**Gap Up:** {'✅' if stock_data['gap_up'] else '❌'}")

    # Risk flags
    if stock_data['risk_flags']:
        st.subheader("⚠️ Risk Warnings")
        for flag in stock_data['risk_flags']:
            st.warning(flag)


def main():
    st.title("🚀 Explosive Penny Stock Detector")
    st.markdown("**Evidence-based screening using Volume, OBV, Float & VWAP analysis**")

    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        api_key = st.text_input(
            "FMP API Key",
            value=config.FMP_API_KEY,
            type="password",
            help="Get your API key from financialmodelingprep.com"
        )

        st.divider()

        st.subheader("Screening Filters")

        exchange = st.selectbox(
            "Exchange",
            ["All", "NASDAQ", "NYSE", "AMEX", "OTC"],
            index=0
        )

        min_score = st.slider(
            "Minimum Score",
            0, 100, 40,
            help="Only show stocks above this score"
        )

        max_stocks = st.slider(
            "Max Stocks to Analyze",
            10, 200, 50,
            help="More stocks = slower but more thorough"
        )

        st.divider()

        st.subheader("📚 Scoring System")
        st.caption("**Tier 1 (60%):** RVOL, OBV, Float")
        st.caption("**Tier 2 (30%):** VWAP, Volume Spike, $ Volume")
        st.caption("**Tier 3 (10%):** RSI, Price Momentum")

        st.divider()

        st.caption("🟢 70+ = STRONG signal")
        st.caption("🟠 50-69 = MODERATE signal")
        st.caption("🟡 30-49 = WEAK signal")
        st.caption("🔴 <30 = AVOID")

    # Main content
    if not api_key or api_key == "your_api_key_here":
        st.warning("⚠️ Please enter your FMP API key in the sidebar to get started")
        st.info("Get your free API key at https://financialmodelingprep.com")
        return

    # Initialize screener
    screener = init_screener(api_key)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Market Scan", "📊 Analyze Symbol", "ℹ️ About"])

    with tab1:
        st.header("Market Scanner")
        st.write("Find explosive penny stocks based on volume, float, and technical indicators")

        if st.button("🚀 Start Scan", type="primary"):
            with st.spinner("Scanning market... This may take a minute..."):
                exchange_filter = None if exchange == "All" else exchange

                results = screener.scan_market(
                    exchange=exchange_filter,
                    max_stocks=max_stocks,
                    min_score=min_score
                )

                if results.empty:
                    st.warning("No stocks found matching criteria. Try lowering the minimum score.")
                else:
                    st.success(f"Found {len(results)} potential explosive stocks!")

                    # Display results table
                    display_df = results[[
                        'symbol', 'name', 'price', 'total_score',
                        'signal_strength', 'rvol', 'obv_trend',
                        'rsi', 'volume', 'market_cap'
                    ]].copy()

                    display_df['price'] = display_df['price'].apply(lambda x: f"${x:.2f}")
                    display_df['rvol'] = display_df['rvol'].apply(lambda x: f"{x:.2f}x")
                    display_df['volume'] = display_df['volume'].apply(format_volume)
                    display_df['market_cap'] = display_df['market_cap'].apply(format_number)

                    display_df.columns = [
                        'Symbol', 'Name', 'Price', 'Score',
                        'Signal', 'RVOL', 'OBV', 'RSI', 'Volume', 'Market Cap'
                    ]

                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Show top pick details
                    if len(results) > 0:
                        st.subheader(f"🎯 Top Pick: {results.iloc[0]['symbol']}")
                        top_pick = results.iloc[0].to_dict()
                        display_stock_details(top_pick)

                        # Chart
                        plot_stock_chart(results.iloc[0]['symbol'], api_key)

    with tab2:
        st.header("Analyze Specific Symbol")

        symbol = st.text_input("Enter Stock Symbol", "").upper()

        if st.button("Analyze") and symbol:
            with st.spinner(f"Analyzing {symbol}..."):
                result = screener.watch_symbol(symbol)

                if result.get('error'):
                    st.error(f"Error analyzing {symbol}: {result['error']}")
                else:
                    signal_emoji = get_signal_emoji(result['signal_strength'])
                    st.subheader(f"{signal_emoji} {symbol} - {result['name']}")

                    display_stock_details(result)

                    # Chart
                    plot_stock_chart(symbol, api_key)

    with tab3:
        st.header("About This App")

        st.markdown("""
        ### 🎯 Purpose
        This app detects penny stocks with potential for explosive 20%+ moves based on:
        - **Volume analysis** (most important indicator per 2024 research)
        - **Float size** (lower float = easier to move)
        - **On-Balance Volume** (OBV trending up = accumulation)
        - **Technical indicators** (VWAP, RSI)

        ### 📊 Why These Indicators?

        **Research-backed approach:**
        - Volume is THE most important indicator for penny stocks (2024 consensus)
        - RVOL 2-4x is the sweet spot used by professional day traders
        - OBV trending up before price = strongest early signal
        - Float <50M = higher volatility potential
        - VWAP = "almost every trader uses this" for penny stocks

        **What we DON'T use:**
        - ❌ MACD (only 56% accuracy, too slow for penny stocks)

        ### ⚠️ Risk Warning
        This tool identifies POTENTIAL explosive moves. Penny stocks are:
        - **High risk** - can lose 50% as fast as they gain
        - **Volatile** - price swings are extreme
        - **Illiquid** - hard to exit positions
        - **Pump & dump risk** - watch for warning flags

        ### 🔬 Methodology

        **Scoring System (0-100):**
        - Tier 1 (60 pts): RVOL, OBV, Float
        - Tier 2 (30 pts): VWAP, Volume Spike, Dollar Volume
        - Tier 3 (10 pts): RSI, Price Momentum

        **Signal Strength:**
        - 🚀 STRONG (70+): High explosive potential
        - 📈 MODERATE (50-69): Worth watching
        - 📊 WEAK (30-49): Marginal setup
        - ⛔ AVOID (<30): No clear signal

        ### 📚 Data Source
        Powered by Financial Modeling Prep (FMP) API
        - Real-time quotes
        - Historical price data
        - Company profiles & float data
        - Market screening

        ### ⚡ Quick Tips
        1. Look for RVOL 2-4x (not 5x+ = pump risk)
        2. OBV up + price not moving yet = best entry
        3. Avoid RSI >80 (too overbought)
        4. Check risk flags before entering
        5. Set stop losses - penny stocks move fast!

        ---
        **Disclaimer:** This is not financial advice. Do your own research.
        Trading penny stocks carries significant risk of loss.
        """)


if __name__ == "__main__":
    main()
