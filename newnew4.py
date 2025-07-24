import streamlit as st
import random
import pandas as pd

# -------------------------------
# 설정
# -------------------------------
MAP_WIDTH = 8
MAP_HEIGHT = 8
MAX_HP = 5

OBSTACLE_TYPES = {
    "🔥": {"name": "불구덩이", "damage": 2, "msg": "🔥 불에 데였어요! HP -2"},
    "💀": {"name": "독 함정", "damage": 3, "msg": "💀 독가스에 당했어요! HP -3"},
    "🪨": {"name": "바위", "damage": 1, "msg": "🪨 바위에 부딪혔어요! HP -1"},
}

GOAL = "🏁"
PLAYER = "🧍"
EMPTY = "⬜"

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "player_pos" not in st.session_state:
    st.session_state.player_pos = [0, 0]
    st.session_state.hp = MAX_HP
    st.session_state.map = [["" for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    st.session_state.goal_pos = [MAP_WIDTH - 1, MAP_HEIGHT - 1]
    st.session_state.history = []

    # 장애물 배치
    for _ in range(15):
        while True:
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            if [x, y] != st.session_state.player_pos and [x, y] != st.session_state.goal_pos and st.session_state.map[y][x] == "":
                st.session_state.map[y][x] = random.choice(list(OBSTACLE_TYPES.keys()))
                break

# -------------------------------
# 맵 렌더링
# -------------------------------
def render_map():
    grid = []
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            if [x, y] == st.session_state.player_pos:
                row.append(PLAYER)
            elif [x, y] == st.session_state.goal_pos:
                row.append(GOAL)
            elif st.session_state.map[y][x] in OBSTACLE_TYPES:
                row.append(st.session_state.map[y][x])
            else:
                row.append(EMPTY)
        grid.append(row)
    df = pd.DataFrame(grid)
    st.dataframe(df, use_container_width=True, height=500)

# -------------------------------
# 이동 처리
# -------------------------------
def move(dx, dy):
    x, y = st.session_state.player_pos
    nx, ny = x + dx, y + dy
    if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
        st.session_state.player_pos = [nx, ny]
        cell = st.session_state.map[ny][nx]
        if cell in OBSTACLE_TYPES:
            dmg = OBSTACLE_TYPES[cell]["damage"]
            st.session_state.hp -= dmg
            st.session_state.history.append(OBSTACLE_TYPES[cell]["msg"])
            st.session_state.map[ny][nx] = ""  # 장애물 제거

# -------------------------------
# UI 구성
# -------------------------------
st.set_page_config(layout="wide")
st.title("🧍 장애물 피하기 RPG 대모험")
st.markdown(f"💖 **HP**: `{st.session_state.hp}` / {MAX_HP} | 🎯 목표 위치: `{st.session_state.goal_pos}`")

render_map()

# 방향 버튼
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ 왼쪽"):
        move(-1, 0)
with col2:
    if st.button("⬆️ 위쪽"):
        move(0, -1)
    st.write("")  # spacer
    if st.button("⬇️ 아래"):
        move(0, 1)
with col3:
    if st.button("➡️ 오른쪽"):
        move(1, 0)

# -------------------------------
# 상태 출력
# -------------------------------
if st.session_state.hp <= 0:
    st.error("💀 체력이 모두 소진되었습니다... Game Over!")
    if st.button("🔁 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

elif st.session_state.player_pos == st.session_state.goal_pos:
    st.balloons()
    st.success("🎉 목표에 도달했습니다! 승리!")
    if st.button("🔄 새 게임"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

elif st.session_state.history:
    st.info(st.session_state.history[-1])
