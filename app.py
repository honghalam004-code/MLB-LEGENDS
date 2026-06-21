import streamlit as st

def main():
    st.set_page_config(page_title="MLB INNINGS", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
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
            <div style="background: #1c2541; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #3a86ff; max-width: 600px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 900;">⚾ 9이닝 리얼 공수교대 매치</h1>
                <p style="color: #94a3b8; margin-top: 5px;">3아웃을 잡으면 공수교대! 수비수 위치에 따라 안타와 아웃이 갈립니다.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏟️ 경기 시작 (플레이어 초공격)"):
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_board, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("### 📋 경기 운영 규칙")
        st.info("🔄 **자동 공수교대**\n\n현재 이닝에서 3아웃을 기록하면 투수와 타자 역할이 자동으로 전환됩니다. 전광판의 포지션 표시를 확인하세요!")
        st.markdown("---")
        if st.button("🔄 게임 리셋"):
            st.session_state.game_active = False
            st.rerun()

    with col_board:
        game_html = """
        <div style="background: #0b1329; padding: 12px; border-radius: 12px; border: 2px solid #1c2541; max-width: 740px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; display: flex; justify-content: space-between; color: white;">
                <div>
                    <span id="current-turn" style="background: #3a86ff; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 10px;">초 공격 (타자)</span>
                    <span style="color: #4cc9f0; font-weight: bold;">나</span> <span id="score-p" style="font-size: 18px; font-weight: 900; color: #4cc9f0;">0</span> 
                    <span style="color: #64748b; margin: 0 5px;">:</span> 
                    <span id="score-opp" style="font-size: 18px; font-weight: 900; color: #f72585;">0</span> <span style="color: #f72585; font-weight: bold;">AI</span>
                </div>
                <div>
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 15px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballField" width="720" height="380" style="background: #143615; border: 2px solid #3a86ff; display: block; border-radius: 6px;"></canvas>
            
            <div id="pitcher-controls" style="margin-top: 8px; text-align: center; display: none;">
                <button onclick="setPitch('직구')" style="background: #1d3557; color: white; border: 1px solid #3a86ff; padding: 6px 12px; border-radius: 4px; font-weight: bold; cursor: pointer;">⚾ 직구</button>
                <button onclick="setPitch('슬라이더')" style="background: #1d3557; color: white; border: 1px solid #3a86ff; padding: 6px 12px; border-radius: 4px; font-weight: bold; cursor: pointer;">🔮 슬라이더</button>
                <button onclick="setPitch('체인지업')" style="background: #1d3557; color: white; border: 1px solid #3a86ff; padding: 6px 12px; border-radius: 4px; font-weight: bold; cursor: pointer;">🍂 체인지업</button>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 700; margin-top: 6px; border-left: 5px solid #3a86ff; text-align: left;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 플레이어가 먼저 타석에 들어섭니다! 공을 노려치세요!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            // 전역 경기 상태 (기본 플레이어 타자 시작 -> 3아웃 시 교대)
            let currentMode = "batter"; // "batter" = 플레이어가 타자, "pitcher" = 플레이어가 투수
            let game = { pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 };
            let ball = { active: false, x: 360, y: 140, z: 0, tx: 360, ty: 270, size: 2, name: "직구" };
            
            let selectedPitch = "직구";
            let aiPitchTimer = 60;
            let isSwung = false;
            let swingFrame = 0;

            // 실제 야구 수비수 위치 좌표 데이터
            let fielders = [
                { pos: "유격수", x: 260, y: 130 },
                { pos: "2루수", x: 460, y: 130 },
                { pos: "3루수", x: 210, y: 190 },
                { pos: "1루수", x: 510, y: 190 },
                { pos: "좌익수", x: 160, y: 70 },
                { pos: "중견수", x: 360, y: 50 },
                { pos: "우익수", x: 560, y: 70 }
            ];

            function setPitch(type) {
                selectedPitch = type;
                document.getElementById('commentary').innerHTML = "🎯 투수 사인 보냄: [" + type + "]. 존 안을 클릭해 투구하세요.";
            }

            canvas.addEventListener('mousedown', (e) => {
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left;
                let my = e.clientY - rect.top;

                if (currentMode === "pitcher") {
                    // 내가 투수일 때 클릭하면 투구
                    if (!ball.active) {
                        ball.name = selectedPitch;
                        ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 140; ball.z = 0; ball.size = 2;
                        ball.active = true; isSwung = false;
                    }
                } else {
                    // 내가 타자일 때 클릭하면 타격 타임
                    if (ball.active && !isSwung) {
                        isSwung = true; swingFrame = 10;
                        evalBatterSwing();
                    }
                }
            });

            // 플레이어가 투수일 때 AI 타자의 반응
            function evalAiBatter() {
                if (ball.active && !isSwung && ball.z >= 0.85 && ball.z <= 0.93) {
                    isSwung = true;
                    let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 210 && ball.ty <= 310);
                    if (insideZone) {
                        if (Math.random() > 0.45) { evaluateHitTrajectory(true); } 
                        else { game.s++; ball.active = false; checkInningStatus(); }
                    } else {
                        if (Math.random() > 0.7) { game.s++; ball.active = false; checkInningStatus(); }
                    }
                }
            }

            // 플레이어가 타자일 때 내가 휘두른 타격 판정
            function evalBatterSwing() {
                let insideZone = (ball.x >= 300 && ball.x <= 420 && ball.y >= 210 && ball.y <= 310);
                if (ball.z >= 0.83 && ball.z <= 0.94) {
                    if (insideZone) {
                        evaluateHitTrajectory(false); // 수비수 위치 계산 구동
                    } else {
                        game.o++; document.getElementById('commentary').innerText = "🎙️ 해설: 유인구에 방망이가 밀리면서 허무하게 아웃당합니다.";
                        ball.active = false; checkInningStatus();
                    }
                } else {
                    game.s++; document.getElementById('commentary').innerText = "🎙️ 캐스터: 스트라이크! 타이밍을 아예 못 맞췄습니다.";
                    ball.active = false; checkInningStatus();
                }
            }

            // 🎯 단순 확률이 아닌, 칠 때마다 무작위로 날아가는 타구와 수비수 사이의 거리를 계산하는 엔진
            function evaluateHitTrajectory(isAiHitter) {
                // 타구 낙하지점 무작위 생성 (그라운드 내부)
                let hitX = 150 + Math.random() * 420;
                let hitY = 40 + Math.random() * 180;
                
                // 가장 가까운 수비수 찾기
                let closestFielder = null;
                let minDist = 999;
                
                fielders.forEach(f => {
                    let dist = Math.sqrt(Math.pow(f.x - hitX, 2) + Math.pow(f.y - hitY, 2));
                    if (dist < minDist) {
                        minDist = dist;
                        closestFielder = f;
                    }
                });

                ball.active = false;

                // 수비수와 낙하지점 거리가 55 미만이면 수비 범위 내로 간주하여 아웃!
                if (minDist < 55) {
                    game.o++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 아! [" + closestFielder.pos + "] 정면으로 가는 타구! 안정적으로 포구하면서 아웃 처리합니다.";
                } else {
                    if (isAiHitter) game.oppScore++; else game.pScore++;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 쳤습니다! 빈 공간을 완벽하게 가르는 안타! 주자 베이스를 밟습니다!";
                }
                checkInningStatus();
            }

            // 🔄 이닝 아웃 카운트를 감시하여 실시간으로 공수를 교대시키는 함수
            function checkInningStatus() {
                aiPitchTimer = 70;
                if (game.s >= 3) { game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 삼진 아웃! 타자가 허탈하게 들어갑니다."; }
                if (game.b >= 4) { if (currentMode === "pitcher") game.oppScore++; else game.pScore++; game.s = 0; game.b = 0; document.getElementById('commentary').innerText = "🎙️ 볼넷 선언! 걸어서 출루합니다."; }
                
                if (game.o >= 3) {
                    game.o = 0; game.s = 0; game.b = 0;
                    
                    // 공수 교대 스위칭
                    if (currentMode === "batter") {
                        currentMode = "pitcher";
                        document.getElementById('current-turn').innerText = "말 수비 (투수)";
                        document.getElementById('current-turn').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 이제 마운드에 올라가 공을 던질 차례입니다.";
                    } else {
                        currentMode = "batter";
                        document.getElementById('current-turn').innerText = "초 공격 (타자)";
                        document.getElementById('current-turn').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none';
                        document.getElementById('commentary').innerHTML = "🚨 <b>3아웃 공수교대!</b> 공수가 전환되어 타석에 입장합니다.";
                    }
                }
                updateScreen();
            }

            function updateScreen() {
                document.getElementById('score-p').innerText = game.pScore;
                document.getElementById('score-opp').innerText = game.oppScore;
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }

            function drawScene() {
                ctx.clearRect(0, 0, 720, 380);

                // 야구 경기장 그라운드 잔디 & 흙 그리기
                ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 380);
                ctx.fillStyle = "#a66a38"; ctx.beginPath();
                ctx.moveTo(0, 380); ctx.lineTo(720, 380); ctx.lineTo(390, 130); ctx.lineTo(330, 130);
                ctx.closePath(); ctx.fill();

                // 가상의 스트라이크 존 프레임
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2;
                ctx.strokeRect(300, 210, 120, 100);

                // 🧤 필드 수비수들 캐릭터 도트 렌더링
                fielders.forEach(f => {
                    ctx.fillStyle = "#1e6091"; ctx.fillRect(f.x - 6, f.y, 12, 10);
                    ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(f.x, f.y - 4, 4, 0, Math.PI*2); ctx.fill();
                });

                // ⚾ 투수 디테일 렌더
                ctx.fillStyle = "#d90429"; ctx.fillRect(353, 135, 14, 15);
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(360, 130, 5, 0, Math.PI*2); ctx.fill();

                // 🏏 타자 디테일 렌더
                ctx.fillStyle = "#ffffff"; ctx.fillRect(452, 260, 16, 22);
                ctx.fillStyle = "#fbc4ab"; ctx.beginPath(); ctx.arc(460, 254, 6, 0, Math.PI*2); ctx.fill();

                // 플레이어가 타자(공격)일 때 AI 투수가 자동으로 판단하여 피칭 동작 가동
                if (currentMode === "batter" && !ball.active) {
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {
                        let pool = ["직구", "슬라이더", "체인지업"];
                        ball.name = pool[Math.floor(Math.random() * pool.length)];
                        ball.tx = 290 + Math.random() * 140; ball.ty = 200 + Math.random() * 110;
                        ball.x = 360; ball.y = 135; ball.z = 0; ball.size = 2;
                        ball.active = true; isSwung = false;
                    }
                }

                // 날아오는 야구공 투구 역학 구현
                if (ball.active) {
                    ball.z += 0.025;
                    ball.x = 360 + (ball.tx - 360) * ball.z;
                    ball.y = 140 + (ball.ty - 140) * ball.z;
                    ball.size = 2 + (Math.pow(ball.z, 3.8) * 32);

                    if (ball.name === "슬라이더") ball.x += Math.sin(ball.z * Math.PI) * 55;
                    if (ball.name === "체인지업") ball.y += Math.pow(ball.z, 2) * 35;

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher") evalAiBatter();

                    if (ball.z >= 1.0) {
                        ball.active = false;
                        let insideZone = (ball.tx >= 300 && ball.tx <= 420 && ball.ty >= 210 && ball.ty <= 310);
                        if (insideZone) game.s++; else game.b++;
                        checkInningStatus();
                    }
                }

                // 배트 휘두르기 모션 효과
                if (swingFrame > 0) {
                    ctx.save();
                    let ratio = (swingFrame / 10) * Math.PI;
                    ctx.translate(430, 260); ctx.rotate(-ratio + Math.PI/3);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7;
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-65, -15); ctx.stroke();
                    ctx.restore(); swingFrame--;
                } else {
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 4;
                    ctx.beginPath(); ctx.moveTo(455, 255); ctx.lineTo(440, 220); stroke();
                }

                requestAnimationFrame(drawScene);
            }

            updateScreen();
            drawScene();
        </script>
        """
        st.components.v1.html(game_html, height=520)

if __name__ == "__main__":
    main()
