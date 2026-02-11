from database.mongo import violations
from collections import defaultdict

POINTS = {
    "Face Missing": 5,
    "Multiple Faces": 10,
    "Tab Switch": 7
}

def get_score():
    """Calculate total suspicious score for all violations"""
    score = 0
    for v in violations.find():
        score += POINTS.get(v["type"], 0)
    return score

def get_user_score(user_id):
    """Calculate suspicious score for a specific user"""
    score = 0
    for v in violations.find({"user_id": user_id}):
        score += POINTS.get(v["type"], 0)
    return score

def get_session_score(session_id):
    """Calculate suspicious score for a specific exam session"""
    score = 0
    for v in violations.find({"session_id": session_id}):
        score += POINTS.get(v["type"], 0)
    return score

def get_violation_breakdown(user_id=None, session_id=None):
    """Get detailed breakdown of violations by type"""
    query = {}
    if user_id:
        query["user_id"] = user_id
    if session_id:
        query["session_id"] = session_id
    
    breakdown = defaultdict(int)
    for v in violations.find(query):
        breakdown[v["type"]] += 1
    
    result = {
        "violations": dict(breakdown),
        "scores": {vtype: count * POINTS.get(vtype, 0) 
                   for vtype, count in breakdown.items()},
        "total_score": sum(count * POINTS.get(vtype, 0) 
                          for vtype, count in breakdown.items())
    }
    return result
