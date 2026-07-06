"""
Keep-Alive Script for Streamlit Dashboard
==========================================

This script prevents your Streamlit app from being put to sleep by cloud hosting services.
It makes periodic HTTP requests to your app's URL to keep it active.

DEPLOYMENT OPTIONS:

1. **LOCAL/DEVELOPMENT**: Run this alongside your Streamlit app
   python keep_alive.py

2. **HEROKU**: Deploy as a separate dyno
   - Create a Procfile with: worker: python keep_alive.py
   - Set STREAMLIT_APP_URL in your environment variables

3. **RENDER**: Deploy as a background worker
   - Add to render.yaml:
     services:
       - type: web
         name: dashboard
         buildCommand: pip install -r requirements.txt
         startCommand: streamlit run dashboard.py
       
       - type: background_worker
         name: keep-alive
         buildCommand: pip install -r requirements.txt
         startCommand: python keep_alive.py

4. **AWS/EC2**: Run as a systemd service
   - Create /etc/systemd/system/streamlit-keepalive.service
   - Enable and start: sudo systemctl enable streamlit-keepalive

CONFIGURATION:
- APP_URL: Set the environment variable or edit the default below
- PING_INTERVAL: Adjust frequency (default 3 minutes)
- TIMEOUT: Connection timeout in seconds
"""

import os
import sys
import time
from datetime import datetime
from urllib import error, request

# Configuration
APP_URL = os.getenv("STREAMLIT_APP_URL", "http://localhost:8501")
PING_INTERVAL = int(os.getenv("KEEP_ALIVE_INTERVAL", 180))  # 3 minutes default
TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 5


def ping_app() -> bool:
    """
    Send a ping request to the Streamlit app.
    
    Returns True if successful, False otherwise.
    """
    try:
        req = request.Request(APP_URL, method="GET")
        req.add_header("User-Agent", "Streamlit-KeepAlive/1.0")
        
        with request.urlopen(req, timeout=TIMEOUT) as response:
            status_code = response.status
            content_length = response.headers.get("Content-Length", "unknown")
            
            if status_code == 200:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(
                    f"[{timestamp}] ✓ Keep-alive ping successful (Status: {status_code}, "
                    f"Content: {content_length} bytes)"
                )
                return True
            else:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"⚠ Unexpected status code: {status_code}"
                )
                return False
                
    except error.HTTPError as exc:
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"✗ HTTP Error {exc.code}: {exc.reason}"
        )
        return False
        
    except error.URLError as exc:
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"✗ Connection failed: {exc.reason}"
        )
        return False
        
    except Exception as exc:
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"✗ Error: {type(exc).__name__}: {exc}"
        )
        return False


def keep_alive_loop():
    """
    Main loop for the keep-alive service.
    Sends periodic pings to the app with retry logic.
    """
    print(f"Starting Streamlit Keep-Alive Service")
    print(f"Target URL: {APP_URL}")
    print(f"Ping interval: {PING_INTERVAL} seconds ({PING_INTERVAL / 60:.1f} minutes)")
    print(f"Max retries: {MAX_RETRIES}")
    print(f"Retry delay: {RETRY_DELAY} seconds")
    print("=" * 70)
    print()
    
    startup_delay = 10  # Wait for app to start on first run
    print(f"Waiting {startup_delay} seconds for app startup...")
    time.sleep(startup_delay)
    
    consecutive_failures = 0
    
    while True:
        try:
            # Attempt ping with retries
            success = False
            for attempt in range(MAX_RETRIES):
                if ping_app():
                    success = True
                    consecutive_failures = 0
                    break
                
                if attempt < MAX_RETRIES - 1:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
            
            if not success:
                consecutive_failures += 1
                print(
                    f"All {MAX_RETRIES} attempts failed. "
                    f"Consecutive failures: {consecutive_failures}"
                )
                
                # Alert after multiple failures
                if consecutive_failures >= 3:
                    print(
                        "⚠ WARNING: App appears to be down. Check your Streamlit server."
                    )
            
            # Wait for next ping
            print(f"Sleeping for {PING_INTERVAL} seconds until next ping...")
            print()
            time.sleep(PING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\nKeep-alive service stopped by user.")
            sys.exit(0)
            
        except Exception as exc:
            print(f"\nUnexpected error in main loop: {exc}")
            print("Attempting to recover in 30 seconds...")
            time.sleep(30)


if __name__ == "__main__":
    if not APP_URL or APP_URL == "http://localhost:8501":
        print("WARNING: Using default localhost URL.")
        print("For remote deployment, set STREAMLIT_APP_URL environment variable.")
        print(f"Example: export STREAMLIT_APP_URL='https://your-app.com'")
        print()
    
    try:
        keep_alive_loop()
    except KeyboardInterrupt:
        print("\n\nService terminated.")
        sys.exit(0)
