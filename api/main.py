from fastapi import FastAPI
import pandas as pd
from api.model import model, feature_cols
from api.utils import recommend_actions
from api.schema import CustomerInput, PredictionOutput
from api.schema import CustomerBatchInput, BatchOutput
from api.utils import revenue_at_risk, best_strategy


app = FastAPI()

@app.post("/predict/batch", response_model=BatchOutput)
def predict_batch(batch: CustomerBatchInput):

    results = []

    for row in batch.data:
        customer_id = row.get("customerID", None)
        monthly = row.get("MonthlyCharges", 0)

        df = pd.DataFrame([row])
        df = df.reindex(columns=feature_cols, fill_value=0)

        prob = model.predict_proba(df)[0][1]

        if prob > 0.7:
            risk = "High"
        elif prob > 0.4:
            risk = "Medium"
        else:
            risk = "Low"

        results.append({
            "customerID": customer_id,
            "probability": round(float(prob), 4),
            "risk": risk,
            "annual_at_risk": revenue_at_risk(prob, monthly),
            "best_strategy": best_strategy(risk),
            "recommendations": recommend_actions(risk)
        })

    return {"results": results}
