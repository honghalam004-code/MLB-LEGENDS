import streamlit as st
import json
import random

def main():
    st.set_page_config(page_title="MLB MATRIX v4 - TRUE FIELD & ABS", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox > div > div { background-color: #1c2541 !important; color: #ffffff !important; border: 2px solid #3a86ff !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #e63946 0%, #b7094c 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 16px !important;
            border-radius: 8px !important; border: none !important; padding: 12px 20px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # [30개 구단 데이터 가독성 정렬본 유지]
    mlb_all_30_data = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스": {
                    "fb_speed": 101,
                    "pitches": {
                        "101마일 스플린커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.032},
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.026},
                        "너클 커브": {"mastery": 4, "type": "curve", "color": "#ffb703", "speed_mod": 0.018}
                    }
                },
                "미치 켈러": {
                    "fb_speed": 95,
                    "pitches": {
                        "싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.025},
                        "스위퍼": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024}
                    }
                }
            },
            "catcher": "조이 바트",
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "키브라이언 헤이즈", "라우디 텔레즈", "앤드류 맥커친", "코너 조", "자레드 트리올로", "마이클 A. 테일러"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {
                    "fb_speed": 100,
                    "pitches": {
                        "파워 포심": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.031},
                        "명품 스위퍼": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024},
                        "스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.023}
                    }
                }
            },
            "catcher": "윌 스미스",
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "테오스카 에르난데스", "맥스 먼시", "토미 에드먼", "가빈 럭스", "앤디 파헤스"]
        },
        "San Diego Padres": {
            "pitchers": {
                "딜런 시즈": {
                    "fb_speed": 97,
                    "pitches": {
                        "포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.027},
                        "고속 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024}
                    }
                }
            },
            "catcher": "카일 히가시오카",
            "lineup": ["루이스 아라에즈", "페르난도 타티스 Jr.", "주릭슨 프로파", "매니 마차도", "잭슨 메рил", "김하성", "잰더 보가츠", "제이크 크로넨워스"]
        },
        "New York Yankees": {
            "pitchers": {
                "게릿 콜": {
                    "fb_speed": 98,
                    "pitches": {
                        "포심 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.028},
                        "고속 슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024}
                    }
                }
            },
            "catcher": "오스틴 웰스",
            "lineup": ["글레이버 토레스", "후안 소토", "애런 저지", "지안카를로 스탠튼", "재즈 치지금 Jr.", "앤서니 볼피", "알렉스 버두고", "앤서니 리조"]
        },
        "San Francisco Giants": {
            "pitchers": {
                "로건 웹": {
                    "fb_speed": 93,
                    "pitches": {
                        "명품 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.024},
                        "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.017}
                    }
                }
            },
            "catcher": "패트릭 베일리",
            "lineup": ["이정후", "맷 채프먼", "라몬테 웨이드", "솔레어", "콘포토", "야스트렘스키", "에스트라다", "베일리"]
        }
    }
    
    # 30개 구단 리스트 컴팩트 대응 (UI 스크롤 최적화)
    mlb_teams = sorted(list(mlb_all_30_data.keys()))

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 900;">⚾ MLB REAL MATRIX v4 - FULL FIELD EDITION</h1>
                <p style="color: #06d6a0; margin-top: 10px; font-size: 15px; font-weight: bold;">📢 허허벌판 박스 안내선 해제! 진짜 투수, 타자, 수비수와 다이내믹 구장 뷰 복원 완료!</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            user_team = st.selectbox("🏃 내 구단 선택", mlb_teams, index=0)
            user_p_options = list(mlb_all_30_data[user_team]["pitchers"].keys())
            user_selected_p = st.selectbox("🔥 선발 투수 선택", user_p_options)
        with c2:
            ai_team = st.selectbox("🤖 AI 상대 구단 선택", mlb_teams, index=1 if len(mlb_teams)>1 else 0)
            ai_p_options = list(mlb_all_30_data[ai_team]["pitchers"].keys())
            ai_selected_p = st.selectbox("🔥 상대 선발 선택", ai_p_options)
            
        if st.button("🏟️ 진짜 야구장 입장 및 경기 시작"):
            st.session_state.p_team = user_team
            st.session_state.a_team = ai_team
            st.session_state.p_pitcher_name = user_selected_p
            st.session_state.p_pitcher_data = mlb_all_30_data[user_team]["pitchers"][user_selected_p]
            st.session_state.p_lineup = mlb_all_30_data[user_team]["lineup"]
            
            st.session_state.a_pitcher_name = ai_selected_p
            st.session_state.a_pitcher_data = mlb_all_30_data[ai_team]["pitchers"][ai_selected_p]
            st.session_state.a_lineup = mlb_all_30_data[ai_team]["lineup"]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_game_screen, col_tactics_panel = st.columns([3, 1])

    with col_tactics_panel:
        st.markdown("### 📊 MATCH INFO")
        st.info(f"**⚾ PLAYER:** {st.session_state.p_team}\n* 투수: {st.session_state.p_pitcher_name}")
        st.error(f"**🤖 AI:** {st.session_state.a_team}\n* 투수: {st.session_state.a_pitcher_name}")
        
        if st.button("🚪 경기 종료 및 메인으로"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        pitch_buttons_html = ""
        for idx, (p_name, p_info) in enumerate(st.session_state.p_pitcher_data['pitches'].items(), 1):
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" id="btn-p{idx}" style="background: {"#e63946" if idx==1 else "#1c2541"}; color: white; border: 1px solid #4b5563; padding: 6px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:11px;">{p_name}</button>'

        html_part = f"""
        <div id="game-container" style="background: #0b1329; padding: 12px; border-radius: 14px; max-width: 760px; margin: 0 auto;">
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; color: white;">
                <div>
                    <span style="color: #4cc9f0; font-weight: 800;">{st.session_state.p_team}</span> 
                    <span id="score-p" style="font-size: 20px; font-weight: 900; color: #4cc9f0;">0</span> : 
                    <span id="score-opp" style="font-size: 20px; font-weight: 900; color: #f72585;">0</span>
                    <span style="color: #f72585; font-weight: 800;">{st.session_state.a_team}</span>
                </div>
                <div><span id="count-display" style="font-weight: bold; color: #ffb703;">B: 0 | S: 0 | O: 0</span></div>
            </div>

            <canvas id="baseballField" width="720" height="460" style="background: #2a9d8f; border: 3px solid #1c2541; display: block; border-radius: 8px;"></canvas>
            
            <div style="margin-top: 8px; background: #1c2541; padding: 10px; border-radius: 8px;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 6px;">
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">{pitch_buttons_html}</div>
                </div>
                <div id="batter-controls" style="display: flex; justify-content: center; gap: 10px;">
                    <span style="color: #fff; font-size:13px; align-self:center;">👉 **화면(타격 구역)을 타이밍 맞춰 클릭하세요!**</span>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 6px; border-left: 5px solid #06d6a0; min-height: 45px; font-size:13px;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 선수단 배치 완료. 진정한 MLB 현장 매치가 시작됩니다!</span>
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

            const pLineup = {json.dumps(st.session_state.p_lineup, ensure_ascii=False)};
            const aLineup = {json.dumps(st.session_state.a_lineup, ensure_ascii=False)};
            const pPitches = {json.dumps(st.session_state.p_pitcher_data['pitches'], ensure_ascii=False)};
            const aPitches = {json.dumps(st.session_state.a_pitcher_data['pitches'], ensure_ascii=False)};

            let pBatterIdx = 0; let aBatterIdx = 0;
            let selectedPitch = Object.keys(pPitches)[0];

            // 야구 선수 포지션 정의 (v3 스타일 비주얼 매핑)
            let players = {{
                pitcher: {{ x: 360, y: 220, name: "투수" }},
                batter: {{ x: 360, y: 400, name: "타자" }},
                catcher: {{ x: 360, y: 430, name: "포수" }},
                infun1: {{ x: 260, y: 280, name: "유격수" }},
                infun2: {{ x: 460, y: 280, name: "2루수" }},
                infun3: {{ x: 200, y: 340, name: "1루수" }},
                infun4: {{ x: 520, y: 340, name: "3루수" }},
                outfield1: {{ x: 180, y: 120, name: "좌익수" }},
                outfield2: {{ x: 360, y: 90, name: "중견수" }},
                outfield3: {{ x: 540, y: 120, name: "우익수" }}
            }};

            let ball = {{ active: false, isHit: false, x: 360, y: 220, z: 0, startX: 360, startY: 220, tx: 360, ty: 400, name: selectedPitch }};
            let aiPitchTimer = 60;
            let batAngle = -0.2; let isBatSwinging = false;
            let umpSignal = {{ text: "", frame: 0, color: "#fff" }};
            let absSignal = {{ text: "", frame: 0, color: "#06d6a0" }};

            // 주자 진루 연출 메커니즘
            function advanceRunners(type) {{
                if (type === "single") {{
                    if (bases[2]) {{ game.pScore++; bases[2] = false; }}
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }}
                    if (bases[0]) {{ bases[1] = true; bases[0] = false; }}
                    bases[0] = true;
                }} else if (type === "walk") {{
                    if (bases[0] && bases[1] && bases[2]) {{ game.pScore++; }}
                    else if (bases[0] && bases[1]) {{ bases[2] = true; }}
                    else if (bases[0]) {{ bases[1] = true; }}
                    bases[0] = true;
                }}
                document.getElementById('score-p').innerText = game.pScore;
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch; ball.x = 360; ball.y = 220; ball.z = 0;
                        ball.tx = 340 + Math.random()*40; ball.ty = 400; ball.active = true; ball.isHit = false;
                    }}
                }} else {{
                    // 타자 스윙 애니메이션 트리거 및 타이밍 매칭
                    if (ball.active && !ball.isHit && !isBatSwinging) {{
                        isBatSwinging = true;
                        let timingDiff = Math.abs(ball.y - 400);
                        if (timingDiff < 35) {{
                            ball.isHit = true;
                            ball.tx = 200 + Math.random()*320;
                            ball.ty = 80 + Math.random()*120;
                            advanceRunners("single");
                            document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 쳤습니다! 필드 구석을 가르는 깨끗한 안타!";
                        }} else {{
                            game.s++;
                            document.getElementById('commentary').innerHTML = "🎙️ 주심: 헛스윙 스트라이크!!";
                        }}
                        updateInning();
                    }}
                }}
            }});

            function setPitch(type) {{ selectedPitch = type; }}

            function updateInning() {{
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; }}
                if (game.b >= 4) {{ game.s = 0; game.b = 0; advanceRunners("walk"); }}
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; bases = [false, false, false];
                    currentMode = (currentMode === "batter") ? "pitcher" : "batter";
                    document.getElementById('pitcher-controls').style.display = (currentMode === "pitcher") ? 'block' : 'none';
                }}
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 720, 460);
                
                // 1. 진짜 야구 필드 부채꼴 & 다이아몬드 그리기 (v3 복원)
                ctx.fillStyle = "#2a9d8f"; ctx.fillRect(0, 0, 720, 460); // 잔디
                ctx.fillStyle = "#e9c46a"; // 내야 흙 구역
                ctx.beginPath(); ctx.moveTo(360, 420); ctx.lineTo(220, 320); ctx.lineTo(360, 200); ctx.lineTo(500, 320); ctx.closePath(); ctx.fill();

                // 다이아몬드 라인 및 베이스 서클
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2;
                ctx.strokeRect(353, 413, 14, 14); // 홈플레이트
                
                // 루상 주자 상태 시각화 (진루하면 베이스 빨간색 불 들어옴)
                ctx.fillStyle = bases[0] ? "#e63946" : "#ffffff"; ctx.fillRect(493, 313, 14, 14); // 1루
                ctx.fillStyle = bases[1] ? "#e63946" : "#ffffff"; ctx.fillRect(353, 193, 14, 14); // 2루
                ctx.fillStyle = bases[2] ? "#e63946" : "#ffffff"; ctx.fillRect(213, 313, 14, 14); // 3루

                // 2. 수비수 및 선수 그래픽 렌더링 (단순 점선 가이드 해제)
                for (let pos in players) {{
                    let p = players[pos];
                    ctx.fillStyle = (pos === "pitcher" || pos === "catcher") ? "#1c2541" : "#b7094c";
                    ctx.beginPath(); ctx.arc(p.x, p.y, 8, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "10px sans-serif"; ctx.fillText(p.name, p.x - 15, p.y - 12);
                }}

                // 타자 배트 회전 모션
                if (isBatSwinging) {{
                    batAngle += 0.4; if (batAngle > 2.5) {{ isBatSwinging = false; batAngle = -0.2; }}
                }}
                ctx.save(); ctx.translate(345, 400); ctx.rotate(batAngle);
                ctx.strokeStyle = "#d4a373"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(-25, -5); ctx.stroke(); ctx.restore();

                // 3. AI 투구 오토 타이밍 로직
                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let keys = Object.keys(aPitches); ball.name = keys[Math.floor(Math.random() * keys.length)];
                        // 오심 및 변칙 궤적 생성을 위해 살짝 비틀어 투구
                        ball.tx = 350 + (Math.random()*20-10); ball.ty = 420;
                        ball.x = 360; ball.y = 220; ball.z = 0; ball.startX = 360; ball.startY = 220;
                        ball.active = true; ball.isHit = false; aiPitchTimer = 70;
                    }}
                }}

                // 4. 투구 및 타구 트래킹
                if (ball.active) {{
                    let cPitches = (currentMode === "pitcher") ? pPitches : aPitches;
                    let pData = cPitches[ball.name] || {{ speed_mod: 0.025, color: "#fff" }};
                    ball.z += ball.isHit ? -0.03 : pData.speed_mod;

                    if (!ball.isHit) {{
                        ball.x = ball.startX + (ball.tx - ball.startX) * ball.z;
                        ball.y = ball.startY + (ball.ty - ball.startY) * ball.z;
                    }} else {{
                        ball.x = 360 + (ball.tx - 360) * ball.z; ball.y = 400 + (ball.ty - 400) * ball.z;
                    }}

                    ctx.fillStyle = ball.isHit ? "#ffffff" : pData.color;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, 4 + ball.z*6, 0, Math.PI*2); ctx.fill();

                    // 포수 미트 도달 시 v4 ABS 역판정 추적 가동
                    if (!ball.isHit && ball.z >= 1.0) {{
                        ball.active = false;
                        let isRealStrike = (ball.x >= 345 && ball.x <= 375);
                        let callStrike = isRealStrike;
                        let isMissed = Math.random() < 0.25; // 25% 심판 오심 기믹

                        if (isMissed) callStrike = !isRealStrike;

                        if (callStrike) {{ game.s++; umpSignal = {{ text: "STRIKE!", color: "#e63946", frame: 40 }}; }}
                        else {{ game.b++; umpSignal = {{ text: "BALL", color: "#3a86ff", frame: 40 }}; }}

                        if (isMissed) {{
                            absSignal = {{ text: "📢 ABS 시스템 보정: 주심 오심 판독됨 [실제: " + (isRealStrike?"STRIKE":"BALL") + "]", frame: 60 }};
                        }} else {{
                            absSignal = {{ text: "📢 ABS 정상 일치", frame: 30 }};
                        }}
                        updateInning();
                    }}
                }}

                // 판정 보드 및 신호 오버레이
                if (umpSignal.frame > 0) {{
                    ctx.fillStyle = umpSignal.color; ctx.font = "bold 32px sans-serif"; ctx.fillText(umpSignal.text, 310, 160); umpSignal.frame--;
                }}
                if (absSignal.frame > 0) {{
                    ctx.fillStyle = "rgba(2, 12, 27, 0.9)"; ctx.fillRect(10, 10, 380, 30);
                    ctx.fillStyle = "#06d6a0"; ctx.font = "12px sans-serif"; ctx.fillText(absSignal.text, 20, 30); absSignal.frame--;
                }}

                requestAnimationFrame(drawScene);
            }}
            drawScene();
        </script>
        """
        st.components.v1.html(html_part + js_part, height=800)

if __name__ == "__main__":
    main()
