import pandas as pd
from utils.schema import validate_schema

def load_kaggle_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    print("Original Columns: ", df.columns)

    rename_map = {
        "Date": "date",
        "Amount": "amount",
        "Transaction Type": "type",
        "Merchant": "merchant",
        "Category": "category",
        "Balance": "balance" 
    }

    df = df.rename(columns=rename_map)

    df["source"] = "csv"

    df = validate_schema(df)

    return df