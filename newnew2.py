import streamlit as st
import random

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(page_title="🧙 장애물 피하기 RPG", page_icon="⚔️", layout="centered")

# -------------------------------
# 스타일 꾸미기
# -------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #fdf0ff;
        background-image: linear-gradient(135deg, #ffe0f0 25%, transparent 25%), 
                          linear-gradient(225deg, #ffe0f0 25%, transparent 25%), 
                          linear-gradient(45deg, #ffe0f0 25%, transparent 25%), 
                          linear-gradient(315deg, #ffe0f0 25%, #fdf0ff 25%);
        background-size: 60px 60px;
        background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
    }
    .title {
        font-size:48px;
        color:#800080;
        text-align:center;
        font-weight:bold;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 게임 상태 초기화
# -------------------------------
if "hp" not in st.session_state:
    st.session_state.hp = 10
    st.session_state.stage = 1
    st.session_state.log = []

# -------------------------------
# 이벤트 정의
# -------------------------------
obstacles = [
    ("🔥 용암 구덩이!", -3, "🔥 뜨거워! HP -3"),
    ("🪨 굴러오는 바위!", -2, "💥 꽝! HP -2"),
    ("🧟 좀비 떼!", -4, "🧟 공격받음! HP -4"),
    ("💀 함정 발판!", -2, "💣 푹 빠졌어! HP -2"),
]

rewards = [
    ("🍖 회복 음식 발견!", +2, "🍖 맛있다! HP +2"),
    ("🧪 체력 포션!", +3, "✨ 회복했다! HP +3"),
    ("💎 보물상자!", 0, "💎 아무 일도 일어나지 않았어..."),
    ("🛡️ 방어 스크롤", 0, "🛡️ 다음 피해 반감 (구현 가능)"),
]

# -------------------------------
# 게임 종료 조건
# -------------------------------
def game_over():
    st.error("💀 당신은 쓰러졌습니다... GAME OVER.")
    st.markdown("### 로그 기록:")
    for log in st.session_state.log:
        st.markdown(f"- {log}")
    if st.button("🔄 다시 시작"):
        st.session_state.hp = 10
        st.session_state.stage = 1
        st.session_state.log = []
        st.rerun()

# -------------------------------
# 게임 제목
# -------------------------------
st.markdown('<div class="title">🧙 장애물 피하기 RPG</div>', unsafe_allow_html=True)
st.markdown(f"### 💖 HP: `{st.session_state.hp}` | 🚪 스테이지: `{st.session_state.stage}`")

# -------------------------------
# 게임 플레이
# -------------------------------
if st.session_state.hp <= 0:
    game_over()
else:
    st.markdown("어디로 이동할까요?")
    col1, col2, col3 = st.columns(3)
    directions = ["⬅️ 왼쪽", "⬆️ 직진", "➡️ 오른쪽"]

    with col1:
        if st.button(directions[0]):
            choice = random.choice(obstacles + rewards)
    with col2:
        if st.button(directions[1]):
            choice = random.choice(obstacles + rewards)
    with col3:
        if st.button(directions[2]):
            choice = random.choice(obstacles + rewards)

    if "choice" in locals():
        name, hp_change, message = choice
        st.session_state.hp += hp_change
        st.session_state.stage += 1
        st.session_state.log.append(f"🚶‍♂️ 스테이지 {st.session_state.stage-1}: {name} → {message} (HP 변화: {hp_change:+})")
        st.success(message)
        st.rerun()
