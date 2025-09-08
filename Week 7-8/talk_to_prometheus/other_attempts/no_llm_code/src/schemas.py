from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any, Tuple

class QueryParams(BaseModel):
    start: Optional[int] = None
    end: Optional[int] = None
    step: Optional[int] = None
    lookback: Optional[str] = None

class PlanItem(BaseModel):
    endpoint: Literal["query","query_range"]
    promql: str
    params: QueryParams
    purpose: Optional[str] = None
    expected_size: Optional[Literal["small","medium","large"]] = None

class Plan(BaseModel):
    user_intent: str
    items: List[PlanItem]
    notes: Optional[str] = None

class DataRef(BaseModel):
    storage: Literal["memory","file"]
    key: str
    approx_bytes: Optional[int] = None
    sampling_info: Optional[Dict[str, Any]] = None

class ExecItemResult(BaseModel):
    plan_index: int
    promql: str
    endpoint: str
    status: Literal["ok","error"]
    error: Optional[str] = None
    data_ref: Optional[DataRef] = None

class ExecResult(BaseModel):
    results: List[ExecItemResult]
    __comments: Optional[str] = None

class MetricsSummary(BaseModel):
    series_count: int
    time_range: Optional[Tuple[int,int]] = None
    sampling_step: Optional[int] = None
    stats: Dict[str, Dict[str, Any]] = {}

class Finding(BaseModel):
    title: str
    detail: str
    severity: Literal["info","low","medium","high"]
    evidence: Optional[Dict[str, Any]] = None

class Recommendation(BaseModel):
    text: str

class Analysis(BaseModel):
    summary: MetricsSummary
    findings: List[Finding]
    recommendations: List[Recommendation]
    next_questions: List[str] = []
