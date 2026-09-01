import re
import uuid
import time
from typing import List, Tuple
import math

from app.schemas.ai_detection import AIDetectionResponse, SentenceAnalysis
from app.repositories.ai_detection_repository import ai_detection_repository
from sqlalchemy.orm import Session
from datetime import datetime
import json

# Common words often overused by AI models
AI_TRANSITION_WORDS = {
    "furthermore", "moreover", "in conclusion", "to summarize", 
    "delve", "tapestry", "landscape", "crucial", "testament",
    "underscore", "realm", "multifaceted", "seamlessly", 
    "navigating", "intricate", "pivotal", "in essence", "comprehensive"
}

def _split_sentences(text: str) -> List[str]:
    # Simple regex to split by ., !, or ? followed by a space or end of string
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s.strip()]

def _calculate_perplexity(text: str) -> float:
    # A proxy for perplexity: how often do "AI-like" words appear?
    # Higher perplexity = more human (less predictable).
    # Lower perplexity = more AI (highly predictable, uses common tropes).
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 100.0
    
    ai_word_count = sum(1 for w in words if w in AI_TRANSITION_WORDS)
    # If 0 AI words, high perplexity (100). If many, low perplexity (approaching 0).
    ratio = ai_word_count / len(words)
    # Heuristic scaling: 2% AI words is considered very AI-like (low perplexity).
    perplexity = max(0.0, 100.0 - (ratio * 5000.0))
    return perplexity

def _calculate_burstiness(sentences: List[str]) -> float:
    # Burstiness measures variance in sentence length.
    # Humans vary sentence lengths widely; AI tends to be uniform.
    if not sentences:
        return 0.0
    lengths = [len(s.split()) for s in sentences]
    if len(lengths) < 2:
        return 50.0 # Neutral if only one sentence
    
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    
    # Scale: std_dev of 2 is low burstiness (0), std_dev of 10+ is high burstiness (100)
    burstiness = min(100.0, (std_dev / 10.0) * 100.0)
    return burstiness

def _analyze_sentence(sentence: str) -> SentenceAnalysis:
    words = re.findall(r'\b\w+\b', sentence.lower())
    ai_word_count = sum(1 for w in words if w in AI_TRANSITION_WORDS)
    
    # Base probability
    prob = 30
    
    # AI models love long, perfectly structured sentences
    if len(words) > 20:
        prob += 20
    if len(words) > 30:
        prob += 10
        
    # Heavy penalty for AI transition words
    prob += (ai_word_count * 25)
    
    prob = min(99, prob)
    if "as an ai" in sentence.lower() or "language model" in sentence.lower():
        prob = 99
        
    return SentenceAnalysis(
        sentence=sentence,
        ai_probability=prob,
        is_ai=prob >= 60
    )

class AIDetectionAnalyzer:
    def analyze(self, content: str, content_type: str, db: Session, user_id: str) -> AIDetectionResponse:
        start_ms = int(time.time() * 1000)
        
        sentences = _split_sentences(content)
        if not sentences:
            sentences = [content]
            
        sentence_analyses = [_analyze_sentence(s) for s in sentences]
        
        if content_type == "text":
            perplexity = _calculate_perplexity(content)
            burstiness = _calculate_burstiness(sentences)
            
            # Combine metrics into overall AI probability
            # Low perplexity -> High AI prob
            # Low burstiness -> High AI prob
            avg_sentence_ai = sum(s.ai_probability for s in sentence_analyses) / len(sentence_analyses)
            
            ai_score = (avg_sentence_ai * 0.5) + ((100 - perplexity) * 0.25) + ((100 - burstiness) * 0.25)
            ai_score = max(1, min(99, int(ai_score)))
            
            # Catch explicit AI phrases
            if "as an ai" in content.lower():
                ai_score = 99
        else:
            # Code analysis heuristic
            # Code is harder to analyze via burstiness. We rely on structural patterns and comments.
            ai_score = 45 # Default middle-ground
            if "TODO" in content or "FIXME" in content:
                ai_score -= 10 # Humans leave these more often
            if "def " in content or "function " in content:
                # Check comment to code ratio
                lines = content.split('\n')
                comments = sum(1 for l in lines if l.strip().startswith('#') or l.strip().startswith('//'))
                if len(lines) > 0 and comments / len(lines) > 0.3:
                    ai_score += 20 # Over-commented code is typical of AI
            ai_score = max(1, min(99, int(ai_score)))
            perplexity = 50.0
            burstiness = 50.0

        human_score = 100 - ai_score
        
        if ai_score >= 80:
            risk_level = "High"
            verdict = "High likelihood of AI-generated content."
        elif ai_score >= 50:
            risk_level = "Medium"
            verdict = "Mixed signals. Content may be partially AI-generated or heavily edited by AI."
        else:
            risk_level = "Low"
            verdict = "High likelihood of human-generated content."
            
        scan_uuid = uuid.uuid4()
        scan_id = str(scan_uuid)
        
        result = AIDetectionResponse(
            id=scan_id,
            ai_probability=ai_score,
            human_probability=human_score,
            perplexity=round(perplexity, 1),
            burstiness=round(burstiness, 1),
            risk_level=risk_level,
            verdict=verdict,
            sentences=sentence_analyses,
            content_type=content_type,
            status="Completed",
            created_at=datetime.utcnow().isoformat()
        )
        
        # Persist
        snippet = content[:200] + "..." if len(content) > 200 else content
        try:
            ai_detection_repository.create(db, obj_in={
                "id": scan_uuid,
                "user_id": user_id,
                "content_snippet": snippet,
                "content_type": content_type,
                "ai_probability": ai_score,
                "risk_level": risk_level,
                "status": "Completed",
                "result_json": result.model_dump_json()
            })
        except Exception as e:
            raise RuntimeError("AI detection completed but could not be saved") from e

        return result

ai_analyzer = AIDetectionAnalyzer()
