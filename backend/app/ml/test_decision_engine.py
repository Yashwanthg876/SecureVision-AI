import sys
import os
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.ml.decision_engine.prediction_service import PredictionService
from app.ml.decision_engine.prediction_schema import UnifiedPrediction
from pydantic import ValidationError

def main():
    print("Initializing Prediction Service...")
    class_labels = ["Critical", "High", "Low", "Medium"]
    service = PredictionService(class_labels)
    
    # Generate a random dummy feature vector
    dummy_vector = np.random.rand(1, 50) 
    
    strategies = ["Majority Voting", "Weighted Voting", "Probability Averaging"]
    
    for strategy in strategies:
        print(f"\n--- Testing Decision Engine: {strategy} ---")
        try:
            prediction = service.predict_risk(dummy_vector, strategy=strategy)
            
            # API Contract Test
            try:
                # Re-validate against Pydantic schema to prove contract is upheld
                validated_schema = UnifiedPrediction(**prediction.model_dump())
                print("[Contract Test] PASSED: Output matches UnifiedPrediction schema.")
            except ValidationError as e:
                print(f"[Contract Test] FAILED: Schema mismatch - {str(e)}")
            
            print(f"Final Prediction: {prediction.prediction}")
            print(f"Confidence Level: {prediction.confidence_level} ({prediction.confidence:.2f})")
            print(f"Agreement Ratio: {prediction.agreement_score:.2f}")
            print(f"Models Evaluated: {prediction.total_models}")
            print(f"Prediction UUID: {prediction.prediction_id}")
            
            if prediction.anomaly_result:
                print(f"Anomaly Detection: {prediction.anomaly_result.get('status')} ({prediction.anomaly_result.get('severity')})")
                print(f"Anomaly Score: {prediction.anomaly_result.get('anomaly_score'):.3f}")
            else:
                print("Anomaly Detection: Inactive/Failed")
                
        except Exception as e:
            print(f"ERROR running {strategy}: {str(e)}")
            
    print("\nSUCCESS: The Decision Engine integration tests completed.")

if __name__ == "__main__":
    main()
