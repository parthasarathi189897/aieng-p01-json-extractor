import json

import pytest

from output_generator import ExtractionFailed, extract

GOOD = json.dumps({
  "category": "order_issue",
  "sentiment": "negative",
  "urgency": 4,
  "summary": "Customer has not received their order",
  "suggested_response": "Sorry for the delay. Let me check your order status.",
  "handoff": True,
  "confidence": 0.9
})
BAD = GOOD.replace('"urgency": 4', '"urgency": 42')


def fake_llm(*replies):
    """A pretend LLM that returns the given replies in order and remembers what it was sent."""
    calls = []
    def llm(messages):
        calls.append(messages)
        return replies[len(calls) - 1]
    return llm, calls

def test_passes_first_try():
    llm, calls = fake_llm(GOOD)
    triage, attempts = extract("where is my order", llm=llm)
    assert attempts == 1

def test_retry_sends_exact_error_back():
    llm, calls = fake_llm(BAD, GOOD)
    triage, attempts = extract("where is my order", llm=llm)
    assert attempts == 2
    assert "less than or equal to 10" in calls[1][-1]["content"]

def test_stops_on_repeated_error():
    llm, calls = fake_llm(BAD, BAD, GOOD)
    with pytest.raises(ExtractionFailed) as e:
        extract("where is my order", llm=llm)
    assert e.value.reason == "repeated error"
    assert len(calls) == 2

def test_gives_up_after_3_attempts():
    llm, calls = fake_llm("not json", BAD, "{}", GOOD)
    with pytest.raises(ExtractionFailed) as e:
        extract("where is my order", llm=llm)
    assert e.value.reason == "max attempts"
    assert len(calls) == 3

def test_empty_input_never_calls_llm():
    llm, calls = fake_llm(GOOD)
    with pytest.raises(ExtractionFailed):
        extract("   ", llm=llm)
    assert calls == []
