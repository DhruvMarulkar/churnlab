import os
import joblib



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "processed", "feature_cols.pkl")


model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_PATH)