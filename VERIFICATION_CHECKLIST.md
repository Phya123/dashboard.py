# Optimization Verification Checklist

Use this checklist to verify that all optimizations have been properly implemented and are working correctly.

## Pre-Deployment Checklist

### Code Review
- [ ] Session state initialization in `dashboard.py` includes all cache variables
- [ ] Cache TTL values are set appropriately (30s, 60s, 300s)
- [ ] `load_dashboard_data()` checks cache freshness before fetching
- [ ] All expensive operations are wrapped in cache logic
- [ ] `keep_alive.py` is executable and syntactically correct
- [ ] `cache_monitor.py` imports work correctly
- [ ] No hardcoded credentials in any file

### File Verification
- [ ] `dashboard.py` - Modified with session state caching
- [ ] `keep_alive.py` - New keep-alive service
- [ ] `cache_monitor.py` - New cache monitoring module
- [ ] `OPTIMIZATION_GUIDE.md` - Deployment guide exists
- [ ] `OPTIMIZATION_QUICK_START.md` - Quick reference exists
- [ ] `IMPLEMENTATION_DETAILS.md` - Technical details exists
- [ ] `Procfile` - Heroku deployment config exists
- [ ] `Dockerfile` - Docker image config exists
- [ ] `docker-compose.yml` - Local dev setup exists
- [ ] `.env.example` - Environment template exists
- [ ] `.streamlit/config.toml` - Updated with optimization notes

### Configuration Review
- [ ] `.streamlit/config.toml` has performance settings
- [ ] `.env.example` has all required variables
- [ ] No `.env` file committed to git (check .gitignore)
- [ ] All imports in modified files are correct

## Local Development Testing

### Test 1: Basic Cache Functionality
```bash
# Start app
streamlit run dashboard.py

# In browser:
# 1. Open http://localhost:8501
# 2. Note the load time (should be 5-8s first time)
# 3. Refresh page (F5)
# 4. Note the load time (should be 0.3-0.5s)
# 5. Wait 30+ seconds
# 6. Refresh again (should re-fetch, 5-8s)
```
- [ ] First load takes 5-8 seconds
- [ ] Page refresh takes 0.3-0.5 seconds
- [ ] Data refreshes after TTL expires

### Test 2: Cache Monitor
```python
# In dashboard.py, add before final line:
with st.expander("Cache Status"):
    from cache_monitor import display_cache_status
    display_cache_status()

# In browser:
# 1. Open the "Cache Status" expander
# 2. Verify cache items are shown
# 3. Refresh page
# 4. Verify cache ages reset or stay minimal
```
- [ ] Cache status expander displays
- [ ] Shows all cache items (dashboard, market_data, etc.)
- [ ] Cache ages are reasonable
- [ ] "Fresh" indicator shows correctly

### Test 3: Session State Persistence
```bash
# 1. Open app in two browser tabs
# 2. In Tab 1: Simulate some interaction (e.g., wait 20s)
# 3. In Tab 2: Refresh the page
# 4. Verify both tabs show same data state
```
- [ ] Session state persists across tabs
- [ ] Bot commands logged set is preserved
- [ ] Cache data is shared in same session

### Test 4: Keep-Alive (Optional Local)
```bash
# Terminal 1: streamlit run dashboard.py
# Terminal 2: python keep_alive.py

# Check output:
# [2024-01-01 12:00:00] ✓ Keep-alive ping successful (Status: 200, Content: 45234 bytes)
# [2024-01-01 12:03:00] ✓ Keep-alive ping successful (Status: 200, Content: 45234 bytes)
```
- [ ] Keep-alive script starts without errors
- [ ] Pings appear every 3 minutes in logs
- [ ] HTTP 200 status shown
- [ ] No errors or warnings

### Test 5: Docker Local Development
```bash
docker-compose up
# In browser: http://localhost:8501

# Test same as Test 1 above
```
- [ ] Dashboard loads in Docker
- [ ] Cache functionality works
- [ ] Keep-alive runs in separate container
- [ ] Logs visible for both services

## Deployment Preparation

### Environment Variables
- [ ] `APCA_API_KEY_ID` set correctly
- [ ] `APCA_API_SECRET_KEY` set correctly
- [ ] `APCA_API_BASE_URL` set (paper or live)
- [ ] `STREAMLIT_APP_URL` matches deployment URL (for keep-alive)
- [ ] `KEEP_ALIVE_INTERVAL` set (180 for 3 minutes)

### Deployment-Specific

#### For Render
- [ ] Created Web Service for dashboard
- [ ] Created Background Worker for keep-alive
- [ ] Environment variables set in both services
- [ ] GitHub repo connected
- [ ] Build command correct
- [ ] Start command correct
- [ ] Both services are running (check "Logs")

#### For Heroku
- [ ] Procfile present in repo
- [ ] `heroku config:set` environment variables
- [ ] `heroku ps:scale web=1 worker=1` run
- [ ] Dyno logs show both running

#### For AWS EC2
- [ ] Systemd services created for both
- [ ] Services enabled: `sudo systemctl enable ...`
- [ ] Services started: `sudo systemctl start ...`
- [ ] Status verified: `sudo systemctl status ...`

#### For Docker
- [ ] `docker-compose.yml` present
- [ ] Environment variables in `.env`
- [ ] `docker-compose up` succeeds
- [ ] Both services healthy

## Post-Deployment Testing

### Test 1: Initial Load
```
Visit your deployed app URL
Time the page load
Expected: 5-8 seconds
```
- [ ] Page loads successfully
- [ ] All data displays correctly
- [ ] Load time is reasonable
- [ ] No errors in console

### Test 2: Page Refresh Performance
```
Refresh the page multiple times
Expected: 0.3-0.5 seconds per refresh (cache hits)
```
- [ ] Refreshes are fast (sub-second)
- [ ] Data matches between refreshes
- [ ] No console errors

### Test 3: Keep-Alive Functionality
```
For deployed services (not local):
1. Wait 5 minutes (let normal keep-alive ping run)
2. Load the app
3. Should load in 5-8 seconds (not 30-60 seconds)
```
- [ ] App loads quickly (keep-alive working)
- [ ] Check keep-alive logs for pings
- [ ] No errors in keep-alive service

### Test 4: Extended Idle Testing
```
For cloud platforms:
1. Deploy and verify it works
2. Let it sit for 35+ minutes (past sleep threshold)
3. Load the app
4. Should load in 5-8 seconds (if keep-alive working)
```
- [ ] App wakes up quickly
- [ ] No increase in load time after idle period
- [ ] Keep-alive proved effective

### Test 5: Production Monitoring
```
Monitor over 24-48 hours:
- Check logs for errors
- Monitor API call frequency  
- Monitor page load times
- Check for any anomalies
```
- [ ] No errors in production logs
- [ ] API calls are 90% reduced vs before
- [ ] Average page load <1 second
- [ ] Keep-alive running without issues

## Performance Metrics Target

| Metric | Target | Status |
|--------|--------|--------|
| First page load | 5-8s | ☐ |
| Page refresh (cache hit) | 0.3-0.5s | ☐ |
| Server wake-up time | 5-8s | ☐ |
| API calls/hour (vs before) | 90% reduction | ☐ |
| Keep-alive success rate | 99%+ | ☐ |
| Dashboard uptime | 99%+ | ☐ |

## Issues Encountered & Resolution

### Issue: App still slow on refresh
- [ ] Verify session state initialized at top of dashboard.py
- [ ] Check cache TTL values are appropriate
- [ ] Run `cache_monitor.display_cache_status()` to debug

### Issue: Keep-alive shows errors
- [ ] Check `STREAMLIT_APP_URL` is correct and accessible
- [ ] Verify firewall allows outbound HTTP
- [ ] Check keep-alive service has correct permissions
- [ ] Verify app is running before keep-alive starts

### Issue: Missing data after reload
- [ ] Verify cache TTL not too short (reset happening too often)
- [ ] Check that data is being cached in session state
- [ ] Verify no errors in data loading functions

### Issue: High API call rate
- [ ] Increase cache TTL values
- [ ] Verify cache logic is being executed
- [ ] Check for functions not using cache

## Sign-Off

- [ ] All checks passed
- [ ] Optimization implemented correctly
- [ ] Performance targets met
- [ ] Ready for production
- [ ] Team notified of changes

**Date Verified**: _______________
**Verified By**: _______________
**Notes**: _______________

---

## Troubleshooting Guide Reference

If any checks fail, see:
- Local issues: OPTIMIZATION_QUICK_START.md
- Deployment issues: OPTIMIZATION_GUIDE.md
- Technical details: IMPLEMENTATION_DETAILS.md
- Code reference: Check inline comments in dashboard.py and keep_alive.py
