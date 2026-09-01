import uuid
import numpy as np
from typing import List
from app.ml.trend_prediction.trend_schema import TrendSchema, Forecast, ConfidenceInterval
from app.ml.trend_prediction.sequence_builder import SequenceBuilder
from app.ml.trend_prediction.lstm.predictor import LSTMPredictor

class TrendService:
    """
    Public API boundary for Security Trend Intelligence Engine.
    Exposes unified multi-horizon forecasts regardless of underlying deep learning model.
    """
    def __init__(self, sequence_builder: SequenceBuilder):
        self.sequence_builder = sequence_builder
        try:
            self.predictor = LSTMPredictor()
            self.is_active = True
        except Exception as e:
            print(f"Trend Engine inactive: {e}")
            self.is_active = False
            
    def _map_risk_level(self, score: float) -> str:
        if score < 30: return "Critical"
        if score < 60: return "High"
        if score < 80: return "Medium"
        return "Low"
        
    def _classify_trend(self, current_score: float, final_score: float) -> str:
        diff = final_score - current_score
        if diff > 15: return "Rapid Improvement"
        if diff > 3:  return "Improving"
        if diff > -3: return "Stable"
        if diff > -15: return "Slight Decline"
        if diff > -30: return "Rapid Decline"
        return "Critical Decline"

    def generate_forecast(self, website_id: str) -> TrendSchema:
        if not self.is_active:
            raise RuntimeError("Trend Engine is currently inactive or untrained.")
            
        sequence = self.sequence_builder.build_inference_sequence(website_id)
        
        # We want to forecast: Next Assessment (1 step), Next 7 Days (approx 1 step if weekly, or 7 if daily)
        # Let's assume assessments are roughly daily. We forecast 30 steps ahead.
        horizon_steps = 30
        
        preds, lowers, uppers = self.predictor.predict(sequence, horizon=horizon_steps)
        
        # preds shape is (30, 5) -> [security_score, anomaly_score, ssl_score, headers_score, dns_score]
        # Current score is the last step of the input sequence
        current_score = sequence[0, -1, 0]
        
        forecasts = []
        horizons = {
            "Next Assessment": 0,  # index 0 is step 1
            "7 Days": 6,          # index 6 is step 7
            "30 Days": 29         # index 29 is step 30
        }
        
        for name, idx in horizons.items():
            if idx < len(preds):
                f_score = float(np.clip(preds[idx, 0], 0, 100))
                l_score = float(np.clip(lowers[idx, 0], 0, 100))
                u_score = float(np.clip(uppers[idx, 0], 0, 100))
                f_anomaly = float(np.clip(preds[idx, 1], 0, 1))
                
                forecast = Forecast(
                    horizon=name,
                    predicted_security_score=f_score,
                    predicted_risk_level=self._map_risk_level(f_score),
                    predicted_anomaly_probability=f_anomaly,
                    security_score_ci=ConfidenceInterval(lower_bound=l_score, upper_bound=u_score)
                )
                forecasts.append(forecast)
                
        # Overall trend is based on the 30 day forecast
        final_score = forecasts[-1].predicted_security_score
        trend_direction = self._classify_trend(current_score, final_score)
        
        # Determine confidence (inversely related to confidence interval width of the 30-day forecast)
        ci_width = forecasts[-1].security_score_ci.upper_bound - forecasts[-1].security_score_ci.lower_bound
        # Max reasonable width is say 40 points, map to 0-100 confidence
        confidence = float(max(0, min(100, 100 - (ci_width * 2))))
        
        return TrendSchema(
            trend_id=str(uuid.uuid4()),
            website_id=website_id,
            overall_trend_direction=trend_direction,
            confidence=confidence,
            forecasts=forecasts
        )
