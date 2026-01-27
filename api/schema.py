from pydantic import BaseModel
from typing import List

class CustomerInput(BaseModel):
    data: dict

class PredictionOutput(BaseModel):
    probability: float
    risk: str
    recommendations: List[str]