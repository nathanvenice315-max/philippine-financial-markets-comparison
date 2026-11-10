# Philippine Financial Instruments Comparison Dashboard

Interactive Streamlit dashboard for the user's Philippine financial markets final-exam project.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) with the GitHub account that can access this repository.
2. Create a new app and select this repository, branch `main`, and entry point `app.py`.
3. Deploy. Wait for a successful build, then copy Streamlit's generated URL into `4_Live_App_Link.txt`.

A live public link cannot be guessed or created from repository files alone. Deployment requires authorization through the owner's Streamlit Community Cloud account. The link text file remains marked pending until the real URL is generated.

## Dashboard

- Instrument comparison table using the returns, volatility, fees, source labels, minimums, and classifications supplied in the user's dashboard brief.
- Compound growth calculator with user-selectable principal and time horizon.
- Return-versus-volatility scatter chart.
- Educational disclaimer and data-verification cautions.

**Important:** Performance figures were supplied in the user's prompt and have not been independently validated against the workbook. The calculator repeats a reported historical annual return as a hypothetical assumption; it is not a forecast. Verify figures and methodology against the original analysis workbook and source materials before submission.
