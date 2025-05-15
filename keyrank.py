# KeyRank - 키워드 연관도 분석 및 시각화 도구
# License: MIT

import pandas as pd
import numpy as np
import re
from IPython.display import display, HTML
import ipywidgets as widgets

try:
    from google.colab import files
except ImportError:
    # Colab 환경이 아닌 경우
    pass

class KeyRank:
    def __init__(self):
        """KeyRank 초기화"""
        self.df = None
        self.custom_mappings = {
            '차박텐트': {
                '차박텐트': 5,
                '차박 도킹 텐트': 5,
                '레이 차박텐트': 4,
                '꼬리 텐트': 4,
                '캠핑장소': 3,
                '인천 캠핑장': 3,
                '마시안해변 차박': 3
            },
            '데오드란트': {
                '데오드란트': 5,
                '액취제거제': 5,
                '땀냄새제거제': 5,
                '겨드랑이스프레이': 5,
                '바디스프레이': 4,
                '퍼스피런트': 4,
                '겨드랑이케어': 4,
                '체취관리': 4,
                '바디미스트': 4,
                '여름데이트': 3,
                '운동 전후': 3,
                '일상루틴': 3,
                '데이트준비': 3,
                '마스크습기': 3,
                '겨울러닝복장': 3
            }
        }
    
    def load_data_from_csv(self, file_path, encoding='utf-8'):
        """CSV 파일에서 데이터 로드"""
        self.df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
        # NaN 값을 가진 열 제거
        self.df = self.df.dropna(axis=1, how='all')
        
        # 필요한 컬럼만 선택
        if '카테고리' in self.df.columns and '소분류' in self.df.columns and '연관키워드' in self.df.columns:
            self.df = self.df[['카테고리', '소분류', '연관키워드']]
            return True
        else:
            print("CSV 파일에 필요한 컬럼(카테고리, 소분류, 연관키워드)이 없습니다.")
            print("사용 가능한 컬럼:", self.df.columns.tolist())
            return False
    
    def calculate_relevance_score(self, keyword, target_keyword):
        """키워드와 대상 키워드 간의 연관도 점수 계산"""
        # 입력값 전처리
        keyword = str(keyword).lower().strip()
        target_keyword = str(target_keyword).lower().strip()
        
        # 5점: 동일하거나 매우 유사한 키워드
        if target_keyword in keyword or keyword in target_keyword:
            if len(keyword) >= len(target_keyword) * 0.8 and len(keyword) <= len(target_keyword) * 1.2:
                return 5
        
        # 4점: 연관도가 높은 키워드 (일부 포함 관계)
        if target_keyword in keyword or keyword in target_keyword:
            return 4
        
        # 3점: 관련성이 있는 키워드 (공통 단어 포함)
        target_words = set(target_keyword.split())
        keyword_words = set(keyword.split())
        
        if len(target_words.intersection(keyword_words)) > 0:
            return 3
        
        # 기타: 관련성이 낮음
        return 0
    
    def get_custom_relevance_mapping(self, target_keyword):
        """특정 키워드에 대한 사용자 정의 연관도 매핑 반환"""
        return self.custom_mappings.get(target_keyword.lower(), {})
    
    def get_month_number(self, month_str):
        """월 이름에서 숫자 부분 추출"""
        if not isinstance(month_str, str):
            return 999  # 문자열이 아닌 경우 가장 뒤로 정렬
            
        match = re.search(r'(\d+)월', month_str)
        if match:
            return int(match.group(1))
        return 999  # 월 패턴이 없는 경우 가장 뒤로 정렬
    
    def find_related_keywords(self, target_keyword):
        """대상 키워드와 연관된 키워드를 찾고 연관도 점수를 계산"""
        if self.df is None:
            print("데이터가 로드되지 않았습니다. CSV 파일을 먼저 로드해주세요.")
            return {}
        
        # 사용자 정의 연관도 매핑 가져오기
        custom_mapping = self.get_custom_relevance_mapping(target_keyword)
        
        # 결과 저장을 위한 딕셔너리 초기화
        result = {}
        
        # 데이터프레임의 각 행 순회
        for idx, row in self.df.iterrows():
            month = row['소분류']  # 월 정보
            keyword = row['연관키워드']  # 키워드
            
            # 키워드가 NaN인 경우 건너뛰기
            if pd.isna(keyword):
                continue
                
            # 연관도 점수 계산
            if keyword in custom_mapping:
                relevance = custom_mapping[keyword]
            else:
                relevance = self.calculate_relevance_score(keyword, target_keyword)
            
            # 관련성이 있는 키워드만 결과에 추가 (점수가 3점 이상)
            if relevance >= 3:
                if month not in result:
                    result[month] = {3: [], 4: [], 5: []}
                
                # 중복 키워드 방지
                if keyword not in result[month][relevance]:
                    result[month][relevance].append(keyword)
        
        return result
    
    def optimize_cell_widths(self, results):
        """각 열별로 최대 내용 길이를 계산하여 셀 너비 최적화"""
        # 월 컬럼의 최대 텍스트 길이
        max_month_length = max([len(str(month)) for month in results.keys()], default=5)
        month_width = max(max_month_length * 12, 80)  # 12px per char, minimum 80px
        
        # 점수별 컬럼의 최대 텍스트 길이
        score_widths = {score: 5 for score in [5, 4, 3]}  # 초기값 설정
        
        for month in results:
            for score in [5, 4, 3]:
                keywords = results[month][score]
                if keywords:
                    # 각 점수별 셀에 표시될 총 텍스트 길이
                    content_length = len(', '.join(keywords))
                    score_widths[score] = max(score_widths[score], content_length)
        
        # 각 점수별 셀 너비 계산 (글자당 약 8픽셀, 최소 100픽셀)
        for score in score_widths:
            score_widths[score] = max(score_widths[score] * 8, 100)
        
        return {
            'month': month_width,
            'score_5': score_widths[5],
            'score_4': score_widths[4],
            'score_3': score_widths[3]
        }
    
    def display_search_results(self, results, target_keyword):
        """검색 결과를 HTML 테이블로 표시"""
        # 결과가 없는 경우
        if not results:
            print(f"'{target_keyword}'에 대한 연관 키워드를 찾을 수 없습니다.")
            return
        
        # 셀 너비 최적화
        cell_widths = self.optimize_cell_widths(results)
        
        # HTML 테이블 생성
        html = f"<h2>'{target_keyword}' 연관 키워드 검색 결과</h2>"
        
        # 테이블 스타일링 (최적화된 셀 크기)
        html += f"""
        <style>
        .keyword-table {{
            border-collapse: collapse;
            width: auto;
            margin-bottom: 20px;
            border: 2px solid #333;
            font-family: Arial, sans-serif;
            table-layout: fixed;
        }}
        .keyword-table th, .keyword-table td {{
            border: 1px solid #333;
            padding: 8px 4px;
            text-align: left;
            color: #333;
            overflow: hidden;
            text-overflow: ellipsis;
            word-wrap: break-word;
        }}
        .keyword-table th {{
            background-color: #2c3e50;
            color: white;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 10px 4px;
        }}
        .month-header {{
            width: {cell_widths['month']}px;
        }}
        .score-5-header {{
            width: {cell_widths['score_5']}px;
        }}
        .score-4-header {{
            width: {cell_widths['score_4']}px;
        }}
        .score-3-header {{
            width: {cell_widths['score_3']}px;
        }}
        .keyword-table tr:nth-child(even) {{
            background-color: #e8e8e8;
        }}
        .keyword-table tr:nth-child(odd) {{
            background-color: #f8f8f8;
        }}
        .score-5 {{
            background-color: #d4edda !important;
            color: #155724 !important;
            font-weight: bold;
            width: {cell_widths['score_5']}px;
        }}
        .score-4 {{
            background-color: #d1ecf1 !important;
            color: #0c5460 !important;
            font-weight: bold;
            width: {cell_widths['score_4']}px;
        }}
        .score-3 {{
            background-color: #e2e3e5 !important;
            color: #383d41 !important;
            font-weight: bold;
            width: {cell_widths['score_3']}px;
        }}
        .month-cell {{
            background-color: #495057 !important;
            color: white !important;
            font-weight: bold;
            text-align: center;
            width: {cell_widths['month']}px;
        }}
        </style>
        """
        
        html += "<table class='keyword-table'>"
        html += "<tr><th class='month-header'></th><th class='score-5-header'>5점</th><th class='score-4-header'>4점</th><th class='score-3-header'>3점</th></tr>"
        
        # 월별 정렬
        months = list(results.keys())
        months.sort(key=self.get_month_number)
        
        # 각 월별 결과 행 추가
        for i, month in enumerate(months):
            row_class = "even" if i % 2 == 0 else "odd"
            html += f"<tr class='{row_class}'><td class='month-cell'>{month}</td>"
            
            # 5, 4, 3점 키워드 추가
            for score in [5, 4, 3]:
                keywords = results[month][score]
                if keywords:
                    html += f"<td class='score-{score}'>{', '.join(keywords)}</td>"
                else:
                    html += f"<td class='score-{score}'>-</td>"  # 해당 점수의 키워드가 없는 경우
            
            html += "</tr>"
        
        html += "</table>"
        
        # 연관도 점수 설명
        html += """
        <div style='margin-top: 20px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #333;'>
            <h3 style='color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 5px;'>연관도 점수 설명:</h3>
            <ul style='color: #333; font-weight: bold;'>
                <li><span style='color: #155724;'>5점</span>: 동의어 이거나, 바로 구매전환으로 이어질 수 있는 키워드</li>
                <li><span style='color: #0c5460;'>4점</span>: 경쟁사 키워드 or 연관도가 높은 키워드</li>
                <li><span style='color: #383d41;'>3점</span>: 해당 상품을 구매할 사람이 검색</li>
            </ul>
        </div>
        """
        
        # HTML 표시
        display(HTML(html))
    
    def search_keyword(self, keyword):
        """키워드 검색 및 결과 표시"""
        # 입력값 검증
        if not keyword.strip():
            print("검색할 키워드를 입력해주세요.")
            return
            
        # 연관 키워드 찾기
        results = self.find_related_keywords(keyword)
        
        # 결과 표시
        self.display_search_results(results, keyword)
    
    def add_custom_mapping(self, target_keyword, mappings):
        """사용자 정의 연관도 매핑 추가"""
        self.custom_mappings[target_keyword.lower()] = mappings
        print(f"'{target_keyword}' 키워드에 대한 사용자 정의 매핑이 추가되었습니다.")


def run_keyrank():
    """KeyRank 프로그램 실행 (Colab 환경용)"""
    try:
        # CSV 파일 업로드 기능
        print("CSV 파일을 업로드해주세요:")
        uploaded = files.upload()  # 사용자가 CSV 파일을 업로드할 수 있는 기능
        
        # 첫 번째 업로드된 파일명 가져오기
        file_name = list(uploaded.keys())[0]
        
        # KeyRank 인스턴스 생성
        keyrank = KeyRank()
        
        # CSV 파일 로드
        success = keyrank.load_data_from_csv(file_name)
        if not success:
            return
        
        # 데이터 확인
        print("데이터 샘플:")
        print(keyrank.df.head())
        print(f"총 데이터 개수: {len(keyrank.df)}")
        
        # 인터랙티브 검색 입력 위젯
        search_input = widgets.Text(
            value='',
            placeholder='검색할 키워드를 입력하세요',
            description='키워드:',
            disabled=False,
            layout=widgets.Layout(width='50%')
        )
        
        search_button = widgets.Button(
            description='검색',
            disabled=False,
            button_style='primary', 
            tooltip='Click to search',
            layout=widgets.Layout(width='100px')
        )
        
        output = widgets.Output()
        
        def on_button_clicked(b):
            with output:
                output.clear_output()
                keyrank.search_keyword(search_input.value)
        
        search_button.on_click(on_button_clicked)
        
        # 엔터 키로도 검색 가능하게 설정
        def on_enter(sender):
            with output:
                output.clear_output()
                keyrank.search_keyword(search_input.value)
            
        search_input.on_submit(on_enter)
        
        # 위젯 표시
        print("\n키워드를 입력하고 검색 버튼을 클릭하세요:")
        display(widgets.HBox([search_input, search_button]))
        display(output)
        
        # 예시 키워드 검색 안내
        print("\n예시 키워드: '차박텐트', '데오드란트'")
        
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    print("KeyRank 프로그램을 시작합니다.")
    print("이 프로그램은 Google Colab 환경에서 실행하는 것을 권장합니다.")
    print("Google Colab에서 실행하려면 다음 코드를 실행하세요:")
    print("from keyrank import run_keyrank")
    print("run_keyrank()")