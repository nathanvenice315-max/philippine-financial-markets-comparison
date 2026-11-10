# Philippine Financial Markets Comparison Dashboard

Streamlit dashboard based on the provided workbook screenshots.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
2. Create a new app and select this repository, branch `main`, and `app.py`.
3. Deploy, wait for a successful build, and copy the generated URL into `4_Live_App_Link.txt`.

The app has already been deployed by the owner according to their message. Put the exact Streamlit URL into `4_Live_App_Link.txt`; never guess a URL.

## Dashboard contents

- Part B instrument comparison table with returns, risk, excess return, return-to-risk, ranks, and one-year illustration.
- JFC monthly price/dividend chart and calculations using September 2025–September 2026 workbook observations.
- Bank time-deposit EAR calculator (5.25% nominal, quarterly compounding by default) and compound-growth illustration.
- Workbook's conservative, moderate, and aggressive model portfolios with recomputed weighted return and simple weighted risk.
- Data/source notes and CSV download.

## Workbook issues called out in the app

- The Bank TD Part A input (5.25%, compounded four times annually) implies about 5.35% EAR, while the Part B summary appears to report 0% return and ₱100,000 one-year value. Comparison retains the Part B value; the calculator uses Part A inputs.
- Visible JFC monthly prices/dividends imply ₱4.90 total dividends and 22.88% price-plus-dividend return, differing from the summary's approximately 20.83% return. The dividend-total cell appears to sum monthly returns by mistake and display 490.00%.
- JFC annualized volatility in the stock worksheet (8.74%) differs from the Part B summary (22.45%). The dashboard shows both and labels their workbook origin.
- Portfolio risk is displayed as the workbook's simple weighted-risk method; it is not true portfolio volatility without covariance/correlation data.

Figures are transcribed from screenshots, not independently audited or live-verified. Please correct discrepancies in the workbook and confirm source terms before submission.
