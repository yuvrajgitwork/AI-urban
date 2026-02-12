from pydantic import BaseModel
from typing import List, Optional


class Evidence(BaseModel):
    source: str
    quote: str


class Finding(BaseModel):
    area: str
    issue: str
    description: str
    source: str
    evidence: List[Evidence]
    confidence: str  # High | Medium | Low


class ThermalSummary(BaseModel):
    max_hotspot: float
    min_coldspot: float
    delta: float
    interpretation: str
    mapping_confidence: str