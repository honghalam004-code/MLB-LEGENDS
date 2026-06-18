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
        # 주자 상태 (1루, 2루, 3루)
        st.session_state.bases = [False, False, False]
        st.session_state.log = ["게임을 시작합니다. 구종과 코스를 선택하세요!"]
        
        # 투수 데이터 기본 세팅
        st.session_state.pitcher = {
            "name": "Gerrit Cole",
            "pitches": {
                "포심 직구": {"speed": 97, "control": 85},
                "슬라이더": {"speed": 88, "control": 75},
                "체인지업": {"speed": 89, "control": 70},
                "커브": {"speed": 83, "control": 65}
            }
        }
        # 마지막 투구 정보 (SVG 애니메이션용)
        st.session_state.last_pitch_data = None

# --- [2. 화려한 야구장 & 스트라이크 존 그래픽 (SVG 사용)] ---
# requirements.txt 없이 파일 하나로 그래픽을 구현하는 핵심 함수입니다.
def draw_game_graphics_svg(pitch_data=None):
    # 야구장 다이아몬드 및 주자 상태 시각화
    b1_color = "#FF4B4B" if st.session_state.bases[0] else "#fff" # 1루
    b2_color = "#FF4B4B" if st.session_state.bases[1] else "#fff" # 2루
    b3_color = "#FF4B4B" if st.session_state.bases[2] else "#fff" # 3루

    # 마지막 투구에 따른 공 색상 및 위치 계산
    pitch_circle = ""
    if pitch_data:
        actual_zone = pitch_data['zone']
        is_strike = actual_zone in range(1, 10)
        ball_color = "#FF4B4B" if is_strike else "#29B6F6" # 스트라이크 빨강, 볼 파랑
        
        # 9분할 존 좌표 계산 (SVG 내부 좌표)
        row = (actual_zone - 1) // 3
        col = (actual_zone - 1) % 3
        
        if actual_zone == 10: # 유인구 구역
            cx, cy = 200, 50
        else:
            cx = 100 + (col * 100)
            cy = 150 + (row * 100)
            
        # 역동적인 투구 애니메이션 효과를 위한 SVG 코드
        pitch_circle = f"""
            <circle cx="{cx}" cy="{cy}" r="15" fill="{ball_color}" stroke="#000" stroke-width="2">
                <animate attributeName="r" from="0" to="15" dur="0.3s" begin="0.1s" fill="freeze" />
                <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="0.1s" fill="freeze" />
            </circle>
            <text x="{cx}" y="{cy+5}" font-family="Arial" font-size="12" text-anchor="middle" fill="white" font-weight="bold">{actual_zone}</text>
        """

    # 전체 그래픽을 구성하는 SVG 코드 (야구장 + 전광판 + 존)
    svg_html = f"""
    <div style="display: flex; justify-content: center; background-color: #f0f2f6; padding: 10px; border-radius: 10px;">
        <svg width="600" height="400" viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
            <rect width="600" height="400" fill="#228B22" rx="10"/>
            
            <path d="M 300 350 L 500 200 L 300 50 L 100 200 Z" fill="none" stroke="#fff" stroke-width="3"/>
            <circle cx="300" cy="200" r="10" fill="#DAA520"/> <rect x="285" y="335" width="30" height="30" fill="#fff" stroke="#000" transform="rotate(45 300 350)"/> <rect x="485" y="185" width="30" height="30" fill="{b1_color}" stroke="#000" transform="rotate(45 500 200)"/> <rect x="285" y="35" width="30" height="30" fill="{b2_color}" stroke="#000" transform="rotate(45 300 50)"/> <rect x="85" y="185" width="30" height="30" fill="{b3_color}" stroke="#000" transform="rotate(45 100 200)"/> <g transform="translate(350, 80)">
                <rect width="300" height="300" fill="#fff" stroke="#333" stroke-width="3" opacity="0.8"/>
                <line x1="100" y1="0" x2="100" y2="300" stroke="#ccc" stroke-dasharray="5,5"/>
                <line x1="200" y1="0" x2="200" y2="300" stroke="#ccc" stroke-dasharray="5,5"/>
                <line x1="0" y1="100" x2="300" y2="100" stroke="#ccc" stroke-dasharray="5,5"/>
                <line x1="0" y1="200" x2="300" y2="200" stroke="#ccc" stroke-dasharray="5,5"/>
                
                <rect x="50" y="-40" width="200" height="30" fill="#eee" stroke="#aaa" rx="5"/>
                <text x="150" y="-20" font-family="Arial" font-size="12" text-anchor="middle" fill="#555">10번 (외곽 유인구 영역)</text>
                
                {pitch_circle}
            </g>
            
            <g transform="translate(450, 10)">
                <rect width="140" height="60" fill="#333" rx="5" opacity="0.9"/>
                <text x="70" y="25" font-family="monospace" font-size="18" text-anchor="middle" fill="#FFD700">AWAY {st.session_state.score["AWAY"]}</text>
                <text x="70" y="50" font-family="monospace" font-size="18" text-anchor="middle" fill="#FFD700">HOME {st.session_state.score["HOME"]}</text>
            </g>
        </svg>
    </div>
    """
    return svg_html

# --- [3. 투구 실행 로직 (그래픽 데이터 저장 추가)] ---
def execute_pitch(pitch_type, zone_section):
    pitcher = st.session_state.pitcher
    pitch_info = pitcher["pitches"][pitch_type]
    
    # 제구력 반영 (실패 확률)
    if random.randint(1, 100) > pitch_info["control"]:
        actual_zone = random.choice([z for z in range(1, 11) if z != zone_section])
        control_miss = True
    else:
        actual_zone = zone_section
        control_miss = False
        
    # 그래픽 애니메이션을 위한 투구 데이터 저장
    st.session_state.last_pitch_data = {
        'zone': actual_zone,
        'type': pitch_type,
        'is_strike': actual_zone in range(1, 10)
    }
    
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
            # 볼넷 주자 이동 (단순화: 1루만 채움)
            st.session_state.bases[0] = True 
            result_msg += " 🚶 볼넷 출루!"

    st.session_state.log.insert(0, result_msg)

    # 공수교대
    if st.session_state.outs >= 3:
        st.session_state.outs = 0
        st.session_state.strikes = 0
        st.session_state.balls = 0
        st.session_state.bases = [False, False, False] # 주자 초기화
        st.session_state.half = "말" if st.session_state.half == "초" else "초"
        if st.session_state.half == "초": st.session_state.inning += 1
        st.session_state.log.insert(0, f"🔄 공수 교대! {st.session_state.inning}회 {st.session_state.half} 시작.")

# --- [4. 메인 UI 화면 그리기 (그래픽 통합)] ---
def draw_ui():
    st.set_page_config(page_title="MLB Legends 시뮬레이터", layout="wide")
    st.title("⚾ MLB Legends: 투구 시뮬레이터")
    
    # 1. 게임 상태 바 (상단 프리뷰 화면처럼)
    st.info(f"현재 경기: {st.session_state.inning}회{st.session_state.half} | 아웃: {st.session_state.outs}🔴 | 스트라이크: {st.session_state.strikes}🟡 | 볼: {st.session_state.balls}🟢")
    
    # 2. 핵심 게임 그래픽 화면 표시 (새로 추가)
    # 야구장, 전광판, 애니메이션 투구 점이 통합된 SVG 화면
    game_gfx_html = draw_game_graphics_svg(st.session_state.last_pitch_data)
    st.components.v1.html(game_gfx_html, height=420)
    
    st.markdown("---")

    # 3. 컨트롤러 및 로그 분할
    col_ctrl, col_log = st.columns([1, 1])
    
    with col_ctrl:
        st.subheader(f"투수: {st.session_state.pitcher['name']}")
        
        # 구종 선택 (라디오 버튼 -> 가로 세팅으로 더 게임답게)
        pitch_options = list(st.session_state.pitcher["pitches"].keys())
        selected_pitch = st.radio("🔮 구종 선택:", pitch_options, horizontal=True)
        
        # 투구 코스 선택
        zone_options = {
            1: "1번 (좌상단)", 2: "2번 (상단 중앙)", 3: "3번 (우상단)",
            4: "4번 (좌측 중앙)", 5: "5번 (한가운데)", 6: "6번 (우측 중앙)",
            7: "7번 (좌하단)", 8: "8번 (하단 중앙)", 9: "9번 (우하단)",
            10: "10번 (외곽 유인구)"
        }
        selected_zone = st.selectbox("🎯 조준 코스:", options=list(zone_options.keys()), format_func=lambda x: zone_options[x])
        
        # 투구 버튼 (Image 0의 'NEXT PITCH'처럼)
        if st.button("⚾ 공 던지기! (NEXT PITCH)", type="primary", use_container_width=True):
            execute_pitch(selected_pitch, selected_zone)
            st.rerun()
            
    with col_log:
        st.subheader("📋 투구 분석 및 중계")
        for line in st.session_state.log[:6]: # 로그 개수 늘림
            st.write(line)

# --- [5. 메인 진입점] ---
if __name__ == "__main__":
    init_game()
    draw_ui()
