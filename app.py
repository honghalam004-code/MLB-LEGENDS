import streamlit as st
import random

# --- [1. 게임 상태 및 데이터 초기화] ---
def init_game():
    if 'game_initialized' not in st.session_state:
        st.session_state.game_initialized = True
        st.session_state.inning = 1
        st.session_state.half = "초"
        st.session_state.outs = 0
        st.session_state.strikes = 0
        st.session_state.balls = 0
        st.session_state.score = {"AWAY": 0, "HOME": 0}
        st.session_state.bases = [False, False, False]
        st.session_state.log = ["🎮 마우스로 스트라이크 존 안팎을 클릭하여 투구하세요!"]
        st.session_state.pitcher_name = "Gerrit Cole"
        st.session_state.batter_name = "Aaron Judge"
        
        # 최근 투구 정보 및 자바스크립트 통신용 카운터
        st.session_state.last_click_x = None
        st.session_state.last_click_y = None
        st.session_state.pitch_count = 0

# --- [2. 자바스크립트 클릭 이벤트를 처리하는 쿼리 파라미터 로직] ---
# HTML Canvas에서 클릭한 좌표를 스트림릿 세션 상태로 전달받는 트릭입니다.
query_params = st.query_params
if "click_x" in query_params and "click_y" in query_params and "p_count" in query_params:
    cx = float(query_params["click_x"])
    cy = float(query_params["click_y"])
    pc = int(query_params["p_count"])
    
    # 새로운 투구 클릭인 경우에만 로직 실행 (중복 실행 방지)
    if pc > st.session_state.get('pitch_count', 0):
        st.session_state.pitch_count = pc
        st.session_state.last_click_x = cx
        st.session_state.last_click_y = cy
        
        # 스트라이크/볼 판정 (캔버스 기준 스트라이크 존: X 350~550, Y 100~300)
        is_strike = (350 <= cx <= 550) and (100 <= cy <= 300)
        speed = random.randint(85, 99)
        
        if is_strike:
            st.session_state.strikes += 1
            msg = f"🔥 스트라이크! ({speed} mph) - 존 구석을 찌릅니다!"
            if st.session_state.strikes >= 3:
                st.session_state.outs += 1
                st.session_state.strikes = 0
                st.session_state.balls = 0
                msg += " ❌ 삼진 아웃!!"
        else:
            st.session_state.balls += 1
            msg = f"🟢 볼! ({speed} mph) - 타자가 잘 골라냈습니다."
            if st.session_state.balls >= 4:
                st.session_state.strikes = 0
                st.session_state.balls = 0
                st.session_state.bases[0] = True
                msg += " 🚶 볼넷 출루!"
                
        st.session_state.log.insert(0, msg)
        
        # 3아웃 공수교대
        if st.session_state.outs >= 3:
            st.session_state.outs = 0
            st.session_state.strikes = 0
            st.session_state.balls = 0
            st.session_state.bases = [False, False, False]
            st.session_state.half = "말" if st.session_state.half == "초" else "초"
            if st.session_state.half == "초": st.session_state.inning += 1
            st.session_state.log.insert(0, f"🔄 공수 교대! {st.session_state.inning}회 {st.session_state.half} 시작.")
        
        # 좌표 찌꺼기 제거 후 리턴하여 화면 갱신
        st.query_params.clear()
        st.rerun()

# --- [3. 통합 그래픽 엔진 (HTML5 Canvas + 타자 애니메이션)] ---
def draw_interactive_game():
    b1 = "#FF4B4B" if st.session_state.bases[0] else "#fff"
    b2 = "#FF4B4B" if st.session_state.bases[1] else "#fff"
    b3 = "#FF4B4B" if st.session_state.bases[2] else "#fff"
    
    # 마지막 투구 점 표시용 자바스크립트 변수
    last_x = st.session_state.last_click_x if st.session_state.last_click_x else -100
    last_y = st.session_state.last_click_y if st.session_state.last_click_y else -100
    next_count = st.session_state.pitch_count + 1

    html_code = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background-color: #f0f2f6; padding: 10px; border-radius: 10px;">
        <canvas id="baseballCanvas" width="800" height="400" style="border: 2px solid #333; background-color: #228B22; border-radius: 8px; cursor: crosshair;"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('baseballCanvas');
        const ctx = canvas.getContext('2d');

        // 1. 야구장 다이아몬드 그리기
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(200, 350); // 홈
        ctx.lineTo(320, 230); // 1루
        ctx.lineTo(200, 110); // 2루
        ctx.lineTo(80, 230);  // 3루
        ctx.closePath();
        ctx.stroke();

        // 투수 마운드
        ctx.fillStyle = "#DAA520";
        ctx.beginPath();
        ctx.arc(200, 230, 12, 0, Math.PI * 2);
        ctx.fill();

        // 베이스 컬러링 (주자 상황 반영)
        function drawBase(x, y, color) {{
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(45 * Math.PI / 180);
            ctx.fillStyle = color;
            ctx.strokeStyle = "#000";
            ctx.fillRect(-10, -10, 20, 20);
            ctx.strokeRect(-10, -10, 20, 20);
            ctx.restore();
        }}
        drawBase(200, 350, "#ffffff"); // 홈
        drawBase(320, 230, "{b1}");   // 1루
        drawBase(200, 110, "{b2}");   // 2루
        drawBase(80, 230, "{b3}");    // 3루

        // 2. 타자 (Batter) 그래픽 그리기 (홈 플레이트 좌측에 배치)
        ctx.fillStyle = "#1E90FF"; // 헬멧/유니폼 색상
        ctx.beginPath();
        ctx.arc(165, 320, 8, 0, Math.PI * 2); // 타자 머리
        ctx.fill();
        ctx.fillRect(160, 328, 10, 22); // 타자 몸통
        
        // 타자 배트 (지포스 느낌의 대각선 라인)
        ctx.strokeStyle = "#D2691E";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(165, 325);
        ctx.lineTo(145, 295); // 위로 비스듬히 들고 있는 배트
        ctx.stroke();

        // 3. 스트라이크 존 격자 그리기 (우측 영역)
        ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
        ctx.fillRect(350, 100, 200, 200);
        ctx.strokeStyle = "#333333";
        ctx.lineWidth = 3;
        ctx.strokeRect(350, 100, 200, 200);

        // 9분할 점선 구획
        ctx.strokeStyle = "#999999";
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        // 가로선
        ctx.beginPath(); ctx.moveTo(350, 166); ctx.lineTo(550, 166); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(350, 233); ctx.lineTo(550, 233); ctx.stroke();
        // 세로선
        ctx.beginPath(); ctx.moveTo(416, 100); ctx.lineTo(416, 300); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(483, 100); ctx.lineTo(483, 300); ctx.stroke();
        ctx.setLineDash([]); // 점선 해제

        // 텍스트 안내 정보
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 14px Arial";
        ctx.fillText("🎯 여기를 클릭해서 투구하세요", 350, 85);
        ctx.fillText("타자: {st.session_state.batter_name}", 110, 390);

        // 4. 전광판 GUI (우측 상단)
        ctx.fillStyle = "#333333";
        ctx.fillRect(600, 20, 180, 80);
        ctx.fillStyle = "#FFD700";
        ctx.font = "16px monospace";
        ctx.fillText("AWAY TEAM: {st.session_state.score['AWAY']}", 615, 45);
        ctx.fillText("HOME TEAM: {st.session_state.score['HOME']}", 615, 75);

        // 5. 마지막 투구 위치에 공 그리기
        let lx = {last_x};
        let ly = {last_y};
        if (lx > 0 && ly > 0) {{
            let isStrike = (lx >= 350 && lx <= 550 && ly >= 100 && ly <= 300);
            ctx.fillStyle = isStrike ? "#FF4B4B" : "#29B6F6";
            ctx.strokeStyle = "#000000";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(lx, ly, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
        }}

        // 6. 마우스 클릭 이벤트 리스너 (부모 스트림릿 창으로 데이터 전송)
        canvas.addEventListener('click', function(event) {{
            const rect = canvas.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            
            // 스트림릿 URL 파라미터를 변경하여 강제 rerun 및 데이터 전송 유도
            const origin = window.location.origin + window.location.pathname;
            window.parent.location.href = origin + `?click_x=${{x}}&click_y=${{y}}&p_count={next_count}`;
        }});
    </script>
    """
    st.components.v1.html(html_code, height=450)

# --- [4. 메인 UI 화면 구성] ---
def draw_ui():
    st.set_page_config(page_title="MLB 마우스 클릭 투구게임", layout="wide")
    st.title("⚾ MLB Legends: 인터랙티브 투구 게임")
    
    # 경기 현황판
    st.info(f"현재 경기: {st.session_state.inning}회{st.session_state.half} | 아웃: {st.session_state.outs}🔴 | 스트라이크: {st.session_state.strikes}🟡 | 볼: {st.session_state.balls}🟢")
    
    # 그래픽 화면 렌더링
    draw_interactive_game()
    
    st.markdown("---")
    
    # 하단 텍스트 중계 및 가이드
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📋 투구 및 매치업 라이브 중계")
        for line in st.session_state.log[:5]:
            st.write(line)
            
    with col2:
        st.subheader("⚙️ 현재 매치업 정보")
        st.write(f"**현재 투수:** 🧢 {st.session_state.pitcher_name} (OVR: 94)")
        st.write(f"**현재 타자:** 🪓 {st.session_state.batter_name} (OVR: 96)")
        st.caption("스트라이크 존(중앙 하얀 격자) 안을 클릭하면 스트라이크, 바깥을 클릭하면 볼로 판정됩니다.")

# --- [5. 메인 진입점] ---
if __name__ == "__main__":
    init_game()
    draw_ui()
