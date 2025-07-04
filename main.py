#!/usr/bin/env python3
"""
Claude API vs HyperClovaX API 성능 비교 도구
메인 실행 파일
"""
import sys
import os

# src 디렉토리를 파이썬 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli.main import main

if __name__ == "__main__":
    main() 