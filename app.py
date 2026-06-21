import streamlit as st

def main():
    st.set_page_config(page_title="MLB BEHIND THE PLATE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox { background: #1c2541 !important; color: white !important; border: 2px solid #3a86ff !important; }
        .stButton>button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: white !important; font-weight: bold; border-radius: 6px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #3a86ff; max-width: 700px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 900;">🏟️ MLB 리얼 포수 시점 라이브 매치</h1>
                <p style="color: #94a3b8; margin-top: 5px;">투수 정면 뷰, 번트 폼, 도루 메커니즘이 완벽 고증된 진짜 야구 게임</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            p_team = st.selectbox("🏃 나의 팀", ["LA Dodgers", "NY Yankees", "SD Padres"])
        with c2:
            a_team = st.selectbox("🤖 상대 팀", ["NY Yankees", "LA Dodgers", "SF Giants"])
            
        if st.button("🏟️ 스타디움 입장 (플레이어 초공격)"):
            st.session_state.p_name = p_team
            st.session_state.a_name = a_team
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 🏟️ {st.session_state.p_name} VS {st.session_state.a_name}")

    col_board, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("### 🎮 덕아웃 작전판")
        st.info("💡 **포수 시점 플레이 팁**\n\n* 저 멀리 마운드에서 공이 출발합니다!\n* **직구:** 정면으로 빠르게 확대됩니다.\n* **슬라이더:** 오다가 옆으로 꺾입니다.\n* **체인지업:** 오다가 뚝 떨어집니다.\n* 타이밍을 맞춰 존 안의 공을 타격하세요.")
        st.markdown("---")
        if st.button("🚪 타이틀로 돌아가기"):
            st.session_state.game_active = False
            st.rerun()

    with col_board:
        game_html = f"""
        <div style="background: #0b1329; padding: 12px; border-radius: 12px; border: 2px solid #1c2541; max-width: 740px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; display: flex; justify-content: space-between; color: white;">
                <div>
                    <span id="current-turn" style="background: #3a86ff; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 10px;">초 공격 (타자)</span>
                    <span style="color: #4cc9f0; font-weight: bold;">{st.session_state.p_name}</span> <span id="score-p" style="font-size: 18px; font-weight: 900; color: #4cc9f0;">0</span> 
                    <span style="color: #64748b; margin: 0 5px;">:</span> 
                    <span id="score-opp" style="font-size: 18px; font-weight: 900; color: #f72585;">0</span> <span style="color: #f72585; font-weight: bold;">{st.session_state.a_name}</span>
                </div>
                <div>
                    <span id="runner-state" style="color: #00b4d8; font-weight: bold; margin-right: 10px;">🔴 루상: 주자 없음</span>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 15px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="400" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 6px;"></canvas>
            
            <div style="margin-top: 8px; text-align: center; background: #1c2541; padding: 10px; border-radius: 6px;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 5px;">
                    <span style="color: white; font-weight: bold; margin-right: 5px;">[투수 구종 선택]</span>
                    <button onclick="setPitch('직구')" style="background: #d90429; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">⚾ 포심 직구</button>
                    <button onclick="setPitch('슬라이더')" style="background: #023e8a; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">🔮 슬라이더</button>
                    <button onclick="setPitch('체인지업')" style="background: #f77f00; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">🍂 체인지업</button>
                </div>
                <div id="batter-controls" style="display: block;">
                    <span style="color: white; font-weight: bold; margin-right: 5px;">[타자 실시간 작전]</span>
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 6px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 8px;">🏏 기습 번트 대기</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 6px 20px; border-radius: 4px; font-weight: bold; cursor: pointer;">🏃 1루 주자 도루!</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 700; margin-top: 6px; border-left: 5px solid #3a86ff; text-align: left;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 플레이어가 타석에서 포수 시점으로 투수를 정면 응시합니다. 긴장되는 순간입니다!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0, hasRunner: false }};
            // 포수 시점: 공이 저 멀리(z=0, x=360, y=160)에서 앞쪽(z=1, y=320)으로 다가옴
            let ball = {{ active: false, x: 360, y: 160, z: 0, tx: 360, ty: 310, size: 2, name: "직구" }};
            
            let selectedPitch = "직구";
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;
            let isBuntMode = false;

            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = "🎯 투수 구종 사인 완료: [" + type + "]. 스트라이크 존을 클릭하면 투구합니다!";
            }}

            // 리얼 번트 모션 및 판정
            function triggerBunt() {{
                if (ball.active && !isSwung) {{
                    isSwung = true;
                    isBuntMode = true;
                    swingFrame = 8;
                    
                    if (ball.z >= 0.82 && ball.z <= 0.95) {{
                        ball.active = false;
                        if (Math.random() > 0.4) {{
                            game.hasRunner = true;
                            game.o++;
                            document.getElementById('commentary').innerHTML = "🎙️ 해설: 절묘한 코스로 공을 죽였습니다! 희생번트 성공, 주자 2루로 진루!";
                        }} else {{
                            game.o++;
                            document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 번트 타구가 포수 바로 앞에 멈추며 홈 아웃 처리됩니다!";
                        }}
                        checkInningStatus();
                    }} else {{
                        game.s++;
                        document.getElementById('commentary').innerText = "🎙️ 캐스터: 파울팁 또는 헛번트 스트라이크!";
                        ball.active = false;
                        checkInningStatus();
                    }}
                }}
            }}

            // 도루 메커니즘
            function triggerSteal() {{
                if (!game.hasRunner) {{
                    document.getElementById('commentary').innerText = "❌ 작전 실패: 현재 루상에 주자가 존재하지 않습니다!";
                    return;
                }}
                if (Math.random() > 0.55) {{
                    if (currentMode === "batter") game.pScore++; else game.oppScore++;
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "🏃 캐스터: 대단합니다! 완전히 투수의 타이밍을 빼앗아 2루 도루에 성공합니다!!";
                }} else {{
                    game.o++;
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "☠️ 해설: 도루 차단! 포수의 미사일 송구에 주자 아웃!";
                }}
                document.getElementById('runner-state').innerText = game.hasRunner ? "📐 루상: 주자 1루" : "🔴 루상: 주자 없음";
                checkInningStatus();
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left;
                let my = e.clientY - rect.top;

                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch;
                        ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 160; ball.z = 0; ball.size = 2;
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
                if (ball.active && !isSwung && ball.z >= 0.86 && ball.z <= 0.94) {{
                    isSwung = true;
                    let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 240 && ball.ty <= 340);
                    if (insideZone) {{
                        if (Math.random() > 0.5) {{ evaluateHitTrajectory(true); }} 
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
                        game.o++; document.getElementById('commentary').innerText = "🎙️ 해설: 하이볼 유인구에 배트가 나가면서 팝플라이 아웃처리됩니다.";
                        ball.active = false; checkInningStatus();
                    }}
                }} else {{
                    game.s++; document.getElementById('commentary').innerText = "🎙️ 캐스터: 타이밍이 완전히 빗나간 헛스윙 스트라이크!";
                    ball.active = false; checkInningStatus();
                }}
            }}

            // 안타 시 주자 진루 연출
            function evaluateHitTrajectory(isAiHitter) {{
                ball.active = false;
                let hitRand = Math.random();

                if (hitRand > 0.4) {{
                    if (game.hasRunner) {{
                        if (isAiHitter) game.oppScore += 2; else game.pScore += 2;
                        game.hasRunner = false;
                        document.getElementById('commentary').innerHTML = "🔥 캐스터: 장타 장타! 우중간을 완전히 갈랐습니다! 루상의 주자 홈인, 타자까지 진루!";
                    }} else {{
                        game.hasRunner = true;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 안타입니다! 투수 키를 넘겨 중견수 앞으로 굴러가는 안타!";
                    }}
                }} else {{
                    game.o++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 잘 맞았으나 외야수 정면! 글러브 속으로 빨려 들어가는 라인드라이브 아웃!";
                }}
                document.getElementById('runner-state').innerText = game.hasRunner ? "📐 루상: 주자 1루" : "🔴 루상: 주자 없음";
                checkInningStatus();
            }}

            function checkInningStatus() {{
                aiPitchTimer = 70;
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 최고의 결정구입니다."; }}
                if (game.b >= 4) {{ 
                    if (currentMode === "pitcher") game.oppScore++; else game.pScore++; 
                    game.s = 0; game.b = 0; game.hasRunner = true;
                    document.getElementById('commentary').innerText = "🎙️ 볼넷! 밀어내기 볼넷으로 출루합니다."; 
                }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; game.hasRunner = false;
                    document.getElementById('runner-state').innerText = "🔴 루상: 주자 없음";
                    
                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn').innerText = "말 수비 (투수)";
                        document.getElementById('current-turn').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block';
                        document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 마운드에 서서 타자를 저격하세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn').innerText = "초 공격 (타자)";
                        document.getElementById('current-turn').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 배트를 쥐고 타석에 들어섭니다.";
                    }}
                }}
                updateScreen();
            }}

            function updateScreen() {{
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            // 🎨 포수 시점 카메라 렌더링 엔진
            function drawScene() {{
                ctx.clearRect(0, 0, 720, 400);

                // 1. 야구장 원근감 잔디 라인 (홈플레이트 중심 뷰)
                ctx.fillStyle = "#2a9d8f"; ctx.fillRect(0, 0, 720, 400);
                
                // 외야 흙 펜스 라인
                ctx.fillStyle = "#e76f51"; ctx.beginPath();
                ctx.moveTo(0, 160); ctx.lineTo(720, 160); ctx.lineTo(720, 140); ctx.lineTo(0, 140);
                ctx.closePath(); ctx.fill();

                // 2. 홈플레이트 뒤쪽 포수용 스트라이크 존 가이드라인
                ctx.strokeStyle = "rgba(255, 255, 255, 0.5)"; ctx.lineWidth = 2;
                ctx.strokeRect(300, 240, 120, 100);

                // 3. 저 멀리 정면에 서 있는 투수 도트 캐릭터 (마운드 원근감 반영으로 작게 렌더)
                ctx.fillStyle = "#d90429"; ctx.fillRect(355, 145, 10, 15); // 유니폼
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(360, 141, 4, 0, Math.PI*2); ctx.fill(); // 얼굴

                // 4. 홈플레이트 근처에 서 있는 좌타자/우타석 캐릭터 (화면 앞이라 크게 렌더)
                ctx.fillStyle = "#ffffff"; ctx.fillRect(450, 260, 24, 45); // 홈팀 유니폼 바디
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(462, 248, 8, 0, Math.PI*2); ctx.fill(); // 타자 머리

                // 5. 우측 상단 미니 야구 다이아몬드 베이스 전광판
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5;
                ctx.strokeRect(620, 30, 40, 40); // 90도 회전된 다이아몬드 베이스 라인
                
                // 루상 주자 있을 때 베이스 불빛 채우기 고증
                ctx.fillStyle = game.hasRunner ? "#ffb703" : "#3d5a80";
                ctx.fillRect(650, 45, 8, 8); // 1루 지점

                // AI 투수 자동 발사 시퀀스 (원근감 출발)
                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let pool = ["직구", "슬라이더", "체인지업"];
                        ball.name = pool[Math.floor(Math.random() * pool.length)];
                        ball.tx = 290 + Math.random() * 140; ball.ty = 230 + Math.random() * 110;
                        ball.x = 360; ball.y = 150; ball.z = 0; ball.size = 2;
                        ball.active = true; isSwung = false;
                    }}
                }}

                // ⚾ 포수 시점 3D 투구 물리 궤적
                if (ball.active) {{
                    ball.z += 0.025; // 홈플레이트로 공이 돌진하는 속도
                    
                    // 원근법 적용: z가 커질수록 투수 마운드(360,150)에서 내가 조준한 포수미트 코스로 확장
                    ball.x = 360 + (ball.tx - 360) * ball.z;
                    ball.y = 150 + (ball.ty - 150) * ball.z;
                    ball.size = 2 + (Math.pow(ball.z, 3.5) * 28); // 다가올수록 엄청 거대해지는 야구공

                    // 구종 마구 무빙 궤적
                    if (ball.name === "슬라이더") ball.x += Math.sin(ball.z * Math.PI) * 60; // 횡으로 휘어짐
                    if (ball.name === "체인지업") ball.y += Math.pow(ball.z, 2) * 40; // 종으로 가라앉음

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.5;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher") evalAiBatter();

                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 240 && ball.ty <= 340);
                        if (insideZone) game.s++; else game.b++;
                        checkInningStatus();
                    }}
                }}

                // 타격 및 기습 번트 모션 렌더링
                if (swingFrame > 0) {{
                    ctx.save();
                    if (isBuntMode) {{
                        // 번트: 배트를 휘두르지 않고 홈플레이트 정면에 수평으로 대고 수비하는 폼 고증
                        ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7;
                        ctx.beginPath(); ctx.moveTo(430, 280); ctx.lineTo(340, 280); ctx.stroke();
                    }} else {{
                        // 풀스윙 메커니즘
                        let ratio = (swingFrame / 10) * Math.PI;
                        ctx.translate(440, 260); ctx.rotate(-ratio + Math.PI/4);
                        ctx.strokeStyle = "#b79457"; ctx.lineWidth = 8;
                        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-75, -10); ctx.stroke();
                    }}
                    ctx.restore(); swingFrame--;
                }} else {{
                    // 평소 대기 상태: 어깨 뒤로 배트를 바짝 올려 세우고 있는 리얼 타격 폼
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 5;
                    ctx.beginPath(); ctx.moveTo(465, 240); ctx.lineTo(485, 195); ctx.stroke();
                }}

                requestAnimationFrame(drawScene);
            }}

            updateScreen();
            drawScene();
        </script>
        """
        st.components.v1.html(game_html, height=560)

if __name__ == "__main__":
    main()
