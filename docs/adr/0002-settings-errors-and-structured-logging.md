# ADR-0002: 타입 기반 설정, 예외 계층, 구조화 로그 도입

## 상태

Accepted

## 배경

서비스가 FastAPI, 데이터 수집, 외부 API, RAG, Agent Runtime으로 확장되면
환경별 설정과 오류·로그를 일관되게 관리해야 한다.

## 결정

- 설정은 pydantic-settings의 BaseSettings로 관리한다.
- 환경변수 prefix는 AIKS_를 사용한다.
- 실제 비밀값은 .env 또는 배포 환경의 secret에 저장한다.
- .env는 Git에 포함하지 않고 .env.example만 포함한다.
- 애플리케이션 예외는 ApplicationError를 기준으로 분류한다.
- 로그는 표준 logging과 structlog를 함께 사용한다.
- local 환경은 console, production 환경은 JSON 로그를 기본으로 한다.
- 정적 타입 검사는 mypy strict 모드를 사용한다.

## 결과

장점:

- 설정 누락과 잘못된 값을 실행 초기에 발견한다.
- 오류 코드와 응답 형식을 통일할 수 있다.
- 로그를 검색·집계하기 쉽다.
- Agent run과 Tool 호출을 추적할 기반이 생긴다.
- 타입 오류를 CI 전에 로컬에서 발견할 수 있다.

비용:

- 설정과 테스트 구조가 초기 단계부터 다소 복잡해진다.
- mypy strict 오류를 해결하는 학습 비용이 있다.
- 구조화 로그 field naming 규칙을 지속적으로 관리해야 한다.