# Philippine Financial Markets Comparison

Streamlit dashboard based on the provided Data and Sources screenshot, featuring a comparison of six instruments, JFC historical price context, and an editable hypothetical projection calculator.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2. Create a new app and select this repository, the `main` branch, and `app.py`.
3. Deploy and wait for Streamlit to build the app.
4. Copy the exact URL generated after a successful deployment into `4_Live_App_Link.txt`.

A live public link cannot be guessed or generated without completing deployment through the repository owner's Streamlit Community Cloud account. `4_Live_App_Link.txt` remains explicit that deployment is pending until then.

## Included pages

- **Overview & Comparison:** the six instruments and terms visible in the provided spreadsheet screenshot.
- **Stock Analysis (JFC):** on-demand historical `JFC.PS` price chart and period change from Yahoo Finance. It is not a fundamental valuation.
- **Comparison & Projection:** user-editable assumptions for hypothetical compounded values; outputs are not forecasts.
- **Data and Sources:** source notes, the comparison table, and CSV download.

## Data cautions

Terms are transcribed from the user's screenshot, with a retrieval date of September 30, 2026, and have not been independently verified against current provider documentation. JFC price data is fetched from Yahoo Finance and can be delayed or incomplete. The raw compressed PDF streams provided in the conversation were not readable as assignment text, so any requirements not visible in the screenshot still need confirmation against the original workbook/PDF. Educational use only; not investment advice.
