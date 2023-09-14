import pandas as pd


def get_demarker(df: pd.DataFrame, n: int) -> pd.Series:
    """
    :param df: forex data of any timeframe which has HIGH and LOW candle parameters (column names)
    :param n: DeMarker period
    :return: pd.Series with DeMarker values
    """
    high_difference = df.HIGH - df.HIGH.shift(periods=1)
    low_difference = df.LOW.shift(periods=1) - df.LOW
    high_difference.loc[high_difference < 0] = 0
    low_difference.loc[low_difference < 0] = 0
    max_sma = high_difference.rolling(n, min_periods=1).mean()
    min_sma = low_difference.rolling(n, min_periods=1).mean()
    demarker = max_sma / (max_sma + min_sma)
    return demarker.map(lambda x: round(x, 2))


def get_rsi(df: pd.DataFrame, n: int) -> pd.Series:
    """
    :param df: forex data of any timeframe which has HIGH and LOW candle parameters (column names)
    :param n: RSI period
    :return: pd.Series with RSI values
    """
    u = df.CLOSE - df.CLOSE.shift(periods=1)
    u[u < 0] = 0
    d = df.CLOSE.shift(periods=1) - df.CLOSE
    d[d < 0] = 0
    rs = u.ewm(alpha=1/n, min_periods=1).mean() / d.ewm(alpha=1/n, min_periods=1).mean()
    rsi = 100 - (100 / (1 + rs))
    return rsi.map(lambda x: round(x, 2))


def get_stochastic(df: pd.DataFrame, k_per: int, d_per: int) -> pd.Series:
    """
    :param df: forex data of any timeframe which has HIGH and LOW candle parameters (column names)
    :param k_per: Stochastic K-period
    :param d_per: Stochastic d-period
    :return: pd.Series with Stochastic values
    """
    max_high = df.HIGH.rolling(k_per, min_periods=0).max()
    min_low = df.LOW.rolling(k_per, min_periods=0).min()
    sma_upper = (df.CLOSE - min_low).rolling(d_per, min_periods=0).sum()
    sma_lower = (max_high - min_low).rolling(d_per, min_periods=0).sum()
    stochastic = (sma_upper / sma_lower)*100
    return stochastic.map(lambda x: round(x, 2))

