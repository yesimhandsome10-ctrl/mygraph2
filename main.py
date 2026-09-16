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

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig_donut = px.pie(
    genre_counts, 
    names='genre', 
    values='count', 
    hole=0.4,
    title='장르별 개봉 영화 비율'
)
fig_donut.update_traces(hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}')

st.plotly_chart(fig_donut, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** (이곳에 장르 분포에 대한 해석을 한 문장으로 적어보세요.)")

st.divider()


# ==========================================
# 2. 두 번째 그래프: 관객 수 기반 트리맵
# ==========================================
st.header("2. 장르별 영화 총 관객 수 (트리맵)")

df_treemap = df[df['total_audi'] > 0]

fig_treemap = px.treemap(
    df_treemap,
    path=['genre', 'movieNm'], 
    values='total_audi',
    title='장르 및 개별 영화의 총 관객 수 분포'
)
fig_treemap.update_traces(hovertemplate='<b>%{label}</b><br>총 관객: %{value:,.0f}명')

st.plotly_chart(fig_treemap, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** (이곳에 장르 내 특정 영화들의 관객 동원력이나 흥행 비중에 대한 해석을 한 문장으로 적어보세요.)")

st.divider()


# ==========================================
# 3. 세 번째 그래프: 총 관객 수 히스토그램
# ==========================================
st.header("3. 총 관객 수 분포 (히스토그램)")

fig_hist = px.histogram(
    df, 
    x='total_audi', 
    nbins=30,
    title='영화별 총 관객 수 분포 구간',
    labels={'total_audi': '총 관객 수'},
    color_discrete_sequence=['#636EFA']
)
fig_hist.update_layout(yaxis_title="영화 수")
fig_hist.update_traces(hovertemplate='관객 수 구간: %{x}<br>영화 수: %{y}편')

st.plotly_chart(fig_hist, use_container_width=True)

max_movie = df.loc[df['total_audi'].idxmax()]
max_title = max_movie['movieNm']
max_audi = max_movie['total_audi']
q75 = df['total_audi'].quantile(0.75)

st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 총 관객 수 **{int(q75):,}명 이하** 구간에 집중되어 있으며, "
    f"가장 관객 수가 많은 영화는 **'{max_title}'**({max_audi:,.0f}명)입니다."
)

st.divider()


# ==========================================
# 4. 네 번째 그래프: 개봉일 스크린수 vs 총 관객수 (산점도)
# ==========================================
st.header("4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)")

fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title='개봉일 스크린수 대비 총 관객 수 분포',
    labels={'first_scrn': '개봉일 스크린수 (개)', 'total_audi': '총 관객 수 (명)'}
)

# 마우스 호버 양식 설정 (영화명, 장르, 스크린수, 총 관객수 표시)
fig_scatter.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 대체로 개봉일 스크린수가 많을수록 총 관객 수도 증가하는 양의 상관관계를 보이지만, 일부 스크린수가 적음에도 높은 흥행을 기록한 예외적 작품도 존재합니다.")

st.divider()
