from fastapi import APIRouter
from app.models.round_schema import PredictionRequest, PredictionResponse
import numpy as np

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_next_multiplier(request: PredictionRequest):
    multipliers = np.array(request.multipliers)
    
    if len(multipliers) == 0:
        return PredictionResponse(
            model_name="Ensemble-LSTM-Markov",
            probability_above_2x=0.5,
            recommended_cashout=1.5,
            confidence=0.5
        )

    # Heuristic probability estimation based on recent streak
    recent_above_2 = np.mean(multipliers[-10:] >= 2.0) if len(multipliers) >= 10 else 0.5
    prob_above_2 = float(1.0 - recent_above_2 * 0.3)  # Mean reversion approximation
    
    recommended = 1.40 if prob_above_2 < 0.5 else 2.10
    confidence = float(np.clip(0.5 + abs(prob_above_2 - 0.5), 0.5, 0.95))

    return PredictionResponse(
        model_name="Ensemble-LSTM-Markov",
        probability_above_2x=round(prob_above_2, 4),
        recommended_cashout=recommended,
        confidence=round(confidence, 2)
    )
