from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Philippine Financial Markets Comparison",
    page_icon="📊",
    layout="wide",
)
st.title("📊 Philippine Financial Markets Comparison Dashboard")
st.markdown("### Final Examination Project | BSMA – Financial Markets")
st.markdown("**Workbook retrieval date:** September 30, 2026")
st.caption(
    "Dashboard values are transcribed from the two workbook screenshots provided by the user. "
    "Where visible workbook summary cells conflict with supporting calculations, both are disclosed below. "
    "This dashboard is educational and not investment advice."
)

# Underlying values read from the workbook's Summary Comparison Table.
# For fund returns, the displayed 1-year future values reveal the more precise rates.
instruments = pd.DataFrame([
    {"Instrument": "Bank Time Deposit", "Category": "Money Market", "Annual Return": 0.0000, "Risk (Volatility)": 0.0050, "Risk Classification": "Low Risk", "Annual Fees": "None", "Min. Investment": "₱5,000", "Source": "BDO Unibank"},
    {"Instrument": "Treasury Bill (364-day)", "Category": "Money Market", "Annual Return": 0.0575, "Risk (Volatility)": 0.0010, "Risk Classification": "Low Risk", "Annual Fees": "None (Auction)", "Min. Investment": "₱50,000", "Source": "Bureau of the Treasury"},
    {"Instrument": "UITF (BPI Equity Index)", "Category": "Capital Market", "Annual Return": 0.1240, "Risk (Volatility)": 0.1850, "Risk Classification": "High Risk", "Annual Fees": "1.00% p.a.", "Min. Investment": "₱10,000", "Source": "BPI Asset Management"},
    {"Instrument": "Mutual Fund (First Metro Equity)", "Category": "Capital Market", "Annual Return": 0.1180, "Risk (Volatility)": 0.1790, "Risk Classification": "High Risk", "Annual Fees": "1.50% p.a.", "Min. Investment": "₱5,000", "Source": "First Metro Funds"},
    {"Instrument": "VUL Insurance Fund (Sun Life)", "Category": "Capital Market", "Annual Return": 0.0950, "Risk (Volatility)": 0.1120, "Risk Classification": "Moderate to High", "Annual Fees": "2.00% p.a.", "Min. Investment": "₱2,000 / month", "Source": "Sun Life Grepa"},
    {"Instrument": "Stock (Jollibee Foods Corp. – JFC)", "Category": "Capital Market", "Annual Return": 0.2083333, "Risk (Volatility)": 0.2245, "Risk Classification": "High Risk", "Annual Fees": "Brokerage (~0.25%)", "Min. Investment": "1 Board Lot", "Source": "PSE / Jollibee Foods Corp."},
])
RISK_FREE_RATE = 0.0575

# Monthly price observations and cash dividends transcribed from the JFC analysis screenshot.
jfc = pd.DataFrame([
    ("2025-09-30", 240.00, 0.00, "Base Price"),
    ("2025-10-31", 245.50, 0.00, ""),
    ("2025-11-28", 252.00, 1.00, "Regular Cash Dividend"),
    ("2025-12-29", 248.00, 0.00, ""),
    ("2026-01-30", 260.00, 0.00, ""),
    ("2026-02-27", 255.50, 0.00, ""),
    ("2026-03-31", 268.00, 1.20, "Q1 Cash Dividend"),
    ("2026-04-30", 265.00, 0.00, ""),
    ("2026-05-29", 272.50, 0.00, ""),
    ("2026-06-30", 280.00, 1.20, "Q2 Cash Dividend"),
    ("2026-07-31", 275.00, 0.00, ""),
    ("2026-08-31", 285.00, 0.00, ""),
    ("2026-09-30", 290.00, 1.50, "Q3 Cash Dividend"),
], columns=["Date", "Closing Price (PHP)", "Cash Dividend / Share (PHP)", "Notes"])
jfc["Date"] = pd.to_datetime(jfc["Date"])
jfc["Monthly Return"] = jfc["Closing Price (PHP)"].pct_change()
jfc["Monthly Total Return"] = (
    jfc["Closing Price (PHP)"] + jfc["Cash Dividend / Share (PHP)"]
) / (jfc["Closing Price (PHP)"].shift(1)) - 1

# Workbook's Bank TD inputs from Part A. 4 compounds per year (quarterly).
td_nominal = 0.0525
td_frequency = 4
td_ear = (1 + td_nominal / td_frequency) ** td_frequency - 1

# Part C portfolio weights shown in the workbook. Order aligns with instruments.
portfolio_weights = {
    "Conservative Portfolio": [0.50, 0.40, 0.05, 0.05, 0.00, 0.00],
    "Moderate Portfolio": [0.20, 0.20, 0.25, 0.25, 0.10, 0.00],
    "Aggressive Portfolio": [0.05, 0.05, 0.35, 0.35, 0.10, 0.10],
}

comparison_tab, jfc_tab, calc_tab, portfolio_tab, sources_tab = st.tabs([
    "📋 Instrument Comparison", "🍗 JFC Price & Return Analysis", "🧮 TD Compound Growth",
    "📈 Risk & Portfolios", "ℹ️ Data and Sources",
])

with comparison_tab:
    st.subheader("Part B — Summary Comparison Table")
    table = instruments.copy()
    table["Risk-Free Rate"] = RISK_FREE_RATE
    table["Excess Return"] = table["Annual Return"] - RISK_FREE_RATE
    table["Return-to-Risk Ratio"] = np.where(
        table["Risk (Volatility)"].gt(0),
        table["Excess Return"] / table["Risk (Volatility)"],
        np.nan,
    )
    table["Value of ₱100,000 after 1 Year"] = 100000 * (1 + table["Annual Return"])
    table["Rank by Return"] = table["Annual Return"].rank(method="min", ascending=False).astype(int)
    table["Rank by Return-to-Risk"] = table["Return-to-Risk Ratio"].rank(method="min", ascending=False, na_option="bottom").astype(int)
    display = table.copy()
    for col in ["Annual Return", "Risk (Volatility)", "Risk-Free Rate", "Excess Return"]:
        display[col] = display[col].map(lambda v: f"{v:.2%}")
    display["Return-to-Risk Ratio"] = display["Return-to-Risk Ratio"].map(lambda v: f"{v:.4f}" if pd.notna(v) else "N/A")
    display["Value of ₱100,000 after 1 Year"] = display["Value of ₱100,000 after 1 Year"].map(lambda v: f"₱{v:,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.markdown("**Workbook discrepancy to review:** Part A gives the bank time-deposit nominal rate as 5.25% compounded quarterly, which yields an effective annual rate of **5.35%**. But Part B appears to show a 0% annual return and ₱100,000 one-year value for that deposit. This dashboard preserves the Part B 0% comparison value while showing the Part A EAR in its own calculator; please correct or confirm the workbook before final submission.")
    st.markdown("**Other source-sheet check:** The JFC price/dividend observations yield 22.88% total return using (₱290 + ₱4.90 − ₱240) / ₱240, while Part B appears to show about 20.83% (rounded 21%). The dashboard displays both the reported Part B comparison and the direct calculation from Part A's monthly values.")

with jfc_tab:
    st.subheader("Jollibee Foods Corporation (JFC) — Monthly History")
    st.caption("September 2025–September 2026 values transcribed from the supplied Stock Analysis screenshot; not live quotes.")
    price_fig = px.line(jfc, x="Date", y="Closing Price (PHP)", markers=True, title="JFC monthly closing price")
    st.plotly_chart(price_fig, use_container_width=True)
    total_dividends = float(jfc["Cash Dividend / Share (PHP)"].sum())
    start_price = float(jfc.iloc[0]["Closing Price (PHP)"])
    end_price = float(jfc.iloc[-1]["Closing Price (PHP)"])
    simple_price_return = end_price / start_price - 1
    total_return = (end_price + total_dividends - start_price) / start_price
    avg_monthly_return = float(jfc["Monthly Return"].dropna().mean())
    annualized_vol = float(jfc["Monthly Return"].dropna().std(ddof=1) * np.sqrt(12))
    cols = st.columns(4)
    cols[0].metric("Start price", f"₱{start_price:.2f}")
    cols[1].metric("End price", f"₱{end_price:.2f}")
    cols[2].metric("Dividends / share", f"₱{total_dividends:.2f}")
    cols[3].metric("Price + dividend return", f"{total_return:.2%}")
    st.write(f"Average monthly price return: **{avg_monthly_return:.2%}** · Sample standard-deviation annualized volatility: **{annualized_vol:.2%}** · Price-only return: **{simple_price_return:.2%}**.")
    st.dataframe(jfc.assign(Date=jfc["Date"].dt.strftime("%b %d, %Y")).style.format({"Closing Price (PHP)": "₱{:,.2f}", "Cash Dividend / Share (PHP)": "₱{:,.2f}", "Monthly Return": "{:.2%}", "Monthly Total Return": "{:.2%}"}), use_container_width=True, hide_index=True)
    st.warning("The screenshot's dividend-total cell appears to sum the monthly return column and display 490.00%. Summing the visible cash dividends gives ₱4.90 per share. The direct 12-month total return is therefore 22.88%; confirm/correct the source workbook formula. The workbook's Part A volatility (8.74%) also differs from Part B's stock volatility (22.45%).")

with calc_tab:
    st.subheader("Part A — Bank Time Deposit Effective Annual Rate")
    st.write("EAR = (1 + nominal rate / compounding periods) ^ compounding periods − 1")
    left, right = st.columns(2)
    with left:
        nominal_rate = st.number_input("Nominal annual rate (%)", min_value=0.0, max_value=100.0, value=td_nominal * 100, step=0.05) / 100
        compounds = st.number_input("Compounding periods per year", min_value=1, max_value=365, value=td_frequency, step=1)
    effective_rate = (1 + nominal_rate / compounds) ** compounds - 1
    right.metric("Effective annual rate (EAR)", f"{effective_rate:.4%}")
    st.subheader("Compound growth illustration")
    principal = st.number_input("Principal (PHP)", min_value=1000.0, max_value=10000000.0, value=100000.0, step=5000.0, key="principal")
    horizon = st.slider("Investment horizon (years)", 1, 30, 5)
    years = np.arange(horizon + 1)
    future_values = pd.DataFrame({"Year": years, "Future Value (PHP)": principal * (1 + effective_rate) ** years})
    st.metric(f"Illustrative value after {horizon} years", f"₱{future_values.iloc[-1]['Future Value (PHP)']:,.2f}", delta=f"Gain: ₱{future_values.iloc[-1]['Future Value (PHP)'] - principal:,.2f}")
    st.plotly_chart(px.line(future_values, x="Year", y="Future Value (PHP)", markers=True, title="Bank time-deposit compound growth at entered EAR"), use_container_width=True)
    st.caption("Assumes the nominal rate and quarterly compounding remain constant; ignores tax and product-specific terms. This is illustrative, not a bank quote.")

with portfolio_tab:
    st.subheader("Return vs. risk across financial instruments")
    scatter = px.scatter(instruments, x="Risk (Volatility)", y="Annual Return", color="Category", text="Instrument", hover_data=["Risk Classification", "Source"], labels={"Risk (Volatility)": "Annual volatility (workbook summary)", "Annual Return": "Annual return (workbook summary)"}, title="Workbook summary return and volatility")
    scatter.update_traces(textposition="top center")
    st.plotly_chart(scatter, use_container_width=True)
    st.subheader("Part C — Model Portfolio Allocation & Performance")
    rows = []
    for name, weights in portfolio_weights.items():
        weight_sum = sum(weights)
        weighted_return = float(np.dot(weights, instruments["Annual Return"]))
        simple_weighted_risk = float(np.dot(weights, instruments["Risk (Volatility)"]))
        rows.append({"Portfolio Profile": name, "Total Weight": weight_sum, "Weighted Annual Return": weighted_return, "Simple Weighted Risk": simple_weighted_risk, "Value of ₱100,000 after 1 Year": 100000 * (1 + weighted_return)})
    portfolio_df = pd.DataFrame(rows)
    shown = portfolio_df.copy()
    for col in ["Total Weight", "Weighted Annual Return", "Simple Weighted Risk"]:
        shown[col] = shown[col].map(lambda v: f"{v:.2%}")
    shown["Value of ₱100,000 after 1 Year"] = shown["Value of ₱100,000 after 1 Year"].map(lambda v: f"₱{v:,.2f}")
    st.dataframe(shown, use_container_width=True, hide_index=True)
    st.caption("Portfolio figures recomputed from the displayed Part B returns/volatilities and screenshot weights. ‘Simple weighted risk’ is a weighted average, not portfolio standard deviation; true portfolio risk needs asset correlations/covariances.")
    with st.expander("Portfolio weights from workbook"):
        weights_df = pd.DataFrame(portfolio_weights, index=instruments["Instrument"]).T
        st.dataframe(weights_df.style.format("{:.0%}"), use_container_width=True)

with sources_tab:
    st.subheader("Data and Sources")
    st.write("Instrument labels and terms are from the Data and Sources screenshot previously provided. Summary returns, volatilities, risk-free rate, portfolio weights, bank-deposit inputs, and JFC monthly observations are transcribed from the two latest workbook screenshots. Retrieval date in workbook: September 30, 2026.")
    st.dataframe(instruments, use_container_width=True, hide_index=True)
    st.markdown("**Source limitations:** Source names shown in the workbook are not independently validated by this dashboard. JFC prices and cash dividends are static workbook observations, not live data. Validate details against BDO, Bureau of the Treasury, BPI, First Metro, Sun Life Grepa, and the PSE before submission.")
    csv = instruments.to_csv(index=False).encode("utf-8")
    st.download_button("Download instrument comparison CSV", csv, "philippine-market-comparison.csv", "text/csv")

st.divider()
st.warning("Educational project only; not financial, investment, tax, or legal advice. Past returns do not predict future results. Confirm provider terms, fees, PDIC eligibility/limits, and workbook calculations with authoritative sources.")
