# ADR-0003: Protocol 기반 Repository와 Service 경계

## 상태

Accepted

## 배경

FastAPI와 PostgreSQL을 도메인 코드에 직접 연결하면 저장 기술 교체와 단위
테스트가 어려워진다.

## 결정

- DocumentRepository를 Protocol로 정의한다.
- DocumentService는 Protocol에만 의존한다.
- 첫 Adapter는 InMemoryDocumentRepository다.
- 중복 정책과 사용 사례 순서는 Service가 담당한다.
- 저장 세부사항은 Repository가 담당한다.
- FastAPI와 PostgreSQL은 이후 Adapter로 추가한다.
- 로컬 검증은 pre-commit으로 자동화한다.
- Coding Agent 규칙은 AGENTS.md에 기록한다.

## 결과

장점:

- 저장 기술 교체 가능
- fake 테스트 간단
- FastAPI와 도메인 분리
- Agent Tool 계약으로 확장 가능

비용:

- 파일과 경계 증가
- Protocol 변경 시 구현체 수정 필요
- mypy 실행 필수