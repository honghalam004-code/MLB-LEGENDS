import streamlit as st

def main():
    st.set_page_config(page_title="MLB PRO ULTIMATE", layout="wide")
    
    # [1] 스타일 가이드 테마 적용
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

    # MLB 정식 30개 구단 리스터 풀 전개
    mlb_teams = [
        "Arizona Diamondbacks (애리조나)", "Atlanta Braves (애틀랜타)", "Baltimore Orioles (볼티모어)",
        "Boston Red Sox (보스턴)", "Chicago Cubs (시카고 컵스)", "Chicago White Sox (화이트삭스)",
        "Cincinnati Reds (신시내티)", "Cleveland Guardians (클리블랜드)", "Colorado Rockies (콜로라도)",
        "Detroit Tigers (디트로이트)", "Houston Astros (휴스턴)", "Kansas City Royals (캔자스시티)",
        "Los Angeles Angels (LA 에인절스)", "Los Angeles Dodgers (LA 다저스)", "Miami Marlins (마이애미)",
        "Milwaukee Brewers (밀워키)", "Minnesota Twins (미네소타)", "New York Mets (뉴욕 메츠)",
        "New York Yankees (뉴욕 양키스)", "Oakland Athletics (오클랜드)", "Philadelphia Phillies (필라델피아)",
        "Pittsburgh Pirates (피츠버그)", "San Diego Padres (샌디에이고)", "San Francisco Giants (샌프란시스코)",
        "Seattle Mariners (시애틀)", "St. Louis Cardinals (세인트루이스)", "Tampa Bay Rays (탬파베이)",
        "Texas Rangers (텍사스)", "Toronto Blue Jays (토론토)", "Washington Nationals (워싱턴)"
    ]

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB FULL SPEC SIMULATOR</h1>
                <p style="color: #4cc9f0; margin-top: 10px; font-size: 16px;">30개 구단 / 투수 선택 / 대타 시스템 / 스피드·파워 가속도 완벽 고증</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 플레이어 구단 선택", mlb_teams, index=13) 
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단 선택", mlb_teams, index=18) 
            
        if st.button("🏟️ 메이저리그 베이스볼 경기장 입장"):
            st.session_state.player_team_name = user_team.split(" (")[0]
            st.session_state.ai_team_name = ai_team.split(" (")[0]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 🏟️ LIVE GAME: **{st.session_state.player_team_name}** vs **{st.session_state.ai_team_name}**")

    col_game_screen, col_tactics_panel = st.columns([3.1, 1])

    with col_tactics_panel:
        st.markdown("### 📊 전술 및 데이터 매니저")
        st.info("💡 **리얼 스피드 & 대타 로직**\n\n* **대타 기용 시:** 주자가 있을 때 안타/홈런 확률이 올라가지만, 발이 느려 번트나 도루 시 불리해집니다.\n* **기교파 투수:** 구속은 느려지지만 슬라이더와 체인지업의 꺾이는 각도가 극대화됩니다.")
        st.markdown("---")
        if st.button("🚪 경기 종료 (로비 이동)"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.player_team_name
        team_a = st.session_state.ai_team_name

        # [2] 인게임 종합 그래픽 및 자바스크립트 엔진 스크립트 작성
        game_html = f"""
        <div style="background: #0b1329; padding: 15px; border-radius: 14px; border: 2px solid #1c2541; max-width: 760px; margin: 0 auto;">
            
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
                    <span id="runner-diamond-text" style="color: #00b4d8; font-weight: bold; font-size: 14px;">📐 주자 없음</span>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 16px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="420" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px;"></canvas>
            
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
                <span id="commentary" style="color: #90e0ef; line-height: 1.5;">🎙️ 해설위원: 플레이어 팀의 1회초 공격입니다. 라인업의 첫 타자는 발이 아주 빠른 리드오프입니다. 변화구 궤적을 예리하게 노려야 합니다!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0, hasRunner: false }};
            let ball = {{ active: false, x: 360, y: 150, z: 0, tx: 360, ty: 320, size: 2, name: "직구", speed: 0.025 }};
            
            let selectedPitch = "직구";
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;
            let isBuntMode = false;

            // [3] 투수/타자 스피드 및 파워 디테일 스펙 구조 설계
            let currentPitcher = {{ type: "ace", veloMod: 1.25, breakMod: 0.85, name: "강속구 선발 에이스" }};
            let currentBatter = {{ type: "speed", power: 0.75, speed: 1.45, name: "1번 타자" }};

            function changePitcher() {{
                let val = document.getElementById('pitcher-select').value;
                if (val === "ace") {{
                    currentPitcher = {{ type: "ace", veloMod: 1.25, breakMod: 0.85, name: "강속구 선발 에이스" }};
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 마운드에 불같은 강속구를 뿌리는 팀의 1선발 에이스가 등판합니다!";
                }} else {{
                    currentPitcher = {{ type: "control", veloMod: 0.82, breakMod: 1.5, name: "기교파 변화구 스페셜리스트" }};
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 투수가 교체됩니다! 제구력과 낙차 큰 무빙 변화구를 구사하는 기교파 투수입니다!";
                }}
            }}

            function callPinchHitter() {{
                currentBatter = {{ type: "power", power: 1.6, speed: 0.55, name: "해결사 대타" }};
                document.getElementById('current-batter-info').innerText = "대타 (파워형 거포)";
                document.getElementById('commentary').innerHTML = "🚨 중계석: 감독이 승부처라고 판단했습니다! 한 방이 있는 파워형 해결사 대타 카드를 꺼내듭니다!";
            }}

            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = `🎯 수비 지시: ${{currentPitcher.name}} 선수가 [${{type}}] 구사 사인을 확인했습니다. 존 안을 클릭하세요!`;
            }}

            function triggerBunt() {{
                if (!ball.active || isSwung) return;
                isSwung = true; isBuntMode = true; swingFrame = 8;
                
                if (ball.z >= 0.82 && ball.z <= 0.96) {{
                    ball.active = false;
                    // 타자의 주력(speed) 스펙이 내야 안타 확률에 다이렉트 반영
                    let buntRoll = Math.random() * currentBatter.speed;
                    if (buntRoll > 0.5) {{
                        game.hasRunner = true; game.o++;
                        document.getElementById('commentary').innerHTML = `📐 번트 성공! ${{currentBatter.name}}가 엄청난 스피드로 1루 베이스를 밟아 세이프 판정을 이끌어냅니다!`;
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 해설: 배트에 공을 맞추긴 했으나 타구 속도가 죽지 않아 포수 정면 아웃입니다.";
                    }}
                    checkInningStatus();
                }} else {{
                    game.s++; ball.active = false; checkInningStatus();
                    document.getElementById('commentary').innerHTML = "🎙️ 주심: 스트라이크! 배트 위치가 날아오는 변화구 궤적과 너무 멀었습니다.";
                }}
            }}

            function triggerSteal() {{
                if (!game.hasRunner) {{
                    document.getElementById('commentary').innerText = "❌ 작전 경고: 루상에 진루한 주자가 존재하지 않습니다.";
                    return;
                }}
                // 타자(주자)의 주력 수치 연산으로 도루 성공과 태그아웃 분기
                let stealRoll = Math.random() * currentBatter.speed;
                if (stealRoll > 0.65) {{
                    if (currentMode === "batter") game.pScore++; else game.oppScore++;
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = `🏃 도루 성공! ${{currentBatter.name}}의 엄청난 스피드가 베이스를 훔쳐냅니다! 타이밍 완승!`;
                }} else {{
                    game.o++; game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "☠️ 캐스터: 아웃! 포수가 주자의 스피드를 읽고 완벽한 2루 송구로 저격 성공합니다!";
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
                        ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 150; ball.z = 0; ball.size = 2;
                        
                        // 구종별 베이스 속도와 투수 고유 구속 가속도(veloMod) 공식 연동
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
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 240 && ball.y <= 340);
                if (ball.z >= 0.84 && ball.z <= 0.95) {{
                    if (insideZone) {{
                        evaluateHitTrajectory(false);
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerText = "🎙️ 해설: 존을 벗어나며 날카롭게 휘는 유인구 무빙에 배트가 완전히 속았습니다. 삼진 아웃!";
                        ball.active = false; checkInningStatus();
                    }}
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerText = "🎙️ 캐스터: 변화구 특유의 감속 타이밍을 맞추지 못했습니다, 스트라이크!";
                    ball.active = false; checkInningStatus();
                }}
            }}

            function evaluateHitTrajectory(isAiHitter) {{
                ball.active = false;
                // 타자의 파워 수치를 반영하여 배트 중심에 맞았을 때 장타 유무 산출
                let hitRoll = Math.random() * (isAiHitter ? 1.0 : currentBatter.power);
                
                if (hitRoll > 0.52) {{
                    if (game.hasRunner) {{
                        if (isAiHitter) game.oppScore += 2; else game.pScore += 2;
                        game.hasRunner = false;
                        document.getElementById('commentary').innerHTML = `🔥 홈런성 타구!! 완벽한 임팩트로 외야 담장을 원바운드로 때리는 초장거리 적시 2루타!`;
                    }} else {{
                        game.hasRunner = true;
                        document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 안타입니다! 강한 파워로 수비수 키를 넘기는 깔끔한 안타로 출루합니다!`;
                    }}
                }} else {{
                    game.o++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 높게 뜬 타구, 야수들이 낙구 지점을 정확히 포착하며 플라이 아웃 처리합니다.";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상: 주자 1루" : "📐 루상: 주자 없음";
                checkInningStatus();
            }}

            function checkInningStatus() {{
                aiPitchTimer = 70;
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 완벽한 궤적의 결정구에 배트가 허공을 가릅니다."; }}
                if (game.b >= 4) {{ 
                    if (currentMode === "pitcher") game.oppScore++; else game.pScore++; 
                    game.s = 0; game.b = 0; game.hasRunner = true;
                    document.getElementById('commentary').innerText = "🎙️ 볼넷 출루! 투수의 제구 제어에 한계가 왔습니다."; 
                }}
                
                // [4] 정식 3아웃 자동 공수전환 루프 메커니즘
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
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대 (3아웃)!</b> 플레이어가 수비에 나섭니다. 투수를 점검하고 구종을 선택하여 상대 타자를 요리하세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격 (타자)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대 (3아웃)!</b> 다시 플레이어 팀의 타석입니다. 집중력을 올려 타격하세요!";
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

                // [5] 3D 원근 궤적 가속도 및 투수 제구/브레이킹(breakMod) 마구 계산식 연산
                if (ball.active) {{
                    ball.z += ball.speed; 
                    
                    let baseX = 360 + (ball.tx - 360) * ball.z;
                    let baseY = 150 + (ball.ty - 150) * ball.z;

                    if (ball.name === "슬라이더") {{
                        let slideEffect = Math.pow(ball.z, 2.5) * (75 * (currentMode === "pitcher" ? currentPitcher.breakMod : 1.0)); 
                        ball.x = baseX + slideEffect;
                        ball.y = baseY;
                    }} else if (ball.name === "체인지업") {{
                        let dropEffect = Math.pow(ball.z, 3.0) * (55 * (currentMode === "pitcher" ? currentPitcher.breakMod : 1.0));
                        ball.x = baseX;
                        ball.y = baseY + dropEffect;
                    }} else {{
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
