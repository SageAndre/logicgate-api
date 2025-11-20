from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class PolicyCreate(BaseModel):
    name: str = Field(..., example="Age Restriction 18+")
    rule: Dict[str, Any] = Field(..., example={"and": [{">": [{"var": "age"}, 18]}]})

class EvaluationRequest(BaseModel):
    data: Dict[str, Any] = Field(..., example={"age": 25, "country": "BW"})

class PolicyResponse(BaseModel):
    id: str
    name: str
    link: str