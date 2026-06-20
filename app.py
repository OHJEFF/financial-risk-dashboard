from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.data_loader import load_prices
from src.metrics import (
    annualised_volatility,
    cumulative_returns,
    daily_returns,
    drawdown_series,
    historical_var,
    max_drawdown,
    portfolio_returns,
    sharpe_ratio,
)

st.set_page_config(page_title="Financial Risk Dashboard", layout="wide")


@st.cache_data
def get_prices(tickers, start, end):
    return load_prices(tickers, start, end)


def main():
    st.title("Financial Risk Dashboard")

    with st.sidebar:
        st.header("Portfolio Settings")
        tickers_input = st.text_input("Tickers (comma separated)", value="AAPL, MSFT, SPY")
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

        default_start = date.today() - timedelta(days=5 * 365)
        start_date = st.date_input("Start date", value=default_start)
        end_date = st.date_input("End date", value=date.today())

        st.subheader("Weights")
        weights = []
        for ticker in tickers:
            w = st.number_input(
                f"{ticker} weight",
                min_value=0.0,
                max_value=1.0,
                value=round(1 / len(tickers), 2) if tickers else 0.0,
                step=0.05,
                key=f"weight_{ticker}",
            )
            weights.append(w)

        rf_rate = st.slider("Risk-free rate (annual)", min_value=0.0, max_value=0.10, value=0.02, step=0.005, format="%.3f")
        var_confidence = st.slider("VaR confidence level", min_value=0.90, max_value=0.99, value=0.95, step=0.01)

    if not tickers:
        st.info("Enter at least one ticker to begin.")
        return

    if sum(weights) == 0:
        st.warning("Weights sum to zero — please assign at least one positive weight.")
        return

    if start_date >= end_date:
        st.warning("Start date must be before end date.")
        return

    try:
        prices = get_prices(tickers, start_date, end_date)
    except Exception as exc:
        st.error(f"Failed to load price data: {exc}")
        return

    missing = [t for t in tickers if t not in prices.columns]
    if missing:
        st.warning(f"No data found for: {', '.join(missing)}. They will be excluded.")
        prices = prices.drop(columns=missing, errors="ignore")
        tickers = [t for t in tickers if t in prices.columns]
        weights = [w for t, w in zip(tickers, weights)]

    if prices.empty or not tickers:
        st.error("No valid price data available for the selected tickers/date range.")
        return

    returns = daily_returns(prices)
    port_returns = portfolio_returns(returns, weights)

    annual_return = port_returns.mean() * 252
    annual_vol = annualised_volatility(port_returns)
    sharpe = sharpe_ratio(port_returns, rf=rf_rate)
    var_value = historical_var(port_returns, confidence=var_confidence)
    mdd = max_drawdown(port_returns)

    st.subheader("Portfolio KPIs")
    cols = st.columns(5)
    cols[0].metric("Annualised Return", f"{annual_return:.2%}")
    cols[1].metric("Annualised Volatility", f"{annual_vol:.2%}")
    cols[2].metric("Sharpe Ratio", f"{sharpe:.2f}")
    cols[3].metric(f"VaR ({var_confidence:.0%})", f"{var_value:.2%}")
    cols[4].metric("Max Drawdown", f"{mdd:.2%}")

    st.subheader("Cumulative Returns")
    cum_returns = cumulative_returns(returns)
    fig_cum = go.Figure()
    for ticker in cum_returns.columns:
        fig_cum.add_trace(go.Scatter(x=cum_returns.index, y=cum_returns[ticker], mode="lines", name=ticker))
    port_cum = cumulative_returns(port_returns)
    fig_cum.add_trace(go.Scatter(x=port_cum.index, y=port_cum, mode="lines", name="Portfolio", line=dict(width=3, dash="dash")))
    fig_cum.update_layout(yaxis_tickformat=".0%", xaxis_title="Date", yaxis_title="Cumulative Return")
    st.plotly_chart(fig_cum, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Portfolio Drawdown")
        dd = drawdown_series(port_returns)
        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(x=dd.index, y=dd, mode="lines", fill="tozeroy", name="Drawdown", line=dict(color="firebrick")))
        fig_dd.update_layout(yaxis_tickformat=".0%", xaxis_title="Date", yaxis_title="Drawdown")
        st.plotly_chart(fig_dd, use_container_width=True)

    with col_right:
        st.subheader("Correlation Heatmap")
        corr = returns.corr()
        fig_corr = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale="RdBu_r",
                zmin=-1,
                zmax=1,
                text=np.round(corr.values, 2),
                texttemplate="%{text}",
            )
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("Per-Asset Risk Metrics")
    asset_vol = annualised_volatility(returns)
    asset_sharpe = returns.apply(lambda col: sharpe_ratio(col, rf=rf_rate))
    asset_var = returns.apply(lambda col: historical_var(col, confidence=var_confidence))
    asset_mdd = returns.apply(lambda col: max_drawdown(col))

    metrics_df = pd.DataFrame(
        {
            "Volatility": asset_vol,
            "Sharpe": asset_sharpe,
            "VaR": asset_var,
            "Max Drawdown": asset_mdd,
        }
    )

    fig_bar = go.Figure()
    for metric in metrics_df.columns:
        fig_bar.add_trace(go.Bar(x=metrics_df.index, y=metrics_df[metric], name=metric))
    fig_bar.update_layout(barmode="group", xaxis_title="Asset", yaxis_title="Value")
    st.plotly_chart(fig_bar, use_container_width=True)


if __name__ == "__main__":
    main()
