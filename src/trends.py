import pandas as pd

def compute_rolling_metrics(df: pd.DataFrame, short_window: int = 7, long_window: int = 14) -> pd.DataFrame:

    df = df.copy()

    df[f"total_load_{short_window}d_avg"] = (
        df["total_system_load"].rolling(short_window).mean()
    )

    df[f"total_load_{long_window}d_avg"] = (
        df["total_system_load"].rolling(long_window).mean()
    )

    df[f"net_intake_{short_window}d_avg"] = (
        df["net_daily_intake"].rolling(short_window).mean()
    )

    df["load_volatility"] = df["total_system_load"].rolling(short_window).std()

    return df


def detect_stress_window(df: pd.DataFrame, threshold: float = None) -> pd.DataFrame:

    df = df.copy()

    if threshold is None:
        threshold = df["total_system_load"].median()

    df["stress_window"] = (df["net_daily_intake"] > 0) & (
        df["total_system_load"] > threshold
    )

    return df
