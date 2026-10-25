from typing import Literal

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    category: Literal["order_issue", "billing_issue", "account_issue", "feedback", "off_topic", "injection_attempt"]
    sentiment: Literal["positive", "negative", "neutral"]
    urgency: int = Field(ge=1, le=10)
    summary: str = Field(max_length=50)
    suggested_response: str = Field(max_length=80)
    handoff: bool
    confidence: float = Field(ge=0,le=1)
