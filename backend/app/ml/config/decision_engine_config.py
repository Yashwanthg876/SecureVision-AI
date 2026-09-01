# Configuration for AI Decision Engine

# The strategy used if none is explicitly requested
DEFAULT_VOTING_STRATEGY = "Probability Averaging"

# If Weighted Voting is used, determine the dynamic metric to use from metadata
# Examples: "roc_auc", "f1_score", "accuracy"
DYNAMIC_WEIGHT_METRIC = "roc_auc"

# Confidence thresholds for human readable mapping
CONFIDENCE_THRESHOLDS = {
    "Very High": 0.90,
    "High": 0.75,
    "Medium": 0.60,
    "Low": 0.40,
    "Very Low": 0.0
}

# Agreement threshold logic (if needed for custom filtering later)
MINIMUM_AGREEMENT_RATIO = 0.5
