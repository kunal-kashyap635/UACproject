import pandas as pd

def check_missing_dates(df: pd.DataFrame) -> pd.DatetimeIndex:
    full_date_range = pd.date_range(
        start=df["date"].min(), end=df["date"].max(), freq="D"
    )
    return full_date_range.difference(df["date"])


def check_duplicate_dates(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.duplicated(subset=["date"], keep=False)]


def validate_constraints(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["flag_invalid_cbp_transfer"] = df["cbp_transfers_to_hhs"] > df["cbp_custody"]

    df["flag_invalid_hhs_discharge"] = df["hhs_discharges"] > df["hhs_care"]

    return df
