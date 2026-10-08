# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes.

## 1. Think Before Coding
- State assumptions explicitly. If uncertain, ask.
- Minimum code that solves the problem. Nothing speculative.

## 2. NASA JPL Rule 4: Single Sheet of Paper Architecture (≤ 60 Lines)
- Every production file and function must fit on a single printed sheet of standard reference paper (hard ceiling of 60 lines per file).
- Test suites (e.g. `tests/` directory or `test_*.py`) are explicitly exempt.

## 3. Python Quality & Verification Gates
The 3 mandatory commands that must always work:
- `uv run ruff check --fix` (0 errors, 0 warnings)
- `uv run ty check` (0 errors, 0 warnings)
- `uv run pytest` (all tests pass)
