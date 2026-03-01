import os
import joblib

# Absolute base path (works locally + Render)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

print("MODEL_PATH:", MODEL_PATH)
print("FEATURE_PATH:", FEATURE_PATH)

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}")

if not os.path.exists(FEATURE_PATH):
    raise RuntimeError(f"Feature cols file not found at {FEATURE_PATH}")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_PATH)