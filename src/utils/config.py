"""
환경 설정 및 API 키 관리 모듈
"""
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env 파일 로드
load_dotenv()

class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # Claude API 설정
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # HyperClovaX API 설정
    hyperclova_api_key: Optional[str] = os.getenv("HYPERCLOVA_API_KEY")
    hyperclova_api_gateway_url: str = os.getenv(
        "HYPERCLOVA_API_GATEWAY_URL", 
        "https://clovastudio.stream.ntruss.com"
    )
    hyperclova_request_id: Optional[str] = os.getenv("HYPERCLOVA_REQUEST_ID")
    
    # OpenAI API 설정 (ChatGPT)
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Google AI 설정 (Gemini)
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    
    # xAI 설정 (Grok) - OpenAI 호환 API 사용
    grok_api_key: Optional[str] = os.getenv("GROK_API_KEY")
    grok_base_url: str = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")
    grok_model: str = os.getenv("GROK_MODEL", "grok-3")
    
    # 테스트 설정
    test_language: str = os.getenv("TEST_LANGUAGE", "ko")
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    # 경로 설정
    results_dir: str = os.getenv("RESULTS_DIR", "./results")
    data_dir: str = os.getenv("DATA_DIR", "./data")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def validate_api_keys(self) -> bool:
        """API 키가 설정되어 있는지 확인"""
        print("🔑 API 키 상태 확인:")
        
        available_apis = []
        
        # Claude API
        if self.anthropic_api_key:
            print("  ✅ Claude API: 설정됨")
            available_apis.append("claude")
        else:
            print("  ❌ Claude API: 미설정")
        
        # OpenAI API (ChatGPT)
        if self.openai_api_key:
            print("  ✅ OpenAI API (ChatGPT): 설정됨")
            available_apis.append("openai")
        else:
            print("  ❌ OpenAI API (ChatGPT): 미설정")
        
        # Google AI (Gemini)
        if self.google_api_key:
            print("  ✅ Google AI (Gemini): 설정됨")
            available_apis.append("gemini")
        else:
            print("  ❌ Google AI (Gemini): 미설정")
        
        # xAI (Grok)
        if self.grok_api_key:
            print("  ✅ xAI (Grok): 설정됨")
            available_apis.append("grok")
        else:
            print("  ❌ xAI (Grok): 미설정")
        
        # HyperClovaX API
        if self.hyperclova_api_key:
            print("  ✅ HyperClovaX API: 설정됨")
            available_apis.append("hyperclova")
        else:
            print("  ❌ HyperClovaX API: 미설정")
        
        # Request ID 확인
        if not self.hyperclova_request_id:
            print("  💡 HYPERCLOVA_REQUEST_ID: 자동 생성됩니다")
        
        if not available_apis:
            print("\n❌ 사용 가능한 API가 없습니다. 최소 1개 이상의 API 키를 설정해주세요.")
            return False
        
        print(f"\n🎯 사용 가능한 API: {', '.join(available_apis)} ({len(available_apis)}개)")
        return True

# 전역 설정 인스턴스
settings = Settings() 