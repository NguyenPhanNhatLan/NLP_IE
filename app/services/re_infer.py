from typing import List, Dict, Any
import random

LABELS = ["HAS_BENEFIT", "TREATS", "SUITABLE_FOR", "HAS_INCI", "NO_RELATION"]

def predict_relations(text: str, pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Dummy để team test end-to-end
    out = []
    for p in pairs:
        out.append({
            "e1": p["e1"],
            "e2": p["e2"],
            "relation": random.choice(LABELS),
            "confidence": round(random.uniform(0.6, 0.95), 3)
        })
    return out
