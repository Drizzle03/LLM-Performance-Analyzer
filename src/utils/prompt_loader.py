"""
프롬프트 로더 유틸리티

프롬프트 파일들을 읽어서 변수를 치환하는 기능을 제공합니다.
"""

import os
from pathlib import Path
from typing import Dict, Any

# 설정 파일 임포트는 런타임에 처리
try:
    from ..config.settings import settings
except ImportError:
    # 절대 경로로 시도
    try:
        from src.config.settings import settings
    except ImportError:
        # 기본값 설정
        class DefaultSettings:
            test_language = "ko"
        settings = DefaultSettings()


class PromptLoader:
    """프롬프트 파일 로더 클래스"""
    
    def __init__(self):
        """프롬프트 폴더 경로 설정"""
        self.prompt_dir = Path(__file__).parent.parent / "prompts"
        self._cache = {}  # 프롬프트 캐시
    
    def load_prompt(self, filename: str, **kwargs) -> str:
        """
        프롬프트 파일을 로드하고 변수를 치환합니다
        
        Args:
            filename: 프롬프트 파일명 (확장자 포함)
            **kwargs: 치환할 변수들
            
        Returns:
            str: 치환된 프롬프트 텍스트
        """
        # 캐시에서 프롬프트 템플릿을 가져오거나 파일에서 읽기
        if filename not in self._cache:
            prompt_path = self.prompt_dir / filename
            if not prompt_path.exists():
                raise FileNotFoundError(f"프롬프트 파일을 찾을 수 없습니다: {prompt_path}")
            
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self._cache[filename] = f.read()
        
        # 변수 치환
        template = self._cache[filename]
        
        # 기본 변수들 추가
        default_vars = {
            'language': "한국어" if settings.test_language == "ko" else "English"
        }
        
        # 사용자 제공 변수와 기본 변수 병합
        variables = {**default_vars, **kwargs}
        
        # 변수 치환 수행
        try:
            return template.format(**variables)
        except KeyError as e:
            raise ValueError(f"프롬프트 템플릿에서 필요한 변수를 찾을 수 없습니다: {e}")
    
    def get_question_prompt(self, user_response: str, context: str = "", use_start: bool = False, simple: bool = False) -> str:
        """
        질문 생성 프롬프트 가져오기
        
        Args:
            user_response: 사용자 응답
            context: 이전 대화 맥락
            use_start: START 기법 사용 여부
            simple: 간단한 프롬프트 사용 여부 (Haiku 등)
            
        Returns:
            str: 질문 생성 프롬프트
        """
        if use_start:
            # START 기법 질문 생성
            filename = "question_generation_start_simple.txt" if simple else "question_generation_start.txt"
            return self.load_prompt(filename, user_response=user_response, context=context)
        else:
            # 일반 질문 생성
            filename = "question_generation_simple.txt" if simple else "question_generation.txt"
            return self.load_prompt(filename, user_response=user_response, context=context)
    
    def get_report_prompt(self, user_response: str, context: str = "") -> str:
        """
        보고서 생성 프롬프트 가져오기
        
        Args:
            user_response: 사용자의 응답
            context: 이전 대화 맥락
            
        Returns:
            str: 보고서 생성 프롬프트
        """
        return self.load_prompt(
            "report_generation.txt",
            user_response=user_response,
            context=context
        )
    
    def list_prompts(self) -> list:
        """
        사용 가능한 프롬프트 파일 목록 반환
        
        Returns:
            list: 프롬프트 파일명 리스트
        """
        if not self.prompt_dir.exists():
            return []
        
        return [f.name for f in self.prompt_dir.glob("*.txt")]
    
    def clear_cache(self):
        """프롬프트 캐시 클리어"""
        self._cache.clear()


# 전역 프롬프트 로더 인스턴스
prompt_loader = PromptLoader() 