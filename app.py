from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Philippine Financial Instruments Comparison",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Philippine Financial Instruments Comparison Dashboard")
st.markdown("### Final Examination Project | BSMA – Financial Markets")
st.markdown("**As of date:** September 30, 2026")
st.caption(
    "Dashboard values below are transcribed from the project materials supplied by the user. "
    "Check the analysis workbook and original sources before submission; figures have not been independently audited."
)
st.divider()

# Performance and risk figures below were supplied in the user's Gemini-generated
# dashboard brief. They are presented as reported historical figures, not forecasts.
data = {
    "Instrument": [
        "1. Bank Time Deposit",
        "2. Treasury Bill (364-day)",
        "3. UITF (BPI Equity Index)",
        "4. Mutual Fund (First Metro Equity)",
        "5. Insurance VUL (Sun Life)",
        "6. Stock (Jollibee – JFC)",
    ],
    "Category": ["Money Market", "Money Market", "Capital Market", "Capital Market", "Capital Market", "Capital Market"],
    "Annual Return": [0.0535, 0.0575, 0.1240, 0.1180, 0.0950, 0.2288],
    "Risk (Volatility)": [0.0050, 0.0010, 0.1850, 0.1790, 0.1120, 0.2245],
    "Excess Return (vs T-Bill)": [-0.0040, 0.0000, 0.0665, 0.0605, 0.0375, 0.1713],
    "Return-to-Risk Ratio": [np.nan, np.nan, 0.3595, 0.3380, 0.3348, 0.7630],
    "Risk Classification": ["Low Risk", "Low Risk", "High Risk", "High Risk", "Moderate to High", "High Risk"],
    "Annual Fees": ["None", "None (Auction)", "1.00% p.a.", "1.50% p.a.", "2.00% p.a.", "Brokerage (~0.25%)"],
    "Min. Investment": ["₱5,000", "₱50,000", "₱10,000", "₱5,000", "₱2,000 / month", "1 Board Lot"],
    "Source": ["BDO Unibank", "Bureau of the Treasury", "BPI Asset Management", "First Metro Funds", "Sun Life Grepa", "PSE / Jollibee Foods Corp."],
    "Retrieval Date": ["September 30, 2026"] * 6,
}
df = pd.DataFrame(data)

comparison_tab, calculator_tab, chart_tab = st.tabs(
    ["📋 Instrument Comparison Table", "🧮 Compound Growth Calculator", "📈 Return vs. Risk Chart"]
)

with comparison_tab:
    st.subheader("Comparison of Philippine Financial Instruments")
    st.write(
        "Reported annual returns, annualized volatility, excess returns relative to the 364-day "
        "Treasury bill (listed at 5.75%), fees, and minimum investment requirements."
    )
    display_df = df.copy()
    for column in ["Annual Return", "Risk (Volatility)", "Excess Return (vs T-Bill)"]:
        display_df[column] = display_df[column].map(lambda value: f"{value:.2%}")
    display_df["Return-to-Risk Ratio"] = display_df["Return-to-Risk Ratio"].map(
        lambda value: f"{value:.4f}" if pd.notna(value) else "N/A"
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(
        "Values were supplied in the user's dashboard brief and should be reconciled with "
        "2_Financial_Analysis.xlsx and source documents. Ratios and return definitions may depend "
        "on the workbook's methodology."
    )

with calculator_tab:
    st.subheader("🧮 Interactive Future Value Calculator")
    st.caption(
        "Illustration assuming the selected reported annual return repeats unchanged each year. "
        "This is a hypothetical scenario, not an expected or guaranteed return."
    )
    left, right = st.columns(2)
    with left:
        principal = st.number_input(
            "Initial principal (₱)",
            min_value=1_000.0,
            max_value=10_000_000.0,
            value=100_000.0,
            step=5_000.0,
            format="%.2f",
        )
        years = st.slider("Investment horizon (years)", min_value=1, max_value=30, value=5)
    with right:
        selected = st.selectbox("Financial instrument", df["Instrument"].tolist())

    row = df.loc[df["Instrument"] == selected].iloc[0]
    rate = float(row["Annual Return"])
    if principal <= 0 or not np.isfinite(principal):
        st.error("Enter a valid positive principal amount.")
    elif rate <= -1:
        st.error("The selected annual return must be greater than -100% for this calculation.")
    else:
        years_range = np.arange(years + 1)
        values = principal * np.power(1 + rate, years_range)
        future_values = pd.DataFrame({"Year": years_range, "Illustrative Value (₱)": values})
        final_value = float(values[-1])
        st.metric(
            label=f"Illustrative value after {years} years",
            value=f"₱{final_value:,.2f}",
            delta=f"Change from principal: ₱{final_value - principal:,.2f}",
        )
        growth_fig = px.line(
            future_values,
            x="Year",
            y="Illustrative Value (₱)",
            title=f"Illustrative growth for {selected}",
            markers=True,
        )
        st.plotly_chart(growth_fig, use_container_width=True)
        st.caption(
            f"Formula: principal × (1 + {rate:.2%})^years. The calculation does not deduct fees, "
            "taxes, inflation, trading costs, insurance charges, or other product-specific costs."
        )

with chart_tab:
    st.subheader("📈 Risk–Return Spectrum")
    st.caption("Reported annual return and annualized volatility figures; verify their calculation period and methodology against the workbook.")
    chart_data = df.copy()
    chart_data["Annual Return (%)"] = chart_data["Annual Return"] * 100
    chart_data["Annualized Volatility (%)"] = chart_data["Risk (Volatility)"] * 100
    risk_fig = px.scatter(
        chart_data,
        x="Annualized Volatility (%)",
        y="Annual Return (%)",
        text="Instrument",
        color="Category",
        hover_data=["Risk Classification", "Excess Return (vs T-Bill)", "Source"],
        title="Reported return vs. volatility",
        labels={
            "Annualized Volatility (%)": "Annualized volatility (%) — risk proxy",
            "Annual Return (%)": "Reported annual return (%)",
        },
    )
    risk_fig.update_traces(textposition="top center")
    risk_fig.update_layout(legend_title_text="Category")
    st.plotly_chart(risk_fig, use_container_width=True)

st.divider()
st.warning(
    "⚠️ **Educational disclaimer:** Past performance is not a guarantee of future results. "
    "This dashboard is for academic and educational purposes only and is not financial advice. "
    "Bank deposits may be PDIC-insured subject to applicable limits and requirements; UITFs, "
    "mutual funds, VUL investments, Treasury bills, and listed shares are not PDIC-insured deposits. "
    "Confirm current coverage, terms, fees, and all figures with authoritative sources."
)
st.caption("Sources listed in the comparison table are source labels from the supplied project materials; the live dashboard does not independently verify them.")
