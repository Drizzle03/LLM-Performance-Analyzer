"""
API 응답 품질 및 성능 평가 시스템
"""
import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import textstat
except ImportError:
    textstat = None

try:
    import pandas as pd
except ImportError:
    pd = None


@dataclass
class QualityMetrics:
    """품질 평가 메트릭"""
    relevance_score: float  # 관련성 점수 (1-5)
    clarity_score: float    # 명확성 점수 (1-5)
    structure_score: float  # 구조 점수 (1-5)
    readability_score: float  # 가독성 점수 (Flesch-Kincaid)
    keyword_overlap: float  # 키워드 겹침 정도
    overall_score: float    # 전체 점수


@dataclass
class PerformanceMetrics:
    """성능 평가 메트릭"""
    response_time: float    # 응답 시간 (초)
    tokens_used: int       # 사용된 토큰 수
    cost: float           # 비용 (달러)
    success_rate: float   # 성공률 (%)


@dataclass
class ComparisonResult:
    """비교 결과"""
    test_id: str
    timestamp: str
    api_provider: str
    task_type: str  # "question_generation" or "report_generation"
    input_text: str
    output_text: str
    quality_metrics: QualityMetrics
    performance_metrics: PerformanceMetrics
    error: Optional[str] = None


class MetricsEvaluator:
    """메트릭 평가 클래스"""
    
    def __init__(self):
        """평가 시스템 초기화"""
        self.results: List[ComparisonResult] = []
        
        if not textstat:
            print("⚠️ textstat 패키지가 설치되지 않았습니다. 가독성 평가가 제한됩니다.")
    
    def evaluate_question_quality(self, 
                                 questions: str, 
                                 user_input: str, 
                                 context: str = "") -> QualityMetrics:
        """생성된 질문의 품질을 평가합니다"""
        relevance_score = self._calculate_relevance(questions, user_input, context)
        clarity_score = self._evaluate_question_clarity(questions)
        structure_score = self._evaluate_question_structure(questions)
        readability_score = self._calculate_readability(questions)
        keyword_overlap = self._calculate_keyword_overlap(questions, user_input)
        overall_score = (relevance_score + clarity_score + structure_score) / 3
        
        return QualityMetrics(
            relevance_score=relevance_score,
            clarity_score=clarity_score,
            structure_score=structure_score,
            readability_score=readability_score,
            keyword_overlap=keyword_overlap,
            overall_score=overall_score
        )
    
    def evaluate_report_quality(self, 
                               report: str, 
                               conversation_history: List[Dict],
                               prompt: str) -> QualityMetrics:
        """생성된 보고서의 품질을 평가합니다"""
        conversation_text = " ".join([msg.get('content', '') for msg in conversation_history])
        relevance_score = self._calculate_relevance(report, conversation_text, prompt)
        clarity_score = self._evaluate_report_clarity(report)
        structure_score = self._evaluate_report_structure(report)
        readability_score = self._calculate_readability(report)
        keyword_overlap = self._calculate_keyword_overlap(report, conversation_text)
        overall_score = (relevance_score + clarity_score + structure_score) / 3
        
        return QualityMetrics(
            relevance_score=relevance_score,
            clarity_score=clarity_score,
            structure_score=structure_score,
            readability_score=readability_score,
            keyword_overlap=keyword_overlap,
            overall_score=overall_score
        )
    
    def calculate_performance_metrics(self, 
                                    response_time: float,
                                    tokens_used: int,
                                    cost: float,
                                    error: Optional[str] = None) -> PerformanceMetrics:
        """성능 메트릭을 계산합니다"""
        success_rate = 0.0 if error else 100.0
        
        return PerformanceMetrics(
            response_time=response_time,
            tokens_used=tokens_used,
            cost=cost,
            success_rate=success_rate
        )
    
    def add_comparison_result(self, 
                            test_id: str,
                            api_provider: str,
                            task_type: str,
                            input_text: str,
                            output_text: str,
                            quality_metrics: QualityMetrics,
                            performance_metrics: PerformanceMetrics,
                            error: Optional[str] = None):
        """비교 결과를 추가합니다"""
        result = ComparisonResult(
            test_id=test_id,
            timestamp=datetime.now().isoformat(),
            api_provider=api_provider,
            task_type=task_type,
            input_text=input_text,
            output_text=output_text,
            quality_metrics=quality_metrics,
            performance_metrics=performance_metrics,
            error=error
        )
        self.results.append(result)
    
    def export_results(self, filename: str, format_type: str = "json"):
        """결과를 파일로 내보냅니다"""
        if format_type == "json":
            self._export_to_json(filename)
        elif format_type == "csv" and pd:
            self._export_to_csv(filename)
        else:
            print(f"⚠️ 지원하지 않는 형식이거나 pandas가 설치되지 않았습니다: {format_type}")
    
    def _export_to_json(self, filename: str):
        """JSON 형식으로 내보내기"""
        data = [asdict(result) for result in self.results]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 결과가 {filename}에 저장되었습니다.")
    
    def _export_to_csv(self, filename: str):
        """CSV 형식으로 내보내기"""
        # 결과를 평탄화
        flattened_data = []
        for result in self.results:
            row = {
                'test_id': result.test_id,
                'timestamp': result.timestamp,
                'api_provider': result.api_provider,
                'task_type': result.task_type,
                'input_text': result.input_text[:200] + "..." if len(result.input_text) > 200 else result.input_text,
                'output_text': result.output_text[:200] + "..." if len(result.output_text) > 200 else result.output_text,
                'relevance_score': result.quality_metrics.relevance_score,
                'clarity_score': result.quality_metrics.clarity_score,
                'structure_score': result.quality_metrics.structure_score,
                'readability_score': result.quality_metrics.readability_score,
                'keyword_overlap': result.quality_metrics.keyword_overlap,
                'overall_quality_score': result.quality_metrics.overall_score,
                'response_time': result.performance_metrics.response_time,
                'tokens_used': result.performance_metrics.tokens_used,
                'cost': result.performance_metrics.cost,
                'success_rate': result.performance_metrics.success_rate,
                'error': result.error
            }
            flattened_data.append(row)
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ 결과가 {filename}에 저장되었습니다.")
    
    def _calculate_relevance(self, text: str, reference: str, context: str = "") -> float:
        """관련성 점수를 계산합니다"""
        reference_words = set(re.findall(r'\b\w+\b', reference.lower()))
        context_words = set(re.findall(r'\b\w+\b', context.lower()))
        text_words = set(re.findall(r'\b\w+\b', text.lower()))
        
        all_reference_words = reference_words.union(context_words)
        
        if not all_reference_words:
            return 3.0
        
        overlap = len(text_words.intersection(all_reference_words))
        overlap_ratio = overlap / len(all_reference_words)
        
        return min(5.0, max(1.0, 1 + (overlap_ratio * 4)))
    
    def _calculate_keyword_overlap(self, text: str, reference: str) -> float:
        """키워드 겹침 비율을 계산합니다"""
        reference_words = set(re.findall(r'\b\w+\b', reference.lower()))
        text_words = set(re.findall(r'\b\w+\b', text.lower()))
        
        if not reference_words:
            return 0.0
        
        overlap = len(text_words.intersection(reference_words))
        return overlap / len(reference_words)
    
    def _calculate_readability(self, text: str) -> float:
        """가독성 점수를 계산합니다"""
        if not textstat:
            return 60.0
        
        try:
            return textstat.flesch_kincaid_grade(text)
        except:
            return 60.0
    
    def _evaluate_question_clarity(self, questions: str) -> float:
        """질문의 명확성을 평가합니다"""
        question_count = len(re.findall(r'\d+\.\s', questions))
        question_marks = questions.count('?')
        
        score = 3.0
        if question_count >= 4:
            score += 1.0
        if question_marks >= question_count * 0.8:
            score += 1.0
        
        return min(5.0, score)
    
    def _evaluate_question_structure(self, questions: str) -> float:
        """질문의 구조를 평가합니다"""
        numbered_lines = len(re.findall(r'^\d+\.\s', questions, re.MULTILINE))
        
        score = 3.0
        if numbered_lines >= 4:
            score += 2.0
        elif numbered_lines >= 2:
            score += 1.0
        
        return min(5.0, score)
    
    def _evaluate_report_clarity(self, report: str) -> float:
        """보고서의 명확성을 평가합니다"""
        sentences = len(re.findall(r'[.!?]+', report))
        paragraphs = len(report.split('\n\n'))
        
        score = 3.0
        if sentences >= 10:
            score += 1.0
        if paragraphs >= 3:
            score += 1.0
        
        return min(5.0, score)
    
    def _evaluate_report_structure(self, report: str) -> float:
        """보고서의 구조를 평가합니다"""
        sections = ['요약', '주요', '분석', '결론', 'Summary', 'Main', 'Analysis', 'Conclusion']
        section_count = sum(1 for section in sections if section in report)
        
        score = 2.0 + (section_count / len(sections)) * 3.0
        return min(5.0, score) 