# Procfile for Heroku and similar platforms
# Runs both the Streamlit dashboard and the keep-alive service

web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
worker: python keep_alive.py
