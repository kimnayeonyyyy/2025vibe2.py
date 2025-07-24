import streamlit as st
import random

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(page_title="📦 택배기사 시뮬레이터", page_icon="🚚", layout="wide")

# -------------------------------
# 배경 설정 (귀엽고 화려하게)
# -------------------------------
def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://i.pinimg.com/originals/8b/64/b7/8b64b7b3f2aa0cd6cc1f547ae8b3792d.jpg");
            background-size: cover;
            background-position: center;
        }}
        .title-style {{
            font-size: 50px;
            color: #fff5f5;
            text-shadow: 2px 2px 4px #ff69b4;
            text-align: center;
        }}
        .choice-button button {{
            background-color: #ffe4e1;
            border: 2px solid #ff69b4;
            border-radius: 10px;
            color: black;
            padding: 0.5em 1em;
            margin: 0.5em;
            font-size: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# -------------------------------
# 타이틀
# -------------------------------
st.markdown('<div class="title-style">📦 택배기사 시뮬레이터 🚚</div>', unsafe_allow_html=True)
st.markdown("### 🧃 오늘도 평화롭지 않은 배달의 현장에 오신 걸 환영합니다.")

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.points = 0
    st.session_state.log = []

# -------------------------------
# 이벤트 시나리오 (랜덤)
# -------------------------------
events = [
    {
        "situation": "🏢 아파트 단지에서 초인종이 안 눌려요!",
        "choices": {
            "문 두드리기": 1,
            "전화 걸기": 2,
            "그냥 돌아가기": -1
        }
    },
    {
        "situation": "🐶 강아지가 문 앞에서 으르렁거려요!",
        "choices": {
            "간식 던지기": 2,
            "눈 마주치지 않기": 1,
            "놀래키기": -2
        }
    },
    {
        "situation": "📦 박스가 살아 움직여요...?",
        "choices": {
            "열어본다": -2,
            "조용히 놓고 떠난다": 1,
            "사진 찍는다": 2
        }
    },
    {
        "situation": "😡 진상 고객이 반말하며 화를 내요!",
        "choices": {
            "웃으며 사과": 2,
            "무시하고 떠남": -1,
            "나도 반말": -3
        }
    },
    {
        "situation": "☔ 비가 억수같이 내려요!",
        "choices": {
            "우산 씌워 배달": 2,
            "적당히 젖어도 배달": 0,
            "몰래 두고 감": -1
        }
    }
]

# -------------------------------
# 게임 진행
# -------------------------------
if st.session_state.step < len(events):
    current = events[st.session_state.step]
    st.subheader(f"📍 상황 {st.session_state.step+1}: {current['situation']}")

    for choice, score in current["choices"].items():
        if st.button(f"👉 {choice}"):
            st.session_state.points += score
            st.session_state.log.append(f"**{current['situation']}** 에서 **{choice}** 선택 → 점수 {score:+}")
            st.session_state.step += 1
            st.rerun()  # ✅ 수정된 부분
else:
    st.success("🎉 오늘의 배달 완료!")

    st.markdown("### 📊 결과 요약")
    for log in st.session_state.log:
        st.markdown(f"- {log}")

    total = st.session_state.points
    st.markdown(f"### 🏁 총 점수: **{total}점**")

    if total >= 7:
        st.balloons()
        st.markdown("🦸 당신은 전설의 배달 히어로입니다!")
    elif total >= 3:
        st.markdown("📦 평범한 하루였군요. 무사히 완료!")
    else:
        st.markdown("😵‍💫 실수 연발... 내일은 더 잘할 수 있겠죠?")

    st.markdown("---")
    if st.button("🔁 다시 하기"):
        st.session_state.step = 0
        st.session_state.points = 0
        st.session_state.log = []
        st.rerun()  # ✅ 수정된 부분
