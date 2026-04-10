from typing import Literal
from pydantic import BaseModel, Field


class ModelResponse(BaseModel):
    condition: list[str] = Field(description="Possible medical conditions identified")
    severity: Literal["low", "medium", "high"] = Field(
        description="Severity of the situation"
    )
    recommendation: str = Field(description="Suggested next steps or advice")
    confidence_score: float = Field(
        ge=0.0, le=1.0, description="Model's confidence in the analysis"
    )
