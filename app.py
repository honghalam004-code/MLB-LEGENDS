import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB PRO ULTIMATE - BATTERY MATRIX", layout="wide")
    
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

    mlb_data = {
        "San Diego Padres": {"pitcher": "딜런 시즈", "catcher": "카일 히가시오카", "lineup": ["루이스 아라에즈", "페르난도 타티스 Jr.", "주릭슨 프로파", "매니 마차도", "잭슨 메릴", "김하성", "잰더 보가츠", "제이크 크로넨워스"]},
        "Los Angeles Dodgers": {"pitcher": "야마모토 요시노부", "catcher": "윌 스미스", "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "T. 에르난데스", "맥스 먼시", "가빈 럭스", "토미 에드먼", "미겔 로하스"]},
        "New York Yankees": {"pitcher": "게릿 콜", "catcher": "오스틴 웰스", "lineup": ["글레이버 토레스", "후안 소토", "애런 저지", "지안카를로 스탠튼", "재즈 치좀 Jr.", "앤서니 볼피", "알렉스 버두고", "앤서니 리조"]},
        "Atlanta Braves": {"pitcher": "맥스 프리드", "catcher": "션 머피", "lineup": ["로날드 아쿠냐 Jr.", "아지 알비스", "오스틴 라일리", "맷 올슨", "마르셀 오수나", "마이클 해리스 2세", "자레드 켈닉", "올랜도 아르시아"]},
        "Philadelphia Phillies": {"pitcher": "잭 휠러", "catcher": "J.T. 리얼무토", "lineup": ["카일 슈와버", "트레이 터너", "브라이스 하퍼", "알렉 봄", "닉 카스테야노스", "브라이슨 스탓", "에드문도 소사", "요한 로하스"]}
    }
    
    mlb_teams = sorted(list(mlb_data.keys()))

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB PRO ULTIMATE - BATTERY MATRIX</h1>
                <p style="color: #ffb703; margin-top: 10px; font-size: 18px; font-weight: bold;">🚨 포수 백스톱 구현! 마구 포구 실패 및 폭투/주자 자동 진루 시스템 가동!</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 구단 선택", mlb_teams, index=0)
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단", mlb_teams, index=1)
            
        if st.button("🏟️ 경기 시작"):
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

    js_p_lineup = json.dumps(p_data['lineup'], ensure_ascii=False)
    js_a_lineup = json.dumps(a_data['lineup'], ensure_ascii=False)

    with col_tactics_panel:
        st.markdown("### 📊 배터리 & 타순")
        st.info(f"**⚾ 내 팀:** {st.session_state.p_team}\n* 투수: {p_data['pitcher']}\n* 포수: {p_data['catcher']}\n\n**현재 타자:** {p_data['lineup'][0]}")
        st.error(f"**🤖 AI 팀:** {st.session_state.a_team}\n* 투수: {a_data['pitcher']}\n* 포수: {a_data['catcher']}\n\n**상대 타자:** {a_data['lineup'][0]}")
        if st.button("🚪 로비로 돌아가기"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.p_team
        team_a = st.session_state.a_team

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
                    현재 타석: <span id="current-batter-name">{p_data['lineup'][0]}</span>
                </span>
            </div>

            <canvas id="baseballField" width="720" height="440" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px; cursor: crosshair;"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px;">
                    <span style="color: white; display: inline-block; margin-bottom: 8px;">안방마님 포수: <b style="color:#4cc9f0;">{p_data['catcher']}</b> (너클볼/스플리터는 포수도 놓칠 수 있음!)</span><br>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">
                        <button onclick="setPitch('포심 직구')" id="btn-p1" style="background: #d90429; color: white; border: 2px solid #ffffff; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">포심 직구</button>
                        <button onclick="setPitch('고속 슬라이더')" id="btn-p2" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">슬라이더</button>
                        <button onclick="setPitch('폭포수 커브')" id="btn-p3" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">곡예 커브</button>
                        <button onclick="setPitch('체인지업')" id="btn-p4" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">체인지업</button>
                        <button onclick="setPitch('파워 싱커')" id="btn-p5" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">파워 싱커</button>
                        <button onclick="setPitch('스플리터')" id="btn-p6" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">스플리터</button>
                        <button onclick="setPitch('커터')" id="btn-p7" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">고속 커터</button>
                        <button onclick="setPitch('마구 너클볼')" id="btn-p8" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 8px 5px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:13px;">🔮 너클볼</button>
                    </div>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">📐 기습 번트 자세</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 15px;">🏃 즉시 도루</button>
                    <button onclick="tryAdvanceBase()" id="btn-advance" style="display: none; background: #e63946; color: white; border: 2px solid #ffffff; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; animation: blinker 1s linear infinite;">🚨 주자 추가 진루!</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-weight: bold; margin-top: 8px; border-left: 6px solid #3a86ff; min-height: 55px;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 안방마님 포수까지 마운드 뒤에 완벽 배치 완료! 마구를 흘리는지 안 흘리는지 지켜보겠습니다!</span>
            </div>
        </div>
        """

        js_part = f"""
        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 }};
            let bases = [false, false, false]; 

            const pLineup = {js_p_lineup};
            const aLineup = {js_a_lineup};
            const aiPitcherName = "{a_data['pitcher']}";
            const aiCatcherName = "{a_data['catcher']}";
            const myCatcherName = "{p_data['catcher']}";

            let pBatterIndex = 0; let aBatterIndex = 0;

            const pitchDict = {{
                "포심 직구": {{ speed: 0.038, type: "fast", color: "#e63946", missProb: 0.01 }},
                "고속 슬라이더": {{ speed: 0.031, type: "slider", color: "#3a86ff", missProb: 0.05 }},
                "폭포수 커브": {{ speed: 0.021, type: "curve", color: "#ffb703", missProb: 0.10 }},
                "체인지업": {{ speed: 0.024, type: "changeup", color: "#06d6a0", missProb: 0.06 }},
                "파워 싱커": {{ speed: 0.034, type: "sinker", color: "#f72585", missProb: 0.07 }},
                "스플리터": {{ speed: 0.032, type: "splitter", color: "#7209b7", missProb: 0.15 }}, 
                "커터": {{ speed: 0.036, type: "cutter", color: "#4cc9f0", missProb: 0.02 }},
                "마구 너클볼": {{ speed: 0.016, type: "knuckle", color: "#ffffff", missProb: 0.25 }} 
            }};

            let ball = {{ active: false, isHit: false, isBunt: false, isPassed: false, x: 360, y: 210, z: 0, startX: 360, startY: 210, tx: 360, ty: 320, size: 2, name: "포심 직구" }};
            let selectedPitch = "포심 직구";
            
            let aiPitchTimer = 55; 
            let isSwung = false; let swingFrame = 0;
            let isBuntStance = false;
            let animTicks = 0;

            let fielders = [
                {{ pos: "1B", x: 490, y: 240, ox: 490, oy: 240 }},
                {{ pos: "2B", x: 410, y: 170, ox: 410, oy: 170 }},
                {{ pos: "SS", x: 310, y: 170, ox: 310, oy: 170 }},
                {{ pos: "3B", x: 230, y: 240, ox: 230, oy: 240 }},
                {{ pos: "LF", x: 170, y: 110, ox: 170, oy: 110 }},
                {{ pos: "CF", x: 360, y: 90,  ox: 360, oy: 90 }},
                {{ pos: "RF", x: 550, y: 110, ox: 550, oy: 110 }}
            ];

            function addScore(points) {{
                if (currentMode === "batter") game.pScore += points; else game.oppScore += points;
                document.getElementById('score-p').innerText = game.pScore; document.getElementById('score-opp').innerText = game.oppScore;
            }}

            function nextBatter() {{
                if (currentMode === "batter") {{
                    pBatterIndex = (pBatterIndex + 1) % 8;
                    document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                }} else {{
                    aBatterIndex = (aBatterIndex + 1) % 8;
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
                }} else if (hitType === "passed_ball") {{
                    if (bases[2]) {{ addScore(1); bases[2] = false; }}
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }}
                    if (bases[0]) {{ bases[1] = true; bases[0] = false; }}
                }}
            }}

            function tryAdvanceBase() {{
                if (game.o >= 3) return;
                document.getElementById('btn-advance').style.display = 'none';
                let safe = Math.random() > 0.48; 
                if (safe) {{
                    advanceRunners("single"); 
                    document.getElementById('commentary').innerHTML = `🎙️ 해설: 세이프! 주자가 베이스를 완전히 찢었습니다!`;
                }} else {{
                    game.o++;
                    if (bases[2]) bases[2] = false; else if (bases[1]) bases[1] = false; else if (bases[0]) bases[0] = false;
                    document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 아웃! 무리한 진루가 화를 불렀습니다.`;
                    updateInningStatus();
                }}
            }}

            function triggerBunt() {{
                if (!ball.active || ball.isHit || ball.isPassed) return;
                isBuntStance = true; evalBunt();
            }}

            function evalBunt() {{
                if (ball.active && ball.z >= 0.78 && ball.z <= 0.95) {{
                    ball.isHit = true; ball.isBunt = true;
                    if (Math.random() > 0.45) {{
                        advanceRunners("single");
                        document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 번트 안타 성공! 절묘하게 굴렀습니다!`;
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = `🎙️ 해설: 야수가 빠르게 집어 1루 아웃!`;
                    }}
                    nextBatter(); updateInningStatus();
                }} else {{
                    game.s++; ball.active = false;
                    document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 번트 헛방, 스트라이크!`;
                    updateInningStatus();
                }}
                isBuntStance = false;
            }}

            function triggerSteal() {{
                if (!bases[0] && !bases[1]) {{
                    document.getElementById('commentary').innerHTML = "🎙️ 중계석: 주자가 없습니다.";
                    return;
                }}
                if (Math.random() > 0.5) {{
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }}
                    else if (bases[0]) {{ bases[1] = true; bases[0] = false; }}
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 2루 도루 성공!";
                }} else {{
                    game.o++;
                    if (bases[1]) bases[1] = false; else if (bases[0]) bases[0] = false;
                    document.getElementById('commentary').innerHTML = "🎙️ 해설: 포수 송구 아웃!";
                    updateInningStatus();
                }}
            }}

            function setPitch(type) {{
                selectedPitch = type;
                for(let i=1; i<=8; i++) {{
                    let btn = document.getElementById("btn-p" + i);
                    if (btn && btn.innerText.includes(type.replace("마구 ","").replace("파워 ","").replace("고속 ","").replace("곡예 ",""))) {{
                        btn.style.background = "#d90429"; btn.style.color = "white"; btn.style.border = "2px solid white";
                    }} else if (btn) {{
                        btn.style.background = "#1c2541"; btn.style.color = "#a1a1aa"; btn.style.border = "1px solid #4b5563";
                    }}
                }}
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect(); let mx = e.clientX - rect.left; let my = e.clientY - rect.top;
                document.getElementById('btn-advance').style.display = 'none';

                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch; ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 210; ball.z = 0;
                        ball.startX = 360; ball.startY = 210;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; ball.isPassed = false; isSwung = false;
                    }}
                }} else {{
                    if (isBuntStance) {{ evalBunt(); return; }}
                    if (ball.active && !ball.isHit && !ball.isPassed && !isSwung) {{ 
                        isSwung = true; swingFrame = 12; evalBatterSwing(mx, my);
                    }}
                }}
            }});

            function evalBatterSwing(mx, my) {{
                let hitDist = Math.hypot(mx - ball.x, my - ball.y);
                let timingScore = Math.abs(ball.z - 0.85); 

                if (ball.z >= 0.72 && ball.z <= 0.96) {{
                    if (hitDist <= 30 && timingScore <= 0.04) evaluateHitTrajectory("homerun", false);
                    else if (hitDist <= 55 && timingScore <= 0.09) evaluateHitTrajectory("good", false);
                    else if (hitDist <= 85) evaluateHitTrajectory("poor", false);
                    else {{
                        game.s++; ball.active = false; 
                        document.getElementById('commentary').innerHTML = `🎙️ 캐스터: <b>헛스윙! 공이 마법처럼 꺾였습니다!</b>`; 
                        updateInningStatus();
                    }}
                }} else {{ 
                    game.s++; ball.active = false; 
                    document.getElementById('commentary').innerHTML = `🎙️ 해설: 타이밍이 안 맞았습니다, 헛스윙!`; 
                    updateInningStatus(); 
                }}
            }}

            function evalAiBatter() {{
                if (ball.active && !ball.isHit && !ball.isPassed && !isSwung && ball.z >= 0.76 && ball.z <= 0.90) {{
                    let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                    let pitchData = pitchDict[ball.name];
                    let aiMissChance = (pitchData.type === "knuckle" || pitchData.type === "splitter") ? 0.58 : 0.35;
                    
                    let willSwing = insideZone ? (Math.random() > 0.42) : (Math.random() > 0.89);

                    if (willSwing) {{
                        isSwung = true; swingFrame = 12;
                        if (Math.random() < aiMissChance) {{
                            document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 삼진! 타자의 배트가 허공을 가릅니다!`;
                            game.s++; ball.active = false; updateInningStatus();
                        }} else {{
                            let roll = Math.random();
                            if (roll > 0.89) evaluateHitTrajectory("homerun", true);
                            else if (roll > 0.45) evaluateHitTrajectory("good", true);
                            else evaluateHitTrajectory("poor", true);
                        }}
                    }}
                }}
            }}

            function evaluateHitTrajectory(hitQuality, isAiHitter) {{
                ball.isHit = true; ball.isBunt = false;

                if (hitQuality === "homerun") {{
                    ball.tx = 360 + (Math.random() * 260 - 130); ball.ty = -160; 
                    advanceRunners("homerun");
                    document.getElementById('commentary').innerHTML = `🎙️ 캐스터: <b>쳤습니다!! 담장 밖으로!! 홈런입니다!!</b>`;
                    nextBatter(); updateInningStatus();
                }} else if (hitQuality === "good") {{
                    ball.tx = 360 + (Math.random() * 340 - 170); ball.ty = 40 + Math.random() * 110; 
                    advanceRunners("single");
                    if (!isAiHitter) {{
                        document.getElementById('commentary').innerHTML = `🎙️ 해설: 안타! 주자 나갑니다.`;
                        document.getElementById('btn-advance').style.display = 'inline-block';
                    }} else {{
                        document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 깨끗한 안타를 허용합니다.`;
                    }}
                    nextBatter(); updateInningStatus();
                }} else {{
                    ball.tx = 360 + (Math.random() * 140 - 70); ball.ty = 175; game.o++; 
                    document.getElementById('commentary').innerHTML = `🎙️ 해설: 뜬공 아웃입니다.`;
                    nextBatter(); updateInningStatus();
                }}
            }}

            function updateInningStatus() {{
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerHTML = `🎙️ 캐스터: 삼진 아웃!`; nextBatter(); }}
                if (game.b >= 4) {{ game.s = 0; game.b = 0; document.getElementById('commentary').innerHTML = `🎙️ 중계석: 볼넷 출루!`; advanceRunners("walk"); nextBatter(); }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; bases = [false, false, false]; 
                    document.getElementById('btn-advance').style.display = 'none'; ball.active = false;
                    
                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비"; document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block'; document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('current-batter-name').innerText = aLineup[aBatterIndex];
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격"; document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none'; document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                    }}
                    aiPitchTimer = 55; 
                }}
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawHuman(x, y, isPitcher, frameTick, label="") {{
                ctx.lineWidth = 3;
                ctx.strokeStyle = isPitcher ? "#e63946" : "#4cc9f0";
                ctx.fillStyle = isPitcher ? "#e63946" : "#4cc9f0";

                let idleOffset = Math.sin(frameTick * 0.08) * 1.8;
                ctx.beginPath(); ctx.arc(x, y - 22 + (isPitcher ? 0 : idleOffset), 6, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.moveTo(x, y - 16 + (isPitcher ? 0 : idleOffset)); ctx.lineTo(x, y); ctx.stroke();

                ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - 6, y + 14); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 6, y + 14); ctx.stroke();
                
                if(label) {{
                    ctx.fillStyle = "#ffffff"; ctx.font = "10px Arial"; ctx.fillText(label, x - 12, y - 30);
                }}
            }}

            function drawScene() {{
                animTicks++;
                ctx.clearRect(0, 0, 720, 440);
                ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 440);
                
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.moveTo(0, 440); ctx.lineTo(720, 440); ctx.lineTo(550, 190); ctx.lineTo(170, 190); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#2a9d8f"; ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(480, 260); ctx.lineTo(360, 140); ctx.lineTo(240, 260); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.arc(360, 210, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.fillRect(350, 208, 20, 4);
                
                ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(370, 370); ctx.lineTo(350, 370); ctx.closePath(); ctx.fill(); 
                ctx.fillRect(475, 255, 12, 12); ctx.fillRect(354, 134, 12, 12); ctx.fillRect(235, 255, 12, 12); 

                if (bases[0]) {{ ctx.fillStyle = "#ffb703"; ctx.beginPath(); ctx.arc(481, 261, 8, 0, Math.PI*2); ctx.fill(); }}
                if (bases[1]) {{ ctx.fillStyle = "#ffb703"; ctx.beginPath(); ctx.arc(360, 140, 8, 0, Math.PI*2); ctx.fill(); }}
                if (bases[2]) {{ ctx.fillStyle = "#ffb703"; ctx.beginPath(); ctx.arc(241, 261, 8, 0, Math.PI*2); ctx.fill(); }}

                drawHuman(360, 195, true, animTicks, "P"); 
                drawHuman(285, 355, false, animTicks, "H"); 
                
                let activeCatcherName = (currentMode === "pitcher") ? myCatcherName : aiCatcherName;
                drawHuman(360, 395, true, animTicks, "C"); 

                fielders.forEach(f => {{
                    if (ball.active && ball.isHit) {{
                        let dx = ball.x - f.x; let dy = ball.y - f.y;
                        let dist = Math.hypot(dx, dy);
                        if(dist > 5) {{ f.x += (dx / dist) * 2.8; f.y += (dy / dist) * 2.8; }} 
                    }} else {{ 
                        let dx = f.ox - f.x; let dy = f.oy - f.y;
                        f.x += dx * 0.06; f.y += dy * 0.06;
                    }}
                    ctx.fillStyle = "#023e8a"; ctx.fillRect(f.x - 8, f.y - 10, 16, 12);
                    ctx.fillStyle = "rgba(255,255,255,0.8)"; ctx.font = "11px Arial"; ctx.fillText(f.pos, f.x - 7, f.y + 14);
                }});

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5; ctx.strokeRect(310, 260, 100, 90);
                
                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let keys = Object.keys(pitchDict);
                        ball.name = keys[Math.floor(Math.random() * keys.length)];
                        ball.tx = 310 + Math.random() * 100; ball.ty = 260 + Math.random() * 90;
                        ball.x = 360; ball.y = 210; ball.z = 0; ball.startX = 360; ball.startY = 210;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; ball.isPassed = false; isSwung = false;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 투수 <b>" + aiPitcherName + "</b>이 구질로 <b>" + ball.name + "</b>을 장착했습니다!";
                    }}
                }}

                if (ball.active) {{
                    let pData = pitchDict[ball.name] || pitchDict["포심 직구"];
                    let currentSpeed = ball.isHit ? -0.042 : (ball.isPassed ? 0.035 : pData.speed);
                    ball.z += currentSpeed; 
                    
                    if (!ball.isHit && !ball.isPassed) {{
                        let base_x = ball.startX + (ball.tx - ball.startX) * ball.z;
                        let base_y = ball.startY + (ball.ty - ball.startY) * ball.z;
                        
                        if (pData.type === "slider") base_x += Math.pow(ball.z, 2.3) * 65;
                        else if (pData.type === "curve") {{ base_y -= Math.sin(ball.z * Math.PI) * 55; base_y += Math.pow(ball.z, 2) * 25; }}
                        else if (pData.type === "changeup") base_y += Math.pow(ball.z, 2.8) * 40;
                        else if (pData.type === "sinker") {{ base_x -= Math.pow(ball.z, 2) * 25; base_y += Math.pow(ball.z, 2) * 30; }}
                        else if (pData.type === "splitter" && ball.z > 0.6) base_y += Math.pow(ball.z - 0.6, 2) * 160;
                        else if (pData.type === "cutter") base_x += Math.pow(ball.z, 2) * 15;
                        else if (pData.type === "knuckle") {{ base_x += Math.sin(ball.z * 12) * 18; base_y += Math.cos(ball.z * 10) * 12; }}
                        
                        ball.x = base_x; ball.y = base_y;
                        ctx.fillStyle = pData.color;
                    }} else if (ball.isPassed) {{
                        ball.y += 4;
                        ctx.fillStyle = "#ff5722";
                    }} else {{
                        ball.x = 360 + (ball.tx - 360) * ball.z; ball.y = 210 + (ball.ty - 210) * ball.z;
                        ctx.fillStyle = "#ffffff";
                    }}
                    
                    ball.size = ball.isHit ? (ball.isBunt ? 4 : Math.max(1, 2.5 + (ball.z * 12))) : (2.5 + (Math.pow(ball.z, 3.2) * 22));
                    ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher" && !ball.isHit && !ball.isPassed) evalAiBatter();

                    if (!ball.isHit && !ball.isPassed && ball.z >= 1.0) {{
                        if (Math.random() < pData.missProb) {{
                            ball.isPassed = true; 
                            let anyRunner = (bases[0] || bases[1] || bases[2]);
                            advanceRunners("passed_ball"); 
                            
                            if (anyRunner) {{
                                document.getElementById('commentary').innerHTML = "🎙️ 해설: <b>어어어?! 공이 빠졌습니다!! 포수 무브먼트를 비껴갑니다! 엉? 으의 아아어ㅣㅇ!! 그 사이에 루상의 주자들 한 베이스씩 자동 진루합니다!! 폭투입니다!</b>";
                            }} else {{
                                document.getElementById('commentary').innerHTML = "🎙️ 캐스터: <b>앗! 뒤로 빠집니다! 워낙 회전이 심한 마구다 보니 포수 " + activeCatcherName + "도 블로킹하지 못했습니다!</b>";
                            }}
                        }} else {{
                            ball.active = false;
                            let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                            if (insideZone) {{ game.s++; document.getElementById('commentary').innerHTML = "🎙️ 해설: 스트라이크 꽂힙니다!"; }} 
                            else {{ game.b++; document.getElementById('commentary').innerHTML = "🎙️ 해설: 볼입니다."; }}
                            updateInningStatus(); aiPitchTimer = 55;
                        }}
                    }} else if (ball.isPassed && ball.y >= 440) {{
                        ball.active = false; ball.isPassed = false;
                        game.b++; 
                        updateInningStatus(); aiPitchTimer = 55;
                    }} else if (ball.isHit && (ball.z <= -0.5 || ball.z >= 1.5)) {{ 
                        ball.active = false; aiPitchTimer = 55;
                    }}
                }}

                if (isBuntStance) {{
                    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(295, 350); ctx.lineTo(355, 350); ctx.stroke();
                }} else if (swingFrame > 0) {{
                    ctx.save(); let angleRatio = ((12 - swingFrame) / 12) * Math.PI; ctx.translate(290, 350); ctx.rotate(angleRatio - Math.PI / 5);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(75, 0); ctx.stroke(); ctx.restore(); swingFrame--;
                }} else {{
                    ctx.save(); let batIdle = Math.sin(animTicks * 0.1) * 0.05; ctx.translate(290, 340); ctx.rotate(-Math.PI / 2.8 + batIdle);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(65, 0); ctx.stroke(); ctx.restore();
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
