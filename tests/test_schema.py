# How to run (from the project root):
#   uv run pytest                     # run all tests
#   uv run pytest -v                  # verbose: list each test by name
#   uv run pytest tests/test_schema.py::test_missing_field_rejected   # run one test
#   source .venv/bin/activate && pytest   # or activate the venv, then plain pytest
# Note: `python tests/test_schema.py` won't run the tests — pytest discovers test_* functions.

import pytest
from pydantic import ValidationError

from models.user_input import UserInput

GOOD = {
  "category": "order_issue",
  "sentiment": "negative",
  "urgency": 4,
  "summary": "Customer has not received their order",
  "suggested_response": "Sorry for the delay. Let me check your order status.",
  "handoff": True,
  "confidence": 0
}

def test_valid_reading_parses():
    r = UserInput(**GOOD)                 # ** spreads the dict into keyword args
    assert r.category == "order_issue"       # assert = "this must be true"

def test_missing_field_rejected():
    data = {k: v for k, v in GOOD.items() if k != "handoff"}
    with pytest.raises(ValidationError):    # passes only if this block raises
        UserInput(**data)

def test_urgency_value_rejected():
    with pytest.raises(ValidationError):
        UserInput(**{**GOOD, "urgency": -5})

def test_confidence_value_rejected():
    with pytest.raises(ValidationError):
        UserInput(**{**GOOD, "confidence": 10})

def test_sentiment_condition_rejected():
    with pytest.raises(ValidationError):
        UserInput(**{**GOOD, "sentiment": "test"})   # copy GOOD, override one key

def test_confidenceJ_type_rejected():
    with pytest.raises(ValidationError):
        UserInput(**{**GOOD, "confidence": "low"})
