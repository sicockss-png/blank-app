import streamlit as st
import requests
from bs4 import BeautifulSoup

# 1. 앱 기본 설정 (폰에서 보기 좋게 넓게 설정)
st.set_page_config(page_title="29% 포착기", layout="wide")
st.title("🔥 시가 29% 돌파 감시기")

# 2. 감시할 종목 리스트 (필요시 코드만 추가하면 됩니다)
target_stocks = {
    "한미반도체": "042700",
    "디아이": "003160",
    "유니테스트": "086390",
    "에이프릴바이오": "397030",
    "전진건설로봇": "079900",
    "태광산업": "003240",
    "현대지에프홀딩스": "052390"
}

# 3. 실행 버튼
if st.button('🚀 지금 바로 기세 확인 (새로고침)'):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for name, code in target_stocks.items():
        try:
            # 네이버 증권 데이터 긁어오기
            url = f"https://finance.naver.com/item/main.naver?code={code}"
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 전일가와 시가 추출
            rate_table = soup.find('div', {'class': 'rate_info'}).find('table')
            prev_close = int(rate_table.find('td', {'class': 'first'}).find('span', {'class': 'blind'}).text.replace(',', ''))
            opening_price = int(rate_table.findAll('td')[1].find('span', {'class': 'blind'}).text.replace(',', ''))
            
            # 등락률 계산
            gap = ((opening_price - prev_close) / prev_close) * 100
            
            # 4. 결과 출력 (29% 기준)
            if gap >= 29.0:
                st.error(f"🚨 {name}: 시가 {opening_price:,}원 ({gap:.2f}%) - 점상급!")
            elif gap <= -29.0:
                st.warning(f"❄️ {name}: 시가 {opening_price:,}원 ({gap:.2f}%) - 점하급!")
            else:
                st.success(f"✅ {name}: 시가 {opening_price:,}원 ({gap:.2f}%)")
                
        except Exception as e:
            st.write(f"⚠️ {name}({code}) 데이터를 읽지 못했습니다.")

st.divider()
st.caption("이 앱은 오전 8:40 ~ 9:00 사이 예상체결가 확인용으로 가장 정확합니다.")
