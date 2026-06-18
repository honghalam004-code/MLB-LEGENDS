import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# --- [1. 게임 상태 및 데이터 초기화] ---
def init_game():
    if 'inning' not in st.session_state:
        st.session_state.inning = 1
        st.session_state.half = "초"
        st.session_state.outs = 0
        st.session_state.strikes = 0
        st.session_state.balls = 0
        st.session_state.score = {"AWAY": 0, "HOME": 0}
        st.session_state.log = ["게임을 시작합니다. 구종과 코스를 선택하세요!"]
        
        # 실제 MLB 투수 데이터 예시 (추후 파일 분리 가능)
        st.session_state.pitcher = {
            "name": "Gerrit Cole",
            "pitches": {
                "포심 직구": {"speed": 97, "control": 85, "break": 0},
                "슬라이더": {"speed": 88, "control": 75, "break": 80},
                "체인지업": {"speed": 89, "control": 70, "break": 75},
                "커브": {"speed": 83, "control": 65, "break": 90}
            }
        }
        # 현재 던진 공의 위치 저장 (X, Y)
        st.session_state.last_pitch_coord = None
        st.session_state.last_pitch_result = ""

# --- [2. 스트라이크 존 그래픽 생성 함수] ---
def draw_strike_zone(pitch_coord=None):
    fig, ax = plt.subplots(figsize=(4, 4))
    
    # 스트라이크 존 경계 설정 (X: -1~1, Y: 1.5~3.5 사이가 스트라이크 존 가정)
    sz_x = [-1, 1, 1, -1, -1]
    sz_y = [1.5, 1.5, 3.5, 3.5, 1.5]
    ax.plot(sz_x, sz_y, color="black", linewidth=2, label="Strike Zone")
    
    # 9분할 가이드라인 내부선 그리기
    ax.plot([-0.33, -0.33], [1.5, 3.5], color="gray", linestyle="--", linewidth=1)
    ax.plot([0.33, 0.33], [1.5, 3.5], color="gray", linestyle="--", linewidth=1)
    ax.plot([-1, 1], [2.16, 2.16], color="gray", linestyle="--", linewidth=1)
    ax.plot([-1, 1], [2.83, 2.83], color="gray", linestyle="--", linewidth=1)
    
    # 공이 던져진 위치 표시
    if pitch_coord:
        x, y = pitch_coord
        # 스트라이크/볼 여부에 따라 공 색상 변경
        is_strike = (-1 <= x <= 1) and (1.5 <= y <= 3.5)
        color = "red" if is_strike else "green"
        ax.scatter(x, y, color=color, s=200, edgecolors="black", zorder=5)
        ax.text(x + 0.1, y + 0.1, "Pitch", fontsize=10, weight="bold")

    # 그래프 스타일 설정
    ax.set_xlim(-2, 2)
    ax.set_ylim(0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off') # 축 숨기기
    fig.patch.set_facecolor('#f0f2f6') # 스트림릿 배경색과 맞춤
    
    return fig

# --- [3. 투구 실행 로직] ---
def execute_pitch(pitch_type, zone_section):
    pitcher = st.session_state.pitcher
    pitch_info = pitcher["pitches"][pitch_type]
    
    # 1. 사용자가 선택한 구역(1~9번 또는 볼 지역)에 따른 기본 좌표 설정
    # 1~9번은 스트라이크 존 내부, 10번은 외곽 볼 유인구
    sections = {
        1: (-0.66, 3.16), 2: (0, 3.16), 3: (0.66, 3.16),
        4: (-0.66, 2.5),  5: (0, 2.5),  6: (0.66, 2.5),
        7: (-0.66, 1.83), 8: (0, 1.83), 9: (0.66, 1.83),
        10: (1.3, 3.8) # 의도적인 유인구 (우상단 볼)
    }
    
    base_x, base_y = sections[zone_section]
    
    # 2. 투수의 제구력(control)에 따른 흔들림(오차) 계산
    # 제구력이 높을수록(최대 100) 오차가 줄어듭니다.
    error_range = (100 - pitch_info["control"]) / 200
    final_x = base_x + random.uniform(-error_range, error_range)
    final_y = base_y + random.uniform(-error_range, error_range)
    
    st.session_state.last_pitch_coord = (final_x, final_y)
    
    # 3. 판정 (스트라이크 존 안에 들어왔는가?)
    is_strike = (-1 <= final_x <= 1) and (1.5 <= final_y <= 3.5)
    
    # 변화구인 경우 무브먼트(Break) 시각 효과 로그 추가
    break_text = f" (변화각: {pitch_info['break']})" if pitch_info['break'] > 0 else ""
    speed_text = f"{pitch_info['speed'] + random.randint(-2, 2)} mph"

    if is_strike:
        st.session_state.strikes += 1
        result_msg = f"🔥 스트라이크! - {pitcher['name']}의 {pitch_type}({speed_text}){break_text}"
        if st.session_state.strikes >= 3:
            st.session_state.outs += 1
            st.session_state.strikes = 0
            st.session_state.balls = 0
            result_msg += " ❌ 삼진 아웃!!"
    else:
        st.session_state.balls += 1
        result_msg = f"🟢 볼! - 코스를 벗어난 {pitch_type}({speed_text})"
        if st.session_state.balls >= 4:
            st.session_state.strikes = 0
            st.session_state.balls = 0
            result_msg += " 🚶 볼넷 출루!"

    st.session_state.log.insert(0, result_msg)

    # 3아웃 공수교대 처리
    if st.session_state.outs >= 3:
        st.session_state.outs = 0
        st.session_state.strikes = 0
        st.session_state.balls = 0
        st.session_state.half = "말" if st.session_state.half == "초" else "초"
        if st.session_state.half == "초": st.session_state.inning += 1
        st.session_state.log.insert(0, f"🔄 공수 교대! {st.session_state.inning}회 {st.session_state.half} 시작.")

# --- [4. 메인 UI 화면 그리기] ---
def draw_ui():
    st.set_page_config(page_title="MLB 투구 시뮬레이터", layout="wide")
    st.title("⚾ MLB 스트라이크 존 투구 시뮬레이터")
    
    # 전광판 상단 배치
    st.info(f"현재 경기: {st.session_state.inning}회{st.session_state.half} | 아웃: {st.session_state.outs}🔴 | 스트라이크: {st.session_state.strikes}🟡 | 볼: {st.session_state.balls}🟢")
    
    # 좌우 분할 (왼쪽: 컨트롤러 및 로그, 오른쪽: 스트라이크 존 그래픽)
    col_ctrl, col_zone = st.columns([1, 1])
    
    with col_ctrl:
        st.subheader(f"투수: {st.session_state.pitcher['name']}")
        
        # 구종 선택 라디오 버튼
        pitch_options = list(st.session_state.pitcher["pitches"].keys())
        selected_pitch = st.radio("🔮 던질 구종을 선택하세요:", pitch_options)
        
        # 투구 코스 선택 (9분할 존 + 유인구)
        zone_options = {
            1: "1번 (좌상단)", 2: "2번 (상단 중앙)", 3: "3번 (우상단)",
            4: "4번 (좌측 중앙)", 5: "5번 (한가운데 한복판)", 6: "6번 (우측 중앙)",
            7: "7번 (좌하단)", 8: "8번 (하단 중앙)", 9: "9번 (우하단)",
            10: "10번 (빠지는 유인구 볼)"
        }
        selected_zone = st.selectbox("🎯 조준할 코스를 선택하세요:", options=list(zone_options.keys()), format_func=lambda x: zone_options[x])
        
        # 투구 버튼
        if st.button("⚾ 공 던지기!", type="primary", use_container_width=True):
            execute_pitch(selected_pitch, selected_zone)
            st.rerun()
            
        # 중계 로그
        st.markdown("---")
        st.subheader("📋 투구 분석 기록")
        for line in st.session_state.log[:5]:
            st.write(line)

    with col_zone:
        st.subheader("🎯 스트라이크 존 현황")
        # 최근 투구 좌표를 넘겨서 실시간으로 점을 찍음
        fig = draw_strike_zone(st.session_state.last_pitch_coord)
        st.pyplot(fig)

# --- [5. 메인 진입점] ---
if __name__ == "__main__":
    init_game()
    draw_ui()
