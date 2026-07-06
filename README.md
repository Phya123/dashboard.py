# dashboard.py

A simple Streamlit dashboard for trading operations. It can display sample data out of the box or connect to the Alpaca trading API when the required environment variables are set.

## Run locally

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Optional live data connection

Set these variables before launching the app:

```bash
export APCA_API_KEY_ID=your_key
export APCA_API_SECRET_KEY=your_secret
export APCA_API_BASE_URL=https://paper-api.alpaca.markets
```
