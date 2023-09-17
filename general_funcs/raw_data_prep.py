import pandas as pd


def add_seven_cols(path: str) -> None:
    """
    :param path:
    :return:
    """
    df = pd.read_table(path)
    df['DATE_TIME'] = df.DATE + ' ' + df.TIME
    print("DATE_TIME OK")

    df["OP_CL"] = (df.OPEN - df.CLOSE) * 100000
    df["HI_LO"] = (df.HIGH - df.LOW) * 100000
    print("OP_CL HI_LO OK")

    df['MON'] = pd.DatetimeIndex(df.DATE).month
    df['DAY'] = pd.to_datetime(df.DATE).dt.dayofweek
    df['HOUR'] = pd.DatetimeIndex(df.reset_index().DATE_TIME).hour
    df['MIN'] = pd.DatetimeIndex(df.reset_index().DATE_TIME).minute
    print("MON DAY HOUR MIN OK")

    df.to_csv(path, sep='\t', index=False)
    print("OK")
