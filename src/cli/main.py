"""
CLI 메인 애플리케이션 - Claude API vs HyperClovaX API 성능 비교 도구
"""
import asyncio
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    import click
except ImportError:
    click = None

from ..api.claude_api import ClaudeAPI
from ..api.hyperclova_api import HyperClovaAPI
from ..api.openai_api import OpenAIAPI
from ..api.gemini_api import GeminiAPI
from ..api.grok_api import GrokAPI
from ..metrics.evaluator import MetricsEvaluator
from ..utils.config import settings


class APIComparator:
    """API 비교 클래스"""
    
    def __init__(self):
        """비교 도구 초기화"""
        self.apis = {}
        self.evaluator = MetricsEvaluator()
        
        # 모든 API 초기화 시도
        api_classes = {
            "Claude": ClaudeAPI,
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
    
    async def test_question_generation(self, user_responses: List[str], contexts: Optional[List[str]] = None) -> Dict[str, Any]:
        """질문 생성 테스트"""
        if contexts is None:
            contexts = [""] * len(user_responses)
        
        results = {api_name.lower(): [] for api_name in self.apis.keys()}
        failed_apis = set()  # 실패한 API 추적
        
        for i, (user_response, context) in enumerate(zip(user_responses, contexts)):
            test_id = f"question_test_{i+1}"
            
            # 모든 사용 가능한 API 테스트
            for api_name, api_instance in self.apis.items():
                # 이미 실패한 API는 스킵
                if api_name in failed_apis:
                    continue
                    
                try:
                    result = await api_instance.generate_questions(user_response, context)
                    
                    if not result.error:
                        quality_metrics = self.evaluator.evaluate_question_quality(
                            result.content, user_response, context
                        )
                        performance_metrics = self.evaluator.calculate_performance_metrics(
                            result.response_time, result.tokens_used, result.cost
                        )
                        
                        self.evaluator.add_comparison_result(
                            test_id, api_name, "question_generation",
                            user_response, result.content,
                            quality_metrics, performance_metrics
                        )
                        
                        results[api_name.lower()].append({
                            "content": result.content,
                            "response_time": result.response_time,
                            "tokens": result.tokens_used,
                            "cost": result.cost,
                            "quality_score": quality_metrics.overall_score
                        })
                    else:
                        # API 오류 시 간결한 메시지
                        error_msg = self._get_simplified_error(result.error)
                        print(f"❌ {api_name}: {error_msg}")
                        failed_apis.add(api_name)
                        
                except Exception as e:
                    # 예외 발생 시 간결한 메시지
                    error_msg = self._get_simplified_error(str(e))
                    print(f"❌ {api_name}: {error_msg}")
                    failed_apis.add(api_name)
        
        return results
    
    def _get_simplified_error(self, error_msg: str) -> str:
        """오류 메시지를 간결하게 변환"""
        error_str = str(error_msg).lower()
        
        if "quota" in error_str or "429" in error_str:
            return "할당량 초과 (무료 티어 한도)"
        elif "timeout" in error_str or "timed out" in error_str:
            return "요청 타임아웃"
        elif "401" in error_str or "unauthorized" in error_str:
            return "API 키 인증 오류"
        elif "404" in error_str or "not found" in error_str:
            return "모델을 찾을 수 없음"
        elif "connection" in error_str:
            return "네트워크 연결 오류"
        else:
            # 긴 오류 메시지를 짧게 자르기
            return error_str[:100] + "..." if len(error_str) > 100 else error_str
    
    async def test_report_generation(self, report_scenarios: List[Any]) -> Dict[str, Any]:
        """보고서 생성 테스트"""
        results = {api_name.lower(): [] for api_name in self.apis.keys()}
        
        for i, scenario in enumerate(report_scenarios):
            test_id = f"report_test_{i+1}"
            
            # 모든 사용 가능한 API 테스트
            for api_name, api_instance in self.apis.items():
                try:
                    result = await api_instance.generate_report(
                        scenario.conversation_history, scenario.prompt
                    )
                    
                    if not result.error:
                        quality_metrics = self.evaluator.evaluate_report_quality(
                            result.content, scenario.conversation_history, scenario.prompt
                        )
                        performance_metrics = self.evaluator.calculate_performance_metrics(
                            result.response_time, result.tokens_used, result.cost, None
                        )
                        
                        self.evaluator.add_comparison_result(
                            test_id, api_name, "report_generation",
                            scenario.prompt, result.content,
                            quality_metrics, performance_metrics
                        )
                        
                        results[api_name.lower()].append({
                            "content": result.content,
                            "response_time": result.response_time,
                            "tokens": result.tokens_used,
                            "cost": result.cost,
                            "quality_score": quality_metrics.overall_score
                        })
                    else:
                        print(f"❌ {api_name} API 오류 (테스트 {i+1}): {result.error}")
                        
                except Exception as e:
                    print(f"❌ {api_name} API 예외 (테스트 {i+1}): {e}")
        
        return results
    
    def print_summary(self, question_results: Dict[str, Any], report_results: Dict[str, Any]):
        """결과 요약 출력"""
        print("\n=== 📊 AI 모델 성능 비교 결과 ===")
        
        # 질문 생성 결과
        print("\n🤔 질문 생성 성능 비교:")
        for api_name in self.apis.keys():
            api_key = api_name.lower()
            if api_key in question_results and question_results[api_key]:
                results = question_results[api_key]
                avg_time = sum(r["response_time"] for r in results) / len(results)
                avg_quality = sum(r["quality_score"] for r in results) / len(results)
                avg_cost = sum(r["cost"] for r in results) / len(results)
                print(f"  {api_name:12}: 응답시간 {avg_time:5.2f}초, 품질 {avg_quality:.2f}/5.0, 비용 ${avg_cost:.4f}")
        
        # 보고서 생성 결과 (향후 구현)
        if any(report_results.values()):
            print("\n📋 보고서 생성 성능 비교:")
            for api_name in self.apis.keys():
                api_key = api_name.lower()
                if api_key in report_results and report_results[api_key]:
                    results = report_results[api_key]
                    avg_time = sum(r["response_time"] for r in results) / len(results)
                    avg_quality = sum(r["quality_score"] for r in results) / len(results)
                    avg_cost = sum(r["cost"] for r in results) / len(results)
                    print(f"  {api_name:12}: 응답시간 {avg_time:5.2f}초, 품질 {avg_quality:.2f}/5.0, 비용 ${avg_cost:.4f}")
        
        # 성능 랭킹 출력
        self._print_performance_ranking(question_results)
    
    def _print_performance_ranking(self, question_results: Dict[str, Any]):
        """성능 순위 출력"""
        if not question_results:
            return
        
        rankings = []
        for api_name in self.apis.keys():
            api_key = api_name.lower()
            if api_key in question_results and question_results[api_key]:
                results = question_results[api_key]
                avg_time = sum(r["response_time"] for r in results) / len(results)
                avg_quality = sum(r["quality_score"] for r in results) / len(results)
                avg_cost = sum(r["cost"] for r in results) / len(results)
                
                # 종합 점수 계산 (품질 중심, 속도와 비용 고려)
                composite_score = avg_quality * 0.6 + (5 - min(avg_time, 5)) * 0.2 + (1 - min(avg_cost, 1)) * 0.2
                
                rankings.append({
                    "name": api_name,
                    "quality": avg_quality,
                    "speed": avg_time,
                    "cost": avg_cost,
                    "composite": composite_score
                })
        
        if rankings:
            print("\n🏆 종합 성능 순위:")
            rankings.sort(key=lambda x: x["composite"], reverse=True)
            
            for i, ranking in enumerate(rankings, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}위"
                print(f"  {medal} {ranking['name']:12} (종합: {ranking['composite']:.2f}, 품질: {ranking['quality']:.2f}, 속도: {ranking['speed']:.2f}초, 비용: ${ranking['cost']:.4f})")
    
    def save_results(self, filename: Optional[str] = None):
        """결과 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"api_comparison_results_{timestamp}"
        
        # 결과 디렉토리 생성
        os.makedirs(settings.results_dir, exist_ok=True)
        
        json_file = os.path.join(settings.results_dir, f"{filename}.json")
        self.evaluator.export_results(json_file, "json")


def get_test_data_by_category(category: str = "all", limit: int = 3):
    """카테고리별 테스트 데이터 반환"""
    from ..tests.test_scenarios import TestScenarios
    
    if category == "all":
        scenarios = TestScenarios.get_question_generation_scenarios()
    else:
        scenarios = TestScenarios.get_scenarios_by_category(category)
    
    # 제한된 수만큼만 선택
    selected_scenarios = scenarios[:limit] if scenarios else []
    
    user_responses = [scenario.user_input for scenario in selected_scenarios]
    contexts = [scenario.context for scenario in selected_scenarios]
    names = [scenario.name for scenario in selected_scenarios]
    
    return user_responses, contexts, names


def get_available_categories():
    """사용 가능한 카테고리 목록 반환"""
    from ..tests.test_scenarios import TestScenarios
    scenarios = TestScenarios.get_question_generation_scenarios()
    categories = list(set(scenario.category for scenario in scenarios))
    return sorted(categories)


def get_sample_test_data():
    """기본 샘플 테스트 데이터 반환 (하위 호환성)"""
    user_responses, contexts, _ = get_test_data_by_category("job_preparation", 3)
    return user_responses, contexts


async def run_comparison_test(category: str = "all", count: int = 3):
    """비교 테스트 실행"""
    print("🚀 API 성능 비교 테스트를 시작합니다...\n")
    
    # 설정 검증
    if not settings.validate_api_keys():
        print("❌ API 키 설정을 확인해주세요.")
        return
    
    # 비교 도구 초기화
    comparator = APIComparator()
    
    # 테스트 데이터 준비
    user_responses, contexts, names = get_test_data_by_category(category, count)
    
    if not user_responses:
        print(f"❌ '{category}' 카테고리에 해당하는 테스트 시나리오가 없습니다.")
        return
    
    print(f"📝 질문 생성 테스트를 실행합니다... (카테고리: {category}, 시나리오 수: {len(user_responses)})")
    
    # 각 시나리오 이름 출력
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")
    print()
    
    question_results = await comparator.test_question_generation(user_responses, contexts)
    
    print("\n📊 결과를 분석합니다...")
    empty_report_results = {api_name.lower(): [] for api_name in comparator.apis.keys()}
    comparator.print_summary(question_results, empty_report_results)
    
    print("\n💾 결과를 저장합니다...")
    comparator.save_results()
    
    print("\n✅ 모든 테스트가 완료되었습니다!")


async def run_report_test(category: str = "start_technique_report", count: int = 1):
    """보고서 생성 테스트 실행"""
    print("📋 보고서 생성 테스트를 시작합니다...\n")
    
    # 설정 검증
    if not settings.validate_api_keys():
        print("❌ API 키 설정을 확인해주세요.")
        return
    
    # 비교 도구 초기화
    comparator = APIComparator()
    
    # 보고서 테스트 시나리오 가져오기
    from ..tests.test_scenarios import TestScenarios
    all_report_scenarios = TestScenarios.get_report_generation_scenarios()
    
    # 카테고리별 필터링
    if category != "all":
        report_scenarios = [s for s in all_report_scenarios if s.category == category]
    else:
        report_scenarios = all_report_scenarios
    
    # 개수 제한
    report_scenarios = report_scenarios[:count]
    
    if not report_scenarios:
        print(f"❌ '{category}' 카테고리에 해당하는 보고서 시나리오가 없습니다.")
        return
    
    print(f"📝 보고서 생성 테스트를 실행합니다... (카테고리: {category}, 시나리오 수: {len(report_scenarios)})")
    
    # 각 시나리오 이름 출력
    for i, scenario in enumerate(report_scenarios, 1):
        print(f"  {i}. {scenario.name}")
    print()
    
    # 보고서 테스트 실행 - 개선된 예외처리 적용
    report_results = {}
    for api_name in comparator.apis.keys():
        report_results[api_name.lower()] = []
    
    failed_apis = set()  # 실패한 API 추적
    
    for i, scenario in enumerate(report_scenarios):
        print(f"📋 시나리오 {i+1}: {scenario.name}")
        test_id = f"report_test_{i+1}"
        
        # 각 API로 보고서 생성
        for api_name, api_instance in comparator.apis.items():
            # 이미 실패한 API는 스킵
            if api_name in failed_apis:
                continue
                
            try:
                # conversation_history를 하나의 텍스트로 합치기
                conversation_text = ""
                for msg in scenario.conversation_history:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    conversation_text += f"{role}: {msg['content']}\n"
                
                # 보고서 생성 요청
                result = await api_instance.generate_report(
                    scenario.conversation_history, scenario.prompt
                )
                
                if not result.error:
                    quality_metrics = comparator.evaluator.evaluate_report_quality(
                        result.content, scenario.conversation_history, scenario.prompt
                    )
                    performance_metrics = comparator.evaluator.calculate_performance_metrics(
                        result.response_time, result.tokens_used, result.cost, None
                    )
                    
                    # 결과를 evaluator에 제대로 저장
                    comparator.evaluator.add_comparison_result(
                        test_id, api_name, "report_generation",
                        conversation_text, result.content,
                        quality_metrics, performance_metrics
                    )
                    
                    report_results[api_name.lower()].append({
                        "content": result.content,
                        "response_time": result.response_time,
                        "tokens": result.tokens_used,
                        "cost": result.cost,
                        "quality_score": quality_metrics.overall_score
                    })
                else:
                    # API 오류 시 간결한 메시지
                    error_msg = comparator._get_simplified_error(result.error)
                    print(f"❌ {api_name}: {error_msg}")
                    failed_apis.add(api_name)
                    
            except Exception as e:
                # 예외 발생 시 간결한 메시지
                error_msg = comparator._get_simplified_error(str(e))
                print(f"❌ {api_name}: {error_msg}")
                failed_apis.add(api_name)
    
    print("\n📊 결과를 분석합니다...")
    empty_question_results = {api_name.lower(): [] for api_name in comparator.apis.keys()}
    comparator.print_summary(empty_question_results, report_results)
    
    print("\n💾 결과를 저장합니다...")
    comparator.save_results()
    
    print("\n✅ 모든 보고서 테스트가 완료되었습니다!")


def main():
    """메인 함수"""
    if not click:
        print("❌ click 패키지가 설치되지 않았습니다. pip install click")
        print("🔄 기본 테스트를 실행합니다...")
        asyncio.run(run_comparison_test())
        return
    
    @click.group()
    def cli():
        """Claude API vs HyperClovaX API 성능 비교 도구"""
        pass
    
    @cli.command()
    @click.option('--category', '-c', default='all', help='테스트할 시나리오 카테고리')
    @click.option('--count', '-n', default=3, help='실행할 시나리오 개수')
    def test(category, count):
        """API 성능 비교 테스트 실행"""
        asyncio.run(run_comparison_test(category, count))
    
    @cli.command()
    @click.option('--category', '-c', default='start_technique_report', help='보고서 테스트 카테고리')
    @click.option('--count', '-n', default=1, help='실행할 시나리오 개수')
    def report(category, count):
        """보고서 생성 테스트 실행"""
        asyncio.run(run_report_test(category, count))
    
    @cli.command()
    def categories():
        """사용 가능한 테스트 시나리오 카테고리 목록"""
        print("📋 사용 가능한 테스트 카테고리:")
        categories = get_available_categories()
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        
        print("\n🎯 카테고리별 시나리오 개수:")
        from ..tests.test_scenarios import TestScenarios
        for cat in categories:
            scenarios = TestScenarios.get_scenarios_by_category(cat)
            print(f"  {cat}: {len(scenarios)}개")
        
        print("\n💡 사용 예시:")
        print("  python main.py test --category job_preparation --count 5")
        print("  python main.py test -c learning -n 2")
        print("  python main.py test --category all --count 10")
    
    @cli.command()
    def scenarios():
        """모든 테스트 시나리오 목록"""
        from ..tests.test_scenarios import TestScenarios
        all_scenarios = TestScenarios.get_question_generation_scenarios()
        
        print(f"📝 전체 테스트 시나리오 ({len(all_scenarios)}개):")
        
        categories = get_available_categories()
        for category in categories:
            cat_scenarios = TestScenarios.get_scenarios_by_category(category)
            print(f"\n🏷️ {category.upper()} ({len(cat_scenarios)}개):")
            for i, scenario in enumerate(cat_scenarios, 1):
                print(f"  {i}. {scenario.name}")
                print(f"     📄 {scenario.user_input[:50]}...")
                print(f"     🎯 {scenario.context}")
    
    @cli.command()
    def info():
        """시스템 정보 및 설정 확인"""
        print("🔧 시스템 정보")
        print(f"- 테스트 언어: {settings.test_language}")
        print(f"- 최대 재시도: {settings.max_retries}")
        print(f"- 요청 타임아웃: {settings.request_timeout}초")
        print(f"- 결과 저장 경로: {settings.results_dir}")
        
        # API 키 검증 (validate_api_keys에서 출력)
        settings.validate_api_keys()
    
    cli()


if __name__ == "__main__":
    main() 