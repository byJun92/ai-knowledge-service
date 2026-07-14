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