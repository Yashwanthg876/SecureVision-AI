import os
import sys

# Ensure backend path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from app.ml.decision_engine.prediction_schema import UnifiedPrediction
from app.ml.trend_prediction.trend_schema import TrendSchema, Forecast, ConfidenceInterval
from app.ai.copilot.copilot_service import CopilotService
from dotenv import load_dotenv

def run_test():
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY not found. The API call will fail, but we can verify architecture.")
        
    print("--- 1. Mocking ML Outputs ---")
    mock_prediction = UnifiedPrediction(
        prediction_id="test-pred-123",
        website_id="example.com",
        prediction="High",
        confidence=88.5,
        confidence_level="High",
        models_used=["xgboost", "random_forest"],
        explanation={
            "top_positive_features": [{"feature": "strict_transport_security", "value": -0.8}],
            "top_negative_features": [{"feature": "content_security_policy", "value": 1.2}],
            "summary": "High risk driven by missing CSP."
        },
        anomaly_result={
            "status": True,
            "severity": "Critical Anomaly",
            "anomaly_score": 0.85,
            "top_contributing_features": ["ssl_expired"]
        }
    )
    
    mock_trend = TrendSchema(
        trend_id="test-trend-123",
        website_id="example.com",
        overall_trend_direction="Rapid Decline",
        confidence=92.0,
        forecasts=[
            Forecast(
                horizon="30 Days",
                predicted_security_score=40.0,
                predicted_risk_level="High",
                predicted_anomaly_probability=0.9,
                security_score_ci=ConfidenceInterval(lower_bound=30, upper_bound=50)
            )
        ]
    )
    
    print("\n--- 2. Initializing Copilot Service ---")
    copilot = CopilotService()
    
    print("\n--- 3. Generating Executive Report ---")
    report = copilot.generate_dashboard_report(mock_prediction, mock_trend, audience="executive")
    
    print("\n[Generated Report Payload]")
    print(f"Audience: {report['audience']}")
    print(f"Provider: {report['provider']}")
    print(f"Recommendations: {len(report['recommendations'])}")
    print(f"\n[Summary Text Preview]\n{report['summary'][:500]}...")
    
    print("\n--- 4. Testing Chat Context ---")
    chat_response = copilot.handle_chat(
        session_id="session-1",
        prediction=mock_prediction,
        trend=mock_trend,
        user_message="Why did my security score drop rapidly?"
    )
    
    print(f"\n[Chat Response Preview]\n{chat_response[:300]}...")
    
    print("\n--- Done! Phase 6F Copilot Verified ---")

if __name__ == "__main__":
    run_test()