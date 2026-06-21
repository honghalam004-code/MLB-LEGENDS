import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB SIMULATOR PRO", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0d1b2a; color: #e0e1dd; font-family: -apple-system, sans-serif; }
        .stSelectbox { background: #1b263b !important; color: #ffffff !important; border-radius: 6px; }
        .stButton>button {
            background: linear-gradient(135deg, #e63946 0%, #1d3557 100%) !important;
            color: white !important; font-weight: 800; border-radius: 6px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    # 30개 구단 기반 대표 라이벌 세팅용 데이터
    mlb_teams = {
        "LA Dodgers": {"pitcher": "오타니 쇼헤이", "speed": 100, "pitches": ["포심 직구", "스위퍼", "커브"]},
        "NY Yankees": {"pitcher": "게릿 콜", "speed": 98, "pitches": ["포심 직구", "슬라이더", "너클커브"]}
    }

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1b263b; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #e63946; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 900;">🏟️ MLB 리얼 볼 배합 배틀</h1>
                <p style="color: #a8dadc; margin-top: 5px;">구종 선택, 체력, 그리고 실시간 릴리즈 타이밍까지 고증된 진짜 야구 매커니즘</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            play_mode = st.selectbox("🎮 나의 플레이 포지션", ["투수 모드 (사인을 보내고 제구하기)", "타자 모드 (상대 수읽기 및 타격)"])
        with c2:
            opponent = st.selectbox("🤖 상대 라이벌 구단", ["NY Yankees (뉴욕 양키스)", "LA Dodgers (로스앤젤레스 다저스)"])
            
        if st.button("⚾ 플레이 ball!!"):
            st.session_state.game_role = "pitcher" if "투수" in play_mode else "batter"
            st.session_state.opp_team = opponent.split(" (")[0]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 🏟️ 경기 진행 중: **{ '투수 시점 (포수 사인 리드)' if st.session_state.game_role == 'pitcher' else '타자 시점 (게스히팅)' }**")

    col_board, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("### 📋 현재 라인업 현황")
        if st.session_state.game_role == "pitcher":
            st.success("🎯 **투구 프로토콜**\n\n1. 하단 화면에서 **구종 버튼**을 선택해 사인을 냅니다.\n2. 스트라이크 존 내부나 외곽을 조준해 클릭하면 투구가 시작됩니다.\n3. 완벽한 제구 타이밍을 맞추는 것이 핵심입니다.")
        else:
            st.info("🏏 **타격 프로토콜**\n\n1. 상대가 와인드업을 시작하면 구종과 코스를 예측(게스히팅)하세요.\n2. 공이 홈플레이트 앞 릴리즈 포인트에 걸릴 때 **화면을 클릭**해 정타를 만들어내야 합니다.")
        
        st.markdown("---")
        if st.button("🚪 덕아웃으로 나가기 (종료)"):
            st.session_state.game_active = False
            st.rerun()

    with col_board:
        game_html = f"""
        <div style="background: #0b1329; padding: 12px; border-radius: 12px; border: 2px solid #1c2541; max-width: 740px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #e63946; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; display: flex; justify-content: space-between; color: white;">
                <div>
                    <span style="color: #4cc9f0; font-weight: bold;">PLAYER</span> <span id="score-p" style="font-size: 18px; font-weight: 900; color: #4cc9f0;">0</span> 
                    <span style="color: #64748b; margin: 0 10px;">VS</span> 
                    <span style="color: #e63946; font-weight: bold;">{st.session_state.opp_team}</span> <span id="score-opp" style="font-size: 18px; font-weight: 900; color: #e63946;">0</span>
                </div>
                <div>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 15px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="360" style="background: #143615; border: 2px solid #4cc9f0; display: block; border-radius: 6px;"></canvas>
            
            <div id="pitcher-controls" style="margin-top: 8px; text-align: center; display: none;">
                <button onclick="setPitch('포심 직구')" style="background: #1d3557; color: white; border: 1px solid #4cc9f0; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">⚾ 포심 직구 (Fastball)</button>
                <button onclick="setPitch('슬라이더')" style="background: #1d3557; color: white; border: 1px solid #4cc9f0; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">🔮 슬라이더 (Slider)</button>
                <button onclick="setPitch('체인지업')" style="background: #1d3557; color: white; border: 1px solid #4cc9f0; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">🍂 체인지업 (Changeup)</button>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 700; margin-top: 6px; border-left: 5px solid #e63946; text-align: left;">
                <span id="commentary" style="color: #a8dadc;">🎙️ 캐스터: 양 팀 선수들 사인 교환하며 진검승부를 준비합니다.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            const myRole = "{st.session_state.game_role}"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 }};
            let ball = {{ active: false, x: 360, y: 150, z: 0, tx: 360, ty: 260, size: 2, speed: 98, name: "포심 직구" }};
            
            let selectedPitch = "포심 직구";
            let aiPitchTimer = 100;
            let isSwung = false;
            let swingFrame = 0;

            if (myRole === "pitcher") {{
                document.getElementById('pitcher-controls').style.display = 'block';
            }}

            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = "🎯 투수가 포수와 사인을 교환했습니다: <span style='color: #ffb703;'>" + type + "</span> 사인 작동. 스트라이크 존을 클릭해 던지세요!";
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left;
                let my = e.clientY - rect.top;

                if (myRole === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch;
                        ball.tx = mx;
                        ball.ty = my;
                        ball.x = 360; ball.y = 150; ball.z = 0; ball.size = 2;
                        ball.active = true;
                        isSwung = false;
                    }}
                }} else {{
                    if (ball.active && !isSwung) {{
                        isSwung = true;
                        swingFrame = 10;
                        evalBatterSwing();
                    }}
                }}
            }});

            // 투수 모드일 때 AI 타자의 정교한 게스히팅 메커니즘
            function evalAiBatter() {{
                if (ball.active && !isSwung && ball.z >= 0.83 && ball.z <= 0.92) {{
                    isSwung = true;
                    let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 200 && ball.ty <= 300);
                    
                    if (insideZone) {{
                        if (Math.random() > 0.5) {{
                            game.oppScore++;
                            document.getElementById('commentary').innerHTML = "🎙️ 해설: 타자가 완벽하게 노려쳤습니다! 중전 안타로 주자 출루합니다!";
                            ball.active = false;
                            nextPitchSequence();
                        }}
                    }} else {{
                        if (Math.random() > 0.65) {{
                            game.s++;
                            document.getElementById('commentary').innerHTML = "🎙️ 해설: 완전히 빠진 유인구인데 타자 배트 나갔습니다! 헛스윙 스트라이크!";
                            ball.active = false;
                            nextPitchSequence();
                        }}
                    }}
                }}
            }}

            // 타자 모드일 때 배트 스윙 정확도 측정 (타이밍과 구종 궤적 결합)
            function evalBatterSwing() {{
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 200 && ball.y <= 300);
                
                // 고증된 실제 안타 유효 프레임존 (0.84~0.94)
                if (ball.z >= 0.84 && ball.z <= 0.94) {{
                    if (insideZone) {{
                        let hitRand = Math.random();
                        if (hitRand > 0.8) {{
                            game.pScore += 1;
                            document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 완전히 한가운데 실투를 받아쳤습니다!! 좌측 담장 넘어갑니다, 홈런!!!";
                        }} else {{
                            game.pScore += 1;
                            document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 밀어친 타구, 유격수 키를 넘기는 시원한 안타입니다!";
                        }}
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 해설: 존을 벗어나는 공에 억지로 갖다 댔어요. 빗맞으면서 3루수 땅볼 아웃입니다.";
                    }}
                    ball.active = false;
                    nextPitchSequence();
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 스트라이크! 타이밍이 너무 늦었습니다. 포수 미트 안착.";
                    ball.active = false;
                    nextPitchSequence();
                }}
            }}

            function nextPitchSequence() {{
                aiPitchTimer = 110; // 투구 간 리프레시 타임 아웃 부여
                
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 완벽한 볼 배합의 승리입니다."; }}
                if (game.b >= 4) {{ 
                    if (myRole === "pitcher") game.oppScore++; else game.pScore++;
                    game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 제구가 무너지며 볼넷 출루를 허용합니다."; 
                }}
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0;
                    document.getElementById('commentary').innerHTML = "🚨 <b>이닝 종료! 공수 교대 타임!</b> 다음 이닝이 곧 전개됩니다.";
                }}
                updateScreen();
            }}

            function updateScreen() {{
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function runMainLoop() {{
                ctx.clearRect(0, 0, 720, 360);

                // 야구 그라운드 로우 앵글 흙 텍스처
                ctx.fillStyle = "#a66a38"; ctx.beginPath();
                ctx.moveTo(0, 360); ctx.lineTo(720, 360); ctx.lineTo(400, 150); ctx.lineTo(320, 150);
                ctx.closePath(); ctx.fill();

                // 가라앉은 실제 스트라이크 존 렌더
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5;
                ctx.strokeRect(300, 200, 120, 100);

                // 마운드 위 투수 포지션 고정
                ctx.fillStyle = "#4ea8de";
                ctx.beginPath(); ctx.arc(360, 135, 6, 0, Math.PI*2); ctx.fill();
                ctx.fillRect(356, 141, 8, 12);

                // 반대편 타석 우타자 상시 대기 모습
                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.arc(460, 250, 10, 0, Math.PI*2); ctx.fill();
                ctx.fillRect(453, 260, 14, 30);

                // 타자 모드일 때 AI가 정해진 딜레이 후 실감나는 볼 배합 자동 투구
                if (myRole === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let pool = ["포심 직구", "슬라이더", "체인지업"];
                        ball.name = pool[Math.floor(Math.random() * pool.length)];
                        ball.tx = 290 + Math.random() * 140;
                        ball.ty = 190 + Math.random() * 120;
                        ball.x = 360; ball.y = 135; ball.z = 0; ball.size = 2;
                        ball.active = true;
                        isSwung = false;
                        document.getElementById('commentary').innerHTML = "🎙️ 상대 투수가 와인드업 후 공을 뿌렸습니다! 구종은 확인할 수 없습니다, 들어옵니다!";
                    }}
                }}

                // 실시간 물리 법칙 궤적 렌더링 시스템 (구종 무빙 세분화)
                if (ball.active) {{
                    ball.z += 0.024; // 공이 날아오는 속도

                    ball.x = 360 + (ball.tx - 360) * ball.z;
                    ball.y = 140 + (ball.ty - 140) * ball.z;
                    ball.size = 2 + (Math.pow(ball.z, 3.8) * 32);

                    // 포심 직구: 정교한 직선 궤적
                    // 슬라이더: 횡으로 날카롭게 꺾이는 꺾임 구현
                    if (ball.name === "슬라이더") {{
                        ball.x += Math.sin(ball.z * Math.PI) * 55;
                    }}
                    // 체인지업: 홈플레이트 앞에서 뚝 떨어지는 종 무빙 효과
                    if (ball.name === "체인지업") {{
                        ball.y += Math.pow(ball.z, 2) * 35;
                    }}

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (myRole === "pitcher") evalAiBatter();

                    // 포수 미트 뒤로 지나갔을 때 (루킹 삼진/볼넷 판정)
                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 200 && ball.ty <= 300);
                        if (insideZone) {{ 
                            game.s++; 
                            document.getElementById('commentary').innerHTML = "🎙️ 루킹 스트라이크! 완벽한 보더라인 제구로 꽂아 넣습니다."; 
                        }} else {{ 
                            game.b++; 
                            document.getElementById('commentary').innerHTML = "🎙️ 유인구 판정 볼! 타자가 영리하게 잘 골라냈습니다."; 
                        }}
                        nextPitchSequence();
                    }}
                }}

                // 타격 배트 스윙 인터랙션
                if (swingFrame > 0) {{
                    ctx.save();
                    let ratio = (swingFrame / 10) * Math.PI;
                    ctx.translate(430, 260);
                    ctx.rotate(-ratio + Math.PI/3);
                    ctx.strokeStyle = "#e63946"; ctx.lineWidth = 8;
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-65, -20); ctx.stroke();
                    ctx.restore();
                    swingFrame--;
                }}

                requestAnimationFrame(runMainLoop);
            }}

            updateScreen();
            runMainLoop();
        </script>
        """
        st.components.v1.html(game_html, height=500)
