from typing import Literal

from pydantic import BaseModel, Field


class TicketTriage(BaseModel):
    category: Literal["order_issue", "billing_issue", "account_issue", "feedback", "off_topic", "injection_attempt"]
    sentiment: Literal["positive", "negative", "neutral"]
    urgency: int = Field(ge=1, le=10)
    summary: str = Field(max_length=300)
    suggested_response: str = Field(max_length=500)
    handoff: bool
    confidence: float = Field(ge=0,le=1)
