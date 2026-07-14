# AGENTS.md

## Project purpose

Document ingestion, retrieval, RAG, and multi-agent AI knowledge service.

## Runtime

- Python 3.13
- Use uv only.
- Do not use global pip.
- Do not edit uv.lock manually.

## Architecture

- Domain must not import FastAPI, DB clients, or LLM SDKs.
- Services depend on Protocols, not concrete repositories.
- Repositories must not contain HTTP response logic.
- API layers must not access storage directly.
- Deterministic validation belongs in Python code, not prompts.

## Required validation

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest --cov=ai_knowledge_service
uv run pre-commit run --all-files
```
# Security
- Never commit .env, API keys, tokens, passwords, or private data.
- Never log secrets.
- Do not weaken secret-related .gitignore rules.

# Git safety
Do not commit, push, merge, force-push, delete branches, create tags, or run destructive Git commands unless explicitly requested.

# Definition of Done
- requested behavior implemented
- architecture boundaries preserved
- success and failure tests added
- Ruff passes
- formatting passes
- mypy passes
- pytest and coverage pass
- documentation updated
- no secret or unrelated change included


루트 `AGENTS.md`는 저장소 전체 규칙으로 사용한다. 특정 하위 경로에 별도 규칙이 필요할 때만 더 가까운 위치에 추가한다.

---

## 15. Task Specification

파일:

```text
docs/tasks/week-03-repository-service.md
```

# Task Specification: Week 03 Repository and Service Boundary

## Goal

Create a storage-independent DocumentService using a DocumentRepository
Protocol and an in-memory adapter.

## In scope

- Repository Protocol
- memory adapter
- Service
- tests and fake
- pre-commit
- AGENTS.md
- ADR

## Out of scope

- FastAPI
- PostgreSQL
- async
- LLM
- embeddings

## Acceptance criteria

- valid registration succeeds
- duplicate registration fails
- invalid input fails
- missing document fails
- list returns documents
- non-inheriting fake satisfies the contract
- Ruff, mypy, pytest, coverage and pre-commit pass