# 📊 START 기법 테스트 도구

**START 기법**을 활용한 자기소개서 작성 및 면접 준비를 위한 AI 모델 성능 비교 도구입니다.

## 🚀 주요 기능

- **START 질문 생성**: 경험을 START 기법으로 구체화하는 질문들을 생성
- **보고서 작성**: 경험을 START 기법에 따라 체계적으로 정리하고 핵심 역량 도출
- **AI 모델 비교**: 6개 주요 AI 모델의 성능 및 응답 내용 비교
- **마크다운 보고서**: 결과를 마크다운 파일로 자동 저장

## 🤖 지원 AI 모델

### 1. Claude (Anthropic)
- **모델**: `claude-3-5-sonnet-20241022`
- **가격**: $3/1M 입력 토큰, $15/1M 출력 토큰
- **특징**: 고품질 응답, 긴 컨텍스트 처리 우수

### 2. Claude Haiku (Anthropic)
- **모델**: `claude-3-5-haiku-20241022`
- **가격**: $1/1M 입력 토큰, $5/1M 출력 토큰
- **특징**: 빠른 응답, 경제적 비용, 간결한 답변

### 3. ChatGPT (OpenAI)
- **모델**: `gpt-4o` (기본값)
- **가격**: $5/1M 입력 토큰, $15/1M 출력 토큰
- **특징**: 균형 잡힌 성능, 빠른 처리 속도

### 4. Gemini (Google)
- **모델**: `gemini-1.5-pro` (기본값)
- **가격**: $3.5/1M 입력 토큰, $10.5/1M 출력 토큰
- **특징**: 고품질 응답, 대화형 상호작용 우수

### 5. Grok (xAI)
- **모델**: `grok-3` (기본값)
- **가격**: $3/1M 입력 토큰, $15/1M 출력 토큰
- **특징**: 창의적 응답, 유머러스한 표현

### 6. HyperClovaX (Naver)
- **모델**: `HCX-003`
- **가격**: $2/1M 입력 토큰, $10/1M 출력 토큰 (추정)
- **특징**: 한국어 특화, 자연스러운 한국어 처리

> **💡 참고**: 한국어 토큰은 조사, 어미, 종성 등으로 인해 영어 대비 약 3배 정도 토큰을 사용합니다.

## 📋 START 기법이란?

**START 기법**은 경험을 구조화하여 면접과 자기소개서에서 효과적으로 어필하는 방법입니다.

- **S (Situation)**: 상황 및 배경
- **T (Task)**: 과제 및 목표
- **A (Action)**: 실행한 행동
- **R (Result)**: 달성한 결과
- **T (Takeaway)**: 배운 교훈

## 🛠️ 설치 및 설정

### 1. 프로젝트 클론
```bash
git clone https://github.com/yourusername/TIO_Prompt_Test.git
cd TIO_Prompt_Test
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 설정
`.env` 파일을 생성하고 API 키들을 설정하세요:

```env
# Claude API (필수)
ANTHROPIC_API_KEY=your_anthropic_api_key

# OpenAI API (필수)
OPENAI_API_KEY=your_openai_api_key

# Google Gemini API (선택)
GOOGLE_API_KEY=your_google_api_key

# xAI Grok API (선택)
XAI_API_KEY=your_xai_api_key

# Naver HyperClovaX API (선택)
HYPERCLOVA_API_KEY=your_hyperclova_api_key
HYPERCLOVA_REQUEST_ID=your_request_id

# 모델 설정 (선택 - 기본값 사용 권장)
OPENAI_MODEL=gpt-4o
GEMINI_MODEL=gemini-1.5-pro
GROK_MODEL=grok-3
```

> **참고**: 모든 API 키가 필요하지 않습니다. 사용 가능한 API만 활용됩니다.

## 📖 사용 방법

### 1. START 질문 생성
경험을 START 기법으로 구체화하는 질문들을 생성합니다.

```bash
python -m src.cli.main questions
```

**결과:**
- 터미널에 성능 비교 및 응답 내용 출력
- `reports/START_questions_YYYYMMDD_HHMMSS.md` 파일 자동 저장

### 2. 보고서 작성
경험을 START 기법에 따라 체계적으로 정리하고 핵심 역량을 도출합니다.

```bash
python -m src.cli.main reports
```

**결과:**
- 터미널에 성능 비교 및 응답 내용 출력
- `reports/START_report_YYYYMMDD_HHMMSS.md` 파일 자동 저장

## 📊 보고서 예시

### 성능 비교 테이블
| 모델 | 평균 응답시간 (초) | 평균 비용 ($) | 평균 토큰 수 |
|------|------------------|-------------|-------------|
| Claude | 8.98 | $0.0117 | 1596 |
| Claude Haiku | 10.06 | $0.0039 | 1598 |
| ChatGPT | 5.80 | $0.0081 | 952 |
| Gemini | 9.21 | $0.0092 | 1374 |
| Grok | 11.98 | $0.0105 | 1188 |
| HyperClovaX | 8.70 | $0.0050 | 1098 |

### 응답 내용 비교
각 AI 모델의 완전한 응답 내용을 비교하여 최적의 결과를 선택할 수 있습니다.

## 🔧 고급 기능

### 프롬프트 관리 시스템
프롬프트는 `src/prompts/` 폴더에서 중앙 관리됩니다:

```
src/prompts/
├── question_generation.txt              # 일반 질문 생성
├── question_generation_simple.txt       # 간단한 질문 생성 (Haiku용)
├── question_generation_start.txt        # START 기법 질문 생성
├── question_generation_start_simple.txt # 간단한 START 질문
└── report_generation.txt                # 보고서 생성
```

### 테스트 시나리오
현재 **마케팅 인턴 경험** 시나리오를 기반으로 테스트가 진행됩니다. 
`src/cli/main.py`에서 시나리오를 수정할 수 있습니다.

## 📁 프로젝트 구조

```
TIO_Prompt_Test/
├── src/
│   ├── api/                    # AI API 클래스들
│   ├── cli/                    # CLI 도구
│   ├── prompts/                # 프롬프트 템플릿
│   ├── utils/                  # 유틸리티 함수
│   └── config/                 # 설정 파일
├── reports/                    # 생성된 보고서
├── requirements.txt            # 의존성 목록
├── .env                       # 환경 변수 (생성 필요)
└── README.md                  # 이 문서
```

## 🎯 활용 예시

### 1. 취업 준비생
- 다양한 경험을 START 기법으로 구조화
- 각 AI 모델의 관점을 비교하여 최적의 표현 방법 선택
- 핵심 역량 키워드 도출

### 2. 면접 준비
- 예상 질문에 대한 답변을 START 기법으로 정리
- 여러 AI 모델의 피드백을 통해 답변 품질 개선

### 3. 자기소개서 작성
- 경험을 체계적으로 정리하고 핵심 역량 강조
- 다양한 AI 모델의 관점으로 내용 검토

## 🔍 성능 최적화

### 💰 비용 효율성
1. **Claude Haiku**: $1 + $5 = $6/1M 토큰 (가장 경제적)
2. **HyperClovaX**: $2 + $10 = $12/1M 토큰 (한국어 특화)
3. **Gemini Pro**: $3.5 + $10.5 = $14/1M 토큰 (고품질 대화)
4. **Claude**: $3 + $15 = $18/1M 토큰 (고품질 응답)
5. **Grok**: $3 + $15 = $18/1M 토큰 (창의적 응답)
6. **ChatGPT**: $5 + $15 = $20/1M 토큰 (균형 잡힌 성능)

### ⚡ 응답 속도
- **ChatGPT**: 평균 5-8초 (가장 빠름)
- **HyperClovaX**: 평균 7-10초 (한국어 특화)
- **Claude Haiku**: 평균 8-12초 (경제적)
- **Gemini Pro**: 평균 8-12초 (고품질)
- **Claude**: 평균 10-15초 (고품질 응답)
- **Grok**: 평균 10-15초 (창의적 응답)

### 🇰🇷 한국어 품질
1. **HyperClovaX**: 한국어 특화 모델, 자연스러운 표현
2. **Claude**: 높은 품질의 한국어 응답
3. **ChatGPT**: 안정적인 한국어 처리
4. **Gemini Pro**: 우수한 한국어 대화 능력
5. **Claude Haiku**: 간결하고 명확한 한국어
6. **Grok**: 창의적이지만 가끔 부자연스러운 표현

### 🎯 모델 선택 가이드
- **비용 최적화**: Claude Haiku 또는 HyperClovaX
- **속도 우선**: ChatGPT 또는 HyperClovaX
- **한국어 품질**: HyperClovaX 또는 Claude
- **창의성**: Grok 또는 Claude
- **균형**: ChatGPT 또는 Gemini Pro

## 🐛 문제 해결

### API 키 관련
```bash
# API 키 설정 확인
python -c "from src.config.settings import settings; settings.validate_api_keys()"
```

### 의존성 문제
```bash
# 의존성 재설치
pip install -r requirements.txt --upgrade
```

## 🤝 기여하기

1. 이 저장소를 포크하세요
2. 새로운 브랜치를 생성하세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성하세요

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 📞 지원

문제가 발생하면 Issues를 통해 문의해주세요.

---

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**
