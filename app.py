import streamlit as st

def main():
    st.set_page_config(page_title="MLB 초정밀 시뮬레이터 v2.0", layout="wide")
    st.title("⚾ MLB Legends: 전 구단 & 투수 커스텀 시뮬레이터")

    # --- [1. MLB 30개 전체 구단 리스트 정의] ---
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

    # --- [2. 상단 사이드바 / 컨트롤러: 팀 및 투수 세팅] ---
    st.sidebar.header("📋 매치업 & 투수 커스텀 설정")
    
    # 팀 선택
    away_team = st.sidebar.selectbox("⚾ 원정 팀 (AWAY) 선택:", mlb_teams, index=18) # 기본 양키스
    home_team = st.sidebar.selectbox("🏠 홈 팀 (HOME) 선택:", mlb_teams, index=13) # 기본 다저스
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 투수 능력치 설정")
    pitcher_name = st.sidebar.text_input("투수 이름 입력:", "나만의 에이스")
    
    # 구종별 최고 구속 및 제구력 커스텀 (스트림릿 슬라이더 활용)
    st.sidebar.write("**🔥 포심 직구 세팅**")
    fb_speed = st.sidebar.slider("직구 최고 구속 (mph)", 85, 105, 98)
    fb_control = st.sidebar.slider("직구 제구력 (1-100)", 1, 100, 85, key="fb_c")

    st.sidebar.write("**🔮 슬라이더 세팅**")
    sl_speed = st.sidebar.slider("슬라이더 구속 (mph)", 75, 95, 88)
    sl_control = st.sidebar.slider("슬라이더 제구력 (1-100)", 1, 100, 75, key="sl_c")

    st.sidebar.write("**🟢 커브 세팅**")
    cb_speed = st.sidebar.slider("커브 구속 (mph)", 65, 88, 78)
    cb_control = st.sidebar.slider("커브 제구력 (1-100)", 1, 100, 70, key="cb_c")

    # 구종 라디오 버튼 (현재 어떤 구종을 장착하고 던질지 캔버스 전송용)
    selected_pitch = st.radio("🔮 현재 장착할 구종 선택:", ["포심 직구", "슬라이더", "커브"], horizontal=True)

    # 현재 선택된 구종의 능력치 매핑
    current_speed = fb_speed if selected_pitch == "포심 직구" else (sl_speed if selected_pitch == "슬라이더" else cb_speed)
    current_control = fb_control if selected_pitch == "포심 직구" else (sl_control if selected_pitch == "슬라이더" else cb_control)

    st.markdown(f"**현재 선택된 투구 조합:** `{pitcher_name}`의 `{selected_pitch}` (설정 구속: {current_speed} mph / 제구력: {current_control})")

    # --- [3. 실시간 HTML5 캔버스 게임 엔진 빌드] ---
    # 파이썬 변수들을 자바스크립트 엔진 내부로 실시간 주입합니다.
    game_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background-color: #1e1e1e; padding: 15px; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
        <div style="width: 780px; background-color: #0b2211; border: 3px solid #fff; border-radius: 8px; display: flex; justify-content: space-between; padding: 10px; margin-bottom: 15px; color: #ffeb3b; font-family: 'Courier New', monospace; font-size: 16px; font-weight: bold;">
            <div>[원정] {away_team} <span id="sb-away" style="color:#fff; font-size:20px;">0</span></div>
            <div>[ <span id="sb-inning">1회 초</span> ]</div>
            <div>[홈] {home_team} <span id="sb-home" style="color:#fff; font-size:20px;">0</span></div>
            <div style="font-size: 14px; color: #aaa;">B:<span id="cnt-b" style="color:#4caf50;">○○○</span> S:<span id="cnt-s" style="color:#ffeb3b;">○○</span> O:<span id="cnt-o" style="color:#f44336;">○○</span></div>
        </div>
        
        <canvas id="gameCanvas" width="800" height="400" style="border: 1px solid #444; background-color: #145214; border-radius: 6px;"></canvas>
        
        <div id="live-log" style="width: 780px; height: 100px; background-color: #000; color: #00ff00; font-family: monospace; padding: 10px; margin-top: 15px; border-radius: 6px; overflow-y: auto; font-size: 14px; line-height: 1.5;">
            [SYSTEM] 마우스로 우측 스트라이크 존을 겨냥하고 클릭하세요. (현재 구종: {selected_pitch})
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 파이썬 환경에서 전달된 실시간 커스텀 투수 스탯 데이터
        const customPitchData = {{
            name: "{pitcher_name}",
            type: "{selected_pitch}",
            baseSpeed: {current_speed},
            control: {current_control}
        }};

        let gameState = {{
            awayScore: 0, homeScore: 0, inning: 1, isTop: true,
            balls: 0, strikes: 0, outs: 0,
            bases: [false, false, false],
            batter: "Aaron Judge"
        }};

        let mouseX = 0, mouseY = 0;
        let isPitching = false;
        let ballX = 200, ballY = 230;
        let targetX = 0, targetY = 0;
        let lastPitches = [];

        canvas.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            mouseX = event.clientX - rect.left;
            mouseY = event.clientY - rect.top;
        }});

        canvas.addEventListener('click', () => {{
            if (isPitching) return;
            if (mouseX >= 400 && mouseX <= 700 && mouseY >= 50 && mouseY <= 350) {{
                // 제구력 수치 반영 (제구력이 낮을수록 목표 조준점에서 공이 더 크게 휘청임)
                let errorRange = (100 - customPitchData.control) * 0.6;
                targetX = mouseX + (Math.random() - 0.5) * errorRange;
                targetY = mouseY + (Math.random() - 0.5) * errorRange;
                
                ballX = 200;
                ballY = 230;
                isPitching = true;
            }}
        }});

        const logBox = document.getElementById('live-log');
        function addLog(text) {{
            logBox.innerHTML = `> ${{text}}<br>` + logBox.innerHTML;
        }}

        function updateScoreboard() {{
            document.getElementById('sb-away').innerText = gameState.awayScore;
            document.getElementById('sb-home').innerText = gameState.homeScore;
            document.getElementById('sb-inning').innerText = `${{gameState.inning}}회 ${{gameState.isTop ? '초' : '말'}}`;
            document.getElementById('cnt-b').innerText = '●'.repeat(gameState.balls) + '○'.repeat(3 - gameState.balls);
            document.getElementById('cnt-s').innerText = '●'.repeat(gameState.strikes) + '○'.repeat(2 - gameState.strikes);
            document.getElementById('cnt-o').innerText = '●'.repeat(gameState.outs) + '○'.repeat(3 - gameState.outs);
        }}

        function judgePitch(tx, ty) {{
            const isStrike = (tx >= 480 && tx <= 620 && ty >= 120 && ty <= 280);
            
            // 설정한 구속에 무작위 변동폭 2mph 가미
            const finalSpeed = customPitchData.baseSpeed + Math.floor(Math.random() * 5) - 2;
            
            // 타자 스윙 AI (구속이 빠를수록 타자가 속을 확률과 헛스윙 확률 상승)
            let speedBonus = (finalSpeed - 85) * 0.01; // 100mph에 가까울수록 보너스 증가
            const swingChance = isStrike ? (0.6 - speedBonus) : (0.2 + speedBonus);
            const isSwing = Math.random() < swingChance;

            if (isSwing) {{
                // 스윙 시 구속이 빠르면 헛스윙 확률이 극대화됨
                let missChance = 0.5 + speedBonus;
                if (Math.random() > missChance) {{ 
                    const hitType = Math.random();
                    if (hitType < 0.1) {{ 
                        gameState.strikes = 0; gameState.balls = 0;
                        let runs = gameState.bases.filter(b => b).length + 1;
                        if(gameState.isTop) gameState.awayScore += runs; else gameState.homeScore += runs;
                        gameState.bases = [false, false, false];
                        addLog(`🚀 💥 대형 홈런!!! ${{gameState.batter}}가 ${{customPitchData.name}}의 ${{customPitchData.type}}(${{finalSpeed}} mph)을 받아쳤습니다!!`);
                    }} else if (hitType < 0.4) {{ 
                        gameState.strikes = 0; gameState.balls = 0;
                        let run = gameState.bases[2] ? 1 : 0;
                        gameState.bases[2] = gameState.bases[1];
                        gameState.bases[1] = gameState.bases[0];
                        gameState.bases[0] = true;
                        if(gameState.isTop) gameState.awayScore += run; else gameState.homeScore += run;
                        addLog(`🔥 안타 성공! 주자 베이스를 채웁니다. (${{finalSpeed}} mph)`);
                    }} else {{ 
                        gameState.strikes = 0; gameState.balls = 0;
                        gameState.outs++;
                        addLog(`⚾ 인플레이 타구 아웃! 야수 정면으로 굴러갑니다.`);
                    }}
                }} else {{
                    gameState.strikes++;
                    addLog(`💨 헛스윙 스트라이크!!! ${{finalSpeed}} mph 강속구에 타자 방망이가 밀립니다!`);
                }}
            }} else {{
                if (isStrike) {{
                    gameState.strikes++;
                    addLog(`🔴 루킹 스트라이크! ${{customPitchData.type}}이 존 구석에 걸칩니다. (${{finalSpeed}} mph)`);
                }} else {{
                    gameState.balls++;
                    addLog(`🟢 볼! 존을 벗어나는 공을 잘 참았습니다. (${{finalSpeed}} mph)`);
                }}
            }}

            if (gameState.strikes >= 3) {{
                gameState.outs++; gameState.strikes = 0; gameState.balls = 0;
                addLog(`❌ K!! 삼진 아웃! ${{customPitchData.name}}의 탈삼진 능력 대폭발.`);
            }}
            if (gameState.balls >= 4) {{
                gameState.strikes = 0; gameState.balls = 0;
                gameState.bases[0] = true;
                addLog(`🚶 볼넷 출루 허용.`);
            }}

            if (gameState.outs >= 3) {{
                gameState.outs = 0; gameState.strikes = 0; gameState.balls = 0;
                gameState.bases = [false, false, false];
                gameState.isTop = !gameState.isTop;
                if(gameState.isTop) gameState.inning++;
                addLog(`🔄 공수 교대! 수비 진형을 변경합니다.`);
            }}

            lastPitches.push({{x: tx, y: ty, isStrike: isStrike}});
            if(lastPitches.length > 5) lastPitches.shift();

            updateScoreboard();
        }}

        function gameLoop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 야구장 드로잉
            ctx.strokeStyle = "rgba(255,255,255,0.4)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(200, 330);
            ctx.lineTo(300, 230);
            ctx.lineTo(200, 130);
            ctx.lineTo(100, 230);
            ctx.closePath();
            ctx.stroke();

            ctx.fillStyle = "#A0522D";
            ctx.beginPath(); ctx.arc(200, 230, 8, 0, Math.PI*2); ctx.fill();
            
            ctx.fillStyle = gameState.bases[0] ? "#f44336" : "#fff";
            ctx.fillRect(295, 225, 10, 10);
            ctx.fillStyle = gameState.bases[1] ? "#f44336" : "#fff";
            ctx.fillRect(195, 125, 10, 10);
            ctx.fillStyle = gameState.bases[2] ? "#f44336" : "#fff";
            ctx.fillRect(95, 225, 10, 10);
            ctx.fillStyle = "#fff"; ctx.fillRect(195, 325, 10, 10);

            // 투수
            ctx.fillStyle = "#e0e0e0";
            ctx.beginPath(); ctx.arc(200, 220, 6, 0, Math.PI*2); ctx.fill();
            ctx.fillRect(196, 226, 8, 12);

            // 타자 & 배트
            ctx.fillStyle = "#64b5f6";
            ctx.beginPath(); ctx.arc(175, 315, 6, 0, Math.PI*2); ctx.fill();
            ctx.fillRect(171, 321, 8, 14);
            ctx.strokeStyle = "#ffb74d";
            ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(175, 320);
            
            // 커브 구종 특수 모션 연출 (배트 낮게 세팅)
            if(customPitchData.type === "커브") {{
                ctx.lineTo(155, 305);
            }} else {{
                ctx.lineTo(160, 290);
            }}
            ctx.stroke();

            // 스트라이크 존
            ctx.fillStyle = "rgba(255, 255, 255, 0.08)";
            ctx.fillRect(480, 120, 140, 160);
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 2;
            ctx.strokeRect(480, 120, 140, 160);
            
            ctx.strokeStyle = "rgba(255,255,255,0.2)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(526, 120); ctx.lineTo(526, 280);
            ctx.moveTo(573, 120); ctx.lineTo(573, 280);
            ctx.moveTo(480, 173); ctx.lineTo(620, 173);
            ctx.moveTo(480, 226); ctx.lineTo(620, 226);
            ctx.stroke();

            ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
            ctx.strokeRect(430, 70, 240, 260);

            // 조준선
            if (mouseX >= 400 && mouseX <= 700 && mouseY >= 50 && mouseY <= 350 && !isPitching) {{
                ctx.strokeStyle = "#ffeb3b";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(mouseX - 15, mouseY); ctx.lineTo(mouseX + 15, mouseY);
                ctx.moveTo(mouseX, mouseY - 15); ctx.lineTo(mouseX + 15, mouseY); // 가이드 크로스
                ctx.moveTo(mouseX, mouseY - 15); ctx.lineTo(mouseX, mouseY + 15);
                ctx.stroke();
                ctx.beginPath(); ctx.arc(mouseX, mouseY, 6, 0, Math.PI*2); ctx.stroke();
            }

            // 흔적 잔상
            lastPitches.forEach(p => {{
                ctx.fillStyle = p.isStrike ? "rgba(244, 67, 54, 0.6)" : "rgba(33, 150, 243, 0.6)";
                ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI*2); ctx.fill();
            }});

            // 실시간 비행 및 휘어지는 궤적 계산 (구종별 특성 반영)
            if (isPitching) {{
                // 기본 직선 이동
                ballX += (targetX - ballX) * 0.16;
                ballY += (targetY - ballY) * 0.16;

                // 변화구 궤적 무브먼트 연출 (슬라이더는 횡 변화, 커브는 종 변화)
                let dist = Math.abs(ballX - targetX);
                if (customPitchData.type === "슬라이더" && dist > 10) {{
                    ballX += 1.2; // 오른쪽으로 휨
                }} else if (customPitchData.type === "커브" && dist > 10) {{
                    ballY += 1.8; // 아래로 뚝 떨어짐
                }}

                let ballRadius = 4 + (1 - dist / 400) * 4;
                ctx.fillStyle = "#ffffff";
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.arc(ballX, ballY, ballRadius, 0, Math.PI*2);
                ctx.fill();
                ctx.stroke();

                if (dist < 2) {{
                    isPitching = false;
                    judgePitch(targetX, targetY);
                }}
            }}

            requestAnimationFrame(gameLoop);
        }}

        updateScoreboard();
        gameLoop();
    </script>
    """
    st.components.v1.html(game_html, height=620)

if __name__ == "__main__":
    main()
