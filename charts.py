import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_candlestick(df, symbol):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
    
    fig.add_trace(go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close']), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['close'].rolling(20).mean(), name='MA20'), row=1, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df['volume'], name='Volume'), row=2, col=1)
    
    fig.update_layout(title=f"{symbol} Analysis", template="plotly_dark", xaxis_rangeslider_visible=False)
    return fig