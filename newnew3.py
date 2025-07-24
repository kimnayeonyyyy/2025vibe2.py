import streamlit as st
import random

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="🧍장애물 피하기 미로", page_icon="🧱")

MAP_SIZE = 5
OBSTACLE_EMOJIS = ["🔥", "💀", "🪨"]
GOAL_EMOJI = "🏁"
PLAYER_EMOJI = "🧍"
EMPTY_EMOJI = "⬜"
MAX_HP = 5

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "player_pos" not in st.session_state:
    st.session_state.player_pos = [0, 0]
    st.session_state.hp = MAX_HP
    st.session_state.map = [["" for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    st.session_state.goal_pos = [MAP_SIZE - 1, MAP_SIZE - 1]
    
    # 장애물 랜덤 배치 (플레이어, 목표 제외)
    for _ in range(5):
        while True:
            x = random.randint(0, MAP_SIZE - 1)
            y = random.randint(0, MAP_SIZE - 1)
            if [x, y] != st.session_state.player_pos and [x, y] != st.session_state.goal_pos and st.session_state.map[y][x] == "":
                st.session_state.map[y][x] = random.choice(OBSTACLE_EMOJIS)
                break

# -------------------------------
# 게임 상태 체크
# -------------------------------
def render_map():
    for y in range(MAP_SIZE):
        row = ""
        for x in range(MAP_SIZE):
            if [x, y] == st.session_state.player_pos:
                row += PLAYER_EMOJI
            elif [x, y] == st.session_state.goal_pos:
                row += GOAL_EMOJI
            elif st.session_state.map[y][x] in OBSTACLE_EMOJIS:
                row += st.session_state.map[y][x]
            else:
                row += EMPTY_EMOJI
        st.write(row)

def move(dx, dy):
    x, y = st.session_state.player_pos
    nx, ny = x + dx, y + dy

    if 0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE:
        st.session_state.player_pos = [nx, ny]
        cell = st.session_state.map[ny][nx]
        if cell in OBSTACLE_EMOJIS:
            st.session_state.hp -= 1
            st.warning(f"💥 {cell} 에 닿아 HP -1! (남은 HP: {st.session_state.hp})")
            st.session_state.map[ny][nx] = ""  # 한번 맞으면 제거

# -------------------------------
# UI 렌더링
# -------------------------------
st.title("🧍 장애물 피하기 미니맵")
st.markdown(f"**💖 HP**: `{st.session_state.hp}` / {MAX_HP}")

render_map()

# 방향 버튼
col1, col2, col3 = st.columns(3)
with col1:
    st.write("")
    if st.button("⬅️ 왼쪽"):
        move(-1, 0)
with col2:
    if st.button("⬆️ 위쪽"):
        move(0, -1)
    st.write("")
    if st.button("⬇️ 아래"):
        move(0, 1)
with col3:
    st.write("")
    if st.button("➡️ 오른쪽"):
        move(1, 0)

# -------------------------------
# 게임 종료 판정
# -------------------------------
if st.session_state.player_pos == st.session_state.goal_pos:
    st.balloons()
    st.success("🎉 목표 지점에 도착! 승리했습니다!")
    if st.button("🔄 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
elif st.session_state.hp <= 0:
    st.error("💀 체력이 모두 소진되었습니다... Game Over!")
    if st.button("🔁 재도전"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
