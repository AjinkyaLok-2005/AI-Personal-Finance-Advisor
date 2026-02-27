import numpy as np
from sklearn.preprocessing import MinMaxScaler

def prepare_lstm_data(monthly_df, category_name, window_size = 3):

    #Prepare Sequences for a single category.

    category_df = monthly_df[monthly_df["category"] == category_name]
    category_df = category_df.sort_values("year_month")

    values = category_df["amount"].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(values)

    X = []
    y = []

    for i in range(len(scaled_values) - window_size):
        X.append(scaled_values[i:i + window_size])
        y.append(scaled_values[i + window_size])

    X = np.array(X)
    y = np.array(y)

    return X, y, scaler
