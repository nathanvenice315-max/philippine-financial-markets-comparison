from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Philippine Financial Markets Comparison", page_icon="🇵🇭", layout="wide")
st.title("🇵🇭 Philippine Financial Markets Comparison")
st.caption("Compare the six instruments in the project’s Data and Sources sheet. Terms shown below are transcribed from the provided screenshot; verify them with each provider before investing.")

AS_OF = "September 30, 2026"
INSTRUMENTS = [
    {"Instrument": "Bank Time Deposit", "Provider / Source Name": "BDO Unibank (1-Year Peso Time Deposit)", "Type": "Money Market", "Risk Classification": "Low Risk", "Annual Fees": "None", "Minimum Investment": "₱5,000.00", "Redemption Settlement": "At Maturity", "PDIC Insured?": "Yes (Up to ₱1M)"},
    {"Instrument": "Treasury Bill", "Provider / Source Name": "Bureau of the Treasury (364-day T-Bill Auction)", "Type": "Money Market / Fixed Income", "Risk Classification": "Low Risk", "Annual Fees": "None (Auction)", "Minimum Investment": "₱50,000.00", "Redemption Settlement": "Secondary Market / Maturity", "PDIC Insured?": "No (Govt. Backed)"},
    {"Instrument": "UITF", "Provider / Source Name": "BPI Asset Management (Philippine Equity Index Fund)", "Type": "Capital Market (Equity)", "Risk Classification": "High Risk", "Annual Fees": "1.00% p.a.", "Minimum Investment": "₱10,000.00", "Redemption Settlement": "T + 3 Business Days", "PDIC Insured?": "No"},
    {"Instrument": "Mutual Fund", "Provider / Source Name": "First Metro Philippine Equity Fund, Inc.", "Type": "Capital Market (Equity)", "Risk Classification": "High Risk", "Annual Fees": "1.50% p.a.", "Minimum Investment": "₱5,000.00", "Redemption Settlement": "T + 7 Business Days", "PDIC Insured?": "No"},
    {"Instrument": "Insurance Fund (VUL)", "Provider / Source Name": "Sun Life Grepa Financial (Sun MaxiLink Prime)", "Type": "Capital Market (Balanced)", "Risk Classification": "Moderate to High", "Annual Fees": "2.00% p.a.", "Minimum Investment": "₱2,000 / month", "Redemption Settlement": "T + 5 to 7 Business Days", "PDIC Insured?": "No"},
    {"Instrument": "Stock", "Provider / Source Name": "Philippine Stock Exchange (Jollibee Foods Corp. - JFC)", "Type": "Capital Market (Equity)", "Risk Classification": "High Risk", "Annual Fees": "Brokerage Comm. (~0.25%)", "Minimum Investment": "1 Board Lot (Current Price)", "Redemption Settlement": "T + 2 Business Days", "PDIC Insured?": "No"},
]
terms = pd.DataFrame(INSTRUMENTS)

comparison_tab, analysis_tab, projection_tab, sources_tab = st.tabs(["Overview & Comparison", "Stock Analysis (JFC)", "Comparison & Projection", "Data and Sources"])

with comparison_tab:
    st.subheader("Compare the instruments")
    st.dataframe(terms, use_container_width=True, hide_index=True)
    st.info("Risk labels, minimums, costs, and settlement terms are copied from the supplied project screenshot (retrieval date: September 30, 2026). They are not live-verified. Confirm current terms directly with the named institution.")
    st.markdown("**Quick take:** The source classifies the time deposit and Treasury bill as low risk, with equities, equity funds, and VUL carrying higher risk. Deposit insurance is shown only for the bank deposit (subject to the listed limit); Treasury bills are marked government-backed, not PDIC-insured. Past performance and capital protection are not implied by these labels.")

with analysis_tab:
    st.subheader("Jollibee Foods Corporation (PSE: JFC)")
    st.write("The source identifies JFC as the stock example. Historical prices are fetched from Yahoo Finance when available; this is market-price context, not a complete fundamental analysis or a recommendation.")
    period = st.selectbox("Price history", ["6 months", "1 year", "2 years", "5 years"], index=1, key="jfc_period")
    period_map = {"6 months": "6mo", "1 year": "1y", "2 years": "2y", "5 years": "5y"}
    try:
        history = yf.Ticker("JFC.PS").history(period=period_map[period], auto_adjust=True)
        closes = history["Close"].dropna() if not history.empty and "Close" in history else pd.Series(dtype=float)
        if closes.empty:
            st.warning("JFC.PS price history is currently unavailable. Try again later; confirm prices with the PSE or your broker.")
        else:
            price_df = pd.DataFrame({"Date": pd.to_datetime(closes.index).tz_localize(None), "Adjusted close (PHP)": closes.to_numpy()})
            first_price, last_price = float(closes.iloc[0]), float(closes.iloc[-1])
            pct = (last_price / first_price - 1) * 100 if first_price else 0
            a, b, c = st.columns(3)
            a.metric("Latest adjusted close", f"₱{last_price:,.2f}")
            b.metric("Change over displayed period", f"{pct:+.2f}%")
            c.metric("Observations", f"{len(closes):,}")
            st.plotly_chart(px.line(price_df, x="Date", y="Adjusted close (PHP)", title="JFC adjusted historical price"), use_container_width=True)
            st.caption("Source: Yahoo Finance symbol JFC.PS, retrieved when this page loads. Historical return excludes dividends, taxes, and transaction costs; prices may be delayed or incomplete.")
    except Exception as exc:
        st.warning(f"Could not retrieve JFC price data: {exc}. Confirm market data with the PSE or your broker.")
    st.markdown("**Risk reminder:** A single stock can lose value and is not PDIC-insured. This dashboard does not calculate valuation ratios or company financial-statement metrics because those data and instructions were not present in the supplied screenshot.")

with projection_tab:
    st.subheader("Illustrative investment projection")
    st.write("Set your own annual return assumptions. The source screenshot does not provide expected returns, so this tool does not invent forecasts. Values are hypothetical, not guaranteed.")
    amount = st.number_input("Initial amount (PHP)", min_value=0.0, value=50000.0, step=5000.0, format="%.2f")
    years = st.slider("Investment horizon (years)", 1, 30, 5)
    selected = st.multiselect("Instruments", terms["Instrument"].tolist(), default=terms["Instrument"].tolist())
    assumptions = {}
    grid = st.columns(3)
    for i, instrument in enumerate(selected):
        assumptions[instrument] = grid[i % 3].number_input(f"{instrument}: assumed annual gross return (%)", min_value=-100.0, max_value=100.0, value=0.0, step=0.5, key=f"rate_{instrument}")
    fee_rates = {"Bank Time Deposit": 0.0, "Treasury Bill": 0.0, "UITF": 1.0, "Mutual Fund": 1.5, "Insurance Fund (VUL)": 2.0, "Stock": 0.25}
    rows = []
    for instrument, gross_pct in assumptions.items():
        fee_pct = fee_rates[instrument]
        net_pct = gross_pct - fee_pct
        end_value = amount * (1 + net_pct / 100) ** years
        rows.append({"Instrument": instrument, "Assumed gross return (%/yr)": gross_pct, "Fee estimate (%/yr)": fee_pct, "Illustrative net return (%/yr)": net_pct, "Starting amount (PHP)": amount, "Value after horizon (PHP)": end_value, "Illustrative gain / loss (PHP)": end_value - amount})
    if rows:
        result = pd.DataFrame(rows)
        st.dataframe(result.style.format({"Assumed gross return (%/yr)": "{:.2f}%", "Fee estimate (%/yr)": "{:.2f}%", "Illustrative net return (%/yr)": "{:.2f}%", "Starting amount (PHP)": "₱{:,.2f}", "Value after horizon (PHP)": "₱{:,.2f}", "Illustrative gain / loss (PHP)": "₱{:,.2f}"}), use_container_width=True, hide_index=True)
        chart = px.bar(result, x="Instrument", y="Value after horizon (PHP)", color="Instrument", title="Hypothetical value at end of horizon")
        st.plotly_chart(chart, use_container_width=True)
    st.caption("Formula: ending value = initial amount × (1 + (assumed gross annual return − listed annual fee) / 100) ^ years. This simplified estimate excludes taxes, inflation, trading costs, changing fees, contributions, VUL insurance charges, and differences in payout/settlement. Stock brokerage is a transaction commission, not an annual management fee; its 0.25% is shown only as a rough single-rate comparison and is not compounded as a recurring annual charge. Treasury bill auction yield is not a management fee.")

with sources_tab:
    st.subheader("Data and Sources")
    st.dataframe(terms, use_container_width=True, hide_index=True)
    st.markdown("**Retrieval date shown in supplied screenshot:** September 30, 2026. **JFC historical price source:** Yahoo Finance, ticker `JFC.PS`, fetched on demand. **Terms source:** user's screenshot of the workbook's Data and Sources sheet; original provider documents were not independently checked. The exact four-page Financial Analysis PDF was supplied as compressed PDF object data, not readable text, and its other worksheets/instructions could not be verified.")
    st.download_button("Download comparison table (CSV)", terms.to_csv(index=False).encode("utf-8"), "philippine-financial-instruments.csv", "text/csv")

st.divider()
st.caption("For educational purposes only; not financial, investment, tax, or legal advice. Verify product terms and market data with the institution, PSE, Bureau of the Treasury, or other official source before acting.")
