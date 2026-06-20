import numpy as np

TRADING_DAYS = 252


def daily_returns(prices):
    return prices.pct_change().dropna()


def cumulative_returns(returns):
    return (1 + returns).cumprod() - 1


def annualised_volatility(returns):
    return returns.std() * np.sqrt(TRADING_DAYS)


def sharpe_ratio(returns, rf=0.0):
    annual_return = returns.mean() * TRADING_DAYS
    annual_vol = annualised_volatility(returns)
    return (annual_return - rf) / annual_vol


def historical_var(returns, confidence=0.95):
    """Historical Value at Risk, returned as a positive loss figure."""
    percentile = (1 - confidence) * 100
    var = np.percentile(returns, percentile)
    return -var


def drawdown_series(returns):
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    return cum / running_max - 1


def max_drawdown(returns):
    return drawdown_series(returns).min()


def portfolio_returns(returns, weights):
    weights = np.array(weights, dtype=float)
    weights = weights / weights.sum()
    return returns.dot(weights)
