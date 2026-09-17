from pathlib import Path

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='판매 대시보드',
    page_icon='📶',
    layout='wide',
)

TAGET_DIR='data'   #데이터 폴더가 바뀌면 얘만 바꿔주면 됨
TARGET_CSV='data.csv' #데이터 파일이 바뀌면 얘만 바꿔주면 됨

BASE_DIR=Path(__file__).resolve().parent
DATA_PATH=BASE_DIR/TAGET_DIR /TARGET_CSV  #문자열은 슬래시(/)로 이을 수 없고 path가 껴야 슬래시로 이을수있다
#코드를 실행한 파일의 경로가 나온다,=절대경로가 나온다 resolve>우리가 쓸 수있는 형태로 바꿈
# parent 를 하면 app.py가 들어있는 부모인 ,,


df=pd.read_csv(DATA_PATH)

st.title('판매 대시보드')

with st.sidebar:

    st.header('조회조건')

    region= st.selectbox(    #columns를 빼는 방법 ,지역이름이 범주형 데이터로 되어있음>빼기가 애매>
        '지역',
     ['전체','서울','대전','부산'],
       # [
       # '전체',
       # *(df['region'].unique().tolist())
       # ]
    )

   minimum_sales=st.slider(
       '최소 매출',
       min_value=0,
       max_value=int(df['sales'].max()),  #numpy int로 잡힌다. int 넣어서 정수로 바꿔줘야함
       value=0,
       step=500_000,
   )

# 검색 조건을 알았기 때문에 필터링을 해주면 된다.

filtered=df[
   df['sales']>=minimum_sales
].copy()

if region !='전체':
    filtered = filtered[
        filtered['region']==region
    ]

# 필터링까지 다했으니 이제 대시보드 만들면 된다.

## KPI
## 1. 총 매출
## 2. 총 판매량
## 3. 평균 매출
## 4. kpi 계산에 사용된 데이터 행수(조회 건수)

# 1.총매출
total_sales=filtered['sales'].sum()

# 2.총판매량
total_amount=filtered['quantity'].sum()

# 4.조회건수
total_rows = len(filtered)

# 3.평균 매출 #조회됐는지부터 봐야된다.
if total_rows>0:
    average_sales=filtered['sales'].mean()
else:
    average_sales=0

col1,col2,col3,col4 = st.columns(4)

#1. 총매출 KPI
with col1:
    st.metric(
        label='총 매출',
        value=f'{total_sales:,}원',
        border=True,
    )

#2.총판매량
with col2:
    st.metric(
        label='총 판매량',
        value=f'{total_amount:,}개',
        border=True,
    )

#3. 평균매출
with col3:
    st.metric(
        label='평균 매출',
        value=f'{average_sales:,}원',
        border=True,
    )

#4.조회건수
with col4:
    st.metric(
        label='조회건수',
        value=f'{total_rows:,}건',
        border=True,
    )

st.divider() # 구역 나눌때 사용해줌

if filtered.empty:
    st.warning('조건에 맞는 데이터가 없습니다!')
else:

    monthly_sales=filtered.groupby('month',as_index=False)['sales'].sum()  #월별 매출이 나온다
    # filtered는 데이터프레임

    left,right = st.columns([2,1])

    with left:   #왼쪽에 뭔갈 쓰겠다.
        st.subheader('월별매출')

        st.line_chart(
            monthly_sales,
            x='month',
            y='sales',
        )

with right:
    st.subheader('조회 데이터')

    st.dataframe(
        filtered,
        hide_index=True,
        column_config={
            'quantity':st.column_config.NumberColumn(
                '판매량',
                format='%,d개'
            ),
            'sales':st.column_config.NumberColumn(
                '매출',
                format='%,d원'
            )
        }
    )