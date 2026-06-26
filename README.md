# Financial Risk Dashboard

An interactive portfolio risk analytics dashboard built with **Python** and **Streamlit** — pulls live market data via `yfinance` and computes standard risk/return metrics (returns, volatility, Sharpe ratio, Value at Risk, drawdown) for any user-defined multi-asset portfolio.

## Dashboard Preview

<p align="center">
  <img src="docs/overview.png" width="45%">
  <img src="docs/risk.png" width="45%">
</p>

<p align="center">
  <img src="docs/montecarlo.png" width="45%">
  <img src="docs/efficient_frontier.png" width="45%">
</p>
## Features

**Core risk analytics**
- **Live data ingestion** from Yahoo Finance via `yfinance` (adjusted close prices, single or multiple tickers)
- **Daily & cumulative returns** for every asset in the portfolio
- **Annualised volatility** to quantify risk per asset and at the portfolio level
- **Sharpe ratio** for risk-adjusted return, with a user-configurable risk-free rate
- **Historical Value at Risk (VaR)** at a user-selectable confidence level
- **Maximum drawdown** and full drawdown time series
- **Portfolio-level analysis** with custom, user-defined asset weights
- **Correlation heatmap** across all selected assets

**Advanced analytics**
- **Rolling volatility & rolling Sharpe ratio** over a user-adjustable lookback window, to see how risk and risk-adjusted performance evolve over time
- **Benchmark comparison** against any ticker (e.g. SPY), with annualised Alpha and Beta
- **Risk contribution decomposition** — how much each asset contributes to total portfolio volatility, compared against its capital weight
- **Historical stress testing** against past market shocks (e.g. the COVID-19 crash, the 2022 bear market)
- **Monte Carlo simulation** of future portfolio value paths, with percentile-based outcome ranges
- **Efficient frontier optimisation** — thousands of randomly weighted portfolios plotted by risk/return, highlighting the Max Sharpe and Min Volatility portfolios
- **Fama-French three-factor analysis** — regresses portfolio excess returns on Market, SMB, and HML factors to decompose alpha and factor exposures

**Dashboard UX**
- **9-tab interactive Streamlit dashboard**, each focused on one layer of analysis:
  1. **Overview** — portfolio KPIs and cumulative returns
  2. **Risk** — drawdown, correlation heatmap, per-asset risk comparison
  3. **Rolling Metrics** — rolling volatility and Sharpe ratio
  4. **Benchmark** — portfolio vs. benchmark performance, Alpha & Beta
  5. **Risk Contribution** — per-asset risk decomposition vs. weight
  6. **Stress Test** — portfolio performance in historical crisis scenarios
  7. **Monte Carlo** — simulated future portfolio paths and outcome distribution
  8. **Efficient Frontier** — optimal risk/return portfolio combinations
  9. **Factor Analysis** — Fama-French three-factor regression
- Quick-start preset portfolios, a built-in common-tickers reference, dynamic weight inputs, risk-free rate and VaR confidence sliders, and friendly error handling for invalid tickers

## Tech Stack

`Python` · `Streamlit` · `Pandas` · `NumPy` · `Plotly` · `yfinance`

## Risk Metrics Explained

**Volatility** — The standard deviation of daily returns, scaled to an annual figure (`std × √252`). It measures how much an asset's returns fluctuate; higher volatility means greater uncertainty/risk.

**Sharpe Ratio** — `(annualised return − risk-free rate) / annualised volatility`. It tells you how much excess return you're earning per unit of risk taken. A higher Sharpe ratio means better risk-adjusted performance.

**Value at Risk (VaR)** — An estimate of the worst expected loss over one day, at a given confidence level (e.g. 95%), based on the historical distribution of returns. For example, a 1-day 95% VaR of 2% means there's a 5% chance of losing more than 2% in a single day, based on historical data.

**Maximum Drawdown** — The largest peak-to-trough decline in cumulative portfolio value over the observed period. It captures the worst-case loss an investor would have experienced if they bought at the top and sold at the bottom.

**Correlation** — A measure (between -1 and 1) of how two assets' returns move together. Low or negative correlation between holdings is a key driver of diversification benefits in a portfolio.

**Alpha** — The annualised excess return a portfolio generates beyond what its Beta-implied exposure to a benchmark would predict. A positive alpha means the portfolio outperformed after adjusting for market risk.

**Beta** — A measure of how sensitive a portfolio is to movements in a benchmark (`Cov(portfolio, benchmark) / Var(benchmark)`). A beta of 1.2 means the portfolio tends to move 20% more than the benchmark in either direction.

**Risk Contribution** — Decomposes total portfolio volatility into each asset's share, accounting for correlation between holdings — not just its capital weight. An asset can have a small weight but a large risk contribution if it's volatile or weakly diversifying.

**Stress Testing** — Replays the portfolio's actual holdings and weights through specific historical crisis windows (e.g. the COVID-19 crash, the 2022 bear market) to see what loss it would have realistically experienced.

**Monte Carlo Simulation** — Generates thousands of random future return paths, drawn from the portfolio's historical mean and volatility, to show a *range* of plausible future outcomes rather than a single forecast.

**Efficient Frontier** — A set of portfolios, generated by randomly varying asset weights, that shows the best possible return for each level of risk. The "Max Sharpe" portfolio offers the best risk-adjusted return; the "Min Volatility" portfolio offers the lowest risk.

**Fama-French Three-Factor Model** — Extends CAPM by explaining returns through three factors: **Market** (overall equity risk), **SMB** ("Small Minus Big", small-cap vs. large-cap exposure), and **HML** ("High Minus Low", value vs. growth exposure). The regression's alpha is the return left unexplained by these factors.

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/financial-risk-dashboard.git
cd financial-risk-dashboard

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py
```

The app will open automatically in your browser, or you can navigate to **http://localhost:8501**.

## Live Demo

🔗 [Live Demo](https://financial-risk-dashboard-bucqq6dw7fuqy4u8mdpnln.streamlit.app)

## Project Structure

```
financial-risk-dashboard/
├── app.py                 # Streamlit dashboard (9 tabs: UI + charts + KPIs)
├── src/
│   ├── data_loader.py     # yfinance data download & cleaning
│   ├── metrics.py         # risk/return/optimisation metric calculations
│   └── factor_analysis.py # Fama-French factor download & OLS regression
├── requirements.txt
└── README.md
```

## Disclaimer

This project is for educational and portfolio-demonstration purposes only. It does not constitute financial advice.
