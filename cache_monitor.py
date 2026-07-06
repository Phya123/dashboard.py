"""
Streamlit Cache Monitoring Module
==================================

Provides utilities to monitor and debug session state caching in your Streamlit app.
Import this module to add real-time cache diagnostics to your dashboard.

Usage:
    from cache_monitor import display_cache_status, get_cache_stats
    
    with st.expander("Cache Status"):
        display_cache_status()
    
    stats = get_cache_stats()
    print(stats)
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Any

import streamlit as st


def get_cache_stats() -> Dict[str, Any]:
    """
    Get current cache statistics from session state.
    
    Returns:
        Dictionary with cache age and freshness status
    """
    current_time = time.time()
    stats = {}
    
    # Dashboard data cache
    if hasattr(st.session_state, "cached_dashboard_timestamp"):
        dashboard_age = current_time - st.session_state.cached_dashboard_timestamp
        stats["dashboard"] = {
            "age_seconds": dashboard_age,
            "is_cached": st.session_state.cached_dashboard_data is not None,
            "ttl": 30,
            "fresh": dashboard_age < 30,
        }
    
    # Market data cache
    if hasattr(st.session_state, "cached_market_timestamp"):
        market_age = current_time - st.session_state.cached_market_timestamp
        stats["market_data"] = {
            "age_seconds": market_age,
            "is_cached": st.session_state.cached_market_data is not None,
            "ttl": 60,
            "fresh": market_age < 60,
        }
    
    # Risk profile cache
    if hasattr(st.session_state, "risk_profile_timestamp"):
        risk_age = current_time - st.session_state.risk_profile_timestamp
        stats["risk_profile"] = {
            "age_seconds": risk_age,
            "is_cached": st.session_state.cached_risk_profile is not None,
            "ttl": 300,
            "fresh": risk_age < 300,
        }
    
    # Trade journal cache
    if hasattr(st.session_state, "trade_journal_timestamp"):
        journal_age = current_time - st.session_state.trade_journal_timestamp
        stats["trade_journal"] = {
            "age_seconds": journal_age,
            "is_cached": st.session_state.cached_trade_journal is not None,
            "ttl": 60,
            "fresh": journal_age < 60,
        }
    
    # Bot commands
    if hasattr(st.session_state, "bot_commands_logged"):
        stats["bot_commands"] = {
            "count": len(st.session_state.bot_commands_logged),
        }
    
    return stats


def display_cache_status():
    """Display formatted cache status in the Streamlit app."""
    stats = get_cache_stats()
    
    if not stats:
        st.warning("No cache statistics available yet.")
        return
    
    # Overall cache health
    cached_items = sum(1 for s in stats.values() if s.get("is_cached"))
    total_items = len([s for s in stats.values() if "ttl" in s])
    cache_health = (cached_items / total_items * 100) if total_items > 0 else 0
    
    st.metric("Cache Health", f"{cache_health:.0f}%")
    
    # Individual cache items
    st.write("**Cache Items:**")
    
    for cache_name, cache_info in stats.items():
        if cache_name == "bot_commands":
            st.write(f"- **{cache_name}**: {cache_info['count']} commands logged")
            continue
        
        if "ttl" not in cache_info:
            continue
        
        age = cache_info["age_seconds"]
        ttl = cache_info["ttl"]
        is_fresh = cache_info["fresh"]
        
        # Status icon
        icon = "🟢" if is_fresh else "🟡" if age < ttl * 1.5 else "🔴"
        status = "Fresh" if is_fresh else "Stale"
        
        # Time remaining
        time_remaining = max(0, ttl - age)
        
        st.write(
            f"{icon} **{cache_name}**: {age:.1f}s old (TTL: {ttl}s) | "
            f"Refresh in: {time_remaining:.0f}s | {status}"
        )
    
    # Last update time
    st.caption(f"Last checked: {datetime.now().strftime('%H:%M:%S')}")


def format_cache_stats() -> str:
    """
    Format cache statistics as a readable string.
    Useful for logging or console output.
    """
    stats = get_cache_stats()
    
    output = "=== Cache Status ===\n"
    
    for cache_name, cache_info in stats.items():
        if cache_name == "bot_commands":
            output += f"{cache_name}: {cache_info['count']} commands\n"
            continue
        
        if "ttl" not in cache_info:
            continue
        
        age = cache_info["age_seconds"]
        ttl = cache_info["ttl"]
        status = "Fresh" if cache_info["fresh"] else "Stale"
        
        output += (
            f"{cache_name}:\n"
            f"  - Age: {age:.1f}s\n"
            f"  - TTL: {ttl}s\n"
            f"  - Status: {status}\n"
        )
    
    return output


def cache_performance_summary():
    """
    Return a summary of cache performance metrics.
    """
    stats = get_cache_stats()
    
    summary = {
        "total_cached_items": sum(1 for s in stats.values() if s.get("is_cached")),
        "fresh_items": sum(1 for s in stats.values() if s.get("fresh")),
        "stale_items": sum(1 for s in stats.values() if not s.get("fresh") and "ttl" in s),
        "average_age": sum(s.get("age_seconds", 0) for s in stats.values()) / len(stats) if stats else 0,
    }
    
    return summary


# Example usage (uncomment to test)
if __name__ == "__main__":
    # This would be run in Streamlit context
    print(format_cache_stats())
    print(cache_performance_summary())
