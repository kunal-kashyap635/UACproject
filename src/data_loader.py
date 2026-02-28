import pandas as pd

def load_clean_data(path: str) -> pd.DataFrame:
    """
    Load clean, feature-engineered UAC dataset.

    Parameters:
        path (str): Path to clean_uac_data.csv

    Returns:
        pd.DataFrame
    """

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df
