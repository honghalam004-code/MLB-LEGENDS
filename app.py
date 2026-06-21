import streamlit as st

def main():
    st.set_page_config(page_title="MLB REAL TRAJECTORY", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox > div > div { background-color: #1c2541 !important; color: #ffffff !important; border: 2px solid #3a86ff !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 16px !important;
            border-radius: 8px !important; border: none !important; padding: 10px 20px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 750px; margin: 50px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB 리얼 변화구 물리 매치</h1>
                <p style="color: #94a3b8; margin-top: 10px; font-size: 16px;">구종별 리얼 구속 차이와 홈플레이트 앞 무빙 궤적 고증 버전</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 플레이어 구단 선택", ["Los Angeles Dodgers", "New York Yankees", "San Diego Padres"])
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단 선택", ["New York Yankees", "Los Angeles Dodgers", "San Francisco Giants"])
            
        if st.button("🏟️ 메이저리그 경기장 입장"):
            st.session_state.player_team_name = user_team
            st.session_state.ai_team_name = ai_team
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 🏟️ 라이브 경기: **{st.session_state.player_team_name}** VS **{st.session_state.ai_team_name}**")

    col_game_screen, col_tactics_panel = st.columns([3, 1])

    with col_tactics_panel:
        st.markdown("### 📊 덕아웃 전술 지시")
        st.success("🥎 **실제 변화구 초고증 완료**\n\n* **포심 직구:** 가장 빠른 구속으로 중앙을 찌릅니다.\n* **슬라이더:** 구속이 살짝 느려지며, 홈플레이트 앞에서 우타자 바깥쪽(오른쪽)으로 촥 휘어져 나갑니다.\n* **체인지업:** 구속이 뚝 떨어지며, 중력에 의해 밑으로 부드럽게 가라앉습니다.")
        st.markdown("---")
        if st.button("🚪 경기 포기 (로비 이동)"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.player_team_name
        team_a = st.session_state.ai_team_name

        game_html = f"""
        <div style="background: #0b1329; padding: 15px; border-radius: 14px; border: 2px solid #1c2541; max-width: 760px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 12px; margin-bottom: 10px; font-family: monospace; display: flex; justify-content: space-between; align-items: center; color: white;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span id="current-turn-badge" style="background: #3a86ff; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 14px;">1회초 공격 (타자)</span>
                    <span style="color: #4cc9f0; font-weight: 800; font-size: 16px;">{team_p}</span> 
                    <span id="score-p" style="font-size: 22px; font-weight: 900; color: #4cc9f0;">0</span> 
                    <span style="color: #64748b;">:</span> 
                    <span id="score-opp" style="font-size: 22px; font-weight: 900; color: #f72585;">0</span> 
                    <span style="color: #f72585; font-weight: 800; font-size: 16px;">{team_a}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span id="runner-diamond-text" style="color: #00b4d8; font-weight: bold; font-size: 14px;">📐 루상 상태: 주자 없음</span>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 16px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="420" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px;"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px; border: 1px solid #2e3d68;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px; border-bottom: 1px solid #2e3d68; padding-bottom: 8px;">
                    <span style="color: #f8fafc; font-weight: bold; margin-right: 10px; font-size: 14px;">⚾ 투수 구종 결정:</span>
                    <button onclick="setPitch('직구')" style="background: #d90429; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; margin-right: 6px;">포심 직구 (Fast)</button>
                    <button onclick="setPitch('슬라이더')" style="background: #023e8a; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; margin-right: 6px;">슬라이더 (무빙/구속 감소)</button>
                    <button onclick="setPitch('체인지업')" style="background: #f77f00; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px;">체인지업 (낙하/저구속)</button>
                </div>
                <div id="batter-controls" style="display: block;">
                    <span style="color: #f8fafc; font-weight: bold; margin-right: 10px; font-size: 14px;">🏏 타자 팀 전술 지시:</span>
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 7px 22px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px; margin-right: 10px;">📐 기습 번트 대기</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 7px 22px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px;">🏃 1루 주자 도루 감행!</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700; margin-top: 8px; border-left: 6px solid #3a86ff; text-align: left;">
                <span id="commentary" style="color: #90e0ef; line-height: 1.5;">🎙️ 중계석: 플레이어가 1회초 타석에 들어섭니다. 날아오는 변화구의 휘어짐을 끝까지 봐야 합니다!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0, hasRunner: false }};
            
            // 공 기본 속성 (speed 변수를 추가하여 구종별 프레임 증가량을 다르게 설정)
            let ball = {{ active: false, x: 360, y: 150, z: 0, tx: 360, ty: 320, size: 2, name: "직구", speed: 0.025 }};
            
            let selectedPitch = "직구";
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;
            let isBuntMode = false;

            let fielders = [
                {{ pos: "유격수", x: 260, y: 140 }},
                {{ pos: "2루수", x: 460, y: 140 }},
                {{ pos: "3루수", x: 220, y: 190 }},
                {{ pos: "1루수", x: 500, y: 190 }},
                {{ pos: "좌익수", x: 150, y: 80 }},
                {{ pos: "중견수", x: 360, y: 60 }},
                {{ pos: "우익수", x: 570, y: 80 }}
            ];

            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = "🎯 수비 지시: 투수가 [" + type + "] 사인을 받았습니다. 존 안을 클릭하면 투구합니다!";
            }}

            function triggerBunt() {{
                if (!ball.active || isSwung) return;
                isSwung = true; isBuntMode = true; swingFrame = 8;
                
                if (ball.z >= 0.82 && ball.z <= 0.96) {{
                    ball.active = false;
                    if (Math.random() > 0.45) {{
                        game.hasRunner = true; game.o++;
                        document.getElementById('commentary').innerHTML = "📐 번트 성공! 배트에 기가 막히게 맞추며 희생번트 성공!";
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 번트 타구가 포수 정면에 떨어지며 아웃당합니다!";
                    }}
                    checkInningStatus();
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerText = "🎙️ 헛번트 스트라이크! 공을 맞추지 못했습니다.";
                    ball.active = false; checkInningStatus();
                }}
            }}

            function triggerSteal() {{
                if (!game.hasRunner) {{
                    document.getElementById('commentary').innerText = "❌ 작전 실패: 루상에 주자가 없습니다.";
                    return;
                }}
                if (Math.random() > 0.5) {{
                    if (currentMode === "batter") game.pScore++; else game.oppScore++;
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "🏃 캐스터: 2루 도루 대성공!! 타이밍을 완전히 뺏었습니다!";
                }} else {{
                    game.o++; game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "☠️ 해설: 포수의 칼송구에 저격당하며 도루 실패 아웃!";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상 상태: 주자 1루" : "📐 루상 상태: 주자 없음";
                checkInningStatus();
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left;
                let my = e.clientY - rect.top;

                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch;
                        ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 150; ball.z = 0; ball.size = 2;
                        
                        // 궤적 고증: 구종별 구속 차등 적용
                        if (ball.name === "직구") ball.speed = 0.032;       // 제일 빠름
                        if (ball.name === "슬라이더") ball.speed = 0.022;   // 중간 변화구 구속
                        if (ball.name === "체인지업") ball.speed = 0.016;   // 느린 타이밍 뺏기 구속
                        
                        ball.active = true; isSwung = false; isBuntMode = false;
                    }}
                }} else {{
                    if (ball.active && !isSwung) {{
                        isSwung = true; isBuntMode = false; swingFrame = 10;
                        evalBatterSwing();
                    }}
                }}
            }});

            function evalAiBatter() {{
                if (ball.active && !isSwung && ball.z >= 0.85 && ball.z <= 0.93) {{
                    isSwung = true;
                    let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 240 && ball.y <= 340);
                    if (insideZone) {{
                        if (Math.random() > 0.48) evaluateHitTrajectory(true);
                        else {{ game.s++; ball.active = false; checkInningStatus(); }}
                    }} else {{
                        if (Math.random() > 0.75) {{ game.s++; ball.active = false; checkInningStatus(); }}
                    }}
                }}
            }}

            function evalBatterSwing() {{
                // 실제 휘어져 들어온 최종 물리 ball.x, ball.y 값 기준으로 판정
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 240 && ball.y <= 340);
                if (ball.z >= 0.84 && ball.z <= 0.95) {{
                    if (insideZone) {{
                        evaluateHitTrajectory(false);
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerText = "🎙️ 해설: 유인구 궤적에 방망이가 따라 나가며 헛스윙 아웃 처리됩니다.";
                        ball.active = false; checkInningStatus();
                    }}
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerText = "🎙️ 캐스터: 타이밍이 안 맞았습니다, 스트라이크!";
                    ball.active = false; checkInningStatus();
                }}
            }}

            function evaluateHitTrajectory(isAiHitter) {{
                ball.active = false;
                if (Math.random() > 0.42) {{
                    if (game.hasRunner) {{
                        if (isAiHitter) game.oppScore += 2; else game.pScore += 2;
                        game.hasRunner = false;
                        document.getElementById('commentary').innerHTML = "🔥 캐스터: 주자 주저 없이 홈인!! 완벽하게 가르는 적시 안타!";
                    }} else {{
                        game.hasRunner = true;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 깔끔한 안타로 주자 1루 베이스를 점령합니다!";
                    }}
                }} else {{
                    game.o++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 수비수 정면 플라이! 아웃입니다.";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상 상태: 주자 1루" : "📐 루상 상태: 주자 없음";
                checkInningStatus();
            }}

            function checkInningStatus() {{
                aiPitchTimer = 70;
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 배트가 허공을 갈랐습니다."; }}
                if (game.b >= 4) {{ 
                    if (currentMode === "pitcher") game.oppScore++; else game.pScore++; 
                    game.s = 0; game.b = 0; game.hasRunner = true;
                    document.getElementById('commentary').innerText = "🎙️ 볼넷! 베이스를 채워나갑니다."; 
                }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; game.hasRunner = false;
                    document.getElementById('runner-diamond-text').innerText = "📐 루상 상태: 주자 없음";
                    
                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비 (투수)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block';
                        document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 수비로 바뀝니다. 구종을 고르고 마우스를 조준해 공을 꽂으세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격 (타자)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 타석으로 다시 돌아옵니다!";
                    }}
                }}
                updateScreen();
            }}

            function updateScreen() {{
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 720, 400);

                ctx.fillStyle = "#2a9d8f"; ctx.fillRect(0, 0, 720, 400);
                ctx.fillStyle = "#e76f51"; ctx.beginPath();
                ctx.moveTo(0, 160); ctx.lineTo(720, 160); ctx.lineTo(720, 140); ctx.lineTo(0, 140);
                ctx.closePath(); ctx.fill();

                ctx.strokeStyle = "rgba(255, 255, 255, 0.5)"; ctx.lineWidth = 2.5;
                ctx.strokeRect(300, 240, 120, 100);

                ctx.fillStyle = "#d90429"; ctx.fillRect(355, 145, 10, 15);
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(360, 141, 4, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = "#ffffff"; ctx.fillRect(452, 260, 24, 46);
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(464, 248, 8, 0, Math.PI*2); ctx.fill();

                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.strokeRect(620, 30, 40, 40);
                ctx.fillStyle = game.hasRunner ? "#ffb703" : "#3d5a80"; ctx.fillRect(652, 46, 8, 8);

                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let pitchPool = ["직구", "슬라이더", "체인지업"];
                        ball.name = pitchPool[Math.floor(Math.random() * pitchPool.length)];
                        ball.tx = 310 + Math.random() * 100; ball.ty = 250 + Math.random() * 80;
                        ball.x = 360; ball.y = 150; ball.z = 0; ball.size = 2;
                        
                        if (ball.name === "직구") ball.speed = 0.032;
                        if (ball.name === "슬라이더") ball.speed = 0.022;
                        if (ball.name === "체인지업") ball.speed = 0.016;
                        
                        ball.active = true; isSwung = false;
                    }}
                }}

                // ⚾ 리얼 물리 변화구 시뮬레이션 시스템
                if (ball.active) {{
                    ball.z += ball.speed; // 구종 고유 속도 반영
                    
                    // 직선 기본 베이스 원근 궤적 계산
                    let baseX = 360 + (ball.tx - 360) * ball.z;
                    let baseY = 150 + (ball.ty - 150) * ball.z;

                    // 진짜 야구공처럼 휘어지는 무빙 로직 (포수 시점 고증)
                    if (ball.name === "슬라이더") {{
                        // 처음엔 직선 같다가 홈플레이트 근처(z가 클 때)에서 우타석 바깥(오른쪽)으로 촥 휘어나감
                        let slideEffect = Math.pow(ball.z, 2.5) * 75; 
                        ball.x = baseX + slideEffect;
                        ball.y = baseY;
                    }} else if (ball.name === "체인지업") {{
                        // 가다가 속도가 죽으면서 중력 효과로 밑으로 툭 가라앉는 종무빙
                        let dropEffect = Math.pow(ball.z, 3.0) * 55;
                        ball.x = baseX;
                        ball.y = baseY + dropEffect;
                    }} else {{
                        // 포심 직구는 변화 없이 칼날같이 정면 돌진
                        ball.x = baseX;
                        ball.y = baseY;
                    }}

                    ball.size = 2.5 + (Math.pow(ball.z, 3.6) * 28);

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher") evalAiBatter();

                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 240 && ball.y <= 340);
                        if (insideZone) game.s++; else game.b++;
                        checkInningStatus();
                    }}
                }}

                if (swingFrame > 0) {{
                    ctx.save();
                    if (isBuntMode) {{
                        ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7;
                        ctx.beginPath(); ctx.moveTo(430, 280); ctx.lineTo(335, 280); ctx.stroke();
                    }} else {{
                        let angleRatio = (swingFrame / 10) * Math.PI;
                        ctx.translate(440, 260); ctx.rotate(-angleRatio + Math.PI / 4);
                        ctx.strokeStyle = "#b79457"; ctx.lineWidth = 8;
                        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-76, -10); ctx.stroke();
                    }}
                    ctx.restore(); swingFrame--;
                }} else {{
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 5;
                    ctx.beginPath(); ctx.moveTo(466, 238); ctx.lineTo(488, 192); ctx.stroke();
                }}

                requestAnimationFrame(drawScene);
            }}

            updateScreen();
            drawScene();
        </script>
        """
        st.components.v1.html(game_html, height=580)

if __name__ == "__main__":
    main()
