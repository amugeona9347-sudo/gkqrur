import streamlit as st

st.set_page_config(page_title="키오스크 시뮬레이터", layout="wide")

# ------------------------------
# 세션 상태 초기화
# ------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "cart" not in st.session_state:
    st.session_state.cart = []

# 메뉴 데이터
menu = [
    {"name": "아메리카노", "price": 3000},
    {"name": "카페라떼", "price": 3500},
    {"name": "카푸치노", "price": 3800},
    {"name": "초코라떼", "price": 4000},
    {"name": "딸기 스무디", "price": 4500}
]

# ------------------------------
# 페이지 이동 함수
# ------------------------------
def go(page):
    st.session_state.page = page

# ------------------------------
# 홈 화면
# ------------------------------
if st.session_state.page == "home":
    st.title("🍔 키오스크 시뮬레이터")
    st.write("주문을 시작하려면 아래 버튼을 눌러주세요.")

    if st.button("주문 시작하기", use_container_width=True):
        go("menu")

# ------------------------------
# 메뉴 선택 화면
# ------------------------------
elif st.session_state.page == "menu":
    st.title("🛒 메뉴 선택")

    cols = st.columns(2)

    for i, item in enumerate(menu):
        with cols[i % 2]:
            st.subheader(f"{item['name']}")
            st.write(f"가격: {item['price']}원")

            if st.button(f"{item['name']} 담기", key=item['name']):
                st.session_state.cart.append(item)
                st.success(f"{item['name']} 추가됨")

    st.markdown("---")
    if st.button("장바구니로 이동", use_container_width=True):
        go("cart")

    if st.button("⬅ 처음으로", use_container_width=True):
        go("home")

# ------------------------------
# 장바구니 화면
# ------------------------------
elif st.session_state.page == "cart":
    st.title("🧺 장바구니")

    if not st.session_state.cart:
        st.write("장바구니가 비어 있습니다.")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"- {item['name']} / {item['price']}원")
            total += item["price"]

        st.subheader(f"총 금액: {total}원")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("메뉴 더 보기", use_container_width=True):
            go("menu")

    with col2:
        if st.button("결제하기", use_container_width=True):
            go("pay")

    if st.button("⬅ 처음으로", use_container_width=True):
        go("home")

# ------------------------------
# 결제 화면
# ------------------------------
elif st.session_state.page == "pay":
    st.title("💳 결제 화면")

    st.success("결제가 완료되었습니다! 감사합니다 😊")

    if st.button("처음으로 돌아가기", use_container_width=True):
        st.session_state.cart = []
        go("home")
