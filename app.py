import streamlit as st

def main():
    st.set_page_config(page_title="MLB PRO ULTIMATE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox > div > div { background-color: #1c2541 !important; color: #ffffff !important; border: 2px solid #3a86ff !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 16px !important;
            border-radius: 8px !important; border: none !important; padding: 12px 20px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    mlb_teams = ["Pittsburgh Pirates", "New York Yankees", "Los Angeles Dodgers", "San Diego Padres", "Boston Red Sox"]

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB FULL SPEC SIMULATOR</h1>
                <p style="color: #4cc9f0; margin-top: 10px; font-size: 16px;">정통 야구 룰 완벽 적용 & 최적의 타격 밸런스</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 플레이어 구단 선택", mlb_teams, index=0)
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단 선택", mlb_teams, index=1)
            
        if st.button("🏟️ 경기 시작"):
            st.session_state.player_team_name = user_team
            st.session_state.ai_team_name = ai_team
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_game_screen, col_tactics_panel = st.columns([3.2, 1])

    with col_tactics_panel:
        st.markdown("### 📊 매니저 패널")
        st.info("💡 **조작 안내**\n\n타석을 클릭해 스윙하세요. 정타를 맞춰도 수비수에게 잡힐 수 있습니다. 단타/홈런/볼넷 등 야구 룰이 정상 적용됩니다.")
        if st.button("🚪 로비로 돌아가기"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.player_team_name
        team_a = st.session_state.ai_team_name

        # HTML 구조 (f-string 사용: 파이썬 변수 삽입)
        html_part = f"""
        <div id="game-container" style="background: #0b1329; padding: 15px; border-radius: 14px; border: 2px solid #1c2541; max-width: 760px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; color: white;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span id="current-turn-badge" style="background: #3a86ff; padding: 4px 8px; border-radius: 4px; font-weight: bold;">1회초 공격</span>
                    <span style="color: #4cc9f0; font-weight: 800;">{team_p}</span> 
                    <span id="score-p" style="font-size: 24px; font-weight: 900; color: #4cc9f0;">0</span> 
                    <span style="color: #64748b;">:</span> 
                    <span id="score-opp" style="font-size: 24px; font-weight: 900; color: #f72585;">0</span> 
                    <span style="color: #f72585; font-weight: 800;">{team_a}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 16px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="440" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px; cursor: crosshair;"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px;">
                    <button onclick="setPitch('직구')" style="background: #d90429; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">포심 직구</button>
                    <button onclick="setPitch('체인지업')" style="background: #f77f00; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">체인지업</button>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 10px;">📐 기습 번트</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer;">🏃 단독 도루</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-weight: bold; margin-top: 8px; border-left: 6px solid #3a86ff;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 해설위원: 경기 시작됩니다! 플레이볼! 타석을 클릭해 스윙하세요.</span>
            </div>
        </div>
        """

        # Javascript 구조 (일반 문자열 사용: 중괄호 에러 방지)
        js_part = """
        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = { pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 };
            let bases = [false, false, false]; 

            let ball = { active: false, x: 360, y: 220, z: 0, tx: 360, ty: 320, size: 2, name: "직구", speed: 0.025 };
            let selectedPitch = "직구";
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;

            let fielders = [
                { pos: "1B", x: 490, y: 240 }, { pos: "2B", x: 410, y: 170 }, { pos: "SS", x: 310, y: 170 },
                { pos: "3B", x: 230, y: 240 }, { pos: "LF", x: 170, y: 110 }, { pos: "CF", x: 360, y: 90 }, { pos: "RF", x: 550, y: 110 }
            ];

            function addScore(points) {
                if (currentMode === "batter") game.pScore += points;
                else game.oppScore += points;
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
            }

            function advanceRunners(hitType) {
                if (hitType === "walk") {
                    if (bases[0] && bases[1] && bases[2]) { addScore(1); document.getElementById('commentary').innerText += " 밀어내기 1득점!"; }
                    else if (bases[0] && bases[1]) { bases[2] = true; }
                    else if (bases[0]) { bases[1] = true; }
                    bases[0] = true;
                } 
                else if (hitType === "single") {
                    if (bases[2]) { addScore(1); bases[2] = false; } 
                    if (bases[1]) { bases[2] = true; bases[1] = false; } 
                    if (bases[0]) { bases[1] = true; bases[0] = false; } 
                    bases[0] = true; 
                }
                else if (hitType === "homerun") {
                    let runs = 1; 
                    if (bases[0]) runs++; if (bases[1]) runs++; if (bases[2]) runs++;
                    addScore(runs);
                    bases = [false, false, false]; 
                }
            }

            function setPitch(type) {
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = `🎯 [${type}] 구종 선택. 존 안을 클릭해 투구하세요!`;
            }

            function triggerBunt() {
                if (!ball.active || isSwung) return;
                isSwung = true; swingFrame = 8;
                if (ball.z >= 0.78 && ball.z <= 0.96) {
                    ball.active = false;
                    if (Math.random() > 0.6) {
                        advanceRunners("single");
                        document.getElementById('commentary').innerHTML = `📐 절묘한 기습 번트 성공! 1루에 안착합니다!`;
                    } else { game.o++; document.getElementById('commentary').innerHTML = "🎙️ 번트 뜬공 아웃! 투수가 바로 잡아냅니다."; }
                    checkInningStatus();
                } else { game.s++; ball.active = false; document.getElementById('commentary').innerHTML = "🎙️ 번트 헛스윙!"; checkInningStatus(); }
            }

            function triggerSteal() {
                if (!bases[0] && !bases[1]) {
                    document.getElementById('commentary').innerHTML = "⚠️ 뛸 수 있는 주자가 없습니다!"; return;
                }
                if (Math.random() > 0.55) {
                    if (bases[1] && !bases[2]) { bases[2] = true; bases[1] = false; document.getElementById('commentary').innerHTML = "🏃 3루 도루 성공!"; }
                    else if (bases[0] && !bases[1]) { bases[1] = true; bases[0] = false; document.getElementById('commentary').innerHTML = "🏃 2루 도루 성공!"; }
                } else {
                    game.o++; document.getElementById('commentary').innerHTML = "☠️ 도루 실패! 포수의 강견에 걸렸습니다!";
                    if (bases[1] && !bases[2]) bases[1] = false;
                    else if (bases[0] && !bases[1]) bases[0] = false;
                }
                checkInningStatus();
            }

            canvas.addEventListener('mousedown', (e) => {
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left; let my = e.clientY - rect.top;

                if (currentMode === "pitcher") {
                    if (!ball.active) {
                        ball.name = selectedPitch; ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        ball.speed = ball.name === "직구" ? 0.035 : 0.020;
                        ball.active = true; isSwung = false;
                    }
                } else {
                    if (ball.active && !isSwung) { isSwung = true; swingFrame = 10; evalBatterSwing(); }
                }
            });

            function evalAiBatter() {
                if (ball.active && !isSwung && ball.z >= 0.82 && ball.z <= 0.94) {
                    let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 250 && ball.y <= 360);
                    if (insideZone && Math.random() > 0.45) { isSwung = true; evaluateHitTrajectory(true); }
                }
            }

            function evalBatterSwing() {
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 250 && ball.y <= 360);
                if (ball.z >= 0.78 && ball.z <= 0.96) {
                    if (insideZone) {
                        evaluateHitTrajectory(false);
                    } else {
                        game.s++; ball.active = false; document.getElementById('commentary').innerText = "🎙️ 유인구에 속았습니다! 헛스윙!"; checkInningStatus();
                    }
                } else {
                    game.s++; ball.active = false; document.getElementById('commentary').innerText = "🎙️ 타이밍이 맞지 않았습니다. 헛스윙!"; checkInningStatus();
                }
            }

            function evaluateHitTrajectory(isAiHitter) {
                ball.active = false;
                let hitRoll = Math.random();
                if (hitRoll > 0.85) {
                    advanceRunners("homerun");
                    document.getElementById('commentary').innerHTML = `🔥 쾅!! 맞는 순간 넘어갔습니다! 대형 홈런!!`;
                } else if (hitRoll > 0.40) {
                    advanceRunners("single");
                    document.getElementById('commentary').innerHTML = `🎙️ 깨끗한 타구! 빈 공간을 가르는 안타입니다.`;
                } else {
                    game.o++; document.getElementById('commentary').innerHTML = "🎙️ 아, 빗맞았습니다. 야수 정면으로 가는 아웃입니다.";
                }
                checkInningStatus();
            }

            function checkInningStatus() {
                aiPitchTimer = 70;
                if (game.s >= 3) { game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 배트가 허공을 가릅니다."; }
                if (game.b >= 4) { 
                    game.s = 0; game.b = 0;
                    document.getElementById('commentary').innerText = "🎙️ 볼넷! 타자가 1루로 걸어 나갑니다."; 
                    advanceRunners("walk");
                }
                
                if (game.o >= 3) {
                    game.o = 0; game.s = 0; game.b = 0; 
                    bases = [false, false, false]; 
                    
                    if (currentMode === "batter") {
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block';
                        document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대!</b> 마운드에 오릅니다. 구종을 선택하고 투구하세요!";
                    } else {
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대!</b> 다시 타석에 섭니다.";
                    }
                }
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }

            function drawScene() {
                ctx.clearRect(0, 0, 720, 440);

                ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 440);
                
                ctx.fillStyle = "#a66a38"; ctx.beginPath();
                ctx.moveTo(0, 440); ctx.lineTo(720, 440); ctx.lineTo(550, 190); ctx.lineTo(170, 190); ctx.closePath(); ctx.fill();

                ctx.fillStyle = "#2a9d8f"; ctx.beginPath();
                ctx.moveTo(360, 380); ctx.lineTo(480, 260); ctx.lineTo(360, 140); ctx.lineTo(240, 260); ctx.closePath(); ctx.fill();

                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.arc(360, 220, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.fillRect(350, 218, 20, 4);

                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(370, 370); ctx.lineTo(350, 370); ctx.closePath(); ctx.fill(); 
                ctx.fillRect(475, 255, 12, 12); ctx.fillRect(354, 134, 12, 12); ctx.fillRect(235, 255, 12, 12); 

                ctx.fillStyle = "#ffb703"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 2;
                if (bases[0]) { ctx.beginPath(); ctx.arc(481, 261, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }
                if (bases[1]) { ctx.beginPath(); ctx.arc(360, 140, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }
                if (bases[2]) { ctx.beginPath(); ctx.arc(241, 261, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }

                ctx.fillStyle = "#d90429"; ctx.fillRect(352, 200, 16, 20); 

                fielders.forEach(f => {
                    ctx.fillStyle = "#023e8a"; ctx.fillRect(f.x - 8, f.y - 10, 16, 12);
                    ctx.fillStyle = "rgba(255,255,255,0.8)"; ctx.font = "11px Arial"; ctx.fillText(f.pos, f.x - 7, f.y + 14);
                });

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5; ctx.strokeRect(310, 260, 100, 90);
                
                ctx.fillStyle = "#ffffff"; ctx.fillRect(390, 330, 20, 40);

                ctx.fillStyle = "rgba(2, 12, 27, 0.7)"; ctx.fillRect(615, 25, 50, 50);
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.strokeRect(620, 30, 40, 40);
                if (bases[0]) { ctx.fillStyle = "#ffb703"; ctx.fillRect(652, 46, 8, 8); } 
                if (bases[1]) { ctx.fillStyle = "#ffb703"; ctx.fillRect(636, 30, 8, 8); } 
                if (bases[2]) { ctx.fillStyle = "#ffb703"; ctx.fillRect(620, 46, 8, 8); } 

                if (currentMode === "batter" && !ball.active) {
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {
                        ball.name = Math.random() > 0.5 ? "직구" : "체인지업";
                        ball.tx = 290 + Math.random() * 140; ball.ty = 240 + Math.random() * 120;
                        ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        ball.speed = ball.name === "직구" ? 0.035 : 0.020;
                        ball.active = true; isSwung = false;
                    }
                }

                if (ball.active) {
                    ball.z += ball.speed; 
                    ball.x = 360 + (ball.tx - 360) * ball.z;
                    ball.y = 220 + (ball.ty - 220) * ball.z;
                    ball.size = 2.5 + (Math.pow(ball.z, 3.2) * 20);

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher") evalAiBatter();

                    if (ball.z >= 1.0) {
                        ball.active = false;
                        let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 250 && ball.y <= 360);
                        if (insideZone) game.s++; else game.b++;
                        checkInningStatus();
                    }
                }

                if (swingFrame > 0) {
                    ctx.save();
                    let angleRatio = (swingFrame / 10) * Math.PI;
                    ctx.translate(400, 350); ctx.rotate(-angleRatio + Math.PI / 3);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 8;
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-80, -20); ctx.stroke();
                    ctx.restore(); swingFrame--;
                } else {
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(395, 340); ctx.lineTo(430, 270); ctx.stroke();
                }

                requestAnimationFrame(drawScene);
            }

            drawScene();
        </script>
        """

        # HTML과 JS를 합치고, 컴포넌트 높이를 800으로 넉넉하게 지정!
        full_html = html_part + js_part
        st.components.v1.html(full_html, height=800)

if __name__ == "__main__":
    main()
