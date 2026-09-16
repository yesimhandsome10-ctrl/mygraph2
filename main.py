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

# ==========================================
# 1. 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.header("1. 장르별 영화 편수 (도넛 그래프)")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# 플롯리 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts, 
    names='genre', 
    values='count', 
    hole=0.4,
    title='장르별 개봉 영화 비율'
)
# 마우스를 올렸을 때(hover) 편수와 비율이 잘 보이도록 설정
fig_donut.update_traces(hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}')

st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석 자리
st.info("💡 **이 그래프로 알 수 있는 것:** (이곳에 장르 분포에 대한 해석을 한 문장으로 적어보세요.)")

st.divider()


# ==========================================
# 2. 두 번째 그래프: 관객 수 기반 트리맵
# ==========================================
st.header("2. 장르별 영화 총 관객 수 (트리맵)")

# 트리맵을 그릴 때는 값이 0보다 커야 하므로 양수 데이터만 사용 (안전장치)
df_treemap = df[df['total_audi'] > 0]

# 플롯리 트리맵 생성
# path에 계층 구조(장르 -> 영화명)를 넣고, values에 크기를 결정할 데이터를 넣습니다.
fig_treemap = px.treemap(
    df_treemap,
    path=['genre', 'movieNm'], 
    values='total_audi',
    title='장르 및 개별 영화의 총 관객 수 분포'
)

# 마우스를 올렸을 때(hover) 영화명(또는 장르명)과 총 관객 수가 천 단위 콤마와 함께 보이도록 설정
fig_treemap.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객: %{value:,.0f}명'
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 그래프 해석 자리
st.info("💡 **이 그래프로 알 수 있는 것:** (이곳에 장르 내 특정 영화들의 관객 동원력이나 흥행 비중에 대한 해석을 한 문장으로 적어보세요.)")

st.divider()
