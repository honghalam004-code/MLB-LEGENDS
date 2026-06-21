import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB 30 TEAMS REAL MATCH", layout="wide")
    
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
        "Arizona Diamondbacks (애리조나 다이아몬드백스)", "Atlanta Braves (애틀랜타 브레이브스)", 
        "Baltimore Orioles (볼티모어 오리올스)", "Boston Red Sox (보스턴 레드삭스)", 
        "Chicago Cubs (시카고 컵스)", "Chicago White Sox (시카고 화이트삭스)", 
        "Cincinnati Reds (신시내티 레즈)", "Cleveland Guardians (클리블랜드 가디언스)", 
        "Colorado Rockies (콜로라도 로키스)", "Detroit Tigers (디트로이트 타이거즈)", 
        "Houston Astros (휴스턴 애스트로스)", "Kansas City Royals (캔자스시티 로열스)", 
        "Los Angeles Angels (LA 에인절스)", "Los Angeles Dodgers (LA 다저스)", 
        "Miami Marlins (마이애미 말린스)", "Milwaukee Brewers (밀워키 브루어스)", 
        "Minnesota Twins (미네소타 트윈스)", "New York Mets (뉴욕 메츠)", 
        "New York Yankees (뉴욕 양키스)", "Oakland Athletics (오클랜드 애슬레틱스)", 
        "Philadelphia Phillies (필라델피아 필리스)", "Pittsburgh Pirates (피츠버그 파이리츠)", 
        "San Diego Padres (샌디에이고 파드리스)", "San Francisco Giants (샌프란시스코 자이언츠)", 
        "Seattle Mariners (시애틀 매리너스)", "St. Louis Cardinals (세인트루이스 카디널스)", 
        "Tampa Bay Rays (탬파베이 레이스)", "Texas Rangers (텍사스 레인저스)", 
        "Toronto Blue Jays (토론토 블루제이스)", "Washington Nationals (워싱턴 내셔널스)"
    ]

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB 선수 능력치 연동 매치</h1>
                <p style="color: #4cc9f0; margin-top: 10px; font-size: 16px;">선수별 스피드/파워 적용, 대타 기용 및 개별 투수 로스터 완벽 탑재</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 플레이어 구단 선택", mlb_teams, index=13) 
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단 선택", mlb_teams, index=18) 
            
        if st.button("🏟️ 선수단 이끌고 경기장 입장 (플레이어 선공)"):
            st.session_state.player_team_name = user_team.split(" (")[0]
            st.session_state.ai_team_name = ai_team.split(" (")[0]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 🏟️ 라이브 매치: **{st.session_state.player_team_name}** VS **{st.session_state.ai_team_name}**")

    col_game_screen, col_tactics_panel = st.columns([3, 1])

    with col_tactics_panel:
        st.markdown("### 📊 덕아웃 능력치 데이터")
        st.success("🥎 **선수 고유 능력치 가이드**\n\n* **파워 타자:** 발은 느리지만 장타(안타/홈런) 확률이 대폭 상승합니다.\n* **스피드 타자:** 장타력은 낮지만 도루 성공률과 기습번트 성공률이 엄청납니다.\n* **에이스 투수:** 구속이 더 빠르고 변화구 각도가 날카롭습니다.\n* **대타 기용:** 찬스 상황에서 선수를 즉시 교체할 수 있습니다.")
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
                        <span style="color: #f8fafc; font-weight: bold; font-size: 14px;">⚾ 투수 선택: </span>
                        <select id="pitcher-select" onchange="changePitcher()" style="background:#023e8a; color:white; border-radius:4px; padding:4px;">
                            <option value="ace">1선발 파이어볼러 (구속 특화)</option>
                            <option value="control">기교파 투수 (변화구 특화)</option>
                        </select>
                    </div>
                    <button onclick="setPitch('직구')" style="background: #d90429; color: white; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px;">포심 직구</button>
                    <button onclick="setPitch('슬라이더')" style="background: #023e8a; color: white; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px;">슬라이더</button>
                    <button onclick="setPitch('체인지업')" style="background: #f77f00; color: white; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px;">체인지업</button>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <div style="margin-bottom: 8px;">
                        <span style="color: #f8fafc; font-weight: bold; font-size: 14px;">🏏 타자 라인업: </span>
                        <span id="current-batter-info" style="color: #4cc9f0; font-weight: bold; margin-right: 15px;">1번 타자 (스피드형)</span>
                        <button onclick="callPinchHitter()" style="background: #e63946; color: white; border: none; padding: 4px 10px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 12px;">🔄 대타 기용 (파워 특화)</button>
                    </div>
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 18px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px;">📐 기습 번트</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 8px 18px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px;">🏃 도루 감행!</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700; margin-top: 8px; border-left: 6px solid #3a86ff; text-align: left;">
                <span id="commentary" style="color: #90e0ef; line-height: 1.5;">🎙️ 캐스터: 경기 시작합니다! 1번 타자가 타석에 들어섭니다. 발이 굉장히 빠른 선수죠.</span>
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

            // --- [선수 고유 능력치 데이터베이스] ---
            let currentPitcher = {{ type: "ace", veloMod: 1.2, breakMod: 0.9, name: "1선발 에이스" }};
            let currentBatter = {{ type: "speed", power: 0.8, speed: 1.4, name: "1번 타자(준족)" }};

            function changePitcher() {{
                let val = document.getElementById('pitcher-select').value;
                if (val === "ace") currentPitcher = {{ type: "ace", veloMod: 1.2, breakMod: 0.9, name: "파이어볼러" }};
                else currentPitcher = {{ type: "control", veloMod: 0.85, breakMod: 1.4, name: "기교파 투수" }};
                document.getElementById('commentary').innerHTML = `🎙️ 해설: 투수 교체입니다! ${{currentPitcher.name}}가 마운드에 올라옵니다.`;
            }}

            function callPinchHitter() {{
                currentBatter = {{ type: "power", power: 1.5, speed: 0.6, name: "거포 대타" }};
                document.getElementById('current-batter-info').innerText = "대타 (파워형)";
                document.getElementById('commentary').innerHTML = "🚨 캐스터: 여기서 승부수를 띄웁니다! 장타력이 엄청난 대타가 타석에 들어섭니다!";
            }}

            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = `🎯 ${{currentPitcher.name}}가 [${{type}}] 사인을 받았습니다. 클릭하여 투구하세요!`;
            }}

            function triggerBunt() {{
                if (!ball.active || isSwung) return;
                isSwung = true; isBuntMode = true; swingFrame = 8;
                
                if (ball.z >= 0.82 && ball.z <= 0.96) {{
                    ball.active = false;
                    // 스피드 능력치가 높을수록 번트 성공률(내야 안타 확률) 급상승
                    let buntChance = Math.random() * currentBatter.speed;
                    if (buntChance > 0.45) {{
                        game.hasRunner = true; game.o++;
                        document.getElementById('commentary').innerHTML = `📐 기가 막힌 번트! ${{currentBatter.name}}의 빠른 발이 빛을 발하며 작전을 성공시킵니다!`;
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 번트 댔습니다만 포수 정면! 아웃입니다.";
                    }}
                    checkInningStatus();
                }} else {{
                    game.s++; ball.active = false; checkInningStatus();
                }}
            }}

            function triggerSteal() {{
                if (!game.hasRunner) return;
                
                // 타자의 스피드 능력치가 도루 성공률에 직접 관여
                let stealChance = Math.random() * currentBatter.speed;
                if (stealChance > 0.6) {{
                    if (currentMode === "batter") game.pScore++; else game.oppScore++;
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = `🏃 2루 도루 성공!! 발 빠른 ${{currentBatter.name}}의 진가가 발휘됩니다! 상대 배터리가 꼼짝 못합니다.`;
                }} else {{
                    game.o++; game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "☠️ 해설: 도루 실패! 포수의 칼송구에 태그아웃 당합니다.";
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
                        
                        // 투수 능력치(veloMod)가 구종별 기본 구속에 곱해짐
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
                        document.getElementById('commentary').innerText = "🎙️ 해설: 예리하게 휘어지는 변화구에 배트가 헛돕니다! 아웃!";
                        ball.active = false; checkInningStatus();
                    }}
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerText = "🎙️ 캐스터: 구속 차이에 타이밍을 뺏겼습니다. 헛스윙!";
                    ball.active = false; checkInningStatus();
                }}
            }}

            function evaluateHitTrajectory(isAiHitter) {{
                ball.active = false;
                // 타자의 파워 능력치가 장타 확률에 직접 관여
                let hitChance = Math.random() * (isAiHitter ? 1.0 : currentBatter.power);
                
                if (hitChance > 0.5) {{
                    if (game.hasRunner) {{
                        if (isAiHitter) game.oppScore += 2; else game.pScore += 2;
                        game.hasRunner = false;
                        document.getElementById('commentary').innerHTML = `🔥 홈런성 타구!!! 담장 직격하는 적시 2루타! 특유의 장타력이 폭발합니다!`;
                    }} else {{
                        game.hasRunner = true;
                        document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 잘 맞은 타구! 외야를 가르는 깨끗한 안타를 쳐냅니다.`;
                    }}
                }} else {{
                    game.o++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 아, 빗맞았습니다. 힘없는 플라이 아웃으로 물러납니다.";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상: 주자 1루" : "📐 루상: 주자 없음";
                checkInningStatus();
            }}

            function checkInningStatus() {{
                aiPitchTimer = 70;
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 투수의 완벽한 승리입니다."; }}
                if (game.b >= 4) {{ 
                    if (currentMode === "pitcher") game.oppScore++; else game.pScore++; 
                    game.s = 0; game.b = 0; game.hasRunner = true;
                    document.getElementById('commentary').innerText = "🎙️ 볼넷 출루! 제구가 흔들립니다."; 
                }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; game.hasRunner = false;
                    document.getElementById('runner-diamond-text').innerText = "📐 루상: 주자 없음";
                    
                    // 공수 교대 시 타자/투수 초기화
                    currentBatter = {{ type: "speed", power: 0.8, speed: 1.4, name: "1번 타자" }};
                    document.getElementById('current-batter-info').innerText = "1번 타자 (스피드형)";

                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비 (투수)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block';
                        document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 마운드에 우리 투수가 올라갑니다. 투수와 구종을 선택하세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격 (타자)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 방망이를 쥐고 다시 공격에 나섭니다!";
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

                if (ball.active) {{
                    ball.z += ball.speed; 
                    
                    let baseX = 360 + (ball.tx - 360) * ball.z;
                    let baseY = 150 + (ball.ty - 150) * ball.z;

                    // 투수 능력치(breakMod)가 변화구 휘어지는 각도에 직접 곱해짐
                    if (ball.name === "슬라이더") {{
                        let slideEffect = Math.pow(ball.z, 2.5) * (75 * (currentMode === "pitcher" ? currentPitcher.breakMod : 1)); 
                        ball.x = baseX + slideEffect;
                        ball.y = baseY;
                    }} else if (ball.name === "체인지업") {{
                        let dropEffect = Math.pow(ball.z, 3.0) * (55 * (currentMode === "pitcher" ? currentPitcher.breakMod : 1));
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
