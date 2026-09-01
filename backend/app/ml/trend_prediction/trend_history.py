import os
import csv
from app.ml.trend_prediction.trend_schema import TrendSchema

class TrendHistoryManager:
    """
    Stores forecast events so they can be compared against future reality,
    enabling Forecast Evaluation (MAE, RMSE tracking).
    """
    def __init__(self):
        self.history_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'trends'))
        os.makedirs(self.history_dir, exist_ok=True)
        self.history_file = os.path.join(self.history_dir, "trend_history.csv")
        self._initialize_file()
        
    def _initialize_file(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "generated_at", "trend_id", "website_id", 
                    "trend_direction", "confidence",
                    "f_next_score", "f_7day_score", "f_30day_score"
                ])
                
    def log_forecast(self, trend: TrendSchema):
        scores = {f.horizon: f.predicted_security_score for f in trend.forecasts}
        
        with open(self.history_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                trend.generated_at,
                trend.trend_id,
                trend.website_id,
                trend.overall_trend_direction,
                trend.confidence,
                scores.get("Next Assessment", ""),
                scores.get("7 Days", ""),
                scores.get("30 Days", "")
            ])
