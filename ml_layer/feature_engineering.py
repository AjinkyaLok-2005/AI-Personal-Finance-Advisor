import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    #Creating ML features from unified transaction table.
    df = df.copy()

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    category_counts = df["category"].value_counts().to_dict()
    df["category_frequency"] = df["category"].map(category_counts)

    return df