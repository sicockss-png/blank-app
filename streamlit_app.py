import streamlit as st
from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta

# 모바일 최적화 설정
st.set_page_config(page_title="에이아이비서", layout="wide")

st.markdown("<h2 style='text-align: center;'>📈 내 전용 주식 비서</h2>", unsafe_allow_html=True)

# 설정값 (어르신 원칙 45%)
drop_val = st.sidebar.number_input("감지 비율(%)", value=45.0)
stock_input = st.sidebar.text_area("종목 입력 (쉼표 구분)", "보성파워텍, 한화솔루션")

if st.sidebar.button('🔄 데이터 새로고침'):
    st.rerun()

# 계산 및 표 표시
names = [s.strip() for s in stock_input.split(',')]
results = []
today = datetime.now().strftime("%Y%m%d")

for name in names:
    try:
        tickers = stock.get_market_ticker_list()
        code = [t for t in tickers if stock.get_market_ticker_name(t) == name][0]
        df = stock.get_market_ohlcv_by_date(today, today, code)
        if df.empty: df = stock.get_market_ohlcv_by_date((datetime.now()-timedelta(days=7)).strftime("%Y%m%d"), today, code)
        
        v = df.iloc[-1]
        curr, high, rate = int(v['종가']), int(v['고가']), v['등락률']
        prev_close = curr / (1 + rate / 100)
        high_r = (high - prev_close) / prev_close * 100
        
        # 어르신 계산법: 고가 등락률 - 45%
        pred_r = high_r - drop_val
        pred_p = round(prev_close * (1 + pred_r / 100))
        
        # 분매 2~5 계산
        m2 = round(prev_close * (1 + (pred_r - 1) / 100))
        m3 = round(prev_close * (1 + (pred_r - 2) / 100))
        m4 = round(prev_close * (1 + (pred_r - 3) / 100))
        m5 = round(prev_close * (1 + (pred_r - 4) / 100))

        results.append({
            "종목명": name, "현재가": f"{curr:,}", "등락률": f"{rate:+.2f}%", 
            "고가(%)": f"{high_r:+.2f}%", "예측가(분매1)": f"{pred_p:,}",
            "분매2": f"{m2:,}", "분매3": f"{m3:,}", "분매4": f"{m4:,}", "분매5": f"{m5:,}"
        })
    except: continue

# 표 그리기 (어르신이 주신 이미지와 똑같은 구성)
if results:
    st.table(pd.DataFrame(results))
else:
    st.write("종목명을 확인해주세요.")
