import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import load_model

def build_and_train_lstm(X, y, epochs = 100):
    
    model = Sequential()

    model.add(
        LSTM(
            units = 50,
            activation = 'relu',
            input_shape = (X.shape[1], X.shape[2])
        )
    )

    model.add(Dense(1))

    model.compile(
        optimizer = 'adam',
        loss = 'mse'
    )

    model.fit(X, y, epochs = epochs, verbose = 1)

    model.save("models/lstm_transport_model.keras")

    return model

def predict_next_month(model, X, scaler):
    # Prediction of next month spending using last sequence(last 3 months)

    last_sequence = X[-1]

    last_sequence = last_sequence.reshape(1, last_sequence.shape[0], last_sequence.shape[1])

    predicted_scaled = model.predict(last_sequence)

    predicted_actual = scaler.inverse_transform(predicted_scaled)

    return predicted_actual[0][0]

def load_lstm_model(path="models/lstm_transport_model.keras"):
    return load_model(path)