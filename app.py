import streamlit as st

def main():
    # 1. 페이지 초기 기본 설정 (브라우저 타이틀 및 레이아웃 확장)
    st.set_page_config(page_title="MAJOR LEAGUE BASEBALL LIVE", layout="wide")
    
    # 2. 프로 야구 게임 전용 스타디움 다크 딥블루 테마 스타일 적용
    st.markdown("""
        <style>
        .main { 
            background-color: #0b1329; 
            color: #f8fafc; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        }
        .stSelectbox > div > div {
            background-color: #1c2541 !important;
            color: #ffffff !important;
            border: 2px solid #3a86ff !important;
            border-radius: 8px !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: #ffffff !important; 
            font-weight: 800 !important; 
            font-size: 16px !important;
            border-radius: 8px !important; 
            border: none !important;
            padding: 10px 20px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(58, 134, 255, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. 게임 세션 상태 정의 및 관리
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 4. 게임 오프닝 및 팀 선택 메인 로비 (정식 구단 이름 반영)
    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 750px; margin: 50px auto; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900; letter-spacing: 1px;">⚾ 9이닝 메이저리그 리얼 정면 매치</h1>
                <p style="color: #94a3b8; margin-top: 10px; font-size: 16px;">포수 시점 3D 투구, 기습 번트, 도루 작전, 공수교대가 완벽히 연동되는 고증 버전</p>
            </div>
        """, unsafe_allow_html=True)
        
        column_left, column_right = st.columns(2)
        
        with column_left:
            user_selected_team = st.selectbox(
                "🏃 내 플레이어 구단 선택", 
                ["Los Angeles Dodgers (로스앤젤레스 다저스)", "New York Yankees (뉴욕 양키스)", "San Diego Padres (샌디에이고 파드리스)", "San Francisco Giants (샌프란시스코 자이언츠)"]
            )
            
        with column_right:
            ai_selected_team = st.selectbox(
                "🤖 라이벌 AI 구단 선택", 
                ["New York Yankees (뉴욕 양키스)", "Los Angeles Dodgers (로스앤젤레스 다저스)", "San Francisco Giants (샌프란시스코 자이언츠)", "San Diego Padres (샌디에이고 파드리스)"]
            )
            
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        if st.button("🏟️ 메이저리그 경기장 입장 (플레이어 초공격 시작)"):
            st.session_state.player_team_name = user_selected_team.split(" (")[0]
            st.session_state.ai_team_name = ai_selected_team.split(" (")[0]
            st.session_state.game_active = True
            st.rerun()
            
        st.stop()

    # 5. 인게임 인터페이스 레이아웃 구성
    st.markdown(f"### 🏟️ 메이저리그 라이브 경기: **{st.session_state.player_team_name}** VS **{st.session_state.ai_team_name}**")

    col_game_screen, col_tactics_panel = st.columns([3, 1])

    with col_tactics_panel:
        st.markdown("### 📊 덕아웃 전술 지시")
        st.success("🥎 **포수 시점 야구 가이드**\n\n화면 하단이 홈플레이트(타자 위치)이며, 저 멀리 화면 중앙이 투수 마운드입니다.\n\n공이 투수 손을 떠나 포수미트 방향으로 날아오면서 엄청나게 크게 확대됩니다! 궤적과 타이밍을 정확히 파악하여 배트를 제어하세요.")
        
        st.markdown("---")
        if st.button("🚪 경기 포기 (메인 로비로 후퇴)"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        # 6. HTML 및 브라우저 독립 실행형 JavaScript 엔진 조립
        # (중괄호 escape 문제를 원천 차단하기 위해 파이썬 변수를 명확히 분리 매핑)
        team_p = st.session_state.player_team_name
        team_a = st.session_state.ai_team_name

        game_html = f"""
        <div style="background: #0b1329; padding: 15px; border-radius: 14px; border: 2px solid #1c2541; max-width: 760px; margin: 0 auto; box-shadow: 0 8px 20px rgba(0,0,0,0.4);">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 12px; margin-bottom: 10px; font-family: 'Courier New', monospace; display: flex; justify-content: space-between; align-items: center; color: white;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span id="current-turn-badge" style="background: #3a86ff; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">1회초 공격 (타자)</span>
                    <span style="color: #4cc9f0; font-weight: 800; font-size: 16px;">{team_p}</span> 
                    <span id="score-p" style="font-size: 22px; font-weight: 900; color: #4cc9f0; min-width: 20px; text-align: center;">0</span> 
                    <span style="color: #64748b; font-weight: bold; font-size: 16px;">:</span> 
                    <span id="score-opp" style="font-size: 22px; font-weight: 900; color: #f72585; min-width: 20px; text-align: center;">0</span> 
                    <span style="color: #f72585; font-weight: 800; font-size: 16px;">{team_a}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span id="runner-diamond-text" style="color: #00b4d8; font-weight: bold; font-size: 14px;">📐 루상 상태: 주자 없음</span>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 16px; background: #121e31; padding: 4px 10px; border-radius: 4px; border: 1px solid #23354f;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="420" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px; box-shadow: inset 0 0 40px rgba(0,0,0,0.6);"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px; border: 1px solid #2e3d68;">
                
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px; border-bottom: 1px solid #2e3d68; padding-bottom: 8px;">
                    <span style="color: #f8fafc; font-weight: bold; margin-right: 10px; font-size: 14px;">⚾ 투수 구종 결정:</span>
                    <button onclick="setPitch('직구')" style="background: #d90429; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; margin-right: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">포심 직구 (Fast)</button>
                    <button onclick="setPitch('슬라이더')" style="background: #023e8a; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; margin-right: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">슬라이더 (Slider)</button>
                    <button onclick="setPitch('체인지업')" style="background: #f77f00; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">체인지업 (Change)</button>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <span style="color: #f8fafc; font-weight: bold; margin-right: 10px; font-size: 14px;">🏏 타자 팀 전술 지시:</span>
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 7px 22px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px; margin-right: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: background 0.2s;">📐 기습 번트 대기</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 7px 22px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: background 0.2s;">🏃 1루 주자 도루 감행!</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700; margin-top: 8px; border-left: 6px solid #3a86ff; text-align: left; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <span id="commentary" style="color: #90e0ef; line-height: 1.5;">🎙️ 중계석: 메이저리그 정규 시즌 경기가 드디어 막을 올립니다! 플레이어가 먼저 1회초 타석에 들어서며 투수를 노려봅니다.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            // --- 1. 전역 게임 엔진 데이터 초기화 (압축 절대 금지 원칙) ---
            let currentMode = "batter"; // "batter" = 플레이어가 타자(공격), "pitcher" = 플레이어가 투수(수비)
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0, hasRunner: false }};
            
            // 포수 원근 시점 설계: 공은 저 멀리 투수 마운드(x:360, y:150, z:0)에서 내 눈앞 홈플레이트(z:1)로 전진 확대
            let ball = {{ active: false, x: 360, y: 150, z: 0, tx: 360, ty: 320, size: 2, name: "직구" }};
            
            let selectedPitch = "직구";
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;
            let isBuntMode = false;

            // 정식 수비 시프트 포지션 데이터 바인딩
            let fielders = [
                {{ pos: "유격수", x: 260, y: 140 }},
                {{ pos: "2루수", x: 460, y: 140 }},
                {{ pos: "3루수", x: 220, y: 190 }},
                {{ pos: "1루수", x: 500, y: 190 }},
                {{ pos: "좌익수", x: 150, y: 80 }},
                {{ pos: "중견수", x: 360, y: 60 }},
                {{ pos: "우익수", x: 570, y: 80 }}
            ];

            // --- 2. 투수 구종 장전 시스템 제어 함수 ---
            function setPitch(type) {{
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = "🎯 수비 지시: 투수가 [" + type + "] 사인을 받아들였습니다. 스트라이크 존 프레임 내부를 조준하여 좌클릭하세요!";
            }}

            // --- 3. 정통 기습 번트 메커니즘 엔진 ---
            function triggerBunt() {{
                if (!ball.active || isSwung) {{
                    document.getElementById('commentary').innerText = "❌ 작전 타이밍 미스: 투수가 공을 던진 상태에서만 번트를 댈 수 있습니다.";
                    return;
                }}
                isSwung = true;
                isBuntMode = true;
                swingFrame = 8; // 번트 모션 유지 프레임셋 호출
                
                // 홈플레이트 근처 원근 임계 구간(z축 0.82 ~ 0.96)에 도달했는지 확인
                if (ball.z >= 0.82 && ball.z <= 0.96) {{
                    ball.active = false;
                    let buntChance = Math.random();
                    if (buntChance > 0.45) {{
                        // 희생 번트 혹은 내야 안타 성공 유도 판정
                        game.hasRunner = true;
                        game.o++;
                        document.getElementById('commentary').innerHTML = "📐 번트 성공! 배트에 공을 절묘하게 죽였습니다! 타자는 1루에서 아웃되지만, 루상의 주자는 안전하게 다음 베이스를 확보합니다!";
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 번트 궤적이 포수 바로 정면에 떨어집니다! 포수가 공을 집어 전력 송구, 타자 아웃입니다!";
                    }}
                    checkInningStatus();
                }} else {{
                    game.s++;
                    document.getElementById('commentary').innerText = "🎙️ 해설: 공이 도달하기 전에 너무 빨리 대거나 늦었습니다! 헛번트 처리되며 스트라이크가 올라갑니다.";
                    ball.active = false;
                    checkInningStatus();
                }}
            }}

            // --- 4. 정통 기습 도루 메커니즘 엔진 ---
            function triggerSteal() {{
                if (!game.hasRunner) {{
                    document.getElementById('commentary').innerText = "❌ 작전 불가능: 현재 1루에 진루한 주자가 없어 도루를 시도할 수 없습니다!";
                    return;
                }}
                
                let stealChance = Math.random();
                if (stealChance > 0.5) {{
                    // 도루 성공 시 주자가 홈으로 들어가 점수가 나는 완전한 스코어 연동 구조 처리
                    if (currentMode === "batter") {{
                        game.pScore++;
                    }} else {{
                        game.oppScore++;
                    }}
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "🏃 캐스터: 2루 도루 성공!! AI 포수가 총알같이 송구했으나 주자의 슬라이딩이 더 빨랐습니다! 완전히 뒤집어놓습니다!";
                }} else {{
                    game.o++;
                    game.hasRunner = false;
                    document.getElementById('commentary').innerHTML = "☠️ 해설: 도루 실패! 포수의 완벽한 2루 저격 송구에 주자 태그아웃 당하며 덕아웃 분위기가 가라앉습니다.";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상 상태: 주자 1루" : "📐 루상 상태: 주자 없음";
                checkInningStatus();
            }}

            // --- 5. 마우스 클릭 연동 실시간 메인 피칭/타격 센서 ---
            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left;
                let my = e.clientY - rect.top;

                if (currentMode === "pitcher") {{
                    // 플레이어가 투수일 때: 마우스 찍은 곳이 공의 타겟 최종 목적지 좌표가 됨
                    if (!ball.active) {{
                        ball.name = selectedPitch;
                        ball.tx = mx; 
                        ball.ty = my; 
                        ball.x = 360; 
                        ball.y = 150; 
                        ball.z = 0; 
                        ball.size = 2;
                        ball.active = true; 
                        isSwung = false; 
                        isBuntMode = false;
                    }}
                }} else {{
                    // 플레이어가 타자일 때: 마운드에서 날아오는 공을 일반 풀스윙 타격 처리
                    if (ball.active && !isSwung) {{
                        isSwung = true; 
                        isBuntMode = false; 
                        swingFrame = 10;
                        evalBatterSwing();
                    }}
                }}
            }});

            // --- 6. AI 인공지능 타자의 물리 수읽기 및 타격 엔진 ---
            function evalAiBatter() {{
                if (ball.active && !isSwung && ball.z >= 0.85 && ball.z <= 0.93) {{
                    isSwung = true;
                    let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 240 && ball.ty <= 340);
                    if (insideZone) {{
                        if (Math.random() > 0.48) {{ 
                            evaluateHitTrajectory(true); 
                        }} else {{ 
                            game.s++; ball.active = false; checkInningStatus(); 
                        }}
                    }} else {{
                        // 유인구 배트 유도 공식
                        if (Math.random() > 0.72) {{ 
                            game.s++; ball.active = false; checkInningStatus(); 
                        }}
                    }}
                }}
            }}

            // --- 7. 플레이어 타자 배트 중심 풀스윙 타격 판정 엔진 ---
            function evalBatterSwing() {{
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 240 && ball.y <= 340);
                if (ball.z >= 0.84 && ball.z <= 0.95) {{
                    if (insideZone) {{
                        evaluateHitTrajectory(false);
                    }} else {{
                        game.o++; 
                        document.getElementById('commentary').innerText = "🎙️ 해설: 완전히 빠진 공에 무리하게 큰 스윙을 가져가다 평범한 내야 팝플라이 아웃으로 이어집니다.";
                        ball.active = false; 
                        checkInningStatus();
                    }}
                }} else {{
                    game.s++; 
                    document.getElementById('commentary').innerText = "🎙️ 캐스터: 호쾌하게 돌렸지만 공이 이미 포수미트에 들어간 뒤였습니다! 헛스윙 스트라이크!";
                    ball.active = false; 
                    checkInningStatus();
                }}
            }}

            // --- 8. 물리 낙하지점 기반 리얼 타구 안타/아웃 시뮬레이터 ---
            function evaluateHitTrajectory(isAiHitter) {{
                ball.active = false;
                let hitResultDeterminant = Math.random();

                if (hitResultDeterminant > 0.42) {{
                    // 안타 성공 판정 및 주자 진루 연동 연출
                    if (game.hasRunner) {{
                        if (isAiHitter) game.oppScore += 2; else game.pScore += 2;
                        game.hasRunner = false;
                        document.getElementById('commentary').innerHTML = "🔥 캐스터: 쳤습니다!! 좌중간을 완벽하게 꿰뚫는 싹쓸이 적시 장타!! 1루 주자 전력 질주하여 홈플레이트 클리어, 스코어를 추가합니다!";
                    }} else {{
                        game.hasRunner = true;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 깨끗한 안타입니다! 투수 키를 훌쩍 넘어 외야 잔디밭에 떨어지는 깨끗한 단타로 주자 1루에 진출합니다!";
                    }}
                }} else {{
                    // 외야 수비 정면 라인드라이브 혹은 플라이 아웃 연출
                    game.o++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 잘 맞은 타구였으나 외야수가 워닝 트랙 앞에서 끝까지 쫓아가 안정적으로 캐치해냅니다! 아웃 처리!";
                }}
                document.getElementById('runner-diamond-text').innerText = game.hasRunner ? "📐 루상 상태: 주자 1루" : "📐 루상 상태: 주자 없음";
                checkInningStatus();
            }}

            // --- 9. 이닝 카운트 연동 및 자동 완벽 공수교대 루프 엔진 ---
            function checkInningStatus() {{
                aiPitchTimer = 70;
                
                if (game.s >= 3) {{ 
                    game.o++; game.s = 0; game.b = 0; 
                    document.getElementById('commentary').innerText = "🎙️ 삼진 아웃!! 완벽한 볼 배합에 타자 배트도 내밀지 못하고 물러납니다."; 
                }}
                if (game.b >= 4) {{ 
                    if (currentMode === "pitcher") game.oppScore++; else game.pScore++; 
                    game.s = 0; game.b = 0; game.hasRunner = true;
                    document.getElementById('commentary').innerText = "🎙️ 볼넷 선언! 스트레이트 볼넷으로 타자 걸어 나갑니다."; 
                }}
                
                // 3아웃 발생 시 야구 정식 규칙에 따른 공수 전면 교대 전환 실행
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; 
                    game.hasRunner = false;
                    document.getElementById('runner-diamond-text').innerText = "📐 루상 상태: 주자 없음";
                    
                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비 (투수)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.style.display = 'block';
                        document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('commentary').innerHTML = "🚨 <b>쓰리 아웃 공수교대!</b> 공격이 끝나고 이제 수비로 전환됩니다. 마운드 위 투수 구종을 선택하고 공을 던지세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격 (타자)";
                        document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>쓰리 아웃 공수교대!</b> 이닝이 교체되어 플레이어가 다시 방망이를 잡고 타석에 입장합니다!";
                    }}
                }}
                updateScreen();
            }}

            // --- 10. 실시간 스코어보드 웹 렌더링 업데이트 함수 ---
            function updateScreen() {{
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            // --- 11. 포수 정면 시점 3D 원근 렌더링 그래픽 코어 엔진 ---
            function drawScene() {{
                ctx.clearRect(0, 0, 720, 400);

                // 야구장 그라운드 잔디 필드 도색
                ctx.fillStyle = "#2a9d8f"; 
                ctx.fillRect(0, 0, 720, 400);
                
                // 원근감 반영 외야 흙 펜스 월 레이어 구축
                ctx.fillStyle = "#e76f51"; 
                ctx.beginPath();
                ctx.moveTo(0, 160); ctx.lineTo(720, 160); 
                ctx.lineTo(720, 140); ctx.lineTo(0, 140);
                ctx.closePath(); ctx.fill();

                // 포수 시선용 중앙 흰색 스트라이크 존 프레임 라인 투사
                ctx.strokeStyle = "rgba(255, 255, 255, 0.5)"; 
                ctx.lineWidth = 2.5;
                ctx.strokeRect(300, 240, 120, 100);

                // 멀리 있는 원근 투수 캐릭터 렌더링 (원근 처리를 위해 작게 묘사)
                ctx.fillStyle = "#d90429"; 
                ctx.fillRect(355, 145, 10, 15);
                ctx.fillStyle = "#fbc4ab"; 
                ctx.beginPath(); ctx.arc(360, 141, 4, 0, Math.PI*2); ctx.fill();

                // 가까이 있는 홈플레이트 우타석 타자 캐릭터 렌더링 (앞쪽에 위치하여 크게 묘사)
                ctx.fillStyle = "#ffffff"; 
                ctx.fillRect(452, 260, 24, 46);
                ctx.fillStyle = "#fbc4ab"; 
                ctx.beginPath(); ctx.arc(464, 248, 8, 0, Math.PI*2); ctx.fill();

                // 화면 우측 상단 인게임 다이아몬드 베이스 물리 상황판 드로잉
                ctx.strokeStyle = "#ffffff"; 
                ctx.lineWidth = 2;
                ctx.strokeRect(620, 30, 40, 40);
                
                // 1루 주자 진출 유무 상태에 따라 베이스 라이팅 실시간 점등
                ctx.fillStyle = game.hasRunner ? "#ffb703" : "#3d5a80";
                ctx.fillRect(652, 46, 8, 8);

                // 플레이어가 타자일 때 AI 투수의 지능형 자동 와인드업 투구 타이머 연동
                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let pitchPool = ["직구", "슬라이더", "체인지업"];
                        ball.name = pitchPool[Math.floor(Math.random() * pitchPool.length)];
                        ball.tx = 290 + Math.random() * 140; 
                        ball.ty = 230 + Math.random() * 110;
                        ball.x = 360; 
                        ball.y = 150; 
                        ball.z = 0; 
                        ball.size = 2;
                        ball.active = true; 
                        isSwung = false;
                    }}
                }}

                // ⚾ 포수 시점 전용 3D 야구공 비행 물리 투사 루틴
                if (ball.active) {{
                    ball.z += 0.024; // 공이 포수미트로 날아드는 고정 프레임 속도 지수
                    
                    // 원근법 적용 공식: 멀리 있는 투수(360, 150)에서 유저 조준점(tx, ty)으로 z축 비례 확장
                    ball.x = 360 + (ball.tx - 360) * ball.z;
                    ball.y = 150 + (ball.ty - 150) * ball.z;
                    ball.size = 2.5 + (Math.pow(ball.z, 3.6) * 28); // 다가올수록 엄청 거대하게 커지는 시각 효과 고증

                    // 구종 선택별 무빙 트랙 디테일 고증
                    if (ball.name === "슬라이더") {{
                        ball.x += Math.sin(ball.z * Math.PI) * 62; // 횡 무빙 슬라이드 궤적
                    }}
                    if (ball.name === "체인지업") {{
                        ball.y += Math.pow(ball.z, 2) * 42; // 홈플레이트 앞에서 뚝 떨어지는 종 무빙 궤적
                    }}

                    // 리얼 야구공 실선 드로잉
                    ctx.fillStyle = "#ffffff"; 
                    ctx.strokeStyle = "#000000"; 
                    ctx.lineWidth = 1.2;
                    ctx.beginPath(); 
                    ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); 
                    ctx.fill(); 
                    ctx.stroke();

                    if (currentMode === "pitcher") evalAiBatter();

                    // 공이 포수 뒤 펜스 혹은 미트에 완전히 도달한 경우 스트라이크/볼 이원 판정
                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 240 && ball.ty <= 340);
                        if (insideZone) game.s++; else game.b++;
                        checkInningStatus();
                    }}
                }}

                // 배트 휘두르기 및 수평 기습 번트 메커니즘 그래픽 폼 스위칭
                if (swingFrame > 0) {{
                    ctx.save();
                    if (isBuntMode) {{
                        // 번트: 휘두르지 않고 홈플레이트 정면에 배트를 툭 갖다 대고 있는 정석 포즈 드로잉
                        ctx.strokeStyle = "#b79457"; 
                        ctx.lineWidth = 7;
                        ctx.beginPath(); 
                        ctx.moveTo(430, 280); 
                        ctx.lineTo(335, 280); 
                        ctx.stroke();
                    }} else {{
                        // 풀스윙 야구 배트 궤적 물리 회전각 렌더링
                        let angleRatio = (swingFrame / 10) * Math.PI;
                        ctx.translate(440, 260); 
                        ctx.rotate(-angleRatio + Math.PI / 4);
                        ctx.strokeStyle = "#b79457"; 
                        ctx.lineWidth = 8;
                        ctx.beginPath(); 
                        ctx.moveTo(0, 0); 
                        ctx.lineTo(-76, -10); 
                        ctx.stroke();
                    }}
                    ctx.restore(); 
                    swingFrame--;
                }} else {{
                    // 기본 대기 프레임: 타자가 어깨 뒤로 나무 배트를 꼿꼿이 세우고 서 있는 타격 폼 고증
                    ctx.strokeStyle = "#b79457"; 
                    ctx.lineWidth = 5;
                    ctx.beginPath(); 
                    ctx.moveTo(466, 238); 
                    ctx.lineTo(488, 192); 
                    ctx.stroke();
                }}

                // 브라우저 프레임 동기화 무한 드로우 호출
                requestAnimationFrame(drawScene);
            }}

            // 엔진 가동선 강제 바인딩
            updateScreen();
            drawScene();
        </script>
        """
        st.components.v1.html(game_html, height=580)

if __name__ == "__main__":
    main()
