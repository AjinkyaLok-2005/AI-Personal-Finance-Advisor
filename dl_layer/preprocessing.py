import pandas as pd

def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:

    #Aggragate monthly total spending per category

    df = df.copy()

    df["year_month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby(["year_month", "category"])["amount"].sum().reset_index()
    )

    monthly["year_month"] = monthly["year_month"].dt.to_timestamp()

    return monthly