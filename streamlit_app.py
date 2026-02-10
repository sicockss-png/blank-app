import streamlit as st
from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="나의 종목 감시자", layout="wide")

# 예쁜 디자인 설정
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

with st.sidebar:
    st.header("📋 종목 및 날짜 입력")
    st.info("형식: 종목명:6자리날짜\n(예: 보성파워텍:240201)")
    # 기본 입력값도 6자리로 바꿔두었습니다.
    user_input = st.text_area("입력란", "보성파워텍:240201, 한화솔루션:240115")
    st.button("🔄 데이터 분석")

today = datetime.now().strftime("%Y%m%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

items = [item.strip() for item in user_input.split(',')]

for item in items:
    try:
        if ':' not in item: continue
        name, t_date = item.split(':')
        name, t_date = name.strip(), t_date.strip()

        # 6자리 날짜(240101)를 8자리(20240101)로 자동 변환
        if len(t_date) == 6:
            full_date = "20" + t_date
        else:
            full_date = t_date
