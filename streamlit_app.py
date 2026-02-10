import streamlit as st
from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta

# 1. 앱 기본 설정
st.set_page_config(page_title="나의 종목 감시자", layout="wide")

# 2. 깔끔한 디자인 (CSS)
st.markdown("""
    <style>
    .stock-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 8px solid #FF5722;
    }
    .status-broken { color: #d32f2f; font-weight: bold; }
    .status-ok { color: #388e3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 종목별 기준일 감시 비서")

# 3. 사이드바 설정
with st.sidebar:
    st.header("📋 종목 및 날짜 입력")
    st.info("형식: 종목명:240101\n(여러 개는 쉼표로 구분)")
    user_input = st.text_area("입력란", "보성파워텍:240201, 한화솔루션:240115")
    if st.button("🔄 데이터 분석 실행"):
        st.rerun()

# 4. 데이터 분석 및 출력
today = datetime.now().strftime("%Y%m%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

items = [item.strip() for item in user_input.split(',')]

for item in items:
    try:
        if ':' not in item: continue
        name, t_date = item.split(':')
        name, t_date = name.strip(), t_date.strip()

        # 6자리 날짜를 8자리로 변환
        full_date = "20" + t_date if len(t_date) == 6 else t_date

        # 종목코드 찾기
        tickers = stock.get_market_ticker_list()
        ticker_dict = {stock.get_market_ticker_name(t): t for t in tickers}
        code = ticker_dict.get(name)
        
        if code:
            df = stock.get_market_ohlcv_by_date(start_date, today, code)
            
            if full_date in df.index.strftime('%Y%m%d'):
                target_info = df.loc[full_date]
                base_open = int(target_info['시가'])
