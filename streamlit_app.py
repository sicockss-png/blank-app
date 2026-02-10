import streamlit as st
from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta

# 1. 화면 설정 (앱 이름과 아이콘)
st.set_page_config(page_title="나의 주식 비서", layout="wide")

# 2. 사진처럼 예쁘게 만들기 위한 '색깔 옷(CSS)' 입히기
st.markdown("""
    <style>
    .stock-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 10px solid #1E88E5;
    }
    .stock-name { font-size: 24px; font-weight: bold; color: #333; }
    .price-up { color: #e53935; font-size: 20px; font-weight: bold; }
    .price-down { color: #1E88E5; font-size: 20px; font-weight: bold; }
    .info-label { color: #666; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 나의 주식 시세 정보")

# 3. 왼쪽 설정 메뉴
with st.sidebar:
    st.header("⚙️ 설정")
    drop_val = st.number_input("하락 감지(%)", value=45.0)
    stocks_input = st.text_area("종목 입력", "보성파워텍, 한화솔루션, 삼성전자")
    target_date = st.text_input("기준일 (돌파확인용)", "20240101")
    st.button("🔄 시세 새로고침")

# 4. 데이터 계산 및 화면 출력
names = [s.strip() for s in stocks_input.split(',')]
today = datetime.now().strftime("%Y%m%d")

for name in names:
    try:
        tickers = stock.get_market_ticker_list()
        ticker_dict = {stock.get_market_ticker_name(t): t for t in tickers}
        code = ticker_dict.get(name)
        if not code: continue

        # 시세 정보 가져오기
        df = stock.get_market_ohlcv_by_date((datetime.now()-timedelta(days=365)).strftime("%Y%m%d"), today, code)
        v = df.iloc[-1]
        curr, high, rate = int(v['종가']), int(v['고가']), v['등락률']
        
        # 돌파 확인 로직
        break_date = "없음"
        if target_date in df.index.strftime('%Y%m%d'):
            base_p = df.loc[target_date, '종가']
            after_df = df.loc[target_date:]
            broken = after_df[after_df['시가'] < base_p]
            if not broken.empty: break_date = broken.index[0].strftime('%Y-%m-%d')

        # 5. 사진처럼 '카드 모양'으로 그리기
        color_class = "price-up" if rate > 0 else "price-down"
        st.markdown(f"""
            <div class="stock-card">
                <div class="stock-name">{name} <span class="{color_class}">{rate:+.2f}%</span></div>
                <hr>
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <p class="info-label">현재가</p>
                        <p style="font-size: 22px; font-weight: bold;">{curr:,}원</p>
                    </div>
                    <div>
                        <p class="info-label">고가대비(원칙)</p>
                        <p style="color: #f4511e; font-weight: bold;">{high:+,}원</p>
                    </div>
                    <div>
                        <p class="info-label">{target_date} 돌파일</p>
                        <p style="color: #43A047; font-weight: bold;">{break_date}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        continue
