import uuid
import json
import time
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from json_logic import jsonLogic

# Import our modules
from .models import PolicyCreate, EvaluationRequest, PolicyResponse
from .database import get_db_connection
from .auth import get_api_key

router = APIRouter()

# 1. Create Policy (PROTECTED - Needs API Key)
@router.post("/policies", response_model=PolicyResponse, dependencies=[Depends(get_api_key)])
def create_policy(policy: PolicyCreate):
    policy_id = str(uuid.uuid4())[:8]
    
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO policies (id, name, rule, created_at) VALUES (?, ?, ?, ?)",
            (policy_id, policy.name, json.dumps(policy.rule), datetime.now().isoformat())
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
            
    return {
        "id": policy_id, 
        "name": policy.name, 
        "link": f"/evaluate/{policy_id}"
    }

# 2. Evaluate (PUBLIC - No API Key needed for now, or add it if you want)
@router.post("/evaluate/{policy_id}")
def evaluate_policy(policy_id: str, payload: EvaluationRequest):
    conn = get_db_connection()
    row = conn.execute("SELECT rule, name FROM policies WHERE id = ?", (policy_id,)).fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    try:
        # Logic Engine
        result = jsonLogic(json.loads(row["rule"]), payload.data)
        return {
            "policy": row["name"],
            "valid": bool(result),
            "data": payload.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Logic Error: {str(e)}")