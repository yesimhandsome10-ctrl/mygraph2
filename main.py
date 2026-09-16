import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화 중 해당 기간에 개봉한 216편의 데이터를 분석합니다.")

# 데이터 불러오기 및 전처리 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르(genre) 전처리: '|' 기호로 여러 개가 적혀 있다면 첫 번째 장르만 추출
    df['genre'] = df['genre'].apply(lambda x: str(x).split('|')[0] if pd.notnull(x) else x)
    
    return df

# 데이터 로드
df = load_data()

# 구역 나누기 (첫 번째 그래프)
st.header("1. 장르별 영화 편수 (도넛 그래프)")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# 플롯리 도넛 그래프 생성
# hole 속성을 주어 가운데가 뚫린 도넛 형태 생성
fig_donut = px.pie(
    genre_counts, 
    names='genre', 
    values='count', 
    hole=0.4,
    title='장르별 개봉 영화 비율'
)
# 마우스를 올렸을 때(hover) 편수와 비율이 잘 보이도록 설정
fig_donut.update_traces(hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}')

# 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석을 적을 자리 마련
st.info("💡 **이 그래프로 알 수 있는 것:** (이곳에 장르 분포에 대한 해석을 한 문장으로 적어보세요.)")

# 다음 구역을 위한 구분선
st.divider()

# (필요하다면 이 아래에 두 번째, 세 번째 그래프 코드를 추가해 나갈 수 있습니다.)
