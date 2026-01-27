import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "data", "processed", "X_train.csv")


model = joblib.load(MODEL_PATH)
feature_cols = pd.read_csv(FEATURE_PATH).columns.tolist()
