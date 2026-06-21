import streamlit as st
import json

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

    # 🌟 MLB 실제 팀별 로스터 (투수 및 1~9번 타순)
    mlb_data = {
        "Los Angeles Dodgers": {
            "pitcher": {"name": "야마모토 요시노부", "p1": "포심 직구", "p2": "폭포수 커브"},
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "T. 에르난데스", "맥스 먼시", "윌 스미스", "가빈 럭스", "토미 에드먼", "미겔 로하스"]
        },
        "New York Yankees": {
            "pitcher": {"name": "게릿 콜", "p1": "포심 직구", "p2": "너클 커브"},
            "lineup": ["글레이버 토레스", "후안 소토", "애런 저지", "지안카를로 스탠튼", "재즈 치좀 Jr.", "앤서니 볼피", "알렉스 버두고", "오스틴 웰스", "앤서니 리조"]
        },
        "Pittsburgh Pirates": {
            "pitcher": {"name": "폴 스킨스", "p1": "광속구", "p2": "스플링커"},
            "lineup": ["앤드류 매커친", "브라이언 레이놀즈", "오닐 크루즈", "조이 바트", "로우디 텔레즈", "키브라이언 헤이스", "카이너-팔레파", "데 라 크루즈", "자레드 트리올로"]
        },
        "San Diego Padres": {
            "pitcher": {"name": "딜런 시즈", "p1": "포심 직구", "p2": "고속 슬라이더"},
            "lineup": ["루이스 아라에즈", "페르난도 타티스 Jr.", "주릭슨 프로파", "매니 마차도", "잭슨 메릴", "잰더 보가츠", "제이크 크로넨워스", "데이비드 페랄타", "카일 히가시오카"]
        },
        "Boston Red Sox": {
            "pitcher": {"name": "태너 하우크", "p1": "싱커", "p2": "스위퍼"},
            "lineup": ["자렌 듀란", "윌리어 아브레유", "라파엘 데버스", "타일러 오닐", "요시다 마사타카", "코너 웡", "트리스턴 카사스", "세단 라파엘라", "데이비드 해밀턴"]
        }
    }
    mlb_teams = list(mlb_data.keys())

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB FULL SPEC SIMULATOR</h1>
                <p style="color: #4cc9f0; margin-top: 10px; font-size: 16px;">실제 스타 플레이어 참전! 헛스윙 유도 삼진의 쾌감을 느껴보세요.</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 구단 선택", mlb_teams, index=0)
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단", mlb_teams, index=1)
            
        if st.button("🏟️ 찐 경기 시작"):
            st.session_state.p_team = user_team
            st.session_state.a_team = ai_team
            st.session_state.p_data = mlb_data[user_team]
            st.session_state.a_data = mlb_data[ai_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_game_screen, col_tactics_panel = st.columns([3.2, 1])

    p_data = st.session_state.p_data
    a_data = st.session_state.a_data

    # 데이터를 JS로 넘기기 위해 JSON 직렬화
    js_p_lineup = json.dumps(p_data['lineup'], ensure_ascii=False)
    js_a_lineup = json.dumps(a_data['lineup'], ensure_ascii=False)

    with col_tactics_panel:
        st.markdown("### 📊 팀 라인업")
        st.info(f"**⚾ 내 투수:** {p_data['pitcher']['name']}\n\n"
                f"**1:** {p_data['lineup'][0]}\n"
                f"**2:** {p_data['lineup'][1]}\n"
                f"**3:** {p_data['lineup'][2]}")
        st.error(f"**🤖 AI 투수:** {a_data['pitcher']['name']}\n\n"
                 f"**1:** {a_data['lineup'][0]}\n"
                 f"**2:** {a_data['lineup'][1]}\n"
                 f"**3:** {a_data['lineup'][2]}")
        if st.button("🚪 로비로 돌아가기"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.p_team
        team_a = st.session_state.a_team
        my_pitch1 = p_data['pitcher']['p1']
        my_pitch2 = p_data['pitcher']['p2']

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

            <div style="text-align: center; margin-bottom: 10px;">
                <span style="background: #ffb703; color: #020c1b; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 18px;">
                    현재 타자: <span id="current-batter-name">{p_data['lineup'][0]}</span>
                </span>
            </div>

            <canvas id="baseballField" width="720" height="440" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px; cursor: crosshair;"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px;">
                    <span style="color: white; margin-right: 10px;">마운드: <b>{p_data['pitcher']['name']}</b></span>
                    <button onclick="setPitch('{my_pitch1}')" id="btn-fast" style="background: #d90429; color: white; border: 2px solid #ffffff; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">{my_pitch1} (선택됨)</button>
                    <button onclick="setPitch('{my_pitch2}')" id="btn-change" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">{my_pitch2}</button>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 10px;">📐 기습 번트</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer;">🏃 단독 도루</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-weight: bold; margin-top: 8px; border-left: 6px solid #3a86ff;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 자, {team_p}의 1번 타자가 타석에 들어섭니다!</span>
            </div>
        </div>
        """

        js_part = f"""
        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = { pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 };
            let bases = [false, false, false]; 

            // 🌟 찐 로스터 데이터 가져오기
            const pLineup = {js_p_lineup};
            const aLineup = {js_a_lineup};
            const aiPitcherName = "{a_data['pitcher']['name']}";
            const aiPitch1 = "{a_data['pitcher']['p1']}";
            const aiPitch2 = "{a_data['pitcher']['p2']}";

            let pBatterIndex = 0;
            let aBatterIndex = 0;

            const pitchDict = {{
                "포심 직구": {{ speed: 0.022, breakX: 0, breakY: 0 }},
                "광속구": {{ speed: 0.028, breakX: 0, breakY: 0 }}, // 스킨스 전용
                "고속 슬라이더": {{ speed: 0.018, breakX: 70, breakY: 15 }},
                "스플링커": {{ speed: 0.020, breakX: -30, breakY: 60 }}, // 스킨스 전용
                "너클 커브": {{ speed: 0.015, breakX: -20, breakY: 100 }}, // 콜 전용
                "라이징 패스트볼": {{ speed: 0.025, breakX: 0, breakY: -40 }},
                "폭포수 커브": {{ speed: 0.014, breakX: -20, breakY: 90 }},
                "싱커": {{ speed: 0.019, breakX: -50, breakY: 30 }},
                "스위퍼": {{ speed: 0.016, breakX: 110, breakY: 0 }}
            }};

            let myPitch1 = document.getElementById('btn-fast').innerText.replace(" (선택됨)", "");
            let myPitch2 = document.getElementById('btn-change').innerText;

            let ball = {{ active: false, isHit: false, isBunt: false, x: 360, y: 220, z: 0, tx: 360, ty: 320, size: 2, name: myPitch1 }};
            let selectedPitch = myPitch1;
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;
            let buntFrame = 0;

            let fielders = [
                {{ pos: "1B", x: 490, y: 240 }}, {{ pos: "2B", x: 410, y: 170 }}, {{ pos: "SS", x: 310, y: 170 }},
                {{ pos: "3B", x: 230, y: 240 }}, {{ pos: "LF", x: 170, y: 110 }}, {{ pos: "CF", x: 360, y: 90 }}, {{ pos: "RF", x: 550, y: 110 }}
            ];

            function addScore(points) {{
                if (currentMode === "batter") game.pScore += points; else game.oppScore += points;
                document.getElementById('score-p').innerText = game.pScore; document.getElementById('score-opp').innerText = game.oppScore;
            }}

            function nextBatter() {{
                if (currentMode === "batter") {{
                    pBatterIndex = (pBatterIndex + 1) % 9;
                    document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                }} else {{
                    aBatterIndex = (aBatterIndex + 1) % 9;
                    document.getElementById('current-batter-name').innerText = aLineup[aBatterIndex];
                }}
            }}

            function advanceRunners(hitType) {{
                if (hitType === "walk") {{
                    if (bases[0] && bases[1] && bases[2]) {{ addScore(1); }}
                    else if (bases[0] && bases[1]) {{ bases[2] = true; }} else if (bases[0]) {{ bases[1] = true; }}
                    bases[0] = true;
                }} else if (hitType === "single") {{
                    if (bases[2]) {{ addScore(1); bases[2] = false; }} 
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }} 
                    if (bases[0]) {{ bases[1] = true; bases[0] = false; }} 
                    bases[0] = true; 
                }} else if (hitType === "homerun") {{
                    let runs = 1; if (bases[0]) runs++; if (bases[1]) runs++; if (bases[2]) runs++;
                    addScore(runs); bases = [false, false, false]; 
                }}
            }}

            function setPitch(type) {{
                selectedPitch = type;
                let bf = document.getElementById('btn-fast'); let bc = document.getElementById('btn-change');
                if(type === myPitch1) {{
                    bf.style.background = '#d90429'; bf.style.color = 'white'; bf.style.border = '2px solid white'; bf.innerText = myPitch1 + " (선택됨)";
                    bc.style.background = '#1c2541'; bc.style.color = '#a1a1aa'; bc.style.border = '1px solid #4b5563'; bc.innerText = myPitch2;
                }} else {{
                    bc.style.background = '#f77f00'; bc.style.color = 'white'; bc.style.border = '2px solid white'; bc.innerText = myPitch2 + " (선택됨)";
                    bf.style.background = '#1c2541'; bf.style.color = '#a1a1aa'; bf.style.border = '1px solid #4b5563'; bf.innerText = myPitch1;
                }}
            }}

            function triggerBunt() {{
                if (!ball.active || isSwung || ball.isHit) return;
                isSwung = true; buntFrame = 25; 
                let insideZone = (ball.x >= 250 && ball.x <= 470 && ball.y >= 200 && ball.y <= 400);
                if (ball.z >= 0.50 && ball.z <= 0.98) {{
                    if (insideZone) {{
                        ball.isHit = true; ball.isBunt = true; ball.tx = Math.random() > 0.5 ? 330 : 260; ball.ty = 260 + Math.random() * 40; 
                        if (Math.random() > 0.4) {{ advanceRunners("single"); document.getElementById('commentary').innerHTML = `📐 ${{pLineup[pBatterIndex]}}의 절묘한 기습 번트! 안타가 됩니다!`; nextBatter(); }} 
                        else {{ game.o++; document.getElementById('commentary').innerHTML = "🎙️ 번트 타구를 투수가 잡아 아웃시킵니다."; nextBatter(); }}
                        updateInningStatus();
                    }} else {{ game.s++; ball.active = false; document.getElementById('commentary').innerHTML = "🎙️ 나쁜 공에 번트를 대려다 헛스윙!"; updateInningStatus(); }}
                }} else {{ game.s++; ball.active = false; document.getElementById('commentary').innerHTML = "🎙️ 타이밍이 안 맞았습니다!"; updateInningStatus(); }}
            }}

            function triggerSteal() {{
                if (!bases[0] && !bases[1]) return;
                if (Math.random() > 0.55) {{
                    if (bases[1] && !bases[2]) {{ bases[2] = true; bases[1] = false; document.getElementById('commentary').innerHTML = "🏃 3루 도루 성공!"; }}
                    else if (bases[0] && !bases[1]) {{ bases[1] = true; bases[0] = false; document.getElementById('commentary').innerHTML = "🏃 2루 도루 성공!"; }}
                }} else {{
                    game.o++; document.getElementById('commentary').innerHTML = "☠️ 도루 실패! 포수 총알 송구에 아웃!";
                    if (bases[1] && !bases[2]) bases[1] = false; else if (bases[0] && !bases[1]) bases[0] = false;
                }}
                updateInningStatus();
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect(); let mx = e.clientX - rect.left; let my = e.clientY - rect.top;
                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch; ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; isSwung = false;
                    }}
                }} else {{
                    if (ball.active && !ball.isHit && !isSwung) {{ isSwung = true; swingFrame = 10; evalBatterSwing(); }}
                }}
            }});

            function evalAiBatter() {{
                // 🌟 AI 헛스윙 너프 로직 핵심 🌟
                if (ball.active && !ball.isHit && !isSwung && ball.z >= 0.70 && ball.z <= 0.92) {{
                    let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                    let willSwing = false;
                    
                    if (insideZone) {{
                        if (Math.random() > 0.3) willSwing = true; // 스트라이크엔 70% 스윙
                    }} else {{
                        if (Math.random() > 0.6) willSwing = true; // 볼(유인구)에도 40% 확률로 속아서 스윙
                    }}

                    if (willSwing) {{
                        isSwung = true; swingFrame = 10;
                        // 스윙을 했어도 헛스윙할 확률 계산 (유인구일수록 헛스윙 높음)
                        let whiffChance = insideZone ? 0.30 : 0.85; 
                        
                        if (Math.random() < whiffChance) {{
                            // 헛스윙!
                            document.getElementById('commentary').innerHTML = `🎙️ AI ${{aLineup[aBatterIndex]}}, <b>헛스윙!!</b> 날카로운 변화구에 완전히 속았습니다!`;
                        }} else {{
                            // 타격 성공
                            evaluateHitTrajectory(true);
                        }}
                    }}
                }}
            }}

            function evalBatterSwing() {{
                let insideZone = (ball.x >= 250 && ball.x <= 470 && ball.y >= 200 && ball.y <= 400);
                if (ball.z >= 0.50 && ball.z <= 1.0) {{
                    if (insideZone) {{ evaluateHitTrajectory(false); }} 
                    else {{ game.s++; ball.active = false; document.getElementById('commentary').innerText = `🎙️ 어이없는 공입니다. 헛스윙!`; updateInningStatus(); }}
                }} else {{ game.s++; ball.active = false; document.getElementById('commentary').innerText = `🎙️ 타이밍이 안 맞았습니다!`; updateInningStatus(); }}
            }}

            function evaluateHitTrajectory(isAiHitter) {{
                ball.isHit = true; ball.isBunt = false;
                let hitRoll = Math.random();
                let batterName = isAiHitter ? aLineup[aBatterIndex] : pLineup[pBatterIndex];

                if (hitRoll > 0.85) {{
                    ball.tx = 360 + (Math.random() * 200 - 100); ball.ty = -100; advanceRunners("homerun");
                    document.getElementById('commentary').innerHTML = isAiHitter ? `☠️ 앗! ${{batterName}}(이)가 홈런을 쳐냅니다!` : `🔥 쾅!! ${{batterName}}의 대형 홈런!! 담장을 넘깁니다!`;
                }} else if (hitRoll > 0.40) {{
                    ball.tx = 360 + (Math.random() * 300 - 150); ball.ty = 50 + Math.random() * 100; advanceRunners("single");
                    document.getElementById('commentary').innerHTML = isAiHitter ? `🎙️ ${{batterName}}에게 안타를 허용합니다.` : `🎙️ ${{batterName}}, 깔끔한 안타를 쳐냅니다!`;
                }} else {{
                    ball.tx = 360 + (Math.random() * 100 - 50); ball.ty = 200; game.o++; 
                    document.getElementById('commentary').innerHTML = isAiHitter ? `🎙️ 나이스 피칭! ${{batterName}}의 타구가 땅볼이 됩니다. 아웃!` : `🎙️ 아, ${{batterName}} 빗맞았습니다. 아웃입니다.`;
                }}
                nextBatter();
                updateInningStatus();
            }}

            function updateInningStatus() {{
                if (game.s >= 3) {{ 
                    game.o++; game.s = 0; game.b = 0; 
                    let batterName = currentMode === "batter" ? pLineup[pBatterIndex] : aLineup[aBatterIndex];
                    document.getElementById('commentary').innerHTML = `🎙️ 삼진 아웃!! ${{batterName}} 물러납니다.`; 
                    nextBatter();
                }}
                if (game.b >= 4) {{ 
                    game.s = 0; game.b = 0; 
                    let batterName = currentMode === "batter" ? pLineup[pBatterIndex] : aLineup[aBatterIndex];
                    document.getElementById('commentary').innerHTML = `🎙️ 볼넷! ${{batterName}} 1루로 걸어 나갑니다.`; 
                    advanceRunners("walk"); nextBatter();
                }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; bases = [false, false, false]; 
                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비"; document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block'; document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('current-batter-name').innerText = aLineup[aBatterIndex];
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대!</b> 유인구를 던져 AI 타자의 헛스윙을 유도하세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격"; document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none'; document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                        document.getElementById('commentary').innerHTML = `🚨 <b>공수교대!</b> 적 투수 <b>${{aiPitcherName}}</b>의 공을 공략하세요!`;
                    }}
                }}
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 720, 440);
                ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 440);
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.moveTo(0, 440); ctx.lineTo(720, 440); ctx.lineTo(550, 190); ctx.lineTo(170, 190); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#2a9d8f"; ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(480, 260); ctx.lineTo(360, 140); ctx.lineTo(240, 260); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.arc(360, 220, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.fillRect(350, 218, 20, 4);
                ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(370, 370); ctx.lineTo(350, 370); ctx.closePath(); ctx.fill(); 
                ctx.fillRect(475, 255, 12, 12); ctx.fillRect(354, 134, 12, 12); ctx.fillRect(235, 255, 12, 12); 

                ctx.fillStyle = "#ffb703"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 2;
                if (bases[0]) {{ ctx.beginPath(); ctx.arc(481, 261, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }}
                if (bases[1]) {{ ctx.beginPath(); ctx.arc(360, 140, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }}
                if (bases[2]) {{ ctx.beginPath(); ctx.arc(241, 261, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }}

                ctx.fillStyle = "#d90429"; ctx.fillRect(352, 200, 16, 20); 
                fielders.forEach(f => {{
                    ctx.fillStyle = "#023e8a"; ctx.fillRect(f.x - 8, f.y - 10, 16, 12);
                    ctx.fillStyle = "rgba(255,255,255,0.8)"; ctx.font = "11px Arial"; ctx.fillText(f.pos, f.x - 7, f.y + 14);
                }});

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5; ctx.strokeRect(310, 260, 100, 90);
                ctx.fillStyle = "#ffffff"; ctx.fillRect(390, 330, 20, 40); 

                ctx.fillStyle = "rgba(2, 12, 27, 0.7)"; ctx.fillRect(615, 25, 50, 50);
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.strokeRect(620, 30, 40, 40);
                if (bases[0]) {{ ctx.fillStyle = "#ffb703"; ctx.fillRect(652, 46, 8, 8); }} 
                if (bases[1]) {{ ctx.fillStyle = "#ffb703"; ctx.fillRect(636, 30, 8, 8); }} 
                if (bases[2]) {{ ctx.fillStyle = "#ffb703"; ctx.fillRect(620, 46, 8, 8); }} 

                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        ball.name = Math.random() > 0.5 ? aiPitch1 : aiPitch2;
                        ball.tx = 290 + Math.random() * 140; ball.ty = 240 + Math.random() * 120;
                        ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; isSwung = false;
                        document.getElementById('commentary').innerHTML = `🤖 적 투수 <b>${{aiPitcherName}}</b>(이)가 <b>${{ball.name}}</b>(을)를 던집니다!`;
                    }}
                }}

                if (ball.active) {{
                    let pData = pitchDict[ball.name] || pitchDict["포심 직구"];
                    let currentSpeed = ball.isHit ? -0.04 : pData.speed;
                    ball.z += currentSpeed; 
                    
                    if (!ball.isHit) {{
                        let break_factor = Math.pow(ball.z, 2.5); 
                        let base_x = 360 + (ball.tx - 360) * ball.z;
                        let base_y = 220 + (ball.ty - 220) * ball.z;
                        ball.x = base_x + (pData.breakX * break_factor);
                        ball.y = base_y + (pData.breakY * break_factor);
                    }} else {{
                        ball.x = 360 + (ball.tx - 360) * ball.z; ball.y = 220 + (ball.ty - 220) * ball.z;
                    }}
                    
                    if (ball.isHit) {{ ball.size = ball.isBunt ? 4 : Math.max(1, 2.5 + (ball.z * 10)); }} 
                    else {{ ball.size = 2.5 + (Math.pow(ball.z, 3.2) * 20); }}

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher" && !ball.isHit) evalAiBatter();

                    if (!ball.isHit && ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.x >= 250 && ball.x <= 470 && ball.y >= 200 && ball.y <= 400);
                        if (insideZone) {{ 
                            game.s++; 
                            if (!isSwung && currentMode === "pitcher") document.getElementById('commentary').innerHTML = "🎙️ 스트라이크 존에 꽂힙니다! 지켜보는 타자.";
                        }} else {{ 
                            game.b++;
                            if (!isSwung && currentMode === "pitcher") document.getElementById('commentary').innerHTML = "🎙️ 존을 살짝 벗어난 볼입니다.";
                        }}
                        updateInningStatus();
                        aiPitchTimer = 60;
                    }} else if (ball.isHit && (ball.z <= -0.5 || ball.z >= 1.5)) {{ 
                        ball.active = false; aiPitchTimer = 60;
                    }}
                }}

                if (buntFrame > 0) {{
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 8;
                    ctx.beginPath(); ctx.moveTo(350, 330); ctx.lineTo(410, 330); ctx.stroke(); buntFrame--;
                }} else if (swingFrame > 0) {{
                    ctx.save(); let angleRatio = (swingFrame / 10) * Math.PI;
                    ctx.translate(400, 350); ctx.rotate(-angleRatio + Math.PI / 3);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 8;
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-80, -20); ctx.stroke(); ctx.restore(); swingFrame--;
                }} else {{
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(395, 340); ctx.lineTo(430, 270); ctx.stroke();
                }}

                requestAnimationFrame(drawScene);
            }}

            drawScene();
        </script>
        """

        full_html = html_part + js_part
        st.components.v1.html(full_html, height=800)

if __name__ == "__main__":
    main()
