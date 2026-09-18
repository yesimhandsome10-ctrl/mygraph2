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
    # 결측치는 '미분류'로 처리
    df['genre'] = df['genre'].apply(lambda x: str(x).split('|')[0] if pd.notnull(x) else '미분류')
    df['nation'] = df['nation'].fillna('미상')
    
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

st.info("💡 **이 그래프로 알 수 있는 것:** 데이터셋 내에서 드라마, 액션, 코미디 순으로 영화 편수가 많음을 알 수 있습니다.")

st.divider()


# ==========================================
# 2. 두 번째 그래프: 관객 수 기반 트리맵
# ==========================================
st.header("2. 장르별 영화 총 관객 수 (트리맵)")

df_treemap = df.dropna(subset=['genre', 'movieNm']).copy()
df_treemap = df_treemap.groupby(['genre', 'movieNm'], as_index=False)['total_audi'].sum()
df_treemap = df_treemap[df_treemap['total_audi'] > 0]

fig_treemap = px.treemap(
    df_treemap,
    path=[px.Constant("전체"), 'genre', 'movieNm'], 
    values='total_audi',
    title='장르 및 개별 영화의 총 관객 수 분포'
)
fig_treemap.update_traces(hovertemplate='<b>%{label}</b><br>총 관객: %{value:,.0f}명')

st.plotly_chart(fig_treemap, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르 내에서 소수의 초대형 흥행작이 전체 장르 관객 수의 대부분을 차지하고 있음을 시각적으로 확인할 수 있습니다.")

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
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 흥행 영화도 총 관객 수 **{int(q75):,}명 이하**(주로 200만 미만) 구간에 촘촘하게 몰려 있으며, "
    f"**'{max_title}'**({max_audi:,.0f}명)과 같은 기록적인 흥행작은 극소수라는 점을 분포를 통해 알 수 있습니다."
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

fig_scatter.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 대체로 개봉일 스크린수가 많을수록 총 관객 수도 증가하는 양의 상관관계를 보이지만, 일부 스크린수가 적음에도 높은 흥행을 기록한 예외적 작품도 존재합니다.")

st.divider()


# ==========================================
# 5. 다섯 번째 그래프: 10편 이상 장르별 총 관객 수 박스플롯
# ==========================================
st.header("5. 주요 장르별 총 관객 수 분포 (박스플롯)")

genre_counts_series = df['genre'].value_counts()
target_genres = genre_counts_series[genre_counts_series >= 10].index
df_box = df[df['genre'].isin(target_genres)]

fig_box = px.box(
    df_box,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points='outliers',
    title='영화 수 10편 이상 주요 장르의 총 관객 수 분포',
    labels={'genre': '장르', 'total_audi': '총 관객 수 (명)'}
)

fig_box.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig_box, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 범죄, 액션 장르가 다른 장르에 비해 흥행 성적의 중간값이 높고 박스 권이 상단에 위치하여 흥행 확률이 상대적으로 높음을 알 수 있습니다.")

st.divider()


# ==========================================
# 6. 여섯 번째 그래프: 초반 화력 vs 최종 성적 (버블 그래프)
# ==========================================
st.header("6. 개봉주 화력(크기), 스크린수, 최종 관객수의 관계 (버블 그래프)")

df_bubble = df[df['first_week_audi'] > 0].copy()

fig_bubble = px.scatter(
    df_bubble,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=50,
    title='개봉일 스크린수 vs 총 관객 수 (버블: 개봉 첫 주 관객)',
    labels={
        'first_scrn': '개봉일 스크린수 (개)', 
        'total_audi': '총 관객 수 (명)',
        'first_week_audi': '개봉 첫 주 관객 (명)'
    }
)

fig_bubble.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br><b>개봉 첫 주 관객: %{marker.size:,.0f}명</b><br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 버블의 크기(개봉 첫 주 관객)도 대체로 큰 경향을 보여 초반 스크린 확보가 초기 관객 동원에 영향을 미침을 알 수 있습니다.")

st.divider()


# ==========================================
# 7. 일곱 번째 그래프: 제작 국가 및 장르별 영화 편수 (선버스트 그래프)
# ==========================================
st.header("7. 제작 국가 및 장르별 영화 편수 (선버스트 그래프)")

df_sunburst = df.groupby(['nation', 'genre'], as_index=False).size()
df_sunburst.columns = ['nation', 'genre', 'count']

fig_sunburst = px.sunburst(
    df_sunburst,
    path=['nation', 'genre'],
    values='count',
    title='제작 국가 및 장르별 영화 편수 분포'
)

fig_sunburst.update_traces(
    hovertemplate='<b>%{label}</b><br>영화 편수: %{value}편'
)

st.plotly_chart(fig_sunburst, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 한국과 미국 등 주요 제작 국가별로 제작되는 주요 장르 구성 비율의 차이를 계층적 도넛 형태로 직관적으로 파악할 수 있습니다.")

st.divider()


# ==========================================
# 8. 여덟 번째 그래프: 10위권 유지 일수 vs 총 관객 수 (산점도)
# ==========================================
st.header("8. 10위권에 오래 머문 영화는 총 관객도 많은가")

fig_top10 = px.scatter(
    df,
    x='days_in_top10',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title='10위권에 오래 머문 영화는 총 관객도 많은가',
    labels={
        'days_in_top10': '10위권 유지 일수 (일)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르'
    }
)

fig_top10.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>10위권 유지: %{x}일<br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig_top10, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 10위권 머문 날수가 길수록 총 관객 수 역시 뚜렷하게 증가하는 강한 양의 상관관계를 보여주며, 장기 흥행(롱런)이 초대형 흥행의 핵심 조건임을 나타냅니다.")

st.divider()
