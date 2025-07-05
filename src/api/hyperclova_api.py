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
from ..utils.prompt_loader import prompt_loader
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
    
    async def generate_report(self, user_response: str, context: str = "") -> APIResponse:
        """
        사용자 응답을 바탕으로 보고서를 생성합니다
        
        Args:
            user_response: 사용자의 응답
            context: 이전 대화 맥락
            
        Returns:
            APIResponse: 생성된 보고서와 메타데이터
        """
        report_prompt = self._build_report_prompt(user_response, context)
        return await self._make_request(report_prompt)
    
    def _build_question_prompt(self, user_response: str, context: str) -> str:
        """질문 생성을 위한 프롬프트 구성"""
        use_start = "START" in context or "start" in context.lower()
        
        return prompt_loader.get_question_prompt(
            user_response=user_response,
            context=context,
            use_start=use_start,
            simple=False
        )
    
    def _build_report_prompt(self, user_response: str, context: str) -> str:
        """보고서 생성을 위한 프롬프트 구성"""
        return prompt_loader.get_report_prompt(user_response, context)
    
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
                
                # 토큰 사용량 계산 (한국어 특성 반영)
                # 한국어는 조사, 어미, 종성 등으로 인해 영어 대비 3배 정도 토큰 사용
                input_tokens = len(prompt.split()) * 3.0  # 한국어 토큰 추정 (보수적)
                output_tokens = len(content.split()) * 3.0
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