"""
CLI 메인 애플리케이션 - START 기법 특화 도구
"""
import asyncio
import os
import sys
import json
import re
import argparse
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    import click
except ImportError:
    click = None

from ..api.claude_api import ClaudeAPI
from ..api.claude_haiku_api import ClaudeHaikuAPI
from ..api.hyperclova_api import HyperClovaAPI
from ..api.openai_api import OpenAIAPI
from ..api.gemini_api import GeminiAPI
from ..api.grok_api import GrokAPI
from ..metrics.evaluator import MetricsEvaluator
from ..utils.config import settings


class STARTTester:
    """START 기법 테스트 도구"""
    
    def __init__(self):
        """테스트 도구 초기화"""
        self.apis = {}
        self.evaluator = MetricsEvaluator()
        
        # 모든 API 초기화 시도
        api_classes = {
            "Claude": ClaudeAPI,
            "Claude Haiku": ClaudeHaikuAPI,
            "ChatGPT": OpenAIAPI,
            "Gemini": GeminiAPI,
            "Grok": GrokAPI,
            "HyperClovaX": HyperClovaAPI
        }
        
        for name, api_class in api_classes.items():
            try:
                self.apis[name] = api_class()
                print(f"✅ {name} API 초기화 완료")
            except Exception as e:
                print(f"❌ {name} API 초기화 실패: {e}")
        
        if not self.apis:
            print("❌ 사용 가능한 API가 없습니다.")
        else:
            print(f"🎯 총 {len(self.apis)}개 AI 모델 사용 가능: {', '.join(self.apis.keys())}")
        
        # 고정 테스트 시나리오
        self.question_scenario = {
            "id": "start_method_01",
            "name": "마케팅 인턴십 경험",
            "user_response": "대학교 3학년 때 6개월간 마케팅 회사에서 인턴을 했습니다. 주로 SNS 마케팅을 담당했고, 회사 인스타그램 팔로워를 늘리는 일을 했습니다. 처음에는 어려웠지만 나중에는 좋은 결과를 얻었습니다.",
            "context": "START 기법을 활용한 대학생 마케팅 인턴십 경험을 통한 성장 스토리"
        }
        
        self.report_scenario = {
            "id": "report_05",
            "name": "팀 프로젝트 리더십 경험",
            "user_response": "팀 프로젝트에서 리더를 맡았습니다. 5명의 팀원과 함께 3개월간 프로젝트를 진행했고, 중간에 갈등이 있었지만 결국 좋은 성과를 냈습니다. 이 경험을 통해 리더십을 배웠습니다.",
            "context": "팀 프로젝트 리더십 경험을 통한 역량 개발"
        }
        
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def _get_start_scenarios(self):
        """START 기법 시나리오 1개 반환 (start_method_01)"""
        return [self.question_scenario]
    
    def _get_report_scenarios(self):
        """보고서 생성 시나리오 1개 반환 (report_05)"""
        return [self.report_scenario]
    
    async def test_start_questions(self):
        """START 질문 생성 테스트"""
        print("\n🤔 START 질문 생성 테스트를 시작합니다...\n")
        
        scenarios = self._get_start_scenarios()
        results = {api_name.lower(): [] for api_name in self.apis.keys()}
        
        for i, scenario in enumerate(scenarios):
            print(f"📝 시나리오 {i+1}: {scenario['name']}")
            
            for api_name, api_instance in self.apis.items():
                try:
                    # START 기법 질문 생성
                    result = await api_instance.generate_questions(
                        scenario['user_response'], 
                        scenario['context']
                    )
                    
                    if not result.error:
                        results[api_name.lower()].append({
                            "scenario": scenario['name'],
                            "content": result.content,
                            "response_time": result.response_time,
                            "tokens": result.tokens_used,
                            "cost": result.cost
                        })
                    else:
                        print(f"❌ {api_name}: API 오류 - {result.error}")
                        
                except Exception as e:
                    print(f"❌ {api_name}: 예외 발생 - {str(e)}")
        
        self._print_question_results(results)
        return results
    
    async def test_reports(self):
        """보고서 생성 테스트"""
        print("\n📋 보고서 생성 테스트를 시작합니다...\n")
        
        scenarios = self._get_report_scenarios()
        results = {api_name.lower(): [] for api_name in self.apis.keys()}
        
        for i, scenario in enumerate(scenarios):
            print(f"📄 시나리오 {i+1}: {scenario['name']}")
            
            for api_name, api_instance in self.apis.items():
                try:
                    result = await api_instance.generate_report(
                        scenario['user_response'], 
                        scenario['context']
                    )
                    
                    if not result.error:
                        results[api_name.lower()].append({
                            "scenario": scenario['name'],
                            "content": result.content,
                            "response_time": result.response_time,
                            "tokens": result.tokens_used,
                            "cost": result.cost
                        })
                    else:
                        print(f"❌ {api_name}: API 오류 - {result.error}")
                        
                except Exception as e:
                    print(f"❌ {api_name}: 예외 발생 - {str(e)}")
        
        self._print_report_results(results)
        return results
    
    def _print_question_results(self, results: Dict[str, Any]):
        """질문 생성 결과 출력 (단순 표 형식)"""
        print("\n# 📊 START 질문 생성 결과\n")
        
        # 성능 테이블
        print("## 🏆 모델별 성능 비교\n")
        print("| 모델 | 평균 응답시간 (초) | 평균 비용 ($) | 평균 토큰 수 |")
        print("|------|------------------|-------------|-------------|")
        
        for api_name in self.apis.keys():
            api_key = api_name.lower()
            if api_key in results and results[api_key]:
                avg_time = sum(r["response_time"] for r in results[api_key]) / len(results[api_key])
                avg_cost = sum(r["cost"] for r in results[api_key]) / len(results[api_key])
                avg_tokens = sum(r["tokens"] for r in results[api_key]) / len(results[api_key])
                print(f"| {api_name} | {avg_time:.2f} | ${avg_cost:.4f} | {avg_tokens:.0f} |")
        
        # 응답 내용 비교
        print("\n## 🔍 모델별 응답 내용 비교\n")
        scenarios = self._get_start_scenarios()
        
        for i, scenario in enumerate(scenarios):
            print(f"### 시나리오 {i+1}: {scenario['name']}\n")
            print("| 모델 | 생성된 질문 내용 |")
            print("|------|---------------------|")
            
            for api_name in self.apis.keys():
                api_key = api_name.lower()
                if api_key in results and results[api_key] and len(results[api_key]) > i:
                    content = self._clean_and_summarize_content(results[api_key][i]["content"])
                    print(f"| {api_name} | {content} |")
            print()
        
        # 마크다운 파일 저장
        self._save_question_report(results)
    
    def _save_question_report(self, results: Dict[str, Any]):
        """질문 생성 마크다운 보고서를 파일로 저장"""
        from datetime import datetime
        import os
        
        # 저장 디렉토리 생성
        os.makedirs("reports", exist_ok=True)
        
        # 타임스탬프 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/START_questions_{timestamp}.md"
        
        # 마크다운 내용 생성
        markdown_content = self._generate_question_markdown_content(results)
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"📄 질문 생성 보고서가 저장되었습니다: {filename}")
    
    def _generate_question_markdown_content(self, results: Dict[str, Any]) -> str:
        """질문 생성 마크다운 내용 생성 (단순 형식)"""
        from datetime import datetime
        
        content = [
            "# 📊 START 질문 생성 결과\n",
            f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
            "## 🏆 모델별 성능 비교\n",
            "| 모델 | 평균 응답시간 (초) | 평균 비용 ($) | 평균 토큰 수 |",
            "|------|------------------|-------------|-------------|"
        ]
        
        # 성능 테이블
        for api_name in self.apis.keys():
            api_key = api_name.lower()
            if api_key in results and results[api_key]:
                avg_time = sum(r["response_time"] for r in results[api_key]) / len(results[api_key])
                avg_cost = sum(r["cost"] for r in results[api_key]) / len(results[api_key])
                avg_tokens = sum(r["tokens"] for r in results[api_key]) / len(results[api_key])
                content.append(f"| {api_name} | {avg_time:.2f} | ${avg_cost:.4f} | {avg_tokens:.0f} |")
        
        content.extend([
            "\n## 🔍 모델별 응답 내용 비교\n"
        ])
        
        # 응답 내용 비교
        scenarios = self._get_start_scenarios()
        for i, scenario in enumerate(scenarios):
            content.extend([
                f"### 시나리오 {i+1}: {scenario['name']}\n",
                "| 모델 | 생성된 질문 내용 |",
                "|------|---------------------|"
            ])
            
            for api_name in self.apis.keys():
                api_key = api_name.lower()
                if api_key in results and results[api_key] and len(results[api_key]) > i:
                    clean_content = self._clean_and_summarize_content(results[api_key][i]["content"])
                    content.append(f"| {api_name} | {clean_content} |")
            
            content.append("")
        
        return "\n".join(content)
    
    def _print_report_results(self, results: Dict[str, Any]):
        """보고서 생성 결과 출력 (단순 표 형식)"""
        print("\n# 📊 보고서 생성 결과\n")
        
        # 성능 테이블
        print("## 🏆 모델별 성능 비교\n")
        print("| 모델 | 평균 응답시간 (초) | 평균 비용 ($) | 평균 토큰 수 |")
        print("|------|------------------|-------------|-------------|")
        
        for api_name in self.apis.keys():
            api_key = api_name.lower()
            if api_key in results and results[api_key]:
                avg_time = sum(r["response_time"] for r in results[api_key]) / len(results[api_key])
                avg_cost = sum(r["cost"] for r in results[api_key]) / len(results[api_key])
                avg_tokens = sum(r["tokens"] for r in results[api_key]) / len(results[api_key])
                print(f"| {api_name} | {avg_time:.2f} | ${avg_cost:.4f} | {avg_tokens:.0f} |")
        
        # 응답 내용 비교
        print("\n## 🔍 모델별 응답 내용 비교\n")
        scenarios = self._get_report_scenarios()
        
        for i, scenario in enumerate(scenarios):
            print(f"### 시나리오 {i+1}: {scenario['name']}\n")
            print("| 모델 | 생성된 보고서 내용 |")
            print("|------|---------------------|")
            
            for api_name in self.apis.keys():
                api_key = api_name.lower()
                if api_key in results and results[api_key] and len(results[api_key]) > i:
                    content = self._clean_and_summarize_content(results[api_key][i]["content"])
                    print(f"| {api_name} | {content} |")
            print()
        
        # 마크다운 파일 저장
        self._save_markdown_report(results)
    
    def _save_markdown_report(self, results: Dict[str, Any]):
        """마크다운 보고서를 파일로 저장"""
        from datetime import datetime
        import os
        
        # 저장 디렉토리 생성
        os.makedirs("reports", exist_ok=True)
        
        # 타임스탬프 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/START_report_{timestamp}.md"
        
        # 마크다운 내용 생성
        markdown_content = self._generate_markdown_content(results)
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"📄 보고서가 저장되었습니다: {filename}")
    
    def _generate_markdown_content(self, results: Dict[str, Any]) -> str:
        """마크다운 내용 생성 (단순 형식)"""
        from datetime import datetime
        
        content = [
            "# 📊 START 기법 보고서 생성 결과\n",
            f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
            "## 🏆 모델별 성능 비교\n",
            "| 모델 | 평균 응답시간 (초) | 평균 비용 ($) | 평균 토큰 수 |",
            "|------|------------------|-------------|-------------|"
        ]
        
        # 성능 테이블
        for api_name in self.apis.keys():
            api_key = api_name.lower()
            if api_key in results and results[api_key]:
                avg_time = sum(r["response_time"] for r in results[api_key]) / len(results[api_key])
                avg_cost = sum(r["cost"] for r in results[api_key]) / len(results[api_key])
                avg_tokens = sum(r["tokens"] for r in results[api_key]) / len(results[api_key])
                content.append(f"| {api_name} | {avg_time:.2f} | ${avg_cost:.4f} | {avg_tokens:.0f} |")
        
        content.extend([
            "\n## 🔍 모델별 응답 내용 비교\n"
        ])
        
        # 응답 내용 비교
        scenarios = self._get_report_scenarios()
        for i, scenario in enumerate(scenarios):
            content.extend([
                f"### 시나리오 {i+1}: {scenario['name']}\n",
                "| 모델 | 생성된 보고서 내용 |",
                "|------|---------------------|"
            ])
            
            for api_name in self.apis.keys():
                api_key = api_name.lower()
                if api_key in results and results[api_key] and len(results[api_key]) > i:
                    clean_content = self._clean_and_summarize_content(results[api_key][i]["content"])
                    content.append(f"| {api_name} | {clean_content} |")
            
            content.append("")
        
        return "\n".join(content)
    
    def _clean_and_summarize_content(self, content: str) -> str:
        """JSON에서 내용 추출하여 읽기 쉽게 정리"""
        import re
        import json
        
        try:
            # JSON 부분 추출
            json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                
                # 질문 생성인지 보고서 생성인지 판단
                if "S" in data and "꼬리질문" in data.get("S", {}):
                    # 질문 생성 형태
                    result = []
                    stages = [('S', 'Situation'), ('T', 'Task'), ('A', 'Action'), ('R', 'Result'), ('T', 'Takeaway')]
                    for stage, stage_name in stages:
                        if stage in data:
                            result.append(f"{stage} ({stage_name}): ")
                            stage_data = data[stage]
                            result.append(f"꼬리질문: {stage_data.get('꼬리질문', '')} ")
                            result.append(f"실무예시: {stage_data.get('실무예시', '')} ")
                            result.append(f"기업어필: {stage_data.get('기업어필', '')} ")
                    return "".join(result)
                
                elif "START_분석" in data:
                    # 보고서 생성 형태
                    result = []
                    
                    # START 분석
                    if "START_분석" in data:
                        result.append("START 기법 분석 - ")
                        start_data = data["START_분석"]
                        stages = [('S', 'Situation'), ('T', 'Task'), ('A', 'Action'), ('R', 'Result'), ('T', 'Takeaway')]
                        for stage, stage_name in stages:
                            if stage in start_data:
                                result.append(f"{stage} ({stage_name}): {start_data[stage]} ")
                    
                    # 핵심 역량
                    if "핵심_역량" in data:
                        result.append("핵심 역량 - ")
                        comp_data = data["핵심_역량"]
                        for comp_type in ["전문_역량", "소프트_스킬", "성장_잠재력"]:
                            if comp_type in comp_data:
                                comp_name = comp_type.replace("_", " ")
                                result.append(f"{comp_name}: {comp_data[comp_type]} ")
                    
                    return "".join(result)
            
            # JSON이 없으면 마크다운 정리
            content = re.sub(r'#+\s*', '', content)
            content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
            content = re.sub(r'\*([^*]+)\*', r'\1', content)
            content = re.sub(r'`([^`]+)`', r'\1', content)
            content = re.sub(r'\n+', ' ', content)
            content = re.sub(r'\s+', ' ', content)
            return content.strip()
            
        except (json.JSONDecodeError, KeyError, AttributeError):
            # JSON 파싱 실패시 원본 반환
            content = re.sub(r'#+\s*', '', content)
            content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
            content = re.sub(r'\*([^*]+)\*', r'\1', content)
            content = re.sub(r'`([^`]+)`', r'\1', content)
            content = re.sub(r'\n+', ' ', content)
            content = re.sub(r'\s+', ' ', content)
            return content.strip()


async def run_start_questions():
    """START 질문 생성 테스트 실행"""
    print("🚀 START 질문 생성 테스트를 시작합니다...")
    
    # 설정 검증
    if not settings.validate_api_keys():
        print("❌ API 키 설정을 확인해주세요.")
        return
    
    tester = STARTTester()
    await tester.test_start_questions()
    
    print("\n✅ START 질문 생성 테스트가 완료되었습니다!")


async def run_reports():
    """보고서 생성 테스트 실행"""
    print("🚀 보고서 생성 테스트를 시작합니다...")
    
    # 설정 검증
    if not settings.validate_api_keys():
        print("❌ API 키 설정을 확인해주세요.")
        return
    
    tester = STARTTester()
    await tester.test_reports()
    
    print("\n✅ 보고서 생성 테스트가 완료되었습니다!")


def main():
    """메인 함수"""
    if not click:
        print("❌ click 패키지가 설치되지 않았습니다. pip install click")
        return
    
    @click.group()
    def cli():
        """START 기법 특화 테스트 도구"""
        pass
    
    @cli.command()
    def questions():
        """START 질문 생성 테스트"""
        asyncio.run(run_start_questions())
    
    @cli.command()
    def reports():
        """보고서 생성 테스트"""
        asyncio.run(run_reports())
    
    cli()


if __name__ == "__main__":
    main() 