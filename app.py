import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB LIVE FIELD", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0d1b2a; color: #e0e1dd; font-family: -apple-system, sans-serif; }
        .stSelectbox { background: #1b263b !important; color: #ffffff !important; border-radius: 6px; }
        .stButton>button {
            background: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%) !important;
            color: white !important; font-weight: 800; border-radius: 6px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1b263b; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #00b4d8; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 900;">⚾ MLB 리얼 라이브 필드</h1>
                <p style="color: #90e0ef; margin-top: 5px;">유니폼을 입은 선수들과 그라운드를 지키는 수비수들의 숨막히는 리얼 플레이</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            play_mode = st.selectbox("🎮 나의 포지션", ["투수 모드 (볼 배합 및 제구)", "타자 모드 (수읽기 및 타격)"])
        with c2:
            opponent = st.selectbox("🤖 상대 라이벌 팀", ["LA Dodgers (로스앤젤레스 다저스)", "NY Yankees (뉴욕 양키스)"])
            
        if st.button("🏟️ 스타디움 입장"):
            st.session_state.game_role = "pitcher" if "투수" in play_mode else "batter"
            st.session_state.opp_team = opponent.split(" (")[0]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 🏟️ 현재 경기: **{ '투수 플레이 (구종/코스 선택)' if st.session_state.game_role == 'pitcher' else '타자 플레이 (실시간 타격)' }**")

    col_board, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("### 🏟️ 전술실")
        if st.session_state.game_role == "pitcher":
            st.info("🎯 **투구 방법**\n하단 구종을 정한 뒤 캔버스 내 스트라이크 존 주변을 클릭해 던지세요.")
        else:
            st.info("🏏 **타격 방법**\n공이 날아올 때 타이밍을 맞춰 클릭하세요!")
        
        st.markdown("---")
        if st.button("🚪 경기 종료 (메인 리셋)"):
            st.session_state.game_active = False
            st.rerun()

    with col_board:
        # 이스케이프 충돌 우려가 있는 중괄호 수식을 안전하게 전송하기 위한 데이터 바인딩
        opp_team_str = st.session_state.opp_team
        role_str = st.session_state.game_role

        game_html = f"""
        <div style="background: #0b1329; padding: 12px; border-radius: 12px; border: 2px solid #1c2541; max-width: 740px; margin: 0 auto;">
            <div style="background: #020c1b; border: 2px solid #00b4d8; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; display: flex; justify-content: space-between; color: white;">
                <div>
                    <span style="color: #00b4d8; font-weight: bold;">PLAYER</span> <span id="score-p" style="font-size: 18px; font-weight: 900; color: #00b4d8;">0</span> 
                    <span style="color: #64748b; margin: 0 10px;">VS</span> 
                    <span style="color: #f72585; font-weight: bold;">{opp_team_str}</span> <span id="score-opp" style="font-size: 18px; font-weight: 900; color: #f72585;">0</span>
                </div>
                <div>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 15px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="380" style="background: #143615; border: 2px solid #00b4d8; display: block; border-radius: 6px;"></canvas>
            
            <div id="pitcher-controls" style="margin-top: 8px; text-align: center; display: none;">
                <button onclick="setPitch('포심 직구')" style="background: #1d3557; color: white; border: 1px solid #00b4d8; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">⚾ 직구 (Fastball)</button>
                <button onclick="setPitch('슬라이더')" style="background: #1d3557; color: white; border: 1px solid #00b4d8; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">🔮 슬라이더 (Slider)</button>
                <button onclick="setPitch('체인지업')" style="background: #1d3557; color: white; border: 1px solid #00b4d8; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">🍂 체인지업 (Changeup)</button>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 700; margin-top: 6px; border-left: 5px solid #00b4d8; text-align: left;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 경기장에 불이 켜집니다!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');
            const myRole = "{role_str}"; 

            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 }};
            let ball = {{ active: false, x: 360, y: 140, z: 0, tx: 360, ty: 270, size: 2, speed: 98, name: "포심 직구" }};
            let selectedPitch = "포심 직구";
            let aiPitchTimer = 100;
            let isSwung = false;
            let swingFrame = 0;

            let fielders = [
                {{ pos: "유격수", x: 260, y: 120, ox: 260 }},
                {{ pos: "2루수", x: 460, y: 120, ox: 460 }},
                {{ pos: "3루수", x: 200, y: 170, ox: 200 }},
                {{ pos: "1루수", x: 520, y: 170, ox: 520 }},
                {{ pos: "좌익수", x: 140, y: 70, ox: 140 }},
                {{ pos: "중견수", x: 360, y: 50, ox: 360 }},
                {{ pos: "우익수", x: 580, y: 70, ox: 580 }}
            ];

            if (myRole === "pitcher") {{
                document.getElementById('pitcher-controls').style.display = 'block';
            }}

            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = "🎯 투수 구종 결정: " + type;
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left;
                let my = e.clientY - rect.top;

                if (myRole === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch;
                        ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 140; ball.z = 0; ball.size = 2;
                        ball.active = true; isSwung = false;
                    }}
                }} else {{
                    if (ball.active && !isSwung) {{
                        isSwung = true; swingFrame = 10;
                        evalBatterSwing();
                    }}
                }}
            }});

            function evalAiBatter() {{
                if (ball.active && !isSwung && ball.z >= 0.84 && ball.z <= 0.92) {{
                    isSwung = true;
                    let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 210 && ball.ty <= 310);
                    if (insideZone) {{
                        if (Math.random() > 0.5) {{ triggerDefenseAction(true); }}
                        else {{ game.s++; ball.active = false; nextPitchSequence(); }}
                    }} else {{
                        if (Math.random() > 0.7) {{ game.s++; ball.active = false; nextPitchSequence(); }}
                    }}
                }}
            }}

            function evalBatterSwing() {{
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 210 && ball.y <= 310);
                if (ball.z >= 0.83 && ball.z <= 0.94) {{
                    if (insideZone) {{
                        if (Math.random() > 0.8) {{ game.pScore++; ball.active = false; nextPitchSequence(); }}
                        else {{ triggerDefenseAction(false); }}
                    }} else {{
                        game.o++; ball.active = false; nextPitchSequence();
                    }}
                }} else {{
                    game.s++; ball.active = false; nextPitchSequence();
                }}
            }}

            function triggerDefenseAction(isAiHitter) {{
                let targetFielder = fielders[Math.floor(Math.random() * fielders.length)];
                targetFielder.x += (Math.random() > 0.5 ? 20 : -20);
                setTimeout(() => {{
                    if (Math.random() > 0.4) {{ game.o++; }}
                    else {{ if (isAiHitter) game.oppScore++; else game.pScore++; }}
                    ball.active = false; nextPitchSequence();
                }}, 300);
            }}

            function nextPitchSequence() {{
                aiPitchTimer = 110;
                fielders.forEach(f => f.x = f.ox);
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; }}
                if (game.b >= 4) {{ if (myRole === "pitcher") game.oppScore++; else game.pScore++; game.s = 0; game.b = 0; }}
                if (game.o >= 3) {{ game.o = 0; game.s = 0; game.b = 0; }}
                updateScreen();
            }}

            function updateScreen() {{
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 720, 380);
                ctx.fillStyle = "#8a5a36"; ctx.beginPath();
                ctx.moveTo(0, 380); ctx.lineTo(720, 380); ctx.lineTo(390, 130); ctx.lineTo(330, 130);
                ctx.closePath(); ctx.fill();

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2;
                ctx.strokeRect(300, 210, 120, 100);

                fielders.forEach(f => {{
                    ctx.fillStyle = "#1e6091"; ctx.fillRect(f.x - 6, f.y, 12, 10);
                    ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(f.x, f.y - 4, 4, 0, Math.PI*2); ctx.fill();
                }});

                ctx.fillStyle = "#d90429"; ctx.fillRect(353, 135, 14, 15);
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(360, 130, 5, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = "#ffffff"; ctx.fillRect(452, 260, 16, 22);
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(460, 254, 6, 0, Math.PI*2); ctx.fill();

                if (myRole === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let pool = ["포심 직구", "슬라이더", "체인지업"];
                        ball.name = pool[Math.floor(Math.random() * pool.length)];
                        ball.tx = 290 + Math.random() * 140; ball.ty = 200 + Math.random() * 110;
                        ball.x = 360; ball.y = 135; ball.z = 0; ball.size = 2;
                        ball.active = true; isSwung = false;
                    }}
                }}

                if (ball.active) {{
                    ball.z += 0.025;
                    ball.x = 360 + (ball.tx - 360) * ball.z;
                    ball.y = 140 + (ball.ty - 140) * ball.z;
                    ball.size = 2 + (Math.pow(ball.z, 3.8) * 32);

                    if (ball.name === "슬라이더") ball.x += Math.sin(ball.z * Math.PI) * 55;
                    if (ball.name === "체인지업") ball.y += Math.pow(ball.z, 2) * 35;

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (myRole === "pitcher") evalAiBatter();

                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 210 && ball.ty <= 310);
                        if (insideZone) game.s++; else game.b++;
                        nextPitchSequence();
                    }}
                }}

                if (swingFrame > 0) {{
                    ctx.save();
                    let ratio = (swingFrame / 10) * Math.PI;
                    ctx.translate(430, 260); ctx.rotate(-ratio + Math.PI/3);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7;
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-65, -15); ctx.stroke();
                    ctx.restore(); swingFrame--;
                }} else {{
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 4;
                    ctx.beginPath(); ctx.moveTo(455, 255); ctx.lineTo(440, 220); ctx.stroke();
                }}

                requestAnimationFrame(drawScene);
            }}

            updateScreen();
            drawScene();
        </script>
        """
        st.components.v1.html(game_html, height=520)

if __name__ == "__main__":
    main()
