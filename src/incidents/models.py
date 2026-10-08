from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high", "critical", "unknown"]
Confidence = Literal["low", "medium", "high"]


class IncidentReport(BaseModel):
    service: str
    severity: Severity
    summary: str

    evidence: list[str] = Field(default_factory=list)

    root_cause: str | None = None
    impact: str | None = None

    recommended_actions: list[str] = Field(default_factory=list)

    confidence: Confidence
