# HyperClovaX Request ID 찾기 상세 가이드

## 🎯 목표
네이버 클라우드 플랫폼에서 HyperClovaX API의 Request ID를 찾아 환경변수에 설정하기

## 📝 단계별 가이드

### 1단계: 네이버 클라우드 플랫폼 접속
1. 브라우저에서 https://console.ncloud.com/ 접속
2. 네이버 계정으로 로그인
3. 콘솔 메인 화면 확인

### 2단계: Clova Studio 서비스 이동
1. 왼쪽 사이드바에서 "AI Service" 메뉴 클릭
2. "Clova Studio" 서비스 선택
3. Clova Studio 대시보드로 이동

### 3단계: Request ID 확인 (3가지 방법)

#### 방법 A: API 키 관리에서 확인
```
경로: Clova Studio → 설정 → API 키 관리
1. API 키 관리 페이지 접속
2. "Request ID" 또는 "요청 ID" 항목 확인
3. 복사 버튼으로 ID 복사
```

#### 방법 B: 플레이그라운드에서 확인
```
경로: Clova Studio → Playground → HyperCLOVA X
1. HyperCLOVA X 모델 선택
2. 간단한 텍스트 입력 후 실행
3. "API 코드 보기" 또는 "Code Generation" 클릭
4. 생성된 예제 코드에서 Request ID 확인
```

#### 방법 C: API 문서에서 확인
```
경로: Clova Studio → 개발자 도구 → API 문서
1. API 문서 페이지 접속
2. Authentication 또는 인증 섹션
3. Request ID 생성 방법 및 형식 확인
```

### 4단계: Request ID 형식 확인

#### 올바른 형식 예시:
- `550e8400-e29b-41d4-a716-446655440000` (UUID 형식)
- `my-hyperclova-project-001` (사용자 정의)
- `hyperclova-test-20241201` (날짜 포함)

#### 잘못된 형식:
- ❌ API 키와 동일한 값
- ❌ 빈 문자열 또는 공백
- ❌ 특수문자가 포함된 값 (일부 특수문자 제외)

### 5단계: 환경변수 설정
```bash
# .env 파일에 추가
HYPERCLOVA_REQUEST_ID=여기에_복사한_Request_ID_입력

# 예시
HYPERCLOVA_REQUEST_ID=550e8400-e29b-41d4-a716-446655440000
```

## 🔍 문제 해결

### Request ID를 찾을 수 없는 경우:
1. **Clova Studio 서비스 활성화 확인**
   - 서비스가 활성화되어 있는지 확인
   - 필요시 서비스 신청 및 승인 대기

2. **권한 확인**
   - 계정에 Clova Studio 접근 권한이 있는지 확인
   - 관리자 권한이 필요할 수 있음

3. **새 Request ID 생성**
   - 기존 ID가 없다면 새로 생성
   - 프로젝트별로 고유한 ID 사용 권장

### Request ID가 작동하지 않는 경우:
1. **형식 검증**
   - 복사 시 공백이나 줄바꿈 포함되지 않았는지 확인
   - 따옴표 없이 값만 입력했는지 확인

2. **API 키와 함께 확인**
   - Request ID만으로는 작동하지 않음
   - API 키와 Request ID 모두 필요

3. **네이버 클라우드 지원 문의**
   - 위 방법으로 해결되지 않으면 고객지원 문의

## 💡 추가 팁

### Request ID의 역할:
- API 호출 시 요청을 식별하는 고유 ID
- 로깅 및 모니터링에 사용
- 사용량 추적 및 과금에 활용

### 보안 주의사항:
- Request ID도 API 키처럼 외부 노출 금지
- .env 파일을 git에 커밋하지 않기
- 정기적으로 ID 갱신 권장

### 테스트 방법:
```bash
# 설정 후 테스트
python main.py info

# Request ID가 올바르게 설정되었는지 확인
# "✅ HyperClovaX Request ID: 설정됨" 메시지 확인
```

## 📞 추가 도움이 필요한 경우
- 네이버 클라우드 플랫폼 고객지원: https://www.ncloud.com/support
- Clova Studio 문서: https://api.ncloud-docs.com/docs/ai-application-service-clovastudio 