# 🚀 TIO Prompt Test - AI API 성능 비교 도구

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 📋 프로젝트 개요

**5개 주요 AI 모델의 성능을 종합 비교**하는 전문 도구입니다. 질문 생성과 보고서 작성 능력을 **품질, 속도, 비용** 측면에서 정량적으로 평가합니다.

### 🎯 특화 기능
- **START 기법 기반 보고서 생성**: 취업준비생을 위한 자기소개서 작성 지원
- **실시간 성능 모니터링**: 응답시간, 토큰 사용량, 비용 실시간 측정
- **다국어 테스트 지원**: 한국어 특화 + 영어 테스트 시나리오

## 🤖 지원 AI 모델

| 모델 | 제공사 | 모델명 | 입력 토큰 가격 | 출력 토큰 가격 | 특징 |
|------|--------|--------|----------------|----------------|------|
| **Claude** | Anthropic | `claude-3-5-sonnet-20241022` | $3.0/1M | $15.0/1M | 균형잡힌 성능, 빠른 속도 |
| **ChatGPT** | OpenAI | `gpt-4o` | $5.0/1M | $15.0/1M | 실용적 접근, 구체적 수치 |
| **Gemini** | Google | `gemini-1.5-pro` | $1.25/1M | $5.0/1M | 무료 티어 제공 |
| **Grok** | xAI | `grok-3` | $3.0/1M | $3.0/1M | 상세한 전문 분석 |
| **HyperClovaX** | Naver | `HyperCLOVA X` | $3.64/1M | $3.64/1M | 한국어 특화, 높은 가성비 |

> *추정값. 실제 테스트에서는 더 저렴한 것으로 확인됨

## 📊 실제 성능 비교 결과

### 🏆 START 기법 보고서 생성 (최신 테스트)

| 순위 | 모델 | 품질 점수 | 응답 시간 | 비용 | 특징 |
|------|------|-----------|----------|------|------|
| 🥇 | **Grok** | **4.10/5.0** | 29.13초 | $0.0279 | 가장 상세하고 전문적 |
| 🥈 | **HyperClovaX** | 3.95/5.0 | 20.20초 | **$0.0039** | 압도적 가성비 |
| 🥉 | **Claude** | 3.89/5.0 | **17.97초** | $0.0197 | 가장 빠른 응답 |

### 💡 모델별 추천 용도

- **🎯 실제 자기소개서 작성**: ChatGPT (실용적, 바로 사용 가능)
- **📚 면접 준비용 심화 자료**: Grok (가장 상세한 분석)
- **⚡ 빠른 초안 작성**: HyperClovaX (압도적 가성비)
- **⚖️ 균형잡힌 활용**: Claude (빠른 속도 + 적당한 분량)

## 🛠️ 설치 및 설정

### 1️⃣ 환경 준비

```bash
# 프로젝트 클론
git clone <repository-url>
cd TIO_Prompt_Test

# Python 가상환경 생성 (권장)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2️⃣ API 키 설정

```bash
# 환경 파일 생성
cp env.example .env  # macOS/Linux
copy env.example .env  # Windows
```

**.env 파일 편집:**
```env
# Claude API (필수)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# OpenAI API (선택)
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4o

# Google AI API (선택)
GOOGLE_API_KEY=your-google-ai-key-here
GEMINI_MODEL=gemini-1.5-pro

# xAI API (선택)
GROK_API_KEY=your-grok-key-here
GROK_MODEL=grok-3

# HyperClovaX API (필수)
HYPERCLOVA_API_KEY=your-hyperclova-key-here
HYPERCLOVA_API_GATEWAY_URL=https://clovastudio.stream.ntruss.com

# 기타 설정
TEST_LANGUAGE=ko
REQUEST_TIMEOUT=60
```

### 3️⃣ 설정 확인

```bash
python main.py info
```

**예상 출력:**
```
🔧 시스템 정보
- 테스트 언어: ko
- 최대 재시도: 3
- 요청 타임아웃: 60초

🔑 API 키 상태 확인:
  ✅ Claude API: 설정됨
  ✅ OpenAI API (ChatGPT): 설정됨
  ✅ Google AI (Gemini): 설정됨
  ✅ xAI (Grok): 설정됨
  ✅ HyperClovaX API: 설정됨

🎯 사용 가능한 API: claude, openai, gemini, grok, hyperclova (5개)
```

## 🚀 사용법

### 📝 질문 생성 테스트

```bash
# 기본 테스트 (3개 시나리오)
python main.py test

# 특정 카테고리 테스트
python main.py test --category start_technique --count 1

# 대량 테스트
python main.py test --category all --count 10
```

### 📋 보고서 생성 테스트 (START 기법)

```bash
# START 기법 보고서 생성
python main.py report --category start_technique_report --count 1

# 다양한 보고서 타입 테스트
python main.py report --category all --count 3
```

### 📊 카테고리 확인

```bash
# 사용 가능한 카테고리 목록
python main.py categories

# 모든 시나리오 목록
python main.py scenarios
```

## 🎯 START 기법 특화 기능

### 📚 START 기법이란?
**S**ituation - **T**ask - **A**ction - **R**esult - **T**akeaway

취업준비생의 모호한 경험을 **구체적이고 매력적인 스토리**로 변환하는 기법

### 💡 프롬프트 구조

각 항목별로 다음 3가지를 제공:
1. **🔍 꼬리질문**: 구체적인 정보를 이끌어내는 질문
2. **📋 실무 예시**: 프로젝트에서 있을법한 구체적인 상황/수치
3. **⭐ 기업 어필 포인트**: 자기소개서에서 강조하면 좋은 표현/키워드

### 📖 실제 결과 예시

**입력 (모호한 경험):**
> "작년 여름에 스타트업에서 마케팅 인턴을 했어요. 메타 광고 집행을 맡았는데 처음엔 결과가 안 좋았어요..."

**출력 (Grok 모델):**
```markdown
## S (Situation) - 상황
🔍 **꼬리질문**: "스타트업에서의 마케팅 인턴십은 어떤 팀이나 프로젝트에 속했으며, 당시 회사의 주된 목표는 무엇이었나요?"
📋 **실무 예시**: "D2C 뷰티 스타트업(직원 30명 규모)에서 3개월간 마케팅팀 인턴으로 근무했습니다. 신제품 런칭을 앞두고 페이스북/인스타그램 광고 성과 개선이 시급한 상황이었으며, 월 광고 예산 2,000만원 규모의 캠페인을 담당했습니다."
⭐ **기업 어필**: 스타트업 환경에서의 빠른 적응력, 실무 중심 업무 경험, 예산 관리 책임감

## 핵심 역량 키워드
1. **데이터 기반 의사결정**: 구글 애널리틱스(GA)를 활용한 이탈률 분석 및 광고 성과 개선
2. **문제 해결 능력**: 낮은 CTR과 높은 이탈률 문제를 인식하고 해결책을 모색한 태도
3. **실험적 접근**: A/B 테스트를 통해 광고 소재를 최적화한 실험 정신
4. **협업 능력**: 디자이너와의 협력을 통해 랜딩페이지 개선에 기여
5. **결과 중심적 태도**: 지속적인 테스트와 수정으로 성과를 향상시킨 노력
```

## 📈 성능 평가 시스템

### 📊 품질 메트릭 (QualityMetrics)

| 항목 | 설명 | 계산 방식 |
|------|------|-----------|
| **관련성 점수** | 원문과의 연관성 | 키워드 겹침 분석 (1 + overlap_ratio × 4) |
| **명확성 점수** | 응답의 명확함 | 질문 개수, 물음표 사용률 기반 |
| **구조 점수** | 체계적 구성 | 번호 매기기, 섹션 구성 평가 |
| **가독성 점수** | 읽기 쉬움 | Flesch-Kincaid Grade Level |
| **종합 점수** | 전체 품질 | (관련성 + 명확성 + 구조) / 3 |

### ⚡ 성능 메트릭 (PerformanceMetrics)

- **응답 시간**: API 호출부터 응답까지의 시간
- **토큰 사용량**: 입력 + 출력 토큰 총량
- **비용**: 실제 사용 비용 (USD)
- **성공률**: 오류 없이 완료된 비율

### 🏆 종합 랭킹 점수

**품질 × 0.6 + 속도 × 0.2 + 비용효율성 × 0.2**

## ⚠️ 중요 고려사항

### 💰 토큰 계산 방식 차이

| 모델 | 토큰 계산 방식 | 정확도 | 비용 신뢰성 |
|------|---------------|--------|------------|
| **Claude, ChatGPT, Grok** | API 제공 (정확) | ✅ 100% | ✅ 신뢰 |
| **Gemini, HyperClovaX** | 단어×1.3 (추정) | ❌ 60-80% | ⚠️ 불정확 |

> **주의**: HyperClovaX와 Gemini의 비용은 **추정값**이며, 실제 사용 시 차이가 있을 수 있습니다.

### 🚫 제한사항

- **Gemini**: 무료 티어 할당량 제한으로 간헐적 오류 발생
- **Grok**: 높은 지연시간으로 타임아웃 발생 가능
- **HyperClovaX**: Bearer 토큰 방식 인증 필요

## 🔧 고급 사용법

### 🎛️ 환경변수 설정

```bash
# 모델 변경
export OPENAI_MODEL=gpt-4o-mini  # 비용 절약
export GEMINI_MODEL=gemini-1.5-flash  # 고속 처리

# 성능 조정
export REQUEST_TIMEOUT=120  # 타임아웃 연장
export MAX_RETRIES=5  # 재시도 증가
```

### 📁 결과 파일 구조

```json
{
  "test_id": "report_test_1",
  "timestamp": "2025-07-05T00:13:06.204954",
  "api_provider": "Claude",
  "task_type": "report_generation",
  "input_text": "원본 사용자 입력...",
  "output_text": "생성된 보고서 내용...",
  "quality_metrics": {
    "relevance_score": 1.68,
    "clarity_score": 5.0,
    "structure_score": 5.0,
    "overall_score": 3.89
  },
  "performance_metrics": {
    "response_time": 17.97,
    "tokens_used": 1990,
    "cost": 0.019722,
    "success_rate": 100.0
  }
}
```

## 🚀 최적화 팁

### 💸 비용 최적화

```bash
# 테스트용 경량 모델 사용
export OPENAI_MODEL=gpt-4o-mini  # $0.15/$0.6 per 1M tokens
export GEMINI_MODEL=gemini-1.5-flash  # $0.075/$0.3 per 1M tokens

# HyperClovaX 우선 사용 (한국어 + 저비용)
python main.py test --category start_technique_report
```

### ⚡ 성능 최적화

- **병렬 API 호출**: 여러 모델 동시 테스트
- **실패 API 스킵**: 전체 테스트 중단 방지
- **타임아웃 설정**: 무한 대기 방지

## 🎯 TIO 서비스 연관성

이 도구는 **TIO 랜딩페이지** 서비스의 핵심 기능을 검증합니다:

- **서비스**: 자기소개서 작성 전 경험 정리 지원
- **목표**: "질문만 답하면 경험 정리 끝"
- **결과**: "자소서에 바로 쓸 수 있는 리포트 생성"

### 📋 PRD 연관 기능

1. **대화 체험**: AI와의 질문-답변을 통한 경험 발굴
2. **경험 구조화**: START 기법 기반 체계적 정리
3. **강점 도출**: 핵심 역량 키워드 자동 추출
4. **자소서 연결**: 완성된 리포트의 자기소개서 활용

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **문서**: 이 README 파일
- **예제**: `src/tests/test_scenarios.py` 참조

---

> 💡 **팁**: 각 AI 모델의 특성을 이해하고 용도에 맞게 선택하면 최적의 결과를 얻을 수 있습니다! 
