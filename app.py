import streamlit as st

def main():
    st.set_page_config(page_title="MLB 초정밀 시뮬레이터", layout="wide")
    st.title("⚾ MLB Legends: 실시간 그래픽 매치업")
    st.write("오른쪽 스트라이크 존에 마우스를 올리면 실시간으로 조준선이 움직입니다. 클릭하면 공이 날아갑니다!")

    # 스트림릿 새로고침 없이 브라우저 자체에서 60fps로 돌아가는 야구 게임 엔진 (HTML5 + JS)
    game_html = """
    <div style="display: flex; flex-direction: column; align-items: center; background-color: #1e1e1e; padding: 15px; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
        <div style="width: 780px; background-color: #0b2211; border: 3px solid #fff; border-radius: 8px; display: flex; justify-content: space-between; padding: 10px; margin-bottom: 15px; color: #ffeb3b; font-family: 'Courier New', monospace; font-size: 20px; font-weight: bold;">
            <div>AWAY <span id="sb-away" style="color:#fff;">0</span></div>
            <div>[ <span id="sb-inning">1회 초</span> ]</div>
            <div>HOME <span id="sb-home" style="color:#fff;">0</span></div>
            <div style="font-size: 16px; color: #aaa;">B:<span id="cnt-b" style="color:#4caf50;">○○○</span> S:<span id="cnt-s" style="color:#ffeb3b;">○○</span> O:<span id="cnt-o" style="color:#f44336;">○○</span></div>
        </div>
        
        <canvas id="gameCanvas" width="800" height="400" style="border: 1px solid #444; background-color: #145214; border-radius: 6px;"></canvas>
        
        <div id="live-log" style="width: 780px; height: 100px; background-color: #000; color: #00ff00; font-family: monospace; padding: 10px; margin-top: 15px; border-radius: 6px; overflow-y: auto; font-size: 14px; line-height: 1.5;">
            [SYSTEM] 마우스로 우측 스트라이크 존을 겨냥하고 클릭하세요...
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 게임 상태 변수 (브라우저 메모리에서 실시간 관리)
        let gameState = {
            awayScore: 0, homeScore: 0, inning: 1, isTop: true,
            balls: 0, strikes: 0, outs: 0,
            bases: [false, false, false],
            pitcher: "Gerrit Cole", batter: "Aaron Judge"
        };

        let mouseX = 0, mouseY = 0;
        let isPitching = false;
        let ballX = 200, ballY = 230; // 투수 마운드 시작점
        let targetX = 0, targetY = 0;
        let lastPitches = []; // 던진 공들의 궤적 저장

        // 마우스 움직임 감지 (실시간 조준선용)
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouseX = event.clientX - rect.left;
            mouseY = event.clientY - rect.top;
        });

        // 클릭 시 투구 애니메이션 시작
        canvas.addEventListener('click', () => {
            if (isPitching) return; // 이미 공이 날아가는 중이면 무시
            
            // 스트라이크 존(450~650, 100~300) 근처 클릭 시에만 작동
            if (mouseX >= 400 && mouseX <= 700 && mouseY >= 50 && mouseY <= 350) {
                targetX = mouseX;
                targetY = mouseY;
                ballX = 200;
                ballY = 230;
                isPitching = true;
            }
        });

        // 로그 기록 함수
        const logBox = document.getElementById('live-log');
        function addLog(text) {
            logBox.innerHTML = `> ${text}<br>` + logBox.innerHTML;
        }

        // 전광판 업데이트
        function updateScoreboard() {
            document.getElementById('sb-away').innerText = gameState.awayScore;
            document.getElementById('sb-home').innerText = gameState.homeScore;
            document.getElementById('sb-inning').innerText = `${gameState.inning}회 ${gameState.isTop ? '초' : '말'}`;
            document.getElementById('cnt-b').innerText = '●'.repeat(gameState.balls) + '○'.repeat(3 - gameState.balls);
            document.getElementById('cnt-s').innerText = '●'.repeat(gameState.strikes) + '○'.repeat(2 - gameState.strikes);
            document.getElementById('cnt-o').innerText = '●'.repeat(gameState.outs) + '○'.repeat(3 - gameState.outs);
        }

        // 판정 및 경기 진행 엔진
        function judgePitch(tx, ty) {
            const isStrike = (tx >= 480 && tx <= 620 && ty >= 120 && ty <= 280);
            const speed = Math.floor(Math.random() * 15) + 85;
            
            // 타자 스윙 AI (스트라이크면 60% 확률 스윙, 볼이면 20% 확률 낚임)
            const swingChance = isStrike ? 0.6 : 0.2;
            const isSwing = Math.random() < swingChance;

            if (isSwing) {
                // 스윙했을 때 (컨택 성공 혹은 헛스윙)
                if (Math.random() < 0.4) { // 40% 확률로 타격 성공 (안타/홈런/범타)
                    const hitType = Math.random();
                    if (hitType < 0.1) { // 홈런
                        gameState.strikes = 0; gameState.balls = 0;
                        let runs = gameState.bases.filter(b => b).length + 1;
                        if(gameState.isTop) gameState.awayScore += runs; else gameState.homeScore += runs;
                        gameState.bases = [false, false, false];
                        addLog(`🚀 💥 대폭발!!! ${gameState.batter}의 어마어마한 ${runs}점 홈런!!! (${speed} mph)`);
                    } else if (hitType < 0.4) { // 안타
                        gameState.strikes = 0; gameState.balls = 0;
                        let run = gameState.bases[2] ? 1 : 0;
                        gameState.bases[2] = gameState.bases[1];
                        gameState.bases[1] = gameState.bases[0];
                        gameState.bases[0] = true;
                        if(gameState.isTop) gameState.awayScore += run; else gameState.homeScore += run;
                        addLog(`🔥 짜릿한 안타! 주자 진루! (${speed} mph)`);
                    } else { // 범타 아웃
                        gameState.strikes = 0; gameState.balls = 0;
                        gameState.outs++;
                        addLog(`⚾ 평범한 플라이 아웃! 타자 아웃.`);
                    }
                } else {
                    gameState.strikes++;
                    addLog(`💨 헛스윙 스트라이크!!! 타자의 배트가 허공을 가릅니다! (${speed} mph)`);
                }
            } else {
                // 지켜봤을 때
                if (isStrike) {
                    gameState.strikes++;
                    addLog(`🔴 루킹 스트라이크!!! 완벽하게 꽂히는 공! (${speed} mph)`);
                } else {
                    gameState.balls++;
                    addLog(`🟢 볼! 타자가 침착하게 잘 골라냅니다. (${speed} mph)`);
                }
            }

            // 삼진 및 볼넷 체크
            if (gameState.strikes >= 3) {
                gameState.outs++; gameState.strikes = 0; gameState.balls = 0;
                addLog(`❌ K!! 삼진 아웃! 투수의 완벽한 판정승.`);
            }
            if (gameState.balls >= 4) {
                gameState.strikes = 0; gameState.balls = 0;
                gameState.bases[0] = true;
                addLog(`🚶 볼넷! 타자가 걸어나갑니다.`);
            }

            // 공수 교대
            if (gameState.outs >= 3) {
                gameState.outs = 0; gameState.strikes = 0; gameState.balls = 0;
                gameState.bases = [false, false, false];
                gameState.isTop = !gameState.isTop;
                if(gameState.isTop) gameState.inning++;
                addLog(`🔄 공수 교대! 다음 이닝으로 넘어갑니다.`);
            }

            // 투구 궤적 저장
            lastPitches.push({x: tx, y: ty, isStrike: isStrike});
            if(lastPitches.length > 5) lastPitches.shift(); // 최근 5개만 유지

            updateScoreboard();
        }

        // 메인 루프 (60fps 실시간 그래픽 렌더링)
        function gameLoop() {
            // 배경 청소
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // --- 1. 야구장 필드 (좌측) ---
            ctx.strokeStyle = "rgba(255,255,255,0.4)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(200, 330); // 홈
            ctx.lineTo(300, 230); // 1루
            ctx.lineTo(200, 130); // 2루
            ctx.lineTo(100, 230); // 3루
            ctx.closePath();
            ctx.stroke();

            // 마운드 & 베이스 시각화
            ctx.fillStyle = "#A0522D";
            ctx.beginPath(); ctx.arc(200, 230, 8, 0, Math.PI*2); ctx.fill(); // 마운드
            
            ctx.fillStyle = gameState.bases[0] ? "#f44336" : "#fff"; // 1루
            ctx.fillRect(295, 225, 10, 10);
            ctx.fillStyle = gameState.bases[1] ? "#f44336" : "#fff"; // 2루
            ctx.fillRect(195, 125, 10, 10);
            ctx.fillStyle = gameState.bases[2] ? "#f44336" : "#fff"; // 3루
            ctx.fillRect(95, 225, 10, 10);
            ctx.fillStyle = "#fff"; ctx.fillRect(195, 325, 10, 10); // 홈플레이트

            // --- 2. 타자(배트 드로잉 포함)와 투수 그래픽 ---
            // 투수 실루엣
            ctx.fillStyle = "#e0e0e0";
            ctx.beginPath(); ctx.arc(200, 220, 6, 0, Math.PI*2); ctx.fill(); // 머리
            ctx.fillRect(196, 226, 8, 12); // 몸통

            // 배트를 들고 대기 중인 타자 실루엣
            ctx.fillStyle = "#64b5f6";
            ctx.beginPath(); ctx.arc(175, 315, 6, 0, Math.PI*2); ctx.fill(); // 머리
            ctx.fillRect(171, 321, 8, 14); // 몸통
            // 배트
            ctx.strokeStyle = "#ffb74d";
            ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(175, 320); ctx.lineTo(160, 290); ctx.stroke();

            // --- 3. 실시간 스트라이크 존 격자 (우측) ---
            ctx.fillStyle = "rgba(255, 255, 255, 0.08)";
            ctx.fillRect(480, 120, 140, 160); // 내곽 존
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 2;
            ctx.strokeRect(480, 120, 140, 160);
            
            // 9분할 선선 가이드
            ctx.strokeStyle = "rgba(255,255,255,0.2)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(526, 120); ctx.lineTo(526, 280);
            ctx.moveTo(573, 120); ctx.lineTo(573, 280);
            ctx.moveTo(480, 173); ctx.lineTo(620, 173);
            ctx.moveTo(480, 226); ctx.lineTo(620, 226);
            ctx.stroke();

            // 외곽 볼 인식 테두리 박스
            ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
            ctx.strokeRect(430, 70, 240, 260);

            // --- 4. 실시간 마우스 조준선 (Crosshair) ---
            if (mouseX >= 400 && mouseX <= 700 && mouseY >= 50 && mouseY <= 350 && !isPitching) {
                ctx.strokeStyle = "#ffeb3b";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(mouseX - 15, mouseY); ctx.lineTo(mouseX + 15, mouseY);
                ctx.moveTo(mouseX, mouseY - 15); ctx.lineTo(mouseX, mouseY + 15);
                ctx.stroke();
                // 조준 원
                ctx.beginPath(); ctx.arc(mouseX, mouseY, 6, 0, Math.PI*2); ctx.stroke();
            }

            // --- 5. 과거 던진 공들의 궤적 잔상 표시 ---
            lastPitches.forEach(p => {
                ctx.fillStyle = p.isStrike ? "rgba(244, 67, 54, 0.6)" : "rgba(33, 150, 243, 0.6)";
                ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI*2); ctx.fill();
            });

            // --- 6. 실시간 투구 비행 애니메이션 계산 ---
            if (isPitching) {
                // 투수 마운드에서 조준점까지 매 프레임 선형 보간 이동
                ballX += (targetX - ballX) * 0.15;
                ballY += (targetY - ballY) * 0.15;

                // 공 그리기 (원근감을 주기 위해 날아갈수록 크기가 조금 커짐)
                let dist = Math.abs(ballX - targetX);
                let ballRadius = 4 + (1 - dist / 400) * 4;

                ctx.fillStyle = "#ffffff";
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.arc(ballX, ballY, ballRadius, 0, Math.PI*2);
                ctx.fill();
                ctx.stroke();

                // 목적지에 거의 도달하면 애니메이션 종료 및 판정 처리
                if (dist < 1.5) {
                    isPitching = false;
                    judgePitch(targetX, targetY);
                }
            }

            requestAnimationFrame(gameLoop);
        }

        // 구동 시작
        updateScoreboard();
        gameLoop();
    </script>
    """
    st.components.v1.html(game_html, height=620)

if __name__ == "__main__":
    main()
