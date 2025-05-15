# test_keyrank.py 파일
from keyrank import KeyRank
from tqdm import tqdm
import time

def test_keyrank():
    # KeyRank 인스턴스 생성
    kr = KeyRank()
    
    # 데이터 로드 중 프로그레스 바 표시
    print("KeyRank 대화형 테스트 시작")
    print("데이터 로드 중...")
    with tqdm(total=100, desc="데이터 로드", colour="green") as pbar:
        # 샘플 데이터 로드
        kr.load_data_from_csv("example_data/sample_keywords.csv")
        # 진행 표시를 위한 임의의 스텝
        for i in range(10):
            time.sleep(0.1)  # 진행 시각화를 위한 지연
            pbar.update(10)
    
    print(f"데이터 로드 완료: {len(kr.df)}개 행")
    
    while True:
        # 사용자 입력 받기
        keyword = input("\n검색할 키워드를 입력하세요 (종료하려면 'exit' 입력): ").strip()
        
        # 빈 입력 처리
        if not keyword:
            print("키워드를 입력해주세요.")
            continue
        
        if keyword.lower() == 'exit':
            print("테스트를 종료합니다.")
            break
        
        # 키워드 검색 프로세스 시작 - 즉시 프로그레스 바 표시
        print(f"\n'{keyword}' 검색 중...")
        
        # 프로그레스 바 표시 (키워드 검색 과정)
        with tqdm(total=100, desc="검색 진행 중", colour="blue", bar_format='{l_bar}{bar:30}{r_bar}') as pbar:
            # 진행 상태 즉시 업데이트 시작
            pbar.update(5)
            
            # 실제 검색 수행
            results = kr.find_related_keywords(keyword)
            pbar.update(45)  # 검색 완료 후 진행률 업데이트
            
            # 결과 처리 단계 시뮬레이션
            for i in range(10):
                time.sleep(0.05)  # 짧은 지연으로 프로그레스 바 움직임 표현
                pbar.update(5)
        
        if not results:
            print(f"'{keyword}'에 대한 연관 키워드를 찾을 수 없습니다.")
            continue
        
        # 결과 출력 (제한된 개수)
        print(f"\n{keyword} 검색 결과:")
        
        # 결과 수 제한 (예: 최대 10개 카테고리까지만 표시)
        max_categories = 10
        categories_shown = 0
        
        for month in results:
            print(f"\n{month}:")
            for score in [5, 4, 3]:
                keywords_str = ', '.join(results[month][score]) if results[month][score] else '-'
                print(f"  {score}점: {keywords_str}")
            
            categories_shown += 1
            if categories_shown >= max_categories:
                remaining = len(results) - max_categories
                if remaining > 0:
                    print(f"\n... 외 {remaining}개 카테고리가 더 있습니다. 전체 결과를 보려면 'all'을 입력하세요.")
                break

        # 모든 결과 보기 옵션
        if categories_shown < len(results) and len(results) > max_categories:
            show_all = input("\n전체 결과를 보시겠습니까? (y/n): ").strip().lower()
            if show_all in ['y', 'yes', 'all']:
                print(f"\n{keyword} 전체 검색 결과:")
                for month in results:
                    print(f"\n{month}:")
                    for score in [5, 4, 3]:
                        keywords_str = ', '.join(results[month][score]) if results[month][score] else '-'
                        print(f"  {score}점: {keywords_str}")

if __name__ == "__main__":
    test_keyrank()