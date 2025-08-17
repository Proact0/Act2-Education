# 포커스 그룹 인터뷰 모듈 (Focus Group Interview Module)

## 개요

이 모듈은 Act2: Marketing의 포커스 그룹 인터뷰 진행 및 분석을 담당하는 LangGraph Workflow입니다. 교육 콘텐츠 개발을 위한 인터뷰 질문 생성, 응답 분석, 통찰 추출 기능을 제공합니다.

## 프로젝트 구조

```
focus_group_interview/
├── Search-Agent/                    # 교육 리소스 검색 에이전트
│   ├── mcp_servers/                # MCP 서버 구성 요소
│   │   ├── web_search_server.py    # 웹 검색 서버
│   │   ├── youtube_transcript_server.py # 유튜브 검색 서버
│   │   ├── docker-compose.yml      # Docker 구성 파일
│   │   └── README.md               # MCP 서버 문서
│   ├── src/react_agent/            # 검색 에이전트 소스 코드
│   ├── app.py                      # Streamlit UI 애플리케이션
│   ├── langgraph.json             # LangGraph 설정 파일
│   └── pyproject.toml             # 검색 에이전트 의존성 관리
├── modules/                        # 포커스 그룹 인터뷰 모듈 구성 요소
│   ├── chains.py                  # LangChain 체인 정의
│   ├── conditions.py              # 조건부 라우팅 함수
│   ├── models.py                  # 사용하는 LLM 모델 설정
│   ├── nodes.py                   # Workflow 노드 클래스들 정의
│   ├── prompts.py                 # 프롬프트 템플릿
│   ├── state.py                   # 상태 정의
│   ├── tools.py                   # 도구 함수
│   └── utils.py                   # 유틸리티 함수
├── pyproject.toml                 # 프로젝트 의존성 관리
├── README.md                      # 이 문서
└── workflow.py                    # 포커스 그룹 인터뷰 Workflow 정의
```

## 시작하기

### 1. 환경 설정

#### 필수 API 키 설정

`.env` 파일을 생성하고 다음 API 키들을 설정하세요:

```bash
# Search-Agent 디렉토리에서
cp .env.example .env
```

`.env` 파일에 다음 내용을 추가:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
SMITHERY_MCP_KEY=your_smithery_mcp_key
EXA_API_KEY=your_exa_api_key
```

#### 의존성 설치

```bash
# 메인 모듈 의존성 설치
cd /root/Act2-Marketing/agents/focus_group_interview
pip install -e .

# Search-Agent 의존성 설치
cd Search-Agent
pip install -e .
pip install -e ".[mcp]"  # MCP 서버 의존성 포함
```

### 2. MCP Server 실행

MCP (Microservice Communication Protocol) 서버는 검색 기능을 제공합니다.

#### 옵션 1: 로컬 실행

```bash
cd Search-Agent/mcp_servers

# MCP 서버 시작
python mcp_server.py
```

이 명령어는 다음 서버들을 실행합니다:
- 메인 MCP 서버 (포트 8000)
- 유튜브 트랜스크립트 검색 서버 (포트 8001)
- 웹 검색 서버 (포트 8002)

#### 옵션 2: Docker 실행

```bash
cd Search-Agent/mcp_servers

# Docker Compose로 MCP 서버 시작
docker-compose up -d
```

### 3. 포커스 그룹 인터뷰 Workflow 실행

#### 기본 사용법

```python
from agents.focus_group_interview.workflow import focus_group_interview_workflow

# 초기 상태 설정
initial_state = {
    "interview_topic": "AI 기반 교육 콘텐츠 개선",
    "target_audience": "고등학생",
    "questions": [],
    "responses": []
}

# Workflow 실행
result = focus_group_interview_workflow().invoke(initial_state)
```

#### Streamlit UI 사용

웹 기반 인터페이스를 통해 에이전트를 실행할 수 있습니다:

```bash
cd Search-Agent
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용하세요.

## 주요 기능

### 1. 교육 리소스 검색 (Search-Agent)

- **다중 소스 검색**: 유튜브 트랜스크립트, 위키피디아, 웹 검색 결과
- **콘텐츠 처리**: 중복 제거, 텍스트 정리, 결과 포맷팅
- **교육 자료 생성**: 구조화된 목차 및 토론 질문 생성
- **유연한 설정**: 검색 매개변수 및 모델 선택 커스터마이징

### 2. 포커스 그룹 인터뷰 Workflow

- **주제 검증**: 교육적 토론/인터뷰에 적합한 주제인지 검증
- **질문 생성**: 대상 청중에 맞는 인터뷰 질문 자동 생성
- **응답 분석**: 인터뷰 응답 분석 및 통찰 추출
- **결과 종합**: 교육 콘텐츠 개선을 위한 종합적인 분석 결과 제공

## 개발 및 확장

### 새로운 검색 소스 추가

1. `Search-Agent/src/react_agent/tools.py`에 새로운 검색 도구 추가
2. 해당 도구를 위한 MCP 서버 구현 (필요시)
3. `Search-Agent/src/react_agent/graph.py`에서 워크플로우에 통합

### 포커스 그룹 인터뷰 기능 확장

1. `modules/nodes.py`에 새로운 노드 클래스 추가
2. `modules/chains.py`에 필요한 LangChain 체인 정의
3. `modules/prompts.py`에 관련 프롬프트 템플릿 추가
4. `workflow.py`에서 새 노드를 Workflow에 연결

### 모델 및 설정 변경

- **모델 변경**: `modules/models.py` 또는 `Search-Agent/src/react_agent/configuration.py`에서 설정
- **프롬프트 커스터마이징**: `modules/prompts.py` 또는 `Search-Agent/src/react_agent/prompts.py` 수정
- **검색 매개변수 조정**: `Search-Agent/src/react_agent/configuration.py`에서 설정

## 문제 해결

### MCP 서버 연결 오류

1. MCP 서버가 실행 중인지 확인:
   ```bash
   ps aux | grep mcp_server
   ```

2. 포트 사용 현황 확인:
   ```bash
   netstat -tlnp | grep :8000
   ```

3. 로그 확인:
   ```bash
   tail -f Search-Agent/mcp_servers/mcp_server.log
   ```

### API 키 관련 오류

1. `.env` 파일이 올바른 위치에 있는지 확인
2. API 키가 유효한지 확인
3. 환경 변수가 제대로 로드되는지 확인:
   ```bash
   cd Search-Agent
   python check_env.py
   ```

### 의존성 관련 오류

1. Python 버전 확인 (>=3.13 필요)
2. 가상 환경 활성화 상태 확인
3. 의존성 재설치:
   ```bash
   pip install -e . --force-reinstall
   ```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

프로젝트 개선을 위한 기여를 환영합니다. Pull Request를 제출하기 전에 다음 사항을 확인해주세요:

1. 코드 스타일 가이드라인 준수
2. 테스트 케이스 추가 (해당하는 경우)
3. 문서 업데이트 (기능 변경시)

## 지원

문제가 발생하거나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.
