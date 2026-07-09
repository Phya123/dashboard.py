import pandas as pd

def calculate_metrics(df):
    if df.empty: return {}
    
    trades = len(df)
    wins = len(df[df['pnl'] > 0])
    losses = len(df[df['pnl'] < 0])
    win_rate = wins / trades if trades > 0 else 0
    total_pnl = df['pnl'].sum()
    
    avg_win = df[df['pnl'] > 0]['pnl'].mean() or 0
    avg_loss = df[df['pnl'] < 0]['pnl'].mean() or 0
    
    return {
        "trades": trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "total_pnl": total_pnl,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "profit_factor": abs(sum(df[df['pnl'] > 0]['pnl']) / sum(df[df['pnl'] < 0]['pnl'])) if avg_loss != 0 else 0
    }