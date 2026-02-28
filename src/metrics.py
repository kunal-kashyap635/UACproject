import numpy as np
import pandas as pd


def compute_system_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["total_system_load"] = df["cbp_custody"] + df["hhs_care"]

    df["net_daily_intake"] = df["cbp_transfers_to_hhs"] - df["hhs_discharges"]

    df["care_load_growth_rate"] = df["total_system_load"].pct_change() * 100

    df["backlog_indicator"] = df["net_daily_intake"] > 0

    df["discharge_offset_ratio"] = np.where(
        df["cbp_transfers_to_hhs"] > 0,
        df["hhs_discharges"] / df["cbp_transfers_to_hhs"],
        np.nan,
    )

    return df
