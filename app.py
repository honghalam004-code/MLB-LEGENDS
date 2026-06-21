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
            st.info("🎯 **투구 방법**\n하단 구종을 정한 뒤 캔버스 내 스트라이크 존 주변을 클릭해 던지세요. 수비수들이 뒤에서 대기 중입니다!")
        else:
            st.info("🏏 **타격 방법**\n공이 날아올 때 타이밍을 맞춰 클릭하세요! 외야 수비수들이 공을 잡으러 이동하므로 틈새를 노려야 합니다.")
        
        st.markdown("---")
        if st.button("🚪 경기 종료 (메인 리셋)"):
            st.session_state.game_active = False
            st.rerun()

    with col_board:
        game_html = f"""
        <div style="background: #0b1329; padding: 12px; border-radius: 12px; border: 2px solid #1c2541; max-width: 740px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #00b4d8; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; display: flex; justify-content: space-between; color: white;">
                <div>
                    <span style="color: #00b4d8; font-weight: bold;">PLAYER</span> <span id="score-p" style="font-size: 18px; font-weight: 900; color: #00b4d8;">0</span> 
                    <span style="color: #64748b; margin: 0 10px;">VS</span> 
                    <span style="color: #f72585; font-weight: bold;">{st.session_state.opp_team}</span> <span id="score-opp" style="font-size: 18px; font-weight: 900; color: #f72585;">0</span>
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
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 수비수들이 각자 포지션에서 넓게 수비 시프트를 잡고 투수를 바라봅니다.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            const myRole = "{st.session_state.game_role}"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 }};
            let ball = {{ active: false, x: 360, y: 140, z: 0, tx: 360, ty: 270, size: 2, speed: 98, name: "포심 직구" }};
            
            let selectedPitch = "포심 직구";
            let aiPitchTimer = 100;
            let isSwung = false;
            let swingFrame = 0;

            // 🧤 라이브 수비수 데이터 세팅 (X, Y 좌표 및 호수비 모션용)
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
                document.getElementById('commentary').innerHTML = "🎯 투수 구종 결정: <span style='color: #ffb703;'>" + type + "</span> 사인을 보냈습니다. 존 안을 클릭하여 투구하세요.";
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
                        ball.x = 360; ball.y = 140; ball.z = 0; ball.size = 2;
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

            function evalAiBatter() {{
                if (ball.active && !isSwung && ball.z >= 0.84 && ball.z <= 0.92) {{
                    isSwung = true;
                    let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 210 && ball.ty <= 310);
                    
                    if (insideZone) {{
                        if (Math.random() > 0.5) {{
                            triggerDefenseAction(true); // 수비수들이 공을 수비하러 움직임
                        }} else {{
                            game.s++;
                            document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 완벽한 제구! AI 타자가 배트를 내밀었지만 허공을 가릅니다!";
                            ball.active = false;
                            nextPitchSequence();
                        }}
                    }} else {{
                        if (Math.random() > 0.7) {{
                            game.s++;
                            document.getElementById('commentary').innerHTML = "🎙️ 해설: 떨어지는 유인구에 배트가 낚였습니다! 삼진을 향해 갑니다.";
                            ball.active = false;
                            nextPitchSequence();
                        }}
                    }}
                }}
            }}

            function evalBatterSwing() {{
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 210 && ball.y <= 310);
                
                if (ball.z >= 0.83 && ball.z <= 0.94) {{
                    if (insideZone) {{
                        let hitRand = Math.random();
                        if (hitRand > 0.82) {{
                            game.pScore += 1;
                            document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 완전히 홈런 직격탄!! 수비수들이 고개만 늘어뜨린 채 바라봅니다, 홈런!!!";
                            ball.active = false;
                            nextPitchSequence();
                        }} else {{
                            triggerDefenseAction(false); // 수비 판정 돌입
                        }}
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 해설: 볼을 건드렸어요. 빗맞은 타구가 유격수 정면으로 가면서 아웃입니다.";
                        ball.active = false;
                        nextPitchSequence();
                    }}
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 스트라이크! 포수가 공을 꽉 잡아냅니다. 스윙 타이밍 미스!";
                    ball.active = false;
                    nextPitchSequence();
                }}
            }}

            // 🧤 타격 시 수비수가 반응하여 움직이고 막아내는 연출 코어
            function triggerDefenseAction(isAiHitter) {{
                let targetFielder = fielders[Math.floor(Math.random() * fielders.length)];
                
                // 수비수 이동 연출 효과
                targetFielder.x += (Math.random() > 0.5 ? 25 : -25);
                
                setTimeout(() => {{
                    let defenseSuccess = Math.random() > 0.4; // 60% 확률로 수비수가 잡아냄
                    if (defenseSuccess) {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 아! [" + targetFielder.pos + "]가 빠르게 따라붙어 몸을 날려 공을 안전하게 낚아챕니다! 호수비 아웃!";
                    }} else {{
                        if (isAiHitter) game.oppScore++; else game.pScore++;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 수비수 사이를 날카롭게 뚫고 나가는 총알 같은 안타입니다! 진루 성공!";
                    }}
                    ball.active = false;
                    nextPitchSequence();
                }}, 400);
            }}

            function nextPitchSequence() {{
                aiPitchTimer = 110;
                // 수비수 위치 리셋
                fielders.forEach(f => f.x = f.ox);

                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 결정구 궤적이 통했습니다."; }}
                if (game.b >= 4) {{ 
                    if (myRole === "pitcher") game.oppScore++; else game.pScore++;
                    game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 볼넷 허용, 출루권을 넘겨줍니다."; 
                }}
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0;
                    document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 체인지!</b> 이닝이 종료되어 공수가 바뀝니다.";
                }}
                updateScreen();
            }}

            function updateScreen() {{
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            // 🎨 디테일 도트 캐릭터 및 야구장 그리기 함수
            function drawScene() {{
                ctx.clearRect(0, 0, 720, 380);

                // 야구 필드 배경
                ctx.fillStyle = "#8a5a36"; ctx.beginPath();
                ctx.moveTo(0, 380); ctx.lineTo(720, 380); ctx.lineTo(390, 130); ctx.lineTo(330, 130);
                ctx.closePath(); ctx.fill();

                // 낮은 스트라이크 존 
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5;
                ctx.strokeRect(300, 210, 120, 100);

                // 🧤 상시 수비수 캐릭터 렌더링 (파란 유니폼 모자 + 상체 도트 비주얼)
                fielders.forEach(f => {{
                    ctx.fillStyle = "#1e6091"; ctx.fillRect(f.x - 6, f.y, 12, 10); // 유니폼 몸통
                    ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(f.x, f.y - 4, 4, 0, Math.PI*2); ctx.fill(); // 얼굴
                    ctx.fillStyle = "#014f86"; ctx.fillRect(f.x - 5, f.y - 9, 10, 3); // 팀 모자
                    ctx.fillStyle = "#ffb703"; ctx.fillRect(f.x + (f.ox > 360 ? -10 : 4), f.y + 2, 5, 5); // 글러브
                }});

                // ⚾ 유니폼 입은 투수 도트 캐릭터 구현 (마운드 위)
                let pX = 360, pY = 135;
                ctx.fillStyle = "#d90429"; ctx.fillRect(pX - 7, pY, 14, 15); // 빨간 원정 유니폼
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(pX, pY - 5, 5, 0, Math.PI*2); ctx.fill(); // 얼굴
                ctx.fillStyle = "#ef233c"; ctx.fillRect(pX - 6, pY - 11, 12, 3); // 모자
                ctx.fillStyle = "#ffffff"; ctx.fillRect(pX - 3, pY + 4, 6, 4); // 등번호 백넘버 디테일

                // 🏏 타석 준비 자세 타자 도트 캐릭터 구현
                let bX = 460, bY = 260;
                ctx.fillStyle = "#ffffff"; ctx.fillRect(bX - 8, bY, 16, 22); // 홈 백색 유니폼
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(bX, bY - 6, 6, 0, Math.PI*2); ctx.fill(); // 얼굴
                ctx.fillStyle = "#0077b6"; ctx.fillRect(bX - 6, bY - 13, 12, 4); // 헬멧

                // 타자 모드일 때 AI 투수 자동 피칭 딜레이 계산
                if (myRole === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let pool = ["포심 직구", "슬라이더", "체인지업"];
                        ball.name = pool[Math.floor(Math.random() * pool.length)];
                        ball.tx = 290 + Math.random() * 140;
                        ball.ty = 200 + Math.random() * 110;
                        ball.x = 360; ball.y = 135; ball.z = 0; ball.size = 2;
                        ball.active = true;
                        isSwung = false;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 투수 와인드업 이후 공을 강하게 뿌립니다! 구종 예측 불허!";
                    }}
                }}

                // 공 날아오는 메커니즘 엔진 (구종 무빙 세분화)
                if (ball.active) {{
                    ball.z += 0.025; 
                    ball.x = 360 + (ball.tx - 360) * ball.z;
                    ball.y = 140 + (ball.ty - 140) * ball.z;
                    ball.size = 2 + (Math.pow(ball.z, 3.8) * 32);

                    if (ball.name === "슬라이더") ball.x += Math.sin(ball.z * Math.PI) * 55;
                    if (ball.name === "체인지업") ball.y += Math.pow(ball.z, 2) * 35;

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (myRole === "pitcher") evalAiBatter();

                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 210 && ball.ty <= 310);
                        if (insideZone) {{ game.s++; document.getElementById('commentary').innerHTML = "🎙️ 루킹 스트라이크! 꼼짝 못 하고 삼진 카운트를 내어줍니다."; }}
                        else {{ game.b++; document.getElementById('commentary').innerHTML = "🎙️ 볼! 완전히 가슴 쪽으로 빠지는 나쁜 공 유도 성공."; }}
                        nextPitchSequence();
                    }}
                }}

                // 리얼 나무 배트 그래픽 및 스윙 처리
                if (swingFrame > 0) {{
                    ctx.save();
                    let ratio = (swingFrame / 10) * Math.PI;
                    ctx.translate(430, 260);
                    ctx.rotate(-ratio + Math.PI/3);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7; // 나무색 컬러 배트 
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-65, -15); ctx.stroke();
                    ctx.restore();
                    swingFrame--;
                }} else {{
                    // 기본 어깨에 메고 있는 대기 자세 배트
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
