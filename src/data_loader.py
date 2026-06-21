import pandas as pd
import yfinance as yf


def load_prices(tickers, start, end):
    """Download adjusted close prices for one or more tickers.

    Returns a DataFrame indexed by date with one column per ticker.
    """
    if isinstance(tickers, str):
        tickers = [t.strip() for t in tickers.split(",") if t.strip()]

    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if data.empty:
        raise ValueError("No price data returned for the given tickers/date range.")

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        # Single ticker: columns are flat (Open, High, Low, Close, Volume)
        prices = data[["Close"]]
        prices.columns = tickers

    prices = prices.dropna(axis=1, how="all")  # drop tickers with no data at all
    prices = prices.dropna(how="all").ffill().dropna()

    if prices.empty:
        raise ValueError("Price data is empty after cleaning missing values.")

    return prices
