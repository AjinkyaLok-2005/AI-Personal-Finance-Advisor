import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "amount",
    "type",
    "merchant",
    "category",
    "balance",
    "source",
]

def validate_schema(df: pd.DataFrame) -> pd.DataFrame:

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    df = df[REQUIRED_COLUMNS]

    df["date"] = pd.to_datetime(df["date"], errors = "coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors = "coerce")
    df["balance"] = pd.to_numeric(df["balance"], errors = "coerce")

    return df