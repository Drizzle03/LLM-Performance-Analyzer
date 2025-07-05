"""
Google AI API 클래스 (Gemini)
"""
import time
import asyncio
from typing import List, Dict, Any, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from ..utils.config import settings
from ..utils.prompt_loader import prompt_loader
from .claude_api import APIResponse  # APIResponse 클래스 재사용


class GeminiAPI:
    """Google AI API 클래스 (Gemini)"""
    
    def __init__(self):
        """Google AI API 클라이언트 초기화"""
        if not genai:
            raise ImportError("google-generativeai 패키지가 설치되지 않았습니다. pip install google-generativeai")
        
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")
        
        # Google AI 설정
        genai.configure(api_key=settings.google_api_key)
        self.model_name = settings.gemini_model
        self.model = genai.GenerativeModel(self.model_name)
        
        # 가격 정보 (2024년 기준, USD/1M tokens)
        self.model_pricing = {
            "gemini-1.5-pro": {"input": 3.5, "output": 10.5},
            "gemini-1.5-flash": {"input": 0.075, "output": 0.3},
            "gemini-pro": {"input": 0.5, "output": 1.5}
        }
        
        self.input_price_per_million = self.model_pricing.get(self.model_name, {"input": 3.5})["input"]
        self.output_price_per_million = self.model_pricing.get(self.model_name, {"output": 10.5})["output"]
    
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
        
        try:
            # 비동기로 Gemini API 호출
            response = await asyncio.to_thread(
                self._sync_gemini_request,
                prompt
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # 응답 내용 추출
            content = response.text
            
            # 토큰 사용량 추정 (한국어 특성 반영)
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
            
        except Exception as e:
            end_time = time.time()
            return APIResponse(
                content="",
                tokens_used=0,
                response_time=end_time - start_time,
                cost=0.0,
                error=str(e)
            )
    
    def _sync_gemini_request(self, prompt: str):
        """동기 Gemini API 요청"""
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=2000,
            temperature=0.7,
        )
        
        return self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보를 반환합니다"""
        return {
            "provider": "Google AI",
            "model": self.model_name,
            "input_price_per_million": self.input_price_per_million,
            "output_price_per_million": self.output_price_per_million
        } 