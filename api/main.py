from fastapi import FastAPI
import pandas as pd
from api.model import model, feature_cols
from api.utils import recommend_actions
from api.schema import CustomerInput, PredictionOutput

app = FastAPI()

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: CustomerInput):
    df = pd.DataFrame([input_data.data])
    df = df.reindex(columns=feature_cols, fill_value=0)

    prob = model.predict_proba(df)[0][1]

    if prob > 0.7:
        risk = "High"
    elif prob > 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "probability": round(float(prob), 4),
        "risk": risk,
        "recommendations": recommend_actions(risk)
    }
