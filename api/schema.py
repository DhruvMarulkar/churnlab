from pydantic import BaseModel
from typing import List
from typing import Dict

class CustomerInput(BaseModel):
    data: dict

class PredictionOutput(BaseModel):
    probability: float
    risk: str
    recommendations: List[str]
    
class CustomerBatchInput(BaseModel):
    data: List[Dict]


class BatchOutput(BaseModel):
    results: List[Dict]