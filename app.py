import streamlit as st

def main():
    st.set_page_config(page_title="MVP BASEBALL: Retro Edition", layout="wide")

    # --- [1. 게임 상태 관리] ---
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # --- [2. MLB 30개 팀 리스트] ---
    mlb_teams = [
        "AZ Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", 
        "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians", 
        "Colorado Rockies", "Detroit Tigers", "Houston Astros", "KC Royals", 
        "LA Angels", "LA Dodgers", "Miami Marlins", "Milwaukee Brewers", 
        "Minnesota Twins", "NY Mets", "NY Yankees", "Oakland Athletics", 
        "Philadelphia Phillies", "Pittsburgh Pirates", "SD Padres", "SF Giants", 
        "Seattle Mariners", "STL Cardinals", "Tampa Bay Rays", "Texas Rangers", 
        "Toronto Blue Jays", "Washington Nationals"
    ]

    # --- [3. 초기 설정 화면 (아무것도 못하는 상태)] ---
    if not st.session_state.game_started:
        st.markdown("""
            <div style="text-align:center; padding:50px; background:#f0f2f6; border-radius:20px; border:5px solid #1e3a8a;">
                <h1 style="color:#1e3a8a; font-family:'Arial Black'; font-size:45px;">EA SPORTS <br><span style="color:#ef4444;">MVP BASEBALL</span></h1>
                <p style="font-weight:bold; color:#475569;">팀과 투수를 선택하고 경기를 시작하세요!</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2, col3 = st.columns(3)
        with col1:
            away_team = st.selectbox("⚾ 원정 팀 선택", mlb_teams, index=18)
        with col2:
            home_team = st.selectbox("🏠 홈 팀 선택", mlb_teams, index=13)
        with col3:
            pitcher_name = st.text_input("👤 투수 이름 입력", "K. Brown")
            
        if st.button("🏟️ GAME START", use_container_width=True, type="primary"):
            st.session_state.away_team = away_team
            st.session_state.home_team = home_team
            st.session_state.pitcher_name = pitcher_name
            st.session_state.game_started = True
            st.rerun()
            
        st.stop() # 게임 시작 전에는 아래 코드를 실행하지 않음

    # --- [4. 경기장 그래픽 (포수 시점)] ---
    st.markdown(f"### 🏟️ {st.session_state.away_team} vs {st.session_state.home_team}")

    # 자바스크립트 엔진으로 보낼 변수 준비
    away_t = st.session_state.away_team
    home_t = st.session_state.home_team
    p_name = st.session_state.pitcher_name

    # 하단 컨트롤러를 미리 선언 (그래픽 아래에 배치하기 위해)
    st.write("")
    c1, c2 = st.columns([1, 2])
    with c1:
        selected_pitch = st.radio("🔮 PITCH TYPE", ["Fastball", "Slider", "Curve"], horizontal=True)
    with c2:
        if selected_pitch == "Fastball":
            p_speed, p_control = st.slider("Velocity", 90, 105, 98), st.slider("Control", 1, 100, 85)
        elif selected_pitch == "Slider":
            p_speed, p_control = st.slider("Velocity", 80, 95, 88), st.slider("Control", 1, 100, 75)
        else:
            p_speed, p_control = st.slider("Velocity", 70, 88, 76), st.slider("Control", 1, 100, 70)

    # --- [5. 메인 게임 엔진 (HTML/Canvas)] ---
    # 클래식 EA Sports 스코어보드와 포수 시점 원근법 적용
    game_html = """
    <div style="position: relative; width: 900px; margin: 0 auto; background: #fff; padding: 10px; border-radius: 15px; border: 3px solid #ccc; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        
        <div style="position: absolute; top: 30px; left: 30px; width: 160px; background: rgba(0,0,0,0.7); border: 2px solid #fff; border-radius: 5px; color: #fff; font-family: sans-serif; padding: 10px; z-index: 10;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #555;">
                <span>__AWAY_ABBR__</span><span id="sb-away">0</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top:5px;">
                <span>__HOME_ABBR__</span><span id="sb-home">0</span>
            </div>
            <div style="font-size: 11px; text-align: center; margin-top: 8px; color: #ffeb3b; font-weight: bold;">
                1st INNING <br> <span id="sb-outs">O O O</span>
            </div>
        </div>

        <canvas id="eaCanvas" width="880" height="480" style="background: #f0f0f0; border-radius: 10px; cursor: crosshair;"></canvas>
        
        <div id="status-bar" style="margin-top: 10px; background: #1e3a8a; color: white; padding: 10px; border-radius: 8px; font-family: sans-serif; font-size: 14px;">
            [READY] PITCHER: __PITCHER_NAME__ | BATTER: A. RODRIGUEZ
        </div>
    </div>

    <script>
        const canvas = document.getElementById('eaCanvas');
        const ctx = canvas.getContext('2d');

        const config = {
            pName: "__PITCHER_NAME__",
            type: "__P_TYPE__",
            speed: __P_SPEED__,
            control: __P_CONTROL__
        };

        let state = { away: 0, home: 0, s: 0, b: 0, o: 0, bases: [0,0,0] };
        let mouse = { x: 0, y: 0 };
        let ball = { active: false, x: 440, y: 180, tx: 0, ty: 0, scale: 2 };
        let history = [];

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = (e.clientX - rect.left);
            mouse.y = (e.clientY - rect.top);
        });

        canvas.addEventListener('mousedown', () => {
            if (ball.active) return;
            // 홈플레이트 주변 클릭 시 투구
            if (mouse.x > 350 && mouse.x < 530 && mouse.y > 280 && mouse.y < 450) {
                let err = (100 - config.control) * 0.4;
                ball.tx = mouse.x + (Math.random() - 0.5) * err;
                ball.ty = mouse.y + (Math.random() - 0.5) * err;
                ball.x = 440; ball.y = 180; ball.scale = 2;
                ball.active = true;
            }
        });

        function log(m) {
            document.getElementById('status-bar').innerText = `[PITCH] ` + m;
        }

        function resolve() {
            const isStrike = (ball.tx > 390 && ball.tx < 490 && ball.ty > 320 && ball.ty < 420);
            const swing = Math.random() < (isStrike ? 0.6 : 0.2);

            if (swing) {
                if (Math.random() < 0.4) {
                    const hit = Math.random();
                    if (hit < 0.1) {
                        state.home += 1; log("BACK BACK BACK... IT'S GONE! HOME RUN!");
                    } else {
                        log("A HARD HIT BALL INTO THE FIELD!");
                    }
                    state.s = 0; state.b = 0;
                } else {
                    state.s++; log("STRIKE! HE SWUNG THROUGH THAT ONE!");
                }
            } else {
                if (isStrike) { state.s++; log("STRIKE ON THE CORNER!"); }
                else { state.b++; log("BALL, JUST A BIT OUTSIDE."); }
            }

            if(state.s >= 3) { state.o++; state.s = 0; log("HE'S OUT! THREE STRIKES!"); }
            if(state.o >= 3) { state.o = 0; log("SIDE RETIRED."); }
            
            document.getElementById('sb-home').innerText = state.home;
            document.getElementById('sb-outs').innerText = "●".repeat(state.o) + "○".repeat(3-state.o);
            history.push({x: ball.tx, y: ball.ty, s: isStrike});
            if(history.length > 5) history.shift();
        }

        function draw() {
            ctx.clearRect(0,0,880,480);

            // --- 1. 배경: 야구장 원근법 ---
            // 잔디 필드
            ctx.fillStyle = "#2e7d32";
            ctx.beginPath(); ctx.moveTo(0, 480); ctx.lineTo(880, 480); ctx.lineTo(600, 150); ctx.lineTo(280, 150); ctx.closePath(); ctx.fill();
            
            // 내야 흙 (홈플레이트 근처)
            ctx.fillStyle = "#8d6e63";
            ctx.beginPath(); ctx.ellipse(440, 400, 250, 100, 0, 0, Math.PI * 2); ctx.fill();
            
            // 투수 마운드
            ctx.fillStyle = "#6d4c41";
            ctx.beginPath(); ctx.arc(440, 200, 30, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.fillRect(425, 195, 30, 5); // 투판

            // 홈 플레이트
            ctx.fillStyle = "#fff";
            ctx.beginPath(); ctx.moveTo(440, 440); ctx.lineTo(460, 420); ctx.lineTo(460, 400); ctx.lineTo(420, 400); ctx.lineTo(420, 420); ctx.closePath(); ctx.fill();

            // --- 2. 투수와 타자 배치 ---
            // 투수 (저 멀리)
            ctx.fillStyle = "#1e3a8a";
            ctx.beginPath(); ctx.arc(440, 180, 10, 0, Math.PI*2); ctx.fill(); // 머리
            ctx.fillRect(435, 190, 10, 15); // 몸통

            // 타자 (가까이 오른쪽 타석)
            ctx.fillStyle = "#b91c1c";
            ctx.beginPath(); ctx.arc(520, 350, 15, 0, Math.PI*2); ctx.fill(); // 머리
            ctx.fillRect(510, 365, 20, 40); // 몸통
            ctx.strokeStyle = "#5d4037"; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.moveTo(520, 360); ctx.lineTo(490, 310); ctx.stroke(); // 배트

            // --- 3. 스트라이크 존 가이드 (EA 스타일 사각형) ---
            ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
            ctx.lineWidth = 2;
            ctx.strokeRect(390, 320, 100, 100);

            // 마우스 조준선
            if (!ball.active && mouse.x > 300) {
                ctx.strokeStyle = "#fff"; ctx.lineWidth = 1;
                ctx.strokeRect(mouse.x - 10, mouse.y - 10, 20, 20);
            }

            // 투구 기록
            history.forEach(h => {
                ctx.fillStyle = h.s ? "#4caf50" : "#f44336";
                ctx.beginPath(); ctx.arc(h.x, h.y, 4, 0, Math.PI*2); ctx.fill();
            });

            // --- 4. 공 날아가기 애니메이션 (원근법) ---
            if (ball.active) {
                ball.x += (ball.tx - ball.x) * 0.12;
                ball.y += (ball.ty - ball.y) * 0.12;
                ball.scale += 0.2; // 다가올수록 커짐

                ctx.fillStyle = "#fff";
                ctx.shadowBlur = 10; ctx.shadowColor = "#fff";
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.scale, 0, Math.PI * 2); ctx.fill();
                ctx.shadowBlur = 0;

                if (Math.abs(ball.y - ball.ty) < 2) {
                    ball.active = false;
                    resolve();
                }
            }

            requestAnimationFrame(draw);
        }
        draw();
    </script>
    """

    # --- [6. 파이썬 변수 매핑 및 출력] ---
    away_abbr = away_t[:3].upper()
    home_abbr = home_t[:3].upper()

    final_html = (
        game_html
        .replace("__AWAY_ABBR__", away_abbr)
        .replace("__HOME_ABBR__", home_abbr)
        .replace("__PITCHER_NAME__", p_name)
        .replace("__P_TYPE__", selected_pitch)
        .replace("__P_SPEED__", str(p_speed))
        .replace("__P_CONTROL__", str(p_control))
    )

    st.components.v1.html(final_html, height=600)

    # 리셋 버튼
    if st.button("🔄 RESET SETUP"):
        st.session_state.game_started = False
        st.rerun()

if __name__ == "__main__":
    main()
