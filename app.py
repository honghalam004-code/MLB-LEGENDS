import streamlit as st

def main():
    st.set_page_config(page_title="MLB 초정밀 시뮬레이터 v3.0", layout="wide")
    
    # 타이틀바 디자인 개선
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <h1 style="color: #ffffff; margin: 0; font-family: 'Segoe UI', Roboto, sans-serif; font-weight: 800; letter-spacing: 2px;">⚾ MLB LEGENDS DIGITAL ARENA</h1>
            <p style="color: #00e676; margin: 5px 0 0 0; font-weight: 500;">Next-Gen Interactive Pitching Simulator</p>
        </div>
    """, unsafe_allow_html=True)

    # --- [1. MLB 30개 전체 구단 리스트] ---
    mlb_teams = [
        "애리조나 다이아몬드백스", "애틀랜타 브레이브스", "볼티모어 오리올스", "보스턴 레드삭스", 
        "시카고 컵스", "시카고 화이트삭스", "신시내티 레즈", "클리블랜드 가디언스", 
        "콜로라도 로키스", "디트로이트 타이거스", "휴스턴 애스트로스", "캔자스시티 로열스", 
        "로스앤젤레스 에인절스", "로스앤젤레스 다저스", "마이애미 말린스", "밀워키 브루어스", 
        "미네소타 트윈스", "뉴욕 메츠", "뉴욕 양키스", "오클랜드 애슬레틱스", 
        "필라델피아 필리스", "피츠버그 파이어리츠", "샌디에이고 파드리스", "샌프란시스코 자이언츠", 
        "시애틀 매리너스", "세인트루이스 카디널스", "탬파베이 레이스", "텍사스 레인저스", 
        "토론토 블루제이스", "워싱턴 내셔널스"
    ]

    # --- STEP 1: 팀 및 투수 기본 선택 (사이드바 없이 상단에 배치) ---
    st.markdown("### 🛠️ 1단계: 경기 팀 및 투수 등록")
    col_t1, col_t2, col_t3 = st.columns([1, 1, 1])
    
    with col_t1:
        away_team = st.selectbox("⚾ 원정 팀 (AWAY):", mlb_teams, index=18)
    with col_t2:
        home_team = st.selectbox("🏠 홈 팀 (HOME):", mlb_teams, index=13)
    with col_t3:
        pitcher_name = st.text_input("👤 투수 이름:", "나만의 에이스")

    st.markdown("---")

    # --- STEP 2: 경기 그래픽 화면 (중앙 배치) ---
    st.markdown("### 🎮 2단계: 실시간 스트라이크 존 타겟팅")

    # 임시 변수 매핑용 (아래 상세 컨트롤에서 받아올 값들 미리 기본 정의)
    fb_speed, fb_control = 98, 85
    sl_speed, sl_control = 88, 75
    cb_speed, cb_control = 78, 70

    # --- [3. 메인 게임 UI 및 하단 컨트롤러 설계] ---
    # 레이아웃을 깔끔하게 정리하기 위해 하단 슬라이더와 구종 선택을 하단으로 내렸습니다.
    # 그래픽은 네온 스타일 테두리와 스태디움 전광판 느낌으로 전면 교체했습니다.
    
    raw_game_html = """
    <div style="display: flex; flex-direction: column; align-items: center; background-color: #0b0f19; padding: 20px; border-radius: 16px; box-shadow: 0px 10px 30px rgba(0,0,0,0.7); border: 1px solid #1f293d;">
        
        <div style="width: 100%; max-width: 820px; background: linear-gradient(180deg, #111827, #1f2937); border: 2px solid #374151; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; margin-bottom: 20px; color: #fff; font-family: 'Segoe UI', sans-serif;">
            <div style="text-align: left;">
                <span style="font-size: 12px; color: #9ca3af; display:block; text-transform:uppercase; letter-spacing:1px;">AWAY</span>
                <span style="font-size: 20px; font-weight: 800; color: #f3f4f6;">__AWAY_TEAM__</span>
                <span id="sb-away" style="font-size: 28px; font-weight: 900; color: #38bdf8; margin-left: 15px;">0</span>
            </div>
            <div style="text-align: center; background: #111827; padding: 8px 20px; border-radius: 30px; border: 1px solid #4b5563;">
                <span id="sb-inning" style="font-size: 16px; font-weight: 700; color: #facc15; letter-spacing: 1px;">1회 초</span>
            </div>
            <div style="text-align: right;">
                <span id="sb-home" style="font-size: 28px; font-weight: 900; color: #38bdf8; margin-right: 15px;">0</span>
                <span style="font-size: 12px; color: #9ca3af; display:block; text-transform:uppercase; letter-spacing:1px;">HOME</span>
                <span style="font-size: 20px; font-weight: 800; color: #f3f4f6;">__HOME_TEAM__</span>
            </div>
        </div>

        <div style="width: 100%; max-width: 820px; display:flex; justify-content: center; gap: 40px; background: #111827; padding: 10px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #1f293d; font-family: monospace; font-size: 16px; font-weight: bold;">
            <div>BALL <span id="cnt-b" style="letter-spacing:4px; font-size:18px;">🟢🟢🟢</span></div>
            <div>STRIKE <span id="cnt-s" style="letter-spacing:4px; font-size:18px;">🟡🟡</span></div>
            <div>OUT <span id="cnt-o" style="letter-spacing:4px; font-size:18px;">🔴🔴</span></div>
        </div>
        
        <canvas id="gameCanvas" width="840" height="420" style="border: 1px solid #1f293d; background: radial-gradient(circle, #0f172a 0%, #020617 100%); border-radius: 12px; box-shadow: inset 0 0 40px rgba(0,0,0,0.8);"></canvas>
        
        <div id="live-log" style="width: 100%; max-width: 820px; height: 90px; background-color: #020617; color: #38bdf8; font-family: 'Courier New', monospace; padding: 12px; margin-top: 20px; border-radius: 8px; overflow-y: auto; font-size: 14px; line-height: 1.6; border: 1px solid #1e293b; box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);">
            [SYSTEM] 경기장에 입장했습니다. 하단에서 구종을 변경하고 스트라이크 존에 마우스를 클릭해 투구하세요!
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const customPitchData = {
            name: "__PITCHER_NAME__",
            type: "__SELECTED_PITCH__",
            baseSpeed: __CURRENT_SPEED__,
            control: __CURRENT_CONTROL__
        };

        let gameState = {
            awayScore: 0, homeScore: 0, inning: 1, isTop: true,
            balls: 0, strikes: 0, outs: 0,
            bases: [false, false, false],
            batter: "Aaron Judge"
        };

        let mouseX = 0, mouseY = 0;
        let isPitching = false;
        let ballX = 220, ballY = 240; 
        let targetX = 0, targetY = 0;
        let lastPitches = [];

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouseX = event.clientX - rect.left;
            mouseY = event.clientY - rect.top;
        });

        canvas.addEventListener('click', () => {
            if (isPitching) return;
            // 캔버스 우측 투구 가능 영역 잠금
            if (mouseX >= 450 && mouseX <= 780 && mouseY >= 50 && mouseY <= 370) {
                let errorRange = (100 - customPitchData.control) * 0.5;
                targetX = mouseX + (Math.random() - 0.5) * errorRange;
                targetY = mouseY + (Math.random() - 0.5) * errorRange;
                
                ballX = 220;
                ballY = 240;
                isPitching = true;
            }
        });

        const logBox = document.getElementById('live-log');
        function addLog(text) {
            logBox.innerHTML = `<span style="color:#facc15;">➔</span> ${text}<br>` + logBox.innerHTML;
        }

        function updateScoreboard() {
            document.getElementById('sb-away').innerText = gameState.awayScore;
            document.getElementById('sb-home').innerText = gameState.homeScore;
            document.getElementById('sb-inning').innerText = `${gameState.inning}회 ${gameState.isTop ? '초' : '말'}`;
            
            document.getElementById('cnt-b').innerHTML = '<span style="color:#22c55e;">●</span>'.repeat(gameState.balls) + '<span style="color:#374151;">○</span>'.repeat(3 - gameState.balls);
            document.getElementById('cnt-s').innerHTML = '<span style="color:#eab308;">●</span>'.repeat(gameState.strikes) + '<span style="color:#374151;">○</span>'.repeat(2 - gameState.strikes);
            document.getElementById('cnt-o').innerHTML = '<span style="color:#ef4444;">●</span>'.repeat(gameState.outs) + '<span style="color:#374151;">○</span>'.repeat(3 - gameState.outs);
        }

        function judgePitch(tx, ty) {
            const isStrike = (tx >= 530 && tx <= 700 && ty >= 130 && ty <= 310);
            const finalSpeed = customPitchData.baseSpeed + Math.floor(Math.random() * 5) - 2;
            
            let speedBonus = (finalSpeed - 85) * 0.01;
            const swingChance = isStrike ? (0.58 - speedBonus) : (0.22 + speedBonus);
            const isSwing = Math.random() < swingChance;

            if (isSwing) {
                let missChance = 0.48 + speedBonus;
                if (Math.random() > missChance) { 
                    const hitType = Math.random();
                    if (hitType < 0.12) { 
                        gameState.strikes = 0; gameState.balls = 0;
                        let runs = gameState.bases.filter(b => b).length + 1;
                        if(gameState.isTop) gameState.awayScore += runs; else gameState.homeScore += runs;
                        gameState.bases = [false, false, false];
                        addLog(`<span style="color:#ef4444; font-weight:bold;">[HOMERUN]</span> ${gameState.batter}가 ${customPitchData.name}의 ${customPitchData.type}을 걷어 올려 담장을 넘깁니다!! (${finalSpeed} mph)`);
                    } else if (hitType < 0.42) { 
                        gameState.strikes = 0; gameState.balls = 0;
                        let run = gameState.bases[2] ? 1 : 0;
                        gameState.bases[2] = gameState.bases[1];
                        gameState.bases[1] = gameState.bases[0];
                        gameState.bases[0] = true;
                        if(gameState.isTop) gameState.awayScore += run; else gameState.homeScore += run;
                        addLog(`<span style="color:#22c55e;">[HIT]</span> 깔끔한 안타! 주자 베이스 러닝 진루 성공. (${finalSpeed} mph)`);
                    } else { 
                        gameState.strikes = 0; gameState.balls = 0;
                        gameState.outs++;
                        addLog(`[OUT] 내야 땅볼 아웃! 유격수가 깔끔하게 처리합니다.`);
                    }
                } else {
                    gameState.strikes++;
                    addLog(`[STRIKE] 배트 허공을 가릅니다, 완전히 타이밍을 뺏은 헛스윙! (${finalSpeed} mph)`);
                }
            } else {
                if (isStrike) {
                    gameState.strikes++;
                    addLog(`[STRIKE] 허를 찌르는 한가운데 루킹 스트라이크 꽂힙니다! (${finalSpeed} mph)`);
                } else {
                    gameState.balls++;
                    addLog(`[BALL] 예리하게 빠지는 볼을 타자가 골라냅니다.`);
                }
            }

            if (gameState.strikes >= 3) {
                gameState.outs++; gameState.strikes = 0; gameState.balls = 0;
                addLog(`<span style="color:#eab308; font-weight:bold;">[SO]</span> 삼진 아웃!! 완벽한 결정구 통했습니다.`);
            }
            if (gameState.balls >= 4) {
                gameState.strikes = 0; gameState.balls = 0;
                gameState.bases[0] = true;
                addLog(`[BB] 포볼, 1루 출루 허용.`);
            }

            if (gameState.outs >= 3) {
                gameState.outs = 0; gameState.strikes = 0; gameState.balls = 0;
                gameState.bases = [false, false, false];
                gameState.isTop = !gameState.isTop;
                if(gameState.isTop) gameState.inning++;
                addLog(`[SYSTEM] 이닝 교대! 수비 교대 들어갑니다.`);
            }

            lastPitches.push({x: tx, y: ty, isStrike: isStrike});
            if(lastPitches.length > 6) lastPitches.shift();

            updateScoreboard();
        }

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // --- 1. 네온 퓨처리스틱 디자인 피치 필드 (좌측) ---
            ctx.strokeStyle = "rgba(56, 189, 248, 0.2)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(220, 340); ctx.lineTo(320, 240); ctx.lineTo(220, 140); ctx.lineTo(120, 240);
            ctx.closePath(); ctx.stroke();

            // 투수 피칭 홈 그라운드 써클
            ctx.fillStyle = "rgba(30, 41, 59, 0.6)";
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 2;
            ctx.beginPath(); ctx.arc(220, 240, 10, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            
            // 다크 테마 주자 루 베이스 시각화
            function drawNeonBase(bx, by, occupied) {
                ctx.fillStyle = occupied ? "#ef4444" : "#1e293b";
                ctx.strokeStyle = occupied ? "#f87171" : "#4b5563";
                ctx.lineWidth = 2;
                ctx.save();
                ctx.translate(bx, by);
                ctx.rotate(45 * Math.PI / 180);
                ctx.fillRect(-6, -6, 12, 12);
                ctx.strokeRect(-6, -6, 12, 12);
                ctx.restore();
            }
            drawNeonBase(320, 240, gameState.bases[0]); // 1루
            drawNeonBase(220, 140, gameState.bases[1]); // 2루
            drawNeonBase(120, 240, gameState.bases[2]); // 3루
            
            // 홈 플레이트 세련되게 드로잉
            ctx.fillStyle = "#f3f4f6";
            ctx.beginPath();
            ctx.moveTo(220, 335); ctx.lineTo(230, 345); ctx.lineTo(230, 352);
            ctx.lineTo(210, 352); ctx.lineTo(210, 345);
            ctx.closePath(); ctx.fill();

            // 사이버 스타일 투수/타자 위젯 리얼 디자인
            // 투수 라인업 마킹
            ctx.fillStyle = "#64748b";
            ctx.beginPath(); ctx.arc(220, 230, 5, 0, Math.PI*2); ctx.fill();
            
            // 타자 스탠딩 라인 마킹
            ctx.fillStyle = "#38bdf8";
            ctx.beginPath(); ctx.arc(195, 335, 5, 0, Math.PI*2); ctx.fill();
            // 타자 배팅 스틱
            ctx.strokeStyle = "#fb923c";
            ctx.lineWidth = 3.5;
            ctx.beginPath(); ctx.moveTo(195, 340);
            if(customPitchData.type === "커브") {
                ctx.lineTo(175, 325);
            } else {
                ctx.lineTo(180, 310);
            }
            ctx.stroke();

            // 구분 센터 스플릿 디바이더 라인
            ctx.strokeStyle = "rgba(55, 65, 81, 0.4)";
            ctx.lineWidth = 1;
            ctx.setLineDash([4, 6]);
            ctx.beginPath(); ctx.moveTo(420, 20); ctx.lineTo(420, 400); ctx.stroke();
            ctx.setLineDash([]);

            // --- 2. 하이테크 스타일 스트라이크 존 (우측) ---
            // 내부 스트라이크 영역 (K-ZONE 테마)
            ctx.fillStyle = "rgba(56, 189, 248, 0.04)";
            ctx.fillRect(530, 130, 170, 180);
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 3;
            ctx.strokeRect(530, 130, 170, 180);
            
            // 정밀 9분할 구획 격자 어두운 매트릭스 스타일
            ctx.strokeStyle = "rgba(56, 189, 248, 0.15)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(586, 130); ctx.lineTo(586, 310);
            ctx.moveTo(643, 130); ctx.lineTo(643, 310);
            ctx.moveTo(530, 190); ctx.lineTo(700, 190);
            ctx.moveTo(530, 250); ctx.lineTo(700, 250);
            ctx.stroke();

            // 외곽 볼 라운드 존 테두리 경계선
            ctx.strokeStyle = "rgba(75, 85, 99, 0.5)";
            ctx.lineWidth = 1;
            ctx.strokeRect(470, 70, 290, 300);

            // 사이드 정보 텍스트 UI 가이드라인
            ctx.fillStyle = "rgba(156, 163, 175, 0.8)";
            ctx.font = "12px sans-serif";
            ctx.fillText("TARGET ZONE (우측 영역 클릭)", 530, 55);
            ctx.fillText("BATTER: " + gameState.batter, 120, 390);

            // --- 3. 세련된 매트 마우스 크로스헤어 (Aim 조준점) ---
            if (mouseX >= 450 && mouseX <= 780 && mouseY >= 50 && mouseY <= 370 && !isPitching) {
                ctx.strokeStyle = "#facc15";
                ctx.lineWidth = 1.5;
                // 타겟 외곽 링
                ctx.beginPath(); ctx.arc(mouseX, mouseY, 8, 0, Math.PI*2); ctx.stroke();
                // 십자 에임 크로스
                ctx.beginPath();
                ctx.moveTo(mouseX - 12, mouseY); ctx.lineTo(mouseX + 12, mouseY);
                ctx.moveTo(mouseX, mouseY - 12); ctx.lineTo(mouseX, mouseY + 12);
                ctx.stroke();
            }

            // --- 4. 히스토리 3D 구질 잔상 흔적 마킹 ---
            lastPitches.forEach((p, idx) => {
                ctx.fillStyle = p.isStrike ? "rgba(239, 68, 68, 0.75)" : "rgba(56, 189, 248, 0.75)";
                ctx.strokeStyle = "#fff";
                ctx.lineWidth = 1;
                ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI*2); ctx.fill(); ctx.stroke();
                
                // 마지막 투구점 마킹에 미세 스팟 서클 효과 추가
                if(idx === lastPitches.length - 1) {
                    ctx.strokeStyle = "#facc15";
                    ctx.lineWidth = 2;
                    ctx.beginPath(); ctx.arc(p.x, p.y, 11, 0, Math.PI*2); ctx.stroke();
                }
            });

            // --- 5. 유기적인 투구 무브먼트 60FPS 역동 물리 가속 계산 ---
            if (isPitching) {
                ballX += (targetX - ballX) * 0.15;
                ballY += (targetY - ballY) * 0.15;

                let dist = Math.abs(ballX - targetX);
                // 실시간 구종 브레이킹볼 물리 특성 변화 렌더링
                if (customPitchData.type === "슬라이더" && dist > 15) {
                    ballX += 1.4; 
                } else if (customPitchData.type === "커브" && dist > 15) {
                    ballY += 2.0; 
                }

                let ballRadius = 3.5 + (1 - dist / 450) * 4.5;
                // 공 그림자 3D 효과 부여
                ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
                ctx.shadowBlur = 4;
                
                ctx.fillStyle = "#ffffff";
                ctx.strokeStyle = "#1e293b";
                ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(ballX, ballY, ballRadius, 0, Math.PI*2); ctx.fill(); ctx.stroke();
                
                // 그림자 초기화
                ctx.shadowBlur = 0;

                if (dist < 2) {
                    isPitching = false;
                    judgePitch(targetX, targetY);
                }
            }

            requestAnimationFrame(gameLoop);
        }

        updateScoreboard();
        gameLoop();
    </script>
    """

    final_html = (
        raw_game_html
        .replace("__AWAY_TEAM__", away_team)
        .replace("__HOME_TEAM__", home_team)
        .replace("__PITCHER_NAME__", pitcher_name)
    )

    # --- STEP 3: 하단 컨트롤러 레이아웃 (요청하신 대로 아래 배치) ---
    st.markdown("### ⚙️ 3단계: 구종 선택 및 투수 세부 스펙 튜닝")
    
    col_ctrl1, col_ctrl2 = st.columns([1, 2])
    
    with col_ctrl1:
        selected_pitch = st.radio(
            "🔮 던질 구종 선택:", 
            ["포심 직구", "슬라이더", "커브"], 
            horizontal=False
        )
    
    with col_ctrl2:
        if selected_pitch == "포심 직구":
            fb_speed = st.slider("직구 최고 구속 (mph)", 85, 105, 98)
            fb_control = st.slider("직구 제구력 스탯 (1-100)", 1, 100, 85)
            current_speed, current_control = fb_speed, fb_control
        elif selected_pitch == "슬라이더":
            sl_speed = st.slider("슬라이더 구속 (mph)", 75, 95, 88)
            sl_control = st.slider("슬라이더 제구력 스탯 (1-100)", 1, 100, 75)
            current_speed, current_control = sl_speed, sl_control
        else:
            cb_speed = st.slider("커브 구속 (mph)", 65, 88, 78)
            cb_control = st.slider("커브 제구력 스탯 (1-100)", 1, 100, 70)
            current_speed, current_control = cb_speed, cb_control

    # 실시간 선택 값 주입 데이터 바인딩 완성
    final_html = (
        final_html
        .replace("__SELECTED_PITCH__", selected_pitch)
        .replace("__CURRENT_SPEED__", str(current_speed))
        .replace("__CURRENT_CONTROL__", str(current_control))
    )

    st.components.v1.html(final_html, height=660)

if __name__ == "__main__":
    main()
