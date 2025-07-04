"""
Naver HyperClovaX API 클래스
"""
import time
import asyncio
import json
from typing import List, Dict, Any, Optional

try:
    import requests
except ImportError:
    requests = None

from ..utils.config import settings
from .claude_api import APIResponse  # APIResponse 클래스 재사용


class HyperClovaAPI:
    """HyperClovaX API 클래스"""
    
    def __init__(self):
        """HyperClovaX API 클라이언트 초기화"""
        if not requests:
            raise ImportError("requests 패키지가 설치되지 않았습니다. pip install requests")
        
        if not settings.hyperclova_api_key:
            raise ValueError("HYPERCLOVA_API_KEY가 설정되지 않았습니다.")
        
        self.api_key = settings.hyperclova_api_key
        self.api_gateway_url = settings.hyperclova_api_gateway_url
        
        # Request ID가 없으면 자동 생성
        if settings.hyperclova_request_id:
            self.request_id = settings.hyperclova_request_id
        else:
            import uuid
            self.request_id = str(uuid.uuid4())
            print(f"📝 자동 생성된 Request ID: {self.request_id}")
        
        # HyperClovaX 모델 설정
        self.model = "HyperCLOVA X"
        
        # 가격 정보 (추정값 - 실제 가격은 네이버 정책에 따라 다를 수 있음)
        self.input_price_per_million = 2.0  # 추정 $2/1M input tokens
        self.output_price_per_million = 10.0  # 추정 $10/1M output tokens
        
        # API 헤더 설정 (새로운 Bearer 인증 방식)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self.request_id
        }
    
    async def generate_questions(self, user_response: str, context: str = "") -> APIResponse:
        """
        사용자 응답을 기반으로 후속 질문들을 생성합니다
        
        Args:
            user_response: 사용자의 응답
            context: 이전 대화 맥락
            
        Returns:
            APIResponse: 생성된 질문들과 메타데이터
        """
        prompt = self._build_question_prompt(user_response, context)
        return await self._make_request(prompt)
    
    async def generate_report(self, conversation_history: List[Dict], prompt: str) -> APIResponse:
        """
        대화 기록을 바탕으로 보고서를 생성합니다
        
        Args:
            conversation_history: 대화 기록 리스트
            prompt: 보고서 생성 프롬프트
            
        Returns:
            APIResponse: 생성된 보고서와 메타데이터
        """
        report_prompt = self._build_report_prompt(conversation_history, prompt)
        return await self._make_request(report_prompt)
    
    def _build_question_prompt(self, user_response: str, context: str) -> str:
        """질문 생성을 위한 프롬프트 구성"""
        language = "한국어" if settings.test_language == "ko" else "English"
        
        # START 기법 특화 프롬프트
        if "START" in context or "start" in context.lower():
            prompt = f"""
당신은 취업 준비생을 위한 전문 면접 코칭 AI입니다. START 기법을 활용하여 취업준비생의 모호한 경험을 **구체적이고 매력적인 스토리**로 변환할 수 있도록 도와주세요.

**취업준비생 경험 내용:**
{user_response}

**목표**: 위 경험을 바탕으로 **합격할 만한 자기소개서**를 작성할 수 있도록 START 기법의 각 항목별로 다음을 제공해주세요:

---

**💡 START 기법 완성 가이드:**

각 항목별로 다음 3가지를 제공해주세요:
1. **🔍 꼬리질문**: 구체적인 정보를 이끌어내는 질문
2. **📋 실무 예시**: 이 프로젝트에서 있을법한 구체적인 상황/수치
3. **⭐ 기업 어필 포인트**: 자기소개서에서 강조하면 좋을 표현/키워드

---

**📝 응답 형식:**

## S (Situation) - 상황
🔍 **꼬리질문**: [구체적인 상황을 파악하는 질문]
📋 **실무 예시**: [마케팅 인턴이 실제로 경험할 수 있는 상황 예시]  
⭐ **기업 어필**: [이 상황에서 강조할 수 있는 키워드나 표현]

## T (Task) - 과제  
🔍 **꼬리질문**: [명확한 목표/문제를 도출하는 질문]
📋 **실무 예시**: [실제 마케팅 과제 예시]
⭐ **기업 어필**: [문제 인식 능력을 보여주는 표현]

## A (Action) - 행동
🔍 **꼬리질문**: [구체적인 실행 과정을 묻는 질문]  
📋 **실무 예시**: [실제 A/B 테스트나 분석 방법 예시]
⭐ **기업 어필**: [실행력과 분석력을 보여주는 키워드]

## R (Result) - 결과
🔍 **꼬리질문**: [정량적 성과를 확인하는 질문]
📋 **실무 예시**: [실제 CTR, 전환율 개선 수치 예시]  
⭐ **기업 어필**: [성과를 임팩트 있게 표현하는 방법]

## T (Takeaway) - 교훈
🔍 **꼬리질문**: [성장과 학습을 확인하는 질문]
📋 **실무 예시**: [마케팅 인사이트나 스킬 향상 예시]
⭐ **기업 어필**: [지속적 학습과 성장 의지를 보여주는 표현]

**중요**: 각 항목은 취업준비생이 **"아, 이런 식으로 표현하면 되겠구나!"** 하고 바로 활용할 수 있을 정도로 구체적이고 실용적으로 작성해주세요.
"""
        else:
            # 기본 질문 생성 프롬프트
            prompt = f"""
당신은 사용자와의 대화에서 의미 있는 후속 질문을 생성하는 AI입니다.

이전 맥락: {context}
사용자 응답: {user_response}

위 사용자 응답을 바탕으로 5개의 후속 질문을 생성해주세요.
질문은 다음 조건을 만족해야 합니다:
1. 사용자의 응답과 관련성이 높을 것
2. 더 구체적인 정보를 얻을 수 있을 것
3. 자연스럽고 대화식일 것
4. {language}로 작성될 것

응답 형식:
1. [첫 번째 질문]
2. [두 번째 질문]
3. [세 번째 질문]
4. [네 번째 질문]
5. [다섯 번째 질문]
"""
        
        return prompt
    
    def _build_report_prompt(self, conversation_history: List[Dict], prompt: str) -> str:
        """보고서 생성을 위한 프롬프트 구성"""
        language = "한국어" if settings.test_language == "ko" else "English"
        
        # 대화 기록을 텍스트로 변환
        conversation_text = "\n".join([
            f"{'사용자' if msg.get('role') == 'user' else 'AI'}: {msg.get('content', '')}"
            for msg in conversation_history
        ])
        
        report_prompt = f"""
다음 대화 기록을 바탕으로 상세한 보고서를 작성해주세요.

대화 기록:
{conversation_text}

보고서 요구사항: {prompt}

보고서는 다음 구조로 작성해주세요:
1. 요약 (Summary)
2. 주요 내용 (Main Content)
3. 분석 및 인사이트 (Analysis & Insights)
4. 결론 (Conclusion)

보고서는 {language}로 작성하고, 500-1000단어 분량으로 작성해주세요.
"""
        return report_prompt
    
    async def _make_request(self, prompt: str) -> APIResponse:
        """실제 API 요청을 수행합니다"""
        start_time = time.time()
        
        # HyperClovaX API 요청 데이터 구성
        request_data = {
            "messages": [
                {
                    "role": "system",
                    "content": "당신은 도움이 되는 AI 어시스턴트입니다."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "topP": 0.8,
            "topK": 0,
            "maxTokens": 2000,
            "temperature": 0.7,
            "repeatPenalty": 1.2,
            "stopBefore": [],
            "includeAiFilters": True
        }
        
        try:
            # 비동기 HTTP 요청 (새로운 API 엔드포인트)
            api_url = f"{self.api_gateway_url}/testapp/v1/chat-completions/HCX-003"
            response = await asyncio.to_thread(
                self._sync_post_request,
                api_url,
                request_data
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # 응답 내용 추출
                content = result.get("result", {}).get("message", {}).get("content", "")
                
                # 토큰 사용량 계산 (추정값)
                input_tokens = len(prompt.split()) * 1.3  # 대략적인 토큰 추정
                output_tokens = len(content.split()) * 1.3
                total_tokens = int(input_tokens + output_tokens)
                
                # 비용 계산
                input_cost = (input_tokens / 1_000_000) * self.input_price_per_million
                output_cost = (output_tokens / 1_000_000) * self.output_price_per_million
                total_cost = input_cost + output_cost
                
                return APIResponse(
                    content=content,
                    tokens_used=total_tokens,
                    response_time=response_time,
                    cost=total_cost
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                return APIResponse(
                    content="",
                    tokens_used=0,
                    response_time=response_time,
                    cost=0.0,
                    error=error_msg
                )
                
        except Exception as e:
            end_time = time.time()
            return APIResponse(
                content="",
                tokens_used=0,
                response_time=end_time - start_time,
                cost=0.0,
                error=str(e)
            )
    
    def _sync_post_request(self, url: str, data: Dict) -> Any:
        """동기 HTTP POST 요청"""
        assert requests is not None, "requests 모듈이 초기화되지 않았습니다"
        return requests.post(
            url,
            headers=self.headers,
            json=data,
            timeout=settings.request_timeout
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보를 반환합니다"""
        return {
            "provider": "Naver",
            "model": self.model,
            "input_price_per_million": self.input_price_per_million,
            "output_price_per_million": self.output_price_per_million
        } 