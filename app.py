import streamlit as st
import random

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
        
        # 투수 데이터
        st.session_state.pitcher = {
            "name": "Gerrit Cole",
            "pitches": {
                "포심 직구": {"speed": 97, "control": 85, "break": 0},
                "슬라이더": {"speed": 88, "control": 75, "break": 80},
                "체인지업": {"speed": 89, "control": 70, "break": 75},
                "커브": {"speed": 83, "control": 65, "break": 90}
            }
        }
        # 현재 던진 공의 위치 (9분할 구역 번호 1~10, 스트라이크/볼 여부)
        st.session_state.last_pitch_zone = None
        st.session_state.last_pitch_type = ""

# --- [2. 에러 없는 스트라이크 존 시각화 (HTML/CSS 사용)] ---
def draw_strike_zone_html(highlight_zone=None, is_strike=True):
    # 각 구역별 스타일 지정을 위한 딕셔너리
    zones = {i: "" for i in range(1, 11)}
    
    # 투구가 발생했다면 해당 구역에 표시
    if highlight_zone and highlight_zone in zones:
        bg_color = "#FF4B4B" if is_strike else "#29B6F6" # 스트라이크는 빨강, 볼은 파랑
        zones[highlight_zone] = f"background-color: {bg_color}; color: white; font-weight: bold;"

    # 외부 라이브러리 없이 HTML 테두리로 9분할 존 생성
    zone_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
        <div style="display: grid; grid-template-columns: repeat(3, 80px); grid-template-rows: repeat(3, 80px); gap: 5px; border: 3px solid #333; background-color: white;">
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[1]}">1</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[2]}">2</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[3]}">3</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[4]}">4</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[5]}">5</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[6]}">6</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[7]}">7</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[8]}">8</div>
            <div style="display: flex; align-items: center; justify-content: center; border: 1px dashed #ccc; {zones[9]}">9</div>
        </div>
        <div style="margin-top: 15px; width: 250px; height: 40px; display: flex; align-items: center; justify-content: center; border: 2px solid #aaa; border-radius: 5px; background-color: #fff; {zones[10]}">
            10번 (빠지는 유인구 볼 영역)
        </div>
    </div>
    """
    return zone_html

# --- [3. 투구 실행 로직] ---
def execute_pitch(pitch_type, zone_section):
    pitcher = st.session_state.pitcher
    pitch_info = pitcher["pitches"][pitch_type]
    
    # 제구력 반영 로직 (실제 투구 위치 결정)
    # 제구 난조 확률: 제구력이 85이면 15% 확률로 의도한 구역을 벗어남
    if random.randint(1, 100) > pitch_info["control"]:
        actual_zone = random.choice([z for z in range(1, 11) if z != zone_section])
        control_miss = True
    else:
        actual_zone = zone_section
        control_miss = False
        
    st.session_state.last_pitch_zone = actual_zone
    st.session_state.last_pitch_type = pitch_type
    
    # 판정 (1~9번은 스트라이크, 10번은 볼)
    is_strike = actual_zone in range(1, 10)
    
    speed_text = f"{pitch_info['speed'] + random.randint(-2, 2)} mph"
    miss_text = " (제구 난조!)" if control_miss else ""

    if is_strike:
        st.session_state.strikes += 1
        result_msg = f"🔥 스트라이크! - {pitcher['name']}의 {pitch_type}({speed_text}){miss_text}"
        if st.session_state.strikes >= 3:
            st.session_state.outs += 1
            st.session_state.strikes = 0
            st.session_state.balls = 0
            result_msg += " ❌ 삼진 아웃!!"
    else:
        st.session_state.balls += 1
        result_msg = f"🟢 볼! - 코스를 벗어난 {pitch_type}({speed_text}){miss_text}"
        if st.session_state.balls >= 4:
            st.session_state.strikes = 0
            st.session_state.balls = 0
            result_msg += " 🚶 볼넷 출루!"

    st.session_state.log.insert(0, result_msg)

    # 공수교대
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
    st.title("⚾ MLB 스트라이크 존 투구 시뮬레이터 v1.2")
    
    st.info(f"현재 경기: {st.session_state.inning}회{st.session_state.half} | 아웃: {st.session_state.outs}🔴 | 스트라이크: {st.session_state.strikes}🟡 | 볼: {st.session_state.balls}🟢")
    
    col_ctrl, col_zone = st.columns([1, 1])
    
    with col_ctrl:
        st.subheader(f"투수: {st.session_state.pitcher['name']}")
        
        pitch_options = list(st.session_state.pitcher["pitches"].keys())
        selected_pitch = st.radio("🔮 던질 구종을 선택하세요:", pitch_options)
        
        zone_options = {
            1: "1번 (좌상단)", 2: "2번 (상단 중앙)", 3: "3번 (우상단)",
            4: "4번 (좌측 중앙)", 5: "5번 (한가운데 한복판)", 6: "6번 (우측 중앙)",
            7: "7번 (좌하단)", 8: "8번 (하단 중앙)", 9: "9번 (우하단)",
            10: "10번 (외곽 유인구)"
        }
        selected_zone = st.selectbox("🎯 조준할 코스를 선택하세요:", options=list(zone_options.keys()), format_func=lambda x: zone_options[x])
        
        if st.button("⚾ 공 던지기!", type="primary", use_container_width=True):
            execute_pitch(selected_pitch, selected_zone)
            st.rerun()
            
        st.markdown("---")
        st.subheader("📋 투구 분석 기록")
        for line in st.session_state.log[:5]:
            st.write(line)

    with col_zone:
        st.subheader("🎯 스트라이크 존 상황판")
        # 실제 공이 들어간 존 판단 후 색상 하이라이트
        is_strike_pitch = st.session_state.last_pitch_zone in range(1, 10)
        zone_html = draw_strike_zone_html(st.session_state.last_pitch_zone, is_strike_pitch)
        st.components.v1.html(zone_html, height=400)

# --- [5. 메인 진입점] ---
if __name__ == "__main__":
    init_game()
    draw_ui()
