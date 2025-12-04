from pydantic import BaseModel
from typing import List

class InferenceRequest(BaseModel):
    image_base64: str

class InferenceResponse(BaseModel):
    status: str
    probabilities: List[float]
    risk_score: float
    predicted_class_index: int

