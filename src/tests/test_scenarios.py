"""
API 테스트를 위한 시나리오 정의
"""
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class TestCase:
    """개별 테스트 케이스"""
    id: str
    name: str
    user_input: str
    context: str
    expected_questions: int = 5
    category: str = "general"


@dataclass
class ReportTestCase:
    """보고서 생성 테스트 케이스"""
    id: str
    name: str
    conversation_history: List[Dict[str, str]]
    prompt: str
    expected_sections: List[str]
    category: str = "general"


class TestScenarios:
    """테스트 시나리오 관리 클래스"""
    
    @staticmethod
    def get_question_generation_scenarios() -> List[TestCase]:
        """질문 생성 테스트 시나리오 반환"""
        return [
            # 취업 준비 시나리오
            TestCase(
                id="job_prep_01",
                name="컴퓨터공학 전공 프로젝트 경험",
                user_input="저는 대학교에서 컴퓨터공학을 전공하고 있고, 최근에 웹 개발 프로젝트를 완료했습니다.",
                context="취업 면접 준비 상담",
                category="job_preparation"
            ),
            TestCase(
                id="job_prep_02", 
                name="팀 리더십 경험",
                user_input="팀 프로젝트에서 리더 역할을 맡아서 5명의 팀원들과 함께 모바일 앱을 개발했어요.",
                context="리더십 경험 탐색",
                category="job_preparation"
            ),
            TestCase(
                id="job_prep_03",
                name="인턴십 경험",
                user_input="인턴십을 통해 스타트업에서 3개월간 마케팅 업무를 경험했습니다.",
                context="직무 경험 분석",
                category="job_preparation"
            ),
            TestCase(
                id="job_prep_04",
                name="동아리 활동 및 멘토링",
                user_input="동아리 활동으로 프로그래밍 스터디를 운영하면서 후배들을 멘토링했어요.",
                context="리더십 및 교육 경험",
                category="job_preparation"
            ),
            TestCase(
                id="job_prep_05",
                name="대회 참가 및 수상",
                user_input="해커톤에 참가해서 AI를 활용한 서비스로 2등상을 받았습니다.",
                context="성취 경험 회고",
                category="job_preparation"
            ),
            
            # 학습 및 개발 시나리오
            TestCase(
                id="learning_01",
                name="새로운 기술 학습",
                user_input="React를 처음 배워서 개인 프로젝트를 만들어보고 있습니다.",
                context="기술 학습 과정",
                category="learning"
            ),
            TestCase(
                id="learning_02",
                name="데이터 분석 프로젝트",
                user_input="Python을 사용해서 데이터 분석 프로젝트를 진행했는데, 흥미로운 인사이트를 발견했어요.",
                context="데이터 분석 경험",
                category="learning"
            ),
            TestCase(
                id="learning_03",
                name="오픈소스 기여",
                user_input="GitHub에서 오픈소스 프로젝트에 기여하기 시작했습니다.",
                context="개발자 성장 과정",
                category="learning"
            ),
            
            # 문제 해결 시나리오
            TestCase(
                id="problem_solving_01",
                name="기술적 문제 해결",
                user_input="프로젝트에서 성능 이슈가 발생해서 데이터베이스 쿼리를 최적화했습니다.",
                context="문제 해결 경험",
                category="problem_solving"
            ),
            TestCase(
                id="problem_solving_02",
                name="팀 갈등 해결",
                user_input="팀 프로젝트에서 의견 충돌이 있었는데, 중재를 통해 해결했어요.",
                context="갈등 해결 및 소통",
                category="problem_solving"
            ),
            
            # 창업 및 비즈니스 시나리오
            TestCase(
                id="business_01",
                name="사이드 프로젝트 운영",
                user_input="친구들과 함께 작은 온라인 서비스를 만들어서 운영하고 있습니다.",
                context="창업 및 비즈니스 경험",
                category="business"
            ),
            TestCase(
                id="business_02",
                name="고객 피드백 수집",
                user_input="서비스 출시 후 사용자들의 피드백을 받아서 개선 작업을 진행했어요.",
                context="제품 개발 및 개선",
                category="business"
            ),
            
            # START 기법 테스트 시나리오
            TestCase(
                id="start_method_01",
                name="마케팅 인턴 경험 - START 기법 질문 생성",
                user_input="""작년 여름에 어떤 스타트업에서 마케팅 인턴을 했어요. 제가 메타 광고 집행을 맡았었는데, 처음엔 그냥 이전에 쓰던 방식 그대로 따라했거든요. 근데 결과가 잘 안 나와서… CTR이 생각보다 낮았어요.

그래서 이미지나 문구를 몇 가지 버전으로 바꿔서 테스트해봤어요. 정확히 어떤 수치였는지는 잘 기억 안 나는데, 그래도 바꾸고 나서 조금은 나아졌던 걸로 기억해요.

그리고 광고는 클릭은 되는데, 사람들이 바로 나가는 거예요. 그래서 GA로 이탈률 같은 거 확인해보고, 랜딩페이지도 디자이너랑 얘기해서 좀 수정했던 것 같아요.

결국에는 어떤 소재가 잘 먹히는지 보고, 그걸로 다시 광고 돌리고 그런 식으로 했었어요. 완전 전문적으로 한 건 아니지만, 그래도 데이터를 계속 보면서 방향을 바꿨던 경험이었어요.""",
                context="START 기법을 활용한 취업 면접 준비 - 질문 생성 능력 테스트",
                category="start_technique"
            )
        ]
    
    @staticmethod
    def get_report_generation_scenarios() -> List[ReportTestCase]:
        """보고서 생성 테스트 시나리오 반환"""
        return [
            # 기술 역량 평가 보고서
            ReportTestCase(
                id="report_01",
                name="웹 개발 프로젝트 기술 역량 평가",
                conversation_history=[
                    {"role": "user", "content": "웹 개발 프로젝트에 대해 알려주세요"},
                    {"role": "assistant", "content": "어떤 기술 스택을 사용하셨나요?"},
                    {"role": "user", "content": "React와 Node.js를 사용했고, 데이터베이스는 MongoDB를 사용했습니다"},
                    {"role": "assistant", "content": "프로젝트에서 가장 어려웠던 부분은 무엇이었나요?"},
                    {"role": "user", "content": "사용자 인증 시스템을 구현하는 것이 어려웠어요. JWT를 사용해서 해결했습니다"}
                ],
                prompt="웹 개발 프로젝트 경험을 바탕으로 지원자의 기술 역량과 성장 가능성을 분석하는 보고서를 작성해주세요.",
                expected_sections=["요약", "기술 역량", "문제 해결 능력", "성장 가능성"],
                category="technical_assessment"
            ),
            
            # 리더십 평가 보고서
            ReportTestCase(
                id="report_02",
                name="팀 리더십 경험 평가",
                conversation_history=[
                    {"role": "user", "content": "팀 프로젝트 리더 경험을 이야기해주세요"},
                    {"role": "assistant", "content": "팀원들과 어떻게 소통하셨나요?"},
                    {"role": "user", "content": "매주 정기 회의를 진행하고, Slack으로 일상적인 소통을 했습니다"},
                    {"role": "assistant", "content": "프로젝트에서 어려움이 있었다면 어떻게 해결하셨나요?"},
                    {"role": "user", "content": "일정이 지연될 때 팀원들과 우선순위를 재조정하고 역할을 재분배했어요"}
                ],
                prompt="팀 리더십 경험을 통해 나타난 지원자의 협업 능력과 커뮤니케이션 스킬을 평가하는 보고서를 작성해주세요.",
                expected_sections=["요약", "리더십 스타일", "소통 능력", "문제 해결"],
                category="leadership_assessment"
            ),
            
            # 학습 능력 평가 보고서
            ReportTestCase(
                id="report_03",
                name="새로운 기술 학습 능력 평가",
                conversation_history=[
                    {"role": "user", "content": "새로운 기술을 어떻게 학습하시나요?"},
                    {"role": "assistant", "content": "최근에 학습한 기술이 있다면 알려주세요"},
                    {"role": "user", "content": "Docker를 학습해서 프로젝트에 적용했습니다"},
                    {"role": "assistant", "content": "학습 과정에서 어려웠던 점이 있었나요?"},
                    {"role": "user", "content": "처음에는 컨테이너 개념이 어려웠지만, 실습을 통해 이해했어요"}
                ],
                prompt="지원자의 새로운 기술 학습 능력과 적응력을 분석하는 보고서를 작성해주세요.",
                expected_sections=["요약", "학습 방법", "적응력", "향후 발전 가능성"],
                category="learning_assessment"
            ),
            
            # 창의성 및 문제 해결 평가
            ReportTestCase(
                id="report_04",
                name="창의적 문제 해결 능력 평가",
                conversation_history=[
                    {"role": "user", "content": "창의적으로 문제를 해결한 경험이 있나요?"},
                    {"role": "assistant", "content": "구체적인 상황을 설명해주세요"},
                    {"role": "user", "content": "서버 비용을 줄이기 위해 캐싱 전략을 새로 설계했어요"},
                    {"role": "assistant", "content": "어떤 결과를 얻으셨나요?"},
                    {"role": "user", "content": "응답 시간이 50% 줄어들고 서버 비용도 30% 절약되었습니다"}
                ],
                prompt="지원자의 창의적 사고와 문제 해결 능력을 종합적으로 평가하는 보고서를 작성해주세요.",
                expected_sections=["요약", "창의적 사고", "문제 해결 과정", "성과 및 영향"],
                category="creativity_assessment"
            ),
            
            # START 기법 보고서 생성 테스트
            ReportTestCase(
                id="report_05",
                name="마케팅 인턴 경험 - START 기법 정리 및 역량 도출",
                conversation_history=[
                    {"role": "user", "content": """작년 여름에 어떤 스타트업에서 마케팅 인턴을 했어요. 제가 메타 광고 집행을 맡았었는데, 처음엔 그냥 이전에 쓰던 방식 그대로 따라했거든요. 근데 결과가 잘 안 나와서… CTR이 생각보다 낮았어요.

그래서 이미지나 문구를 몇 가지 버전으로 바꿔서 테스트해봤어요. 정확히 어떤 수치였는지는 잘 기억 안 나는데, 그래도 바꾸고 나서 조금은 나아졌던 걸로 기억해요.

그리고 광고는 클릭은 되는데, 사람들이 바로 나가는 거예요. 그래서 GA로 이탈률 같은 거 확인해보고, 랜딩페이지도 디자이너랑 얘기해서 좀 수정했던 것 같아요.

결국에는 어떤 소재가 잘 먹히는지 보고, 그걸로 다시 광고 돌리고 그런 식으로 했었어요. 완전 전문적으로 한 건 아니지만, 그래도 데이터를 계속 보면서 방향을 바꿨던 경험이었어요."""}
                ],
                prompt="""위 마케팅 인턴 경험을 START 기법에 따라 체계적으로 정리하고, 이 지원자만의 핵심 역량을 키워드로 도출해주세요. 지원자의 강점을 어필할 수 있도록 작성해주세요.

START 기법 구조:
- S (Situation): 상황 정리
- T (Task): 주어진 과제/목표 
- A (Action): 구체적 행동/해결과정
- R (Result): 성과/결과
- T (Takeaway): 배운 점/성장한 부분

마지막에 '핵심 역량 키워드' 섹션을 추가하여 이 경험에서 드러나는 지원자의 강점을 5개 키워드로 정리해주세요.""",
                expected_sections=["S (Situation)", "T (Task)", "A (Action)", "R (Result)", "T (Takeaway)", "핵심 역량 키워드"],
                category="start_technique_report"
            )
        ]
    
    @staticmethod
    def get_performance_test_scenarios() -> List[TestCase]:
        """성능 테스트용 시나리오 (대량 데이터)"""
        base_scenarios = TestScenarios.get_question_generation_scenarios()
        
        # 더 긴 텍스트로 성능 테스트
        performance_scenarios = [
            TestCase(
                id="perf_01",
                name="긴 텍스트 처리 테스트",
                user_input="""저는 컴퓨터공학과 4학년 학생으로, 지난 3년간 다양한 프로젝트와 경험을 쌓아왔습니다. 
                대학교 1학년 때부터 프로그래밍에 관심을 가지기 시작해서, C언어부터 시작해서 Java, Python, JavaScript 등 
                다양한 언어를 학습했습니다. 2학년 때는 웹 개발에 관심을 가지게 되어 HTML, CSS, JavaScript를 깊이 있게 
                공부했고, React와 Node.js를 활용한 풀스택 개발 프로젝트를 여러 개 진행했습니다. 3학년 때는 팀 프로젝트에서 
                리더 역할을 맡아 5명의 팀원들과 함께 모바일 앱을 개발했는데, 이 과정에서 프로젝트 관리와 팀워크의 중요성을 
                깊이 깨달았습니다. 또한 스타트업에서 3개월간 인턴십을 경험하면서 실무 환경에서의 개발 프로세스와 
                협업 방식을 배울 수 있었습니다.""",
                context="종합적인 경험 평가",
                category="performance"
            ),
            TestCase(
                id="perf_02", 
                name="복잡한 기술 스택 설명",
                user_input="""최근에 완료한 프로젝트는 마이크로서비스 아키텍처를 기반으로 한 전자상거래 플랫폼입니다. 
                프론트엔드는 React와 TypeScript로 개발했고, 상태관리는 Redux Toolkit을 사용했습니다. 
                백엔드는 Node.js Express 서버를 여러 개의 마이크로서비스로 분리했으며, 각 서비스는 Docker 컨테이너로 
                패키징되어 Kubernetes 클러스터에서 운영됩니다. 데이터베이스는 PostgreSQL을 메인 DB로 사용하고, 
                캐싱을 위해 Redis를 활용했습니다. API 게이트웨이로는 Kong을 사용했고, 모니터링을 위해 Prometheus와 
                Grafana를 구축했습니다. CI/CD 파이프라인은 GitHub Actions으로 구성했으며, AWS ECS에 자동 배포됩니다.""",
                context="기술적 깊이 평가",
                category="performance"
            )
        ]
        
        return base_scenarios + performance_scenarios
    
    @staticmethod
    def get_scenarios_by_category(category: str) -> List[TestCase]:
        """카테고리별 시나리오 반환"""
        all_scenarios = TestScenarios.get_question_generation_scenarios()
        return [scenario for scenario in all_scenarios if scenario.category == category]
    
    @staticmethod
    def get_multilingual_scenarios() -> List[TestCase]:
        """다국어 테스트 시나리오"""
        return [
            TestCase(
                id="multilingual_01",
                name="영어 입력 테스트",
                user_input="I recently completed a web development project using React and Node.js. It was a challenging but rewarding experience.",
                context="English conversation practice",
                category="multilingual"
            ),
            TestCase(
                id="multilingual_02",
                name="한영 혼용 입력 테스트", 
                user_input="저는 React와 JavaScript를 사용해서 SPA(Single Page Application)를 개발했습니다. API integration도 구현했어요.",
                context="한영 혼용 기술 설명",
                category="multilingual"
            )
        ] 