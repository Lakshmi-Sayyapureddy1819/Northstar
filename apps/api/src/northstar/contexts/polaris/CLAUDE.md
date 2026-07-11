# contexts/polaris — The AI Assistant

**Polaris explains. It never computes.**

Polaris consumes structured outputs (engine `EngineResult`s and context contracts) and turns them into language. It is architecturally incapable of producing business facts — and it must stay that way.

## Polaris MAY

- Explain a recommendation the CIE already produced.
- Summarize / compare options using engine outputs.
- Answer follow-up questions grounded in provided structured data.
- Personalize communication (tone, framing, relevance).

## Polaris MUST NOT

- Compute a match score, salary band, skill gap, commute, ranking, or any business fact. Those come from `contexts/career_intelligence/` only.
- Import another context's internals — only their `contract.py`.
- Invent facts not present in the structured inputs it was given.

## How it works

`application/` orchestrates: call the relevant engine/context contracts → collect their `EngineResult`s → hand those structured results to the **platform LLM capability** (`platform/llm/`, the `LLMPort`) → narrate. The LLM sees already-computed facts; it does not decide them.

## AI plumbing is NOT here

The `LLMPort`, Claude adapter, prompt infrastructure, structured-output handling, and AI observability live in `platform/llm/` (AI is a platform capability). Polaris holds conversation + orchestration only.

See `docs/ai/` for prompt strategy, guardrails, and the evaluation strategy.
