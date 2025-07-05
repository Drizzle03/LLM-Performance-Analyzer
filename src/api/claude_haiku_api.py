"""
Anthropic Claude 3.5 Haiku API 클래스
"""
import time
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    import anthropic
except ImportError:
    anthropic = None

from ..utils.config import settings
from ..utils.prompt_loader import prompt_loader


@dataclass
class APIResponse:
    """API 응답 데이터 클래스"""
    content: str
    tokens_used: int
    response_time: float
    cost: float
    error: Optional[str] = None


class ClaudeHaikuAPI:
    """Claude 3.5 Haiku API 클래스 - 빠르고 경제적인 모델"""
    
    def __init__(self):
        """Claude 3.5 Haiku API 클라이언트 초기화"""
        if not anthropic:
            raise ImportError("anthropic 패키지가 설치되지 않았습니다. pip install anthropic")
        
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-5-haiku-20241022"
        
        # 가격 정보 (1M 토큰당 달러) - Haiku는 더 저렴!
        self.input_price_per_million = 1.0   # $1/1M input tokens  
        self.output_price_per_million = 5.0  # $5/1M output tokens
    
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
        """질문 생성을 위한 프롬프트 구성 - Haiku 최적화"""
        # START 기법 특화 프롬프트 (간결하게 최적화)
        use_start = "START" in context or "start" in context.lower()
        
        return prompt_loader.get_question_prompt(
            user_response=user_response,
            context=context,
            use_start=use_start,
            simple=True  # Haiku는 간결한 프롬프트 사용
        )
    
    def _build_report_prompt(self, conversation_history: List[Dict], prompt: str) -> str:
        """보고서 생성을 위한 프롬프트 구성 - Haiku 최적화"""
        return prompt_loader.get_report_prompt(conversation_history, prompt)
    
    async def _make_request(self, prompt: str) -> APIResponse:
        """실제 API 요청을 수행합니다"""
        start_time = time.time()
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=1500,  # Haiku는 더 적은 토큰으로 효율적 사용
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # 토큰 사용량 계산
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            
            # 비용 계산 (입력 토큰 + 출력 토큰)
            input_cost = (input_tokens / 1_000_000) * self.input_price_per_million
            output_cost = (output_tokens / 1_000_000) * self.output_price_per_million
            total_cost = input_cost + output_cost
            
            # 응답 텍스트 추출 (getattr로 안전하게 처리)
            content_text = ""
            if response.content and len(response.content) > 0:
                first_block = response.content[0]
                content_text = getattr(first_block, 'text', str(first_block))
            
            return APIResponse(
                content=content_text,
                tokens_used=total_tokens,
                response_time=response_time,
                cost=total_cost
            )
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            return APIResponse(
                content="",
                tokens_used=0,
                response_time=response_time,
                cost=0.0,
                error=str(e)
            )
    
    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보 반환"""
        return {
            "name": "Claude 3.5 Haiku",
            "provider": "Anthropic",
            "model": self.model,
            "input_price_per_million": self.input_price_per_million,
            "output_price_per_million": self.output_price_per_million,
            "features": ["빠른 응답", "경제적 가격", "간결한 답변"],
            "optimal_use": ["빠른 초안", "대량 처리", "비용 최적화"]
        } 