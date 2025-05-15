
# KeyRank

KeyRank는 키워드 연관도 분석 및 시각화 도구입니다. CSV 파일에서 키워드를 불러와 특정 키워드와 연관된 키워드들을 찾고, 연관도 점수(5점, 4점, 3점)별로 분류하여 시각적으로 표시합니다.

## 주요 기능

- 키워드 연관도 자동 계산 및 점수화 (5점, 4점, 3점)
- 월별 또는 카테고리별 연관 키워드 분류
- 사용자 정의 연관도 매핑 지원
- 최적화된 테이블 형태의 결과 시각화
- Google Colab에서 인터랙티브 사용 지원

## 설치 방법

```bash
git clone https://github.com/yourusername/KeyRank.git
cd KeyRank
pip install -r requirements.txt
```

## 사용 방법

### Google Colab에서 사용하기

1. `keyrank.py` 파일을 Colab에 업로드하거나 GitHub에서 직접 로드
2. 다음과 같이 실행:

```python
from keyrank import run_keyrank
run_keyrank()
```

3. CSV 파일 업로드 프롬프트가 표시되면 키워드 데이터가 포함된 CSV 파일 업로드
4. 검색할 키워드 입력 후 결과 확인

### 로컬 환경에서 사용하기

파이썬 스크립트로 직접 실행할 수도 있습니다:

```python
from keyrank import KeyRank

# KeyRank 인스턴스 생성
kr = KeyRank()

# CSV 파일 로드
kr.load_data_from_csv("example_data/sample_keywords.csv")

# 키워드 검색
kr.search_keyword("데오드란트")
```

## 연관도 점수 의미

- **5점**: 동의어 이거나, 바로 구매전환으로 이어질 수 있는 키워드
- **4점**: 경쟁사 키워드 or 연관도가 높은 키워드
- **3점**: 해당 상품을 구매할 사람이 검색하는 키워드

## 예시

**입력 키워드**: "차박텐트"

**결과**:
- **5점**: 차박텐트, 차박 도킹 텐트
- **4점**: 레이 차박텐트, 꼬리 텐트
- **3점**: 캠핑장소, 인천 캠핑장, 마시안해변 차박

## 사용자 정의 매핑 추가

자신만의 연관도 매핑을 추가할 수 있습니다:

```python
kr = KeyRank()
kr.add_custom_mapping("새우깡", {
    "새우깡": 5,
    "농심 새우깡": 5,
    "짭짤한 새우깡": 5,
    "과자 새우깡": 5,
    "농심": 4,
    "과자": 4,
    "스낵": 4,
    "짭짤한 과자": 3,
    "간식": 3,
    "편의점 과자": 3
})
```

## 기여하기

이슈와 풀 리퀘스트를 환영합니다!

## 라이센스

MIT License
