# aieng-p01-json-extractor

Turns a free-text customer support message into a validated `TicketTriage` JSON object using a local LLM (Ollama).

## Problem

Support messages are messy: typos, sarcasm, mixed languages, several issues at once, prompt injection. Downstream systems need one fixed shape: category, sentiment, urgency (1–10), summary, suggested response, handoff flag, confidence.

## Approach

- **Contract:** Pydantic model `TicketTriage` (`models/ticket_triage.py`).
- **Constrained output:** Ollama `format=TicketTriage.model_json_schema()`, temperature 0.
- **Prompt:** every category defined; `injection_attempt` *only* when the message tries to override rules.
- **`extract()`:** rejects empty input before any LLM call, validates, and retries up to 3 times, sending the exact validation error back. Stops early if the same error repeats.

## Tradeoffs

- **`llama3.1:8b` over `gemma3:270m` / `gemma:2b`:** several seconds per call instead of about 1 s, but the small models returned valid JSON with wrong labels.
- **Schema-valid ≠ correct.** Known misses: sarcasm → positive, refund → `order_issue`, "UNACCEPTABLE." → injection, urgency mostly 1.
- **Retries are only tested with a fake LLM.** Constrained decoding has always validated on the first attempt.

## Numbers

`llama3.1:8b`, 20 fixtures, model already loaded (`results/2026-11-01-llama3.1-8b.txt`):

| Metric | Value |
|---|---|
| Pass rate | 20/20, all on attempt 1 (#20 empty input rejected before the LLM) |
| p95 latency | 8,482 ms over 19 calls |
| Avg tokens | 189.5 in / 106.5 out |
| Cost per call | $0 local, ~$0.000092 at gpt-4o-mini rates |

"Pass" means schema-valid. Labels are not yet checked against expected answers.

## How to run

Requires Python 3.11+, [uv](https://docs.astral.sh/uv/), and [Ollama](https://ollama.com) running locally.

```bash
ollama pull llama3.1:8b
uv sync
uv run python main.py   # all fixtures: PASS/FAIL, attempts, latency, tokens, cost
uv run pytest           # schema + retry tests, no Ollama needed
```

Design notes and failure log: [SPEC.md](SPEC.md).
