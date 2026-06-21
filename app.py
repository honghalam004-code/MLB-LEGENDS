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

    mlb_teams = [
        "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", 
        "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians", 
        "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals", 
        "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", 
        "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics", 
        "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants", 
        "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", 
        "Toronto Blue Jays", "Washington Nationals"
    ]

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB FULL SPEC SIMULATOR</h1>
                <p style="color: #4cc9f0; margin-top: 10px; font-size: 16px;">30개 구단 / 수비수 렌더링 / 대타 / 스피드·파워 고증 완벽 적용</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 플레이어 구단 선택", mlb_teams, index=21) # Pittsburgh
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단 선택", mlb_teams, index=18) # Yankees
            
        if st.button("🏟️ 메이저리그 베이스볼 경기장 입장"):
            st.session_state.player_team_name = user_team
            st.session_state.ai_team_name = ai_team
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 🏟️ LIVE GAME: **{st.session_state.player_team_name}** vs **{st.session_state.ai_team_name}**")

    col_game_screen, col_tactics_panel = st.columns([3.2, 1])

    with col_tactics_panel:
        st.markdown("### 📊 전술 및 데이터 매니저")
        st.info("💡 **리얼 스피드 & 대타 로직**\n\n* **파워 대타:** 안타/홈런 확률이 올라가지만, 발이 느려 도루 시 불리합니다.\n* **기교파 투수:** 구속은 느려지지만 슬라이더와 체인지업의 꺾이는 각도가 극대화됩니다.")
        st.markdown("---")
        if st.button("🚪 경기 종료 (로비 이동)"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.player_team_name
        team_a = st.session_state.ai_team_name

        game_html = f"""
        <div id="game-container-v2" style="background: #0b1329; padding: 15px; border-radius: 14px; border: 2px solid #1c2541; max-width: 760px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 12px; margin-bottom: 10px; font-family: monospace; display: flex; justify-content: space-between; align-items: center; color: white;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span id="current-turn-badge" style="background: #3a86ff; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 14px;">1회초 공격 (타자)</span>
                    <span style="color: #4cc9f0; font-weight: 800; font-size: 16px;">{team_p}</span> 
                    <span id="score-p" style="font-size: 24px; font-weight: 900; color: #4cc9f0;">0</span> 
                    <span style="color: #64748b;">:</span> 
                    <span id="score-opp" style="font-size: 24px; font-weight: 900; color: #f72585;">0</span> 
                    <span style="color: #f72585; font-weight: 800; font-size: 16px;">{team_a}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span id="runner-diamond-text" style="color: #00b4d8; font-weight: bold; font-size: 14px;">📐 루상: 주자 없음</span>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 16px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="440" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px;"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px; border: 1px solid #2e3d68;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px; border-bottom: 1px solid #2e3d68; padding-bottom: 8px;">
                    <div style="margin-bottom: 8px;">
                        <span style="color: #f8fafc; font-weight: bold; font-size: 14px;">⚾ 마운드 투수 교체: </span>
                        <select id="pitcher-select" onchange="changePitcher()" style="background:#023e8a; color:white; border-radius:4px; padding:4px; font-weight:bold;">
                            <option value="ace">강속구 에이스 (구속 강화형)</option>
                            <option value="control">기교파 셋업맨 (변화구 브레이크형)</option>
                        </select>
                    </div>
                    <button onclick="setPitch('직구')" style="background: #d90429; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; margin-right: 5px;">포심 직구</button>
                    <button onclick="setPitch('슬라이더')" style="background: #023e8a; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; margin-right: 5px;">슬라이더</button>
                    <button onclick="setPitch('체인지업')" style="background: #f77f00; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px;">체인지업</button>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <div style="margin-bottom: 8px;">
                        <span style="color: #f8fafc; font-weight: bold; font-size: 14px;">🏏 현재 타석: </span>
                        <span id="current-batter-info" style="color: #4cc9f0; font-weight: bold; margin-right: 15px;">선발 1번 타자 (스피드형)</span>
                        <button onclick="callPinchHitter()" style="background: #e63946; color: white; border: none; padding: 5px 12px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 12px;">🔄 대타 작전 투입 (파워형 거포)</button>
                    </div>
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px; margin-right: 10px;">📐 기습 번트</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px;">🏃 기습 도루 감행</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700; margin-top: 8px; border-left: 6px solid #3a86ff; text-align: left;">
                <span id="commentary" style="color: #90e0ef; line-height: 1.5;">🎙️ 해설위원: 야구장 그래픽이 마침내 정상적인 비율로 재정비되었습니다! 플레이어 팀의 공격입니다.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0, hasRunner: false }};
            
            // 공의 시작점 마운드(360, 220) 수정
            let ball = {{ active: false, x: 360, y: 220, z: 0, tx: 360, ty: 320, size: 2, name: "직구", speed: 0.025 }};
            
            let selectedPitch = "직구";
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;
            let isBuntMode = false;

            let currentPitcher = {{ type: "ace", veloMod: 1.25, breakMod: 0.85, name: "강속구 선발 에이스" }};
            let currentBatter = {{ type: "speed", power: 0.75, speed: 1.45, name: "1번 타자" }};

            // 수정된 다이아몬드 비율에 맞춘 7명 수비수 좌표 재설정
            let fielders = [
                {{ pos: "1B", x: 490, y: 240 }},
                {{ pos: "2B", x: 410, y: 170 }},
                {{ pos: "SS", x: 310, y: 170 }},
                {{ pos: "3B", x: 230, y: 240 }},
                {{ pos: "LF", x: 170, y: 110 }},
                {{ pos: "CF", x: 360, y: 90 }},
                {{ pos: "RF", x: 550, y: 110 }}
            ];

            function changePitcher() {{
                let val = document.getElementById('pitcher-select').value;
                if (val === "ace") {{
                    currentPitcher = {{ type: "ace", veloMod: 1.25, breakMod: 0.85, name: "강속구 선발 에이스" }};
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 강속구를 뿌리는 1선발 에이스가 등판합니다!";
                }} else {{
                    currentPitcher = {{ type: "control", veloMod: 0.82, breakMod: 1.5, name: "기교파 변화구 스페셜리스트" }};
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 제구력과 낙차 큰 무빙을 구사하는 기교파 투수입니다!";
                }}
            }}

            function callPinchHitter() {{
                currentBatter = {{ type: "power", power: 1.6, speed: 0.55, name: "해결사 대타" }};
                document.getElementById('current-batter-info').innerText = "대타 (파워형 거포)";
                document.getElementById('commentary').innerHTML = "🚨 중계석: 승부처입니다! 장타율이 엄청난 대타 카드를 꺼냅니다!";
            }}

            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = `🎯 ${{currentPitcher.name}}가 [${{type}}] 사인을 확인했습니다. 존 안을 클릭하세요!`;
            }}

            function triggerBunt() {{
                if (!ball.active || isSwung) return;
                isSwung = true; isBuntMode = true; swingFrame = 8;
                
                if (ball.z >= 0.82 && ball.z <= 0.96) {{
                    ball.active = false;
                    let buntRoll = Math.random() * currentBatter.speed;
                    if (buntRoll > 0.5) {{
                        game.hasRunner = true; game.o++;
                        document.getElementById('commentary').innerHTML = `📐 번트 성공! ${{currentBatter.name}}의 스피드가 내야안타를 만들어냅니다!`;
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 해설: 타구 속도가 빠릅니다. 포수 정면 아웃입니다.";
                    }}
                    checkInningStatus();
                }} else {{
                    game.s++; ball.active = false; checkInningStatus();
                    document.getElementById('commentary').innerHTML = "🎙️ 스트라이크! 번트 타이밍이 완전히 빗나갔습니다.";
                }}
            }}

            function triggerSteal() {{
                if (!game.hasRunner) return;
                let stealRoll = Math.random() * currentBatter.speed;
                if (stealRoll > 0.65) {{
                    if (currentMode === "batter") game.pScore++; else game.oppScore++;
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = `🏃 도루 대성공! ${{currentBatter.name}}의 스피드로 베이스를 훔쳐냅니다!`;
                }} else {{
                    game.o++; game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "☠️ 캐스터: 아웃! 포수가 주자를 완벽하게 저격했습니다!";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상: 주자 1루" : "📐 루상: 주자 없음";
                checkInningStatus();
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left;
                let my = e.clientY - rect.top;

                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch;
                        ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        
                        if (ball.name === "직구") ball.speed = 0.032 * currentPitcher.veloMod;       
                        if (ball.name === "슬라이더") ball.speed = 0.022 * currentPitcher.veloMod;   
                        if (ball.name === "체인지업") ball.speed = 0.016 * currentPitcher.veloMod;   
                        
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
                    let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                    if (insideZone) {{
                        if (Math.random() > 0.48) evaluateHitTrajectory(true);
                        else {{ game.s++; ball.active = false; checkInningStatus(); }}
                    }} else {{
                        if (Math.random() > 0.75) {{ game.s++; ball.active = false; checkInningStatus(); }}
                    }}
                }}
            }}

            function evalBatterSwing() {{
                let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                if (ball.z >= 0.84 && ball.z <= 0.95) {{
                    if (insideZone) {{
                        evaluateHitTrajectory(false);
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerText = "🎙️ 해설: 유인구 무빙에 방망이가 속았습니다. 삼진 아웃!";
                        ball.active = false; checkInningStatus();
                    }}
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerText = "🎙️ 캐스터: 변화구 타이밍을 맞추지 못했습니다, 스트라이크!";
                    ball.active = false; checkInningStatus();
                }}
            }}

            function evaluateHitTrajectory(isAiHitter) {{
                ball.active = false;
                let hitRoll = Math.random() * (isAiHitter ? 1.0 : currentBatter.power);
                
                if (hitRoll > 0.52) {{
                    if (game.hasRunner) {{
                        if (isAiHitter) game.oppScore += 2; else game.pScore += 2;
                        game.hasRunner = false;
                        document.getElementById('commentary').innerHTML = `🔥 홈런성 타구!! 완벽한 임팩트로 싹쓸이 적시 2루타를 만듭니다!`;
                    }} else {{
                        game.hasRunner = true;
                        document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 안타입니다! 강한 파워로 수비수를 넘기는 안타!`;
                    }}
                }} else {{
                    game.o++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 야수들이 낙구 지점을 포착하며 플라이 아웃 처리합니다.";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상: 주자 1루" : "📐 루상: 주자 없음";
                checkInningStatus();
            }}

            function checkInningStatus() {{
                aiPitchTimer = 70;
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 결정구에 허공을 가릅니다."; }}
                if (game.b >= 4) {{ 
                    if (currentMode === "pitcher") game.oppScore++; else game.pScore++; 
                    game.s = 0; game.b = 0; game.hasRunner = true;
                    document.getElementById('commentary').innerText = "🎙️ 볼넷 출루! 제구가 많이 흔들립니다."; 
                }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; game.hasRunner = false;
                    document.getElementById('runner-diamond-text').innerText = "📐 루상: 주자 없음";
                    
                    currentBatter = {{ type: "speed", power: 0.75, speed: 1.45, name: "1번 타자" }};
                    document.getElementById('current-batter-info').innerText = "선발 1번 타자 (스피드형)";

                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비 (투수)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block';
                        document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대!</b> 수비에 나섭니다. 투수를 점검하고 구종을 선택하세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격 (타자)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대!</b> 다시 공격입니다. 집중력을 올려 타격하세요!";
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
                ctx.clearRect(0, 0, 720, 440);

                // 1. 외야 천연 잔디
                ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 440);
                
                // 2. 내야 흙바닥 (원근감 사다리꼴 수정)
                ctx.fillStyle = "#a66a38";
                ctx.beginPath();
                ctx.moveTo(0, 440); ctx.lineTo(720, 440);
                ctx.lineTo(550, 190); ctx.lineTo(170, 190);
                ctx.closePath(); ctx.fill();

                // 3. 내야 잔디 다이아몬드 (비율 정상화)
                ctx.fillStyle = "#2a9d8f";
                ctx.beginPath();
                ctx.moveTo(360, 380); // 홈
                ctx.lineTo(480, 260); // 1루
                ctx.lineTo(360, 140); // 2루
                ctx.lineTo(240, 260); // 3루
                ctx.closePath(); ctx.fill();

                // 4. 마운드 및 투수판 (2루와 분리)
                ctx.fillStyle = "#a66a38";
                ctx.beginPath(); ctx.arc(360, 220, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.fillRect(350, 218, 20, 4);

                // 5. 홈플레이트
                ctx.fillStyle = "#ffffff";
                ctx.beginPath();
                ctx.moveTo(360, 380); ctx.lineTo(370, 370); ctx.lineTo(370, 365);
                ctx.lineTo(350, 365); ctx.lineTo(350, 370); ctx.closePath(); ctx.fill();

                // 6. 투수 및 수비수 7명 렌더링
                ctx.fillStyle = "#d90429"; ctx.fillRect(352, 200, 16, 20); // 마운드 투수
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(360, 194, 6, 0, Math.PI*2); ctx.fill();

                fielders.forEach(f => {{
                    ctx.fillStyle = "#023e8a"; ctx.fillRect(f.x - 8, f.y - 10, 16, 12);
                    ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(f.x, f.y - 14, 5, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#03045e"; ctx.beginPath(); ctx.arc(f.x, f.y - 16, 5, Math.PI, 0); ctx.fill();
                    ctx.fillStyle = "rgba(255,255,255,0.8)"; ctx.font = "11px Arial"; ctx.fillText(f.pos, f.x - 7, f.y + 14);
                }});

                // 7. 타석 및 스트라이크 존 (타자를 홈으로 복귀)
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5;
                ctx.strokeRect(310, 260, 100, 90);

                ctx.fillStyle = "#ffffff"; ctx.fillRect(390, 330, 20, 40); // 타자 몸통
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(400, 320, 10, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#03045e"; ctx.beginPath(); ctx.arc(400, 318, 10, Math.PI, 0); ctx.fill(); 

                // 미니맵 루상 표시기
                ctx.fillStyle = "rgba(2, 12, 27, 0.7)"; ctx.fillRect(615, 25, 50, 50);
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.strokeRect(620, 30, 40, 40);
                ctx.fillStyle = game.hasRunner ? "#ffb703" : "#3d5a80"; ctx.fillRect(652, 46, 8, 8);

                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let pitchPool = ["직구", "슬라이더", "체인지업"];
                        ball.name = pitchPool[Math.floor(Math.random() * pitchPool.length)];
                        ball.tx = 310 + Math.random() * 100; ball.ty = 260 + Math.random() * 90;
                        ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        
                        if (ball.name === "직구") ball.speed = 0.032;
                        if (ball.name === "슬라이더") ball.speed = 0.022;
                        if (ball.name === "체인지업") ball.speed = 0.016;
                        
                        ball.active = true; isSwung = false;
                    }}
                }}

                if (ball.active) {{
                    ball.z += ball.speed; 
                    
                    let baseX = 360 + (ball.tx - 360) * ball.z;
                    let baseY = 220 + (ball.ty - 220) * ball.z;

                    if (ball.name === "슬라이더") {{
                        let slideEffect = Math.pow(ball.z, 2.5) * (70 * (currentMode === "pitcher" ? currentPitcher.breakMod : 1.0)); 
                        ball.x = baseX + slideEffect;
                        ball.y = baseY;
                    }} else if (ball.name === "체인지업") {{
                        let dropEffect = Math.pow(ball.z, 3.0) * (50 * (currentMode === "pitcher" ? currentPitcher.breakMod : 1.0));
                        ball.x = baseX;
                        ball.y = baseY + dropEffect;
                    }} else {{
                        ball.x = baseX;
                        ball.y = baseY;
                    }}

                    ball.size = 2.5 + (Math.pow(ball.z, 3.2) * 20);

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher") evalAiBatter();

                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                        if (insideZone) game.s++; else game.b++;
                        checkInningStatus();
                    }}
                }}

                if (swingFrame > 0) {{
                    ctx.save();
                    if (isBuntMode) {{
                        ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7;
                        ctx.beginPath(); ctx.moveTo(390, 340); ctx.lineTo(310, 340); ctx.stroke();
                    }} else {{
                        let angleRatio = (swingFrame / 10) * Math.PI;
                        ctx.translate(400, 350); ctx.rotate(-angleRatio + Math.PI / 3);
                        ctx.strokeStyle = "#b79457"; ctx.lineWidth = 8;
                        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-80, -20); ctx.stroke();
                    }}
                    ctx.restore(); swingFrame--;
                }} else {{
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(395, 340); ctx.lineTo(430, 270); ctx.stroke();
                }}

                requestAnimationFrame(drawScene);
            }}

            updateScreen();
            drawScene();
        </script>
        """
        st.components.v1.html(game_html, height=620)

if __name__ == "__main__":
    main()
