from pydantic import BaseModel, Field
from typing import List

class AIDetectionRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=100_000)
    content_type: str = Field(default="text", pattern="^(text|code)$")

class SentenceAnalysis(BaseModel):
    sentence: str
    ai_probability: int
    is_ai: bool

class AIDetectionResponse(BaseModel):
    id: str
    ai_probability: int
    human_probability: int
    perplexity: float
    burstiness: float
    risk_level: str  # Critical, High, Medium, Low
    verdict: str
    sentences: List[SentenceAnalysis]
    content_type: str
    status: str
    created_at: str
