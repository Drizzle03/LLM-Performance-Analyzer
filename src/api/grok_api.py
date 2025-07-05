"""
xAI API 클래스 (Grok)
"""
import time
import asyncio
from typing import List, Dict, Any, Optional

try:
    import openai
except ImportError:
    openai = None

from ..utils.config import settings
from ..utils.prompt_loader import prompt_loader
from .claude_api import APIResponse  # APIResponse 클래스 재사용


class GrokAPI:
    """xAI API 클래스 (Grok)"""
    
    def __init__(self):
        """xAI API 클라이언트 초기화"""
        if not openai:
            raise ImportError("openai 패키지가 설치되지 않았습니다. pip install openai")
        
        if not settings.grok_api_key:
            raise ValueError("GROK_API_KEY가 설정되지 않았습니다.")
        
        # xAI 클라이언트 초기화 (OpenAI 호환)
        self.client = openai.OpenAI(
            api_key=settings.grok_api_key,
            base_url=settings.grok_base_url
        )
        self.model = settings.grok_model
        
        # 가격 정보 (2024년 기준, USD/1M tokens)
        self.model_pricing = {
            "grok-3": {"input": 3.0, "output": 15.0},  # 실제 가격 ($3.00 / $15.00 per 1M tokens)
            "grok-2": {"input": 10.0, "output": 30.0}     # 추정 가격
        }
        
        self.input_price_per_million = self.model_pricing.get(self.model, {"input": 5.0})["input"]
        self.output_price_per_million = self.model_pricing.get(self.model, {"output": 15.0})["output"]
    
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
        use_start = "START" in context or "start" in context.lower()
        
        return prompt_loader.get_question_prompt(
            user_response=user_response,
            context=context,
            use_start=use_start,
            simple=False
        )
    
    def _build_report_prompt(self, conversation_history: List[Dict], prompt: str) -> str:
        """보고서 생성을 위한 프롬프트 구성"""
        return prompt_loader.get_report_prompt(conversation_history, prompt)
    
    async def _make_request(self, prompt: str) -> APIResponse:
        """실제 API 요청을 수행합니다"""
        start_time = time.time()
        
        try:
            # 비동기로 Grok API 호출
            response = await asyncio.to_thread(
                self._sync_grok_request,
                prompt
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # 응답 내용 추출
            content = response.choices[0].message.content
            
            # 토큰 사용량 정보 (xAI API가 제공하는 경우)
            if hasattr(response, 'usage') and response.usage:
                usage = response.usage
                input_tokens = usage.prompt_tokens
                output_tokens = usage.completion_tokens
                total_tokens = usage.total_tokens
            else:
                # 토큰 사용량 추정
                input_tokens = len(prompt.split()) * 1.3
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
            
        except Exception as e:
            end_time = time.time()
            return APIResponse(
                content="",
                tokens_used=0,
                response_time=end_time - start_time,
                cost=0.0,
                error=str(e)
            )
    
    def _sync_grok_request(self, prompt: str):
        """동기 Grok API 요청"""
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            timeout=settings.request_timeout
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보를 반환합니다"""
        return {
            "provider": "xAI",
            "model": self.model,
            "input_price_per_million": self.input_price_per_million,
            "output_price_per_million": self.output_price_per_million
        } 