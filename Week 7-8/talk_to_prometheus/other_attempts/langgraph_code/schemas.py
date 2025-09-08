# Pydantic Schemas for structured outputs
from pydantic import BaseModel
from typing import Any, List

class Plan(BaseModel):
    query: str
    parameters: dict | None = None
    query_type: str
    step: str | None = None

class ExecutionResult(BaseModel):
    result: Any
    stored_in_file: bool = False
    filepath: str | None = None

class Analysis(BaseModel):
    summary: str
    stats: dict
    recommendations: List[str]
