# Week 01 도구 학습 가이드

- 프로젝트: AI Knowledge Service
- 대상: Java/Spring 개발자
- 개발 환경: macOS
- 학습 도구: `uv`, `pytest`, `Ruff`
- 권장 GitHub 경로: `docs/learning/week-01-tools-guide.md`

---

## 1. 문서 목적

이 문서는 AI 지식 서비스 프로젝트 1주 차에서 사용하는 `uv`, `pytest`, `Ruff`를 단순 설치 명령이 아니라 실제 프로젝트 운영 관점에서 이해하기 위한 학습 자료다.

각 도구마다 다음 내용을 다룬다.

- 무엇인지와 필요한 이유
- Java/Spring 생태계의 유사 개념
- macOS 설치와 핵심 명령
- 명령 실행 전후 변경되는 파일
- 최소 사용 예제
- 자주 발생하는 오류
- 꼭 기억할 명령
- 미니 실습과 이해 확인 질문
- 이후 16주 프로젝트에서 확장되는 범위

---

# 2. uv

## 2.1 uv란 무엇인가

`uv`는 Python 버전, 가상환경, 패키지 의존성, 잠금 파일과 프로젝트 명령 실행을 관리하는 도구다.

기존 Python 환경에서 여러 도구가 나눠 담당하던 다음 기능을 하나의 흐름으로 제공한다.

- Python 버전 설치
- 프로젝트별 Python 버전 고정
- 가상환경 생성
- 패키지 설치
- 의존성 잠금
- 프로젝트 명령 실행
- 패키지 프로젝트 초기화

대표적인 기존 도구는 `pyenv`, `venv`, `pip`, `pip-tools`, `pipx`, `Poetry`다.

## 2.2 Java/Spring과 비교

| Java/Spring | Python + uv |
|---|---|
| JDK 설치 | `uv python install` |
| Gradle toolchain | `.python-version` |
| `pom.xml`, `build.gradle` | `pyproject.toml` |
| Maven/Gradle dependency resolution | `uv add`, `uv lock` |
| dependency lock | `uv.lock` |
| `./gradlew test` | `uv run pytest` |
| 프로젝트 전용 실행 환경 | `.venv` |

`uv`는 JDK 버전 관리와 Gradle/Maven 일부 기능을 함께 제공한다고 이해하면 쉽다.

## 2.3 왜 필요한가

AI 프로젝트에서는 다음과 같이 많은 패키지를 사용하게 된다.

- FastAPI
- Pydantic
- SQLAlchemy
- HTTPX
- Embedding SDK
- Vector DB SDK
- LLM SDK
- OpenTelemetry
- pytest, Ruff

Python은 라이브러리 버전에 따라 동작 차이가 생기기 쉽다. 따라서 Python 버전, 직접 의존성, 하위 의존성, 실행 명령을 재현 가능하게 관리해야 한다.

## 2.4 macOS 설치

Homebrew:

```bash
brew install uv
uv --version
```

공식 설치 스크립트:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc
uv --version
```

둘 중 하나만 사용한다.

설치 위치 확인:

```bash
which uv
uv --version
```

## 2.5 프로젝트 생성

```bash
mkdir -p ~/workspace
cd ~/workspace

uv init --package --python 3.13 ai-knowledge-service
cd ai-knowledge-service
```

일반적으로 다음 파일이 생성된다.

```text
ai-knowledge-service/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── src/
```

## 2.6 Python 설치와 고정

```bash
uv python install 3.13
uv python pin 3.13
uv run python --version
```

`uv python pin`을 실행하면 `.python-version`이 생성되거나 수정된다.

## 2.7 의존성 추가

운영 의존성:

```bash
uv add fastapi
```

개발 의존성:

```bash
uv add --dev pytest pytest-cov ruff
```

명령 실행 후 다음 항목이 바뀐다.

1. `pyproject.toml`
2. `uv.lock`
3. `.venv` 내부 패키지

## 2.8 uv add와 uv sync 차이

`uv add`는 새 패키지를 프로젝트 의존성으로 등록한다.

```bash
uv add fastapi
```

수행 작업:

1. `pyproject.toml` 수정
2. 의존성 버전 계산
3. `uv.lock` 수정
4. `.venv` 설치

`uv sync`는 이미 선언된 프로젝트 환경을 현재 PC에 맞춘다.

```bash
uv sync
```

주요 사용 상황:

- 저장소를 처음 clone
- 다른 branch로 이동
- `uv.lock` 변경
- 다른 개발자가 패키지 추가

```bash
git clone https://github.com/example/ai-knowledge-service.git
cd ai-knowledge-service
uv sync
```

## 2.9 uv run

```bash
uv run pytest
uv run ruff check .
uv run python -m ai_knowledge_service
```

`uv run`은 프로젝트의 `.venv`를 사용해 명령을 실행한다.

기존 방식:

```bash
source .venv/bin/activate
pytest
```

권장 방식:

```bash
uv run pytest
```

장점:

- 가상환경 수동 활성화 불필요
- 전역 Python 오사용 방지
- 로컬, CI, Docker 명령 통일
- 필요한 의존성 자동 확인

## 2.10 주요 파일

### pyproject.toml

프로젝트 설정의 중심 파일이다.

- 프로젝트명과 버전
- Python 최소 버전
- 운영 의존성
- 개발 의존성
- pytest 설정
- Ruff 설정

### uv.lock

정확한 패키지와 하위 의존성 버전을 기록한다.

`uv.lock`은 Git에 포함한다.

### .python-version

프로젝트에서 사용할 Python 버전을 기록한다.

### .venv

프로젝트 전용 가상환경이다.

`.venv`는 Git에 포함하지 않는다.

## 2.11 꼭 기억할 명령

```bash
uv init
uv python install 3.13
uv python pin 3.13
uv add <package>
uv add --dev <package>
uv sync
uv run <command>
uv lock
```

## 2.12 자주 발생하는 오류

### uv: command not found

```bash
source ~/.zshrc
which uv
uv --version
```

Homebrew 확인:

```bash
brew list uv
```

### Python 버전을 찾지 못함

```bash
uv python install 3.13
uv python pin 3.13
uv sync
```

### 설치했는데 import가 안 됨

전역 Python으로 실행했을 가능성이 있다.

```bash
uv run python app.py
```

### uv.lock 충돌

`pyproject.toml`을 올바르게 병합한 뒤 잠금 파일을 다시 생성한다.

```bash
uv lock
uv sync
```

`uv.lock`을 임의로 직접 수정하지 않는다.

## 2.13 이번 프로젝트에서 사용하는 범위

Week 01:

- Python 3.13 고정
- `.venv` 관리
- pytest와 Ruff 설치
- `uv.lock` 관리
- 프로젝트 명령 실행

향후:

- FastAPI와 DB 패키지 관리
- Vector DB와 LLM SDK 관리
- GitHub Actions에서 `uv sync`
- Docker build에서 동일한 lock file 사용

## 2.14 5분 미니 실습

```bash
mkdir uv-practice
cd uv-practice

uv init
uv add requests
uv run python -c "import requests; print(requests.__version__)"
```

생성 파일 확인:

```bash
ls -la
cat pyproject.toml
```

## 2.15 이해 확인 질문

1. `uv add`와 `uv sync`의 차이는 무엇인가?
2. `.venv`는 Git에서 제외하지만 `uv.lock`은 포함하는 이유는 무엇인가?
3. `python app.py`보다 `uv run python app.py`가 안전한 이유는 무엇인가?

---

# 3. pytest

## 3.1 pytest란 무엇인가

`pytest`는 Python 테스트 프레임워크다.

주요 특징:

- 일반 `assert` 사용
- 자동 테스트 탐색
- 자세한 실패 메시지
- fixture
- parameterized test
- 예외 검증
- coverage 연동
- API, DB, 비동기 테스트 확장

## 3.2 Java/Spring과 비교

| JUnit/Spring Test | pytest |
|---|---|
| `@Test` | `test_` 함수 |
| `assertEquals` | `assert` |
| `assertThrows` | `pytest.raises` |
| `@ParameterizedTest` | `pytest.mark.parametrize` |
| `@BeforeEach` | fixture |
| `@Disabled` | `pytest.mark.skip` |
| MockMvc | TestClient, HTTPX |
| Mockito | `unittest.mock`, `monkeypatch` |

## 3.3 설치

```bash
uv add --dev pytest pytest-cov
uv run pytest --version
```

## 3.4 기본 테스트

```python
def add(left: int, right: int) -> int:
    return left + right


def test_add() -> None:
    result = add(2, 3)

    assert result == 5
```

실행:

```bash
uv run pytest
```

## 3.5 테스트 탐색 규칙

파일명:

```text
test_document.py
test_service.py
```

함수명:

```python
def test_create_document() -> None:
    ...
```

클래스:

```python
class TestDocument:
    def test_create(self) -> None:
        ...
```

## 3.6 예외 테스트

```python
import pytest


def divide(left: int, right: int) -> float:
    if right == 0:
        raise ValueError("right must not be zero")

    return left / right


def test_divide_rejects_zero() -> None:
    with pytest.raises(ValueError, match="must not be zero"):
        divide(10, 0)
```

Java의 `assertThrows`와 유사하다.

## 3.7 Parameterized Test

```python
import pytest


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_add(left: int, right: int, expected: int) -> None:
    assert left + right == expected
```

동일한 검증 로직을 여러 데이터로 실행한다.

## 3.8 Fixture

```python
import pytest

from ai_knowledge_service.domain.document import Document, DocumentType


@pytest.fixture
def sample_document() -> Document:
    return Document.create(
        document_id="doc-001",
        title="Python Testing",
        source_url="https://example.com/python-testing",
        document_type=DocumentType.TECH_ARTICLE,
    )


def test_document_title(sample_document: Document) -> None:
    assert sample_document.title == "Python Testing"
```

fixture는 테스트 함수에 필요한 값을 주입한다.

Java의 `@BeforeEach`와 유사하지만 필요한 테스트에만 선택적으로 주입하고 fixture끼리 의존할 수 있다.

## 3.9 주요 명령

```bash
uv run pytest
uv run pytest -v
uv run pytest -x
uv run pytest --lf
uv run pytest -k "document"
uv run pytest tests/domain/test_document.py
uv run pytest tests/domain/test_document.py::test_create_document
```

| 옵션 | 의미 |
|---|---|
| `-v` | 상세 테스트명 |
| `-x` | 첫 실패에서 중단 |
| `--lf` | 이전 실패 테스트부터 실행 |
| `-k` | 이름 키워드 필터 |
| `-s` | stdout 출력 표시 |

## 3.10 Coverage

```bash
uv run pytest --cov=ai_knowledge_service
```

누락 라인 표시:

```bash
uv run pytest \
  --cov=ai_knowledge_service \
  --cov-report=term-missing
```

HTML 보고서:

```bash
uv run pytest \
  --cov=ai_knowledge_service \
  --cov-report=html

open htmlcov/index.html
```

## 3.11 pyproject.toml 설정

```toml
[tool.pytest.ini_options]
addopts = "-q --strict-markers"
testpaths = ["tests"]

[tool.coverage.run]
source = ["ai_knowledge_service"]
branch = true

[tool.coverage.report]
show_missing = true
skip_covered = true
fail_under = 80
```

## 3.12 자주 발생하는 오류

### 테스트 0개 수집

다음을 확인한다.

- 파일명: `test_*.py`
- 함수명: `test_*`

### ModuleNotFoundError

```bash
uv sync
uv run pytest
```

`src` layout과 패키지 설정을 확인한다.

### 테스트끼리 상태 공유

공통 파일과 전역 변수를 직접 공유하지 않는다.

```python
def test_write_file(tmp_path) -> None:
    target = tmp_path / "sample.txt"
    target.write_text("hello", encoding="utf-8")

    assert target.read_text(encoding="utf-8") == "hello"
```

### 실행 순서 의존

테스트는 하나만 따로 실행해도 통과해야 한다.

## 3.13 꼭 기억할 명령

```bash
uv run pytest
uv run pytest -v
uv run pytest --lf
uv run pytest --cov=ai_knowledge_service
```

## 3.14 10분 미니 실습

```python
def normalize_title(title: str) -> str:
    normalized = " ".join(title.split())

    if not normalized:
        raise ValueError("title must not be blank")

    return normalized
```

다음 항목을 테스트한다.

1. 앞뒤 공백 제거
2. 여러 공백을 한 칸으로 변경
3. 빈 문자열에서 `ValueError`

## 3.15 이해 확인 질문

1. pytest가 테스트를 자동으로 찾는 이름 규칙은 무엇인가?
2. fixture와 `@BeforeEach`의 차이는 무엇인가?
3. coverage 100%가 좋은 테스트를 보장하지 않는 이유는 무엇인가?

---

# 4. Ruff

## 4.1 Ruff란 무엇인가

`Ruff`는 Python lint와 format 도구다.

- 사용하지 않는 import 탐지
- 정의되지 않은 변수 탐지
- import 순서 정리
- 잠재적 버그 패턴 탐지
- 최신 Python 문법 권장
- 코드 단순화
- 형식 자동 정리
- 일부 문제 자동 수정

## 4.2 Java와 비교

| Java 도구 | Ruff |
|---|---|
| Checkstyle | 스타일·규칙 검사 |
| PMD | 코드 패턴 검사 |
| SpotBugs | 일부 잠재 오류 검사 |
| Spotless | format |
| Google Java Format | format |
| import sorter | import 정리 |

Ruff가 모든 Java 분석 도구를 완전히 대체하지는 않지만 Python 초기 프로젝트에서 여러 도구를 하나로 줄여준다.

## 4.3 설치

```bash
uv add --dev ruff
uv run ruff --version
```

## 4.4 Linter와 Formatter

Linter:

```bash
uv run ruff check .
```

Formatter:

```bash
uv run ruff format .
```

Linter는 품질과 규칙 위반을 찾고, formatter는 코드 외형을 통일한다.

## 4.5 핵심 명령

```bash
uv run ruff check .
uv run ruff check . --fix
uv run ruff format .
uv run ruff format --check .
uv run ruff rule F401
```

## 4.6 예제

수정 전:

```python
import os
import sys


def add(a,b):
    return a+b
```

실행:

```bash
uv run ruff check . --fix
uv run ruff format .
```

수정 후:

```python
def add(a, b):
    return a + b
```

## 4.7 pyproject.toml 설정

```toml
[tool.ruff]
target-version = "py313"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

| 코드 | 의미 |
|---|---|
| `E` | 스타일 오류 |
| `F` | Pyflakes 기반 오류 |
| `I` | import 정렬 |
| `B` | 버그 가능성 |
| `UP` | 최신 Python 문법 |
| `SIM` | 코드 단순화 |

## 4.8 check --fix와 format 차이

`check --fix`:

```bash
uv run ruff check . --fix
```

규칙 위반 중 안전하게 고칠 수 있는 문제를 수정한다.

- 미사용 import 삭제
- import 정렬
- 일부 코드 단순화

`format`:

```bash
uv run ruff format .
```

코드 외형을 통일한다.

- 공백
- 들여쓰기
- 줄바꿈
- 따옴표
- 괄호 배치

## 4.9 권장 실행 순서

개발 중:

```bash
uv run ruff check . --fix
uv run ruff format .
```

커밋 전:

```bash
uv run ruff check .
uv run ruff format --check .
```

전체:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run ruff format --check .
```

## 4.10 자주 발생하는 오류

### lint는 통과하지만 format 검사 실패

```bash
uv run ruff format .
```

### 자동 수정되지 않는 오류

```bash
uv run ruff check .
```

출력된 파일과 줄 번호를 직접 수정한다.

### IDE formatter 충돌

IDE에서 Black 등 다른 formatter를 사용하고 있을 수 있다. 저장 시 formatter를 Ruff로 통일한다.

### 규칙 과다 활성화

초기부터 모든 규칙을 켜면 학습보다 규칙 대응에 시간이 많이 든다. 프로젝트 성장에 맞춰 점진적으로 확장한다.

## 4.11 꼭 기억할 명령

```bash
uv run ruff check .
uv run ruff check . --fix
uv run ruff format .
uv run ruff format --check .
```

## 4.12 5분 미니 실습

```python
import os
import sys


def greet(name):
    if name == "":
        return "hello"
    else:
        return "hello " + name
```

실행:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
```

## 4.13 이해 확인 질문

1. `ruff check . --fix`와 `ruff format .`의 차이는 무엇인가?
2. lint는 통과했는데 format 검사가 실패할 수 있는 이유는 무엇인가?
3. 모든 Ruff 규칙을 처음부터 활성화하지 않는 이유는 무엇인가?

---

# 5. 세 도구의 관계

```text
uv
 ├─ Python 버전 관리
 ├─ 가상환경 관리
 ├─ 의존성 관리
 ├─ pytest 설치·실행
 └─ Ruff 설치·실행

pytest
 └─ 코드가 요구사항대로 동작하는지 검증

Ruff
 ├─ 잠재 오류와 품질 문제 검사
 └─ 코드 형식 통일
```

## 5.1 일반 개발 흐름

```bash
uv sync

# 코드 작성

uv run ruff check . --fix
uv run ruff format .
uv run pytest

uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=ai_knowledge_service
```

## 5.2 커밋 전 체크리스트

- [ ] `uv sync` 성공
- [ ] Ruff lint error 0개
- [ ] format 변경 필요 파일 0개
- [ ] 전체 테스트 통과
- [ ] coverage 기준 충족

---

# 6. 앞으로 배우게 될 내용

## 6.1 다음 1주

### Python 타입 힌트 심화

함수 입력과 반환 계약을 표현한다.

```python
def find_document(document_id: str) -> Document | None:
    ...
```

### Pydantic Settings

환경변수와 설정을 Python 객체로 관리한다.

Spring Boot의 `@ConfigurationProperties`와 유사하다.

### .env와 .env.example

- `.env`: 실제 로컬 값
- `.env.example`: GitHub에 올리는 설정 예시

### 예외 계층

오류를 역할별로 분리한다.

```text
ApplicationError
├── DocumentNotFoundError
├── ValidationError
└── ExternalServiceError
```

### 구조화 로깅

문자열이 아니라 검색 가능한 필드 형태로 로그를 남긴다.

## 6.2 다음 4주

### pre-commit

commit 전에 Ruff와 테스트를 자동 실행한다.

### FastAPI

Python API 프레임워크다. Spring MVC Controller와 비교해 학습한다.

### Pydantic

요청·응답 DTO와 입력 검증을 담당한다.

### Dependency Injection

설정과 Service 객체를 주입한다.

### Service 계층

도메인 로직과 API 계층을 분리한다.

### async/await

외부 API와 파일·DB I/O를 효율적으로 처리한다.

### HTTPX

Python HTTP Client다. Spring `WebClient`와 유사하다.

## 6.3 데이터 파이프라인 단계

- 문서 다운로드
- PDF·HTML·Markdown 파싱
- 텍스트 정제와 chunk 분할
- 메타데이터 DB 저장
- 중복 수집 방지
- 실패 문서 재처리

## 6.4 검색과 RAG 단계

### Embedding

텍스트를 의미를 담은 숫자 벡터로 변환한다.

### Vector DB

Embedding을 저장하고 유사한 문서를 검색한다.

### 인덱싱

문서 chunk와 embedding을 검색 가능한 구조로 저장한다.

### RAG

검색한 문서를 LLM 입력에 포함해 근거 기반 답변을 만든다.

### 출처 표시

답변에 사용한 원문과 chunk를 표시한다.

## 6.5 평가와 운영 단계

### Recall@K

정답 문서가 상위 K개 검색 결과에 포함되는 비율이다.

### 근거성 평가

생성 답변이 검색된 출처에 실제로 근거하는지 평가한다.

### OpenTelemetry

trace, metric, log로 시스템 흐름을 관찰한다.

### Prometheus

처리량과 응답시간 등의 지표를 수집한다.

### Docker Compose

API, PostgreSQL, Vector DB를 함께 실행한다.

### GitHub Actions

push와 pull request 시 테스트와 품질 검사를 자동 실행한다.

---

# 7. 향후 학습 지도

## 다음 1주

현재 배운 `uv`, `pytest`, `Ruff`를 기반으로 다음 기능을 추가한다.

- 설정 관리
- 환경변수
- 예외 계층
- 구조화 로깅
- pytest fixture
- 타입 검사

결과물:

- 환경별 설정
- 일관된 오류 처리
- 테스트 데이터 재사용
- 검색 가능한 로그

## 다음 4주

HTTP API 기반을 만든다.

결과물:

- 문서 등록 API
- 문서 조회 API
- 요청 검증
- Service 계층
- 예외 응답
- API 테스트

현재 도구 연결:

- `uv`: FastAPI 관련 패키지 관리
- `pytest`: API와 Service 테스트
- `Ruff`: 코드 품질 유지

## 최종 서비스 단계

### uv

- 로컬 개발
- GitHub Actions
- Docker build
- 배포 환경 의존성 고정

### pytest

- 도메인 테스트
- API 테스트
- 데이터 파이프라인 테스트
- 검색 품질 테스트
- RAG 평가 자동화

### Ruff

- 코드 스타일 통일
- CI 품질 검사
- 잠재 오류 방지

---

# 8. 최종 요약

| 도구 | 핵심 역할 | Java/Spring 비교 |
|---|---|---|
| `uv` | Python·가상환경·의존성·실행 관리 | JDK + Gradle/Maven 일부 |
| `pytest` | 기능 검증과 자동 테스트 | JUnit |
| `Ruff` | lint와 format | Checkstyle + PMD + Spotless 일부 |

기본 작업 흐름:

```bash
uv sync
uv run ruff check . --fix
uv run ruff format .
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=ai_knowledge_service
```

이 흐름은 이후 FastAPI, 데이터 파이프라인, RAG, Docker, CI/CD 단계에서도 계속 유지한다.
