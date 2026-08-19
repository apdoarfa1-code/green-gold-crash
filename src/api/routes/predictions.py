from fastapi import APIRouter
from src.api.schemas.round import PredictionRequest, PredictionResponse
from src.analytics.ml_models.markov_model import MarkovChainModel
import numpy as np

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_next(request: PredictionRequest):
    arr = np.array(request.multipliers)
    
    # Simple Markov / statistical heuristic prediction for demonstration
    markov = MarkovChainModel()
    markov.train(arr[:-1], arr[1:])
    probs = markov.predict(arr)
    
    prob_above_2 = float(probs[1] + probs[2]) if len(probs) >= 3 else 0.5

    return PredictionResponse(
        model_name="Ensemble-Markov-Heuristic",
        probability_above_2x=round(prob_above_2, 4),
        recommended_cashout=1.50 if prob_above_2 < 0.6 else 2.10,
        confidence=round(float(np.max(probs)) if len(probs) > 0 else 0.5, 2)
    )
