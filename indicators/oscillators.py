import pandas as pd

def get_demarker(df: pd.DataFrame, n: int):
    HIGH_diff = df.HIGH - df.HIGH.shift(periods=1)
    LOW_diff = df.LOW.shift(periods=1) - df.LOW
    HIGH_diff.loc[HIGH_diff < 0] = 0
    LOW_diff.loc[LOW_diff < 0] = 0
    DeMax_SMA = HIGH_diff.rolling(n, min_periods = 1).mean()
    DeMin_SMA = LOW_diff.rolling(n, min_periods = 1).mean()
    DeMarker = DeMax_SMA / (DeMax_SMA + DeMin_SMA)
    return DeMarker.map(lambda x: round(x, 2))


def get_rsi(df: pd.DataFrame, n: int):
    U = df.CLOSE -  df.CLOSE.shift(periods=1)
    U[U < 0] = 0
    D = df.CLOSE.shift(periods=1) - df.CLOSE
    D[D < 0] = 0
    RS = U.ewm(alpha=1/n, min_periods=1).mean() / D.ewm(alpha=1/n, min_periods=1).mean()
    RSI = 100 - (100 / (1 + df.RS))
    return RSI.map(lambda x: round(x, 2))


def get_stochastic(df: pd.DataFrame, K: int, n: int):
    MaxHigh = df.HIGH.rolling(K, min_periods=0).max()
    MinLow = df.LOW.rolling(K, min_periods=0).min()
    SMA_upper = (df.CLOSE - MinLow).rolling(n, min_periods=0).sum()
    SMA_lower = (MaxHigh - MinLow).rolling(n, min_periods=0).sum()
    Stochastic = (SMA_upper / SMA_lower)*100
    return Stochastic.map(lambda x: round(x, 2))

