import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train_random_forest(df: pd.DataFrame):

    X = df[["amount", "day_of_week", "month", "day", "category_frequency"]]

    y = df["category"]

    #Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size = 0.2, random_state = 42
    )

    model = RandomForestClassifier(n_estimators = 100, random_state = 42)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)

    # print("Training Accuracy: ", accuracy_score(y_train, y_train_pred))
    # print("Testing Accuracy: ", accuracy_score(y_test, y_pred))
    # print("\nClassification Report: \n")
    # print(classification_report(y_test, y_pred))

    joblib.dump(model, "models/random_forest_model.pkl")
    joblib.dump(label_encoder, "models/label_encoder.pkl")

    # print("\nModel saved")

    return model, label_encoder