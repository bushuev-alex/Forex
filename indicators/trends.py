import pandas as pd


def get_ichimoku(df: pd.DataFrame, tenkan_sen: int = 9, kijun_sen: int = 26, senkou_span_b: int = 52) -> pd.DataFrame:
    """
    :param df: forex data of any timeframe which has HIGH and LOW candle parameters (column names)
    :param tenkan_sen: short-size time frame (default = 9)
    :param kijun_sen: middle-size time frame (default = 26)
    :param senkou_span_b: long-size time frame (default = 52)
    :return: pd.DataFrame with Ichimoku values in columns with names 'tenkan', 'kijun', 'senkou_a', 'senkou_b', 'chikou'
    """
    max_high_short: pd.Series = df.HIGH.rolling(tenkan_sen, min_periods=0).max()
    min_low_short: pd.Series = df.LOW.rolling(tenkan_sen, min_periods=0).min()
    tenkan: pd.Series = ((max_high_short + min_low_short) / 2).rename("tenkan", inplace=True)

    max_high_mid: pd.Series = df.HIGH.rolling(kijun_sen, min_periods=0).max()
    min_low_mid: pd.Series = df.LOW.rolling(kijun_sen, min_periods=0).min()
    kijun: pd.Series = ((max_high_mid + min_low_mid) / 2).rename("kijun", inplace=True)

    senkou_a: pd.Series = ((tenkan + kijun) / 2).shift(periods=kijun_sen).rename("senkou_a", inplace=True)

    max_high_long: pd.Series = df.HIGH.rolling(senkou_span_b, min_periods=0).max()
    min_low_long: pd.Series = df.LOW.rolling(senkou_span_b, min_periods=0).min()
    senkou_b: pd.Series = ((max_high_long + min_low_long) / 2).shift(periods=kijun_sen).rename("senkou_b", inplace=True)

    chikou: pd.Series = df.CLOSE.shift(periods=-kijun_sen).rename("chikou", inplace=True)
    ichimoku_kinko_hyo = pd.concat([tenkan, kijun, senkou_a, senkou_b, chikou], axis="columns")
    return ichimoku_kinko_hyo
