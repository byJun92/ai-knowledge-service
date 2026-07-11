# ADR-0001: uv와 src layout 사용

## 상태

Accepted

## 배경

16주 동안 Python, FastAPI, 데이터 파이프라인, RAG, CI/CD로 확장되는 프로젝트에서
의존성과 실행 환경을 재현할 수 있어야 한다.

## 결정

- Python·가상환경·의존성 관리는 uv를 사용한다.
- 애플리케이션 패키지는 src layout을 사용한다.
- lint와 format은 Ruff를 사용한다.
- 테스트는 pytest를 사용한다.

## 결과

장점:
- 로컬, CI, Docker에서 명령을 통일할 수 있다.
- uv.lock으로 의존성을 재현할 수 있다.
- 도구 수를 줄일 수 있다.

비용:
- 기존 pip/venv 사용자에게 uv 명령 학습이 필요하다.
- 팀 표준이 Poetry 또는 Conda인 경우 전환 비용이 있다.