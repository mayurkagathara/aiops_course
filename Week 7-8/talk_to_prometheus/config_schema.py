from pydantic import BaseModel, Field
from typing import Dict, Optional
import uuid

# --- 2. State Management & Pydantic Schemas ---

class PromParams(BaseModel):
    start: Optional[int] = None  # Unix timestamp
    end: Optional[int] = None    # Unix timestamp
    step: Optional[str] = "1m"  # Step duration like '1m', '5m'

class PromQLPlan(BaseModel):
    query: str
    query_type: str = "query_range"
    parameters: PromParams = None

class PromQLWorkflowState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_query: str = ""
    promql_plan: PromQLPlan = None
    validation_result: bool = None
    validation_feedback: Optional[str] = None
    final_prometheus_result: Optional[Dict] = None
    final_answer: Optional[str] = None
    retry_count: int = 0
    next_task: Optional[str] = None