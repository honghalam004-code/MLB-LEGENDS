import streamlit as st

def main():
    # 1. 고화질 모니터 대응을 위한 와이드 레이아웃 설정
    st.set_page_config(page_title="MLB PRO: CINEMATIC HD", layout="wide")
    
    # 화면 찌그러짐 방지 및 다크 스타디움 테마 적용 CSS
    st.markdown("""
        <style>
        .main { background-color: #030712; color: #f3f4f6; }
        div[data-testid="stBlock"] { padding: 5px; }
        .stRadio, .stSlider { background: #111827; padding: 10px 20px; border-radius: 10px; border: 1px solid #1f2937; }
        </style>
    """, unsafe_allow_html=True)

    # --- [1. MLB 전체 30개 구단 데이터 정의] ---
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

    # ----------------------------------------------------
    # [위치 1] 가장 상단: 매치업 구단 및 투수 이름 등록
    # ----------------------------------------------------
    st.markdown("### 📋 1. MATCHUP CONFIG (팀 및 투수 설정)")
    top_col1, top_col2, top_col3 = st.columns([1, 1, 1])
    with top_col1:
        away_team = st.selectbox("⚾ 원정 팀 (AWAY)", mlb_teams, index=18)
    with top_col2:
        home_team = st.selectbox("🏠 홈 팀 (HOME)", mlb_teams, index=13)
    with top_col3:
        pitcher_name = st.text_input("👤 투수 등록", "나만의 에이스")

    st.markdown("---")

    # ----------------------------------------------------
    # [위치 2] 중간: 고해상도 그래픽 경기장 화면 배치
    # ----------------------------------------------------
    st.markdown("### 🎮 2. LIVE STADIUM (스트라이크 존을 클릭하여 투구)")

    # 자바스크립트 엔진으로 실시간 주입될 가상 데이터 플레이스홀더 생성
    # (하단 슬라이더 입력 값을 자바스크립트가 안전하게 동기화하도록 replace 처리 예정)
    
    raw_game_html = """
    <div style="background: radial-gradient(circle at center, #0b1329 0%, #020617 100%); padding: 25px; border-radius: 24px; box-shadow: 0 25px 60px rgba(0,0,0,0.8); border: 2px solid #1e293b; max-width: 960px; margin: 0 auto;">
        
        <div style="background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; margin-bottom: 20px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <div>
                <span style="font-size: 11px; color: #64748b; display:block; font-weight:700; letter-spacing:1px;">AWAY</span>
                <span style="font-size: 22px; font-weight: 800; color: #fff;">__AWAY_TEAM__</span>
                <span id="sb-away" style="font-size: 32px; font-weight: 900; color: #38bdf8; margin-left: 15px;">0</span>
            </div>
            
            <div style="text-align: center;">
                <div id="sb-inning" style="background: linear-gradient(135deg, #00e676, #00b0ff); color: #000; font-size: 14px; font-weight: 900; padding: 6px 20px; border-radius: 30px; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(0,230,118,0.3);">1회 초</div>
                <div style="display: flex; justify-content: center; gap: 12px; margin-top: 10px; font-family: monospace; font-size: 13px; font-weight:bold;">
                    <div>B <span id="lamp-b"></span></div>
                    <div>S <span id="lamp-s"></span></div>
                    <div>O <span id="lamp-o"></span></div>
                </div>
            </div>
            
            <div style="text-align: right;">
                <span id="sb-home" style="font-size: 32px; font-weight: 900; color: #38bdf8; margin-right: 15px;">0</span>
                <span style="font-size: 11px; color: #64748b; display:block; font-weight:700; letter-spacing:1px;">HOME</span>
                <span style="font-size: 22px; font-weight: 800; color: #fff;">__HOME_TEAM__</span>
            </div>
        </div>

        <canvas id="mainCanvas" width="910" height="420" style="border-radius: 16px; background: #000; border: 1px solid #334155; display: block; margin: 0 auto; box-shadow: inset 0 0 50px rgba(0,0,0,0.9);"></canvas>
        
        <div id="broadcast-ticker" style="margin-top: 15px; background: #020617; border: 1px solid #1e293b; color: #38bdf8; font-family: 'Courier New', monospace; padding: 15px; height: 75px; overflow-y: auto; font-size: 14px; border-radius: 12px; line-height: 1.6;">
            [STADIUM] __PITCHER_NAME__ 선수가 마운드에 등판했습니다. 하단에서 구종을 정하고 오른쪽 스트라이크 존에 투구하세요.
        </div>
    </div>

    <script>
        const canvas = document.getElementById('mainCanvas');
        const ctx = canvas.getContext('2d');

        // 하단 컨트롤러와 연동될 데이터 패키지
        const currentSpec = {
            name: "__PITCHER_NAME__",
            type: "__PITCH_TYPE__",
            speed: __PITCH_SPEED__,
            control: __PITCH_CONTROL__
        };

        let game = {
            awayScore: 0, homeScore: 0, inning: 1, isTop: true,
            balls: 0, strikes: 0, outs: 0,
            bases: [false, false, false],
            batter: "AARON JUDGE"
        };

        let mouse = { x: 0, y: 0 };
        let ball = { active: false, x: 230, y: 220, tx: 0, ty: 0 };
        let pitchLog = [];

        // 화면 왜곡 없는 완벽한 정밀 마우스 클릭 좌표 연산
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            // 스케일 비율 계산을 통해 해상도가 깨지거나 밀려 보이는 버그 전면 수정
            mouse.x = (e.clientX - rect.left) * (canvas.width / rect.width);
            mouse.y = (e.clientY - rect.top) * (canvas.height / rect.height);
        });

        canvas.addEventListener('mousedown', () => {
            if (ball.active) return;
            // 정확한 우측 스트라이크 존 타겟팅 구역 안에서만 조준 투구 발동
            if (mouse.x > 480 && mouse.x < 860 && mouse.y > 40 && mouse.y < 380) {
                let precisionError = (100 - currentSpec.control) * 0.45;
                ball.tx = mouse.x + (Math.random() - 0.5) * precisionError;
                ball.ty = mouse.y + (Math.random() - 0.5) * precisionError;
                ball.x = 230; ball.y = 220; ball.active = true;
            }
        });

        function printLog(text) {
            const ticker = document.getElementById('broadcast-ticker');
            ticker.innerHTML = `<span style="color:#00e676;">⚡</span> ${text}<br>` + ticker.innerHTML;
        }

        function refreshDashboard() {
            document.getElementById('sb-away').innerText = game.awayScore;
            document.getElementById('sb-home').innerText = game.homeScore;
            document.getElementById('sb-inning').innerText = `${game.inning}회 ${game.isTop ? '초' : '말'}`;
            
            const makeLamps = (cnt, max, color) => '<span style="color:'+color+'; margin-right:3px;">●</span>'.repeat(cnt) + '<span style="color:#334155; margin-right:3px;">○</span>'.repeat(max-cnt);
            document.getElementById('lamp-b').innerHTML = makeLamps(game.balls, 3, '#22c55e');
            document.getElementById('lamp-s').innerHTML = makeLamps(game.strikes, 2, '#eab308');
            document.getElementById('lamp-o').innerHTML = makeLamps(game.outs, 3, '#ef4444');
        }

        function calculatePlay() {
            const inZone = (ball.tx >= 580 && ball.tx <= 760 && ball.ty >= 130 && ball.ty <= 310);
            const displaySpeed = currentSpec.speed + Math.floor(Math.random() * 5) - 2;
            
            let advantage = (displaySpeed - 85) * 0.012;
            const swingChance = inZone ? (0.62 - advantage) : (0.24 + advantage);
            const isSwing = Math.random() < swingChance;

            if (isSwing) {
                let missPercent = 0.46 + advantage;
                if (Math.random() > missPercent) {
                    const hitSeed = Math.random();
                    if (hitSeed < 0.12) {
                        let runners = game.bases.filter(b=>b).length + 1;
                        if(game.isTop) game.awayScore += runners; else game.homeScore += runners;
                        game.bases = [false, false, false];
                        printLog(`<span style="color:#ef4444; font-weight:900;">[CRITICAL HOMERUN]</span> ${game.batter}가 ${currentSpec.name}의 ${currentSpec.type}을 강타해 거대한 홈런을 기록합니다!! (${displaySpeed} mph)`);
                    } else if (hitSeed < 0.45) {
                        let scoreIn = game.bases[2] ? 1 : 0;
                        game.bases[2] = game.bases[1]; game.bases[1] = game.bases[0]; game.bases[0] = true;
                        if(game.isTop) game.awayScore += scoreIn; else game.homeScore += scoreIn;
                        printLog(`[HIT] 안타! 주자 전원 진루하며 찬스를 이어갑니다. (${displaySpeed} mph)`);
                    } else {
                        game.outs++; printLog(`[OUT] 내야 플라이 아웃! 3루수 글러브 속으로 공이 들어갑니다.`);
                    }
                    game.strikes = 0; game.balls = 0;
                } else {
                    game.strikes++; printLog(`[STRIKE] 헛스윙! ${displaySpeed} mph 광속구가 배트를 완벽하게 제압합니다.`);
                }
            } else {
                if (inZone) {
                    game.strikes++; printLog(`[STRIKE] 루킹 스트라이크! 완벽한 보더라인 제구입니다. (${displaySpeed} mph)`);
                } else {
                    game.balls++; printLog(`[BALL] 볼! 유인구에 타자가 속지 않고 멈춰 섭니다.`);
                }
            }

            if(game.strikes >= 3) { game.outs++; game.strikes = 0; game.balls = 0; printLog(`[삼진] 💥 K!! 투수의 위력적인 결정구 삼진 처리!`); }
            if(game.balls >= 4) { game.bases[0] = true; game.strikes = 0; game.balls = 0; printLog([`[볼넷] 밀어내기 찬스, 베이스 출루 허용.`]); }
            if(game.outs >= 3) { game.outs = 0; game.strikes = 0; game.balls = 0; game.bases = [false,false,false]; game.isTop = !game.isTop; if(game.isTop) game.inning++; printLog(`[SYSTEM] 🔄 공수 교대! 공수가 전격 전환됩니다.`); }
            
            pitchLog.push({ x: ball.tx, y: ball.ty, inside: inZone });
            if(pitchLog.length > 6) pitchLog.shift();
            refreshDashboard();
        }

        function engineLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // --- 1. 좌측 시네마틱 스타디움 필드 그래픽 ---
            let grassGrad = ctx.createRadialGradient(230, 220, 30, 230, 220, 220);
            grassGrad.addColorStop(0, '#14532d'); grassGrad.addColorStop(1, '#022c22');
            ctx.fillStyle = grassGrad;
            ctx.beginPath(); ctx.ellipse(230, 220, 190, 140, 0, 0, Math.PI * 2); ctx.fill();
            
            ctx.strokeStyle = "rgba(255,255,255,0.15)";
            ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(230, 330); ctx.lineTo(330, 220); ctx.lineTo(230, 110); ctx.lineTo(130, 220);
            ctx.closePath(); ctx.stroke();

            // 리얼 주자 베이스 그리기
            const drawDiamondBase = (bx, by, active) => {
                ctx.fillStyle = active ? "#f43f5e" : "#475569";
                ctx.strokeStyle = active ? "#ffe4e6" : "#1e293b";
                ctx.save(); ctx.translate(bx, by); ctx.rotate(45 * Math.PI / 180);
                ctx.fillRect(-7, -7, 14, 14); ctx.strokeRect(-7, -7, 14, 14); ctx.restore();
            };
            drawDiamondBase(330, 220, game.bases[0]);
            drawDiamondBase(230, 110, game.bases[1]);
            drawDiamondBase(130, 220, game.bases[2]);

            // 투수/타자 리얼 엔티티 실루엣
            ctx.fillStyle = "#e2e8f0"; ctx.beginPath(); ctx.arc(230,220,5,0,Math.PI*2); ctx.fill(); // 투수
            ctx.fillStyle = "#38bdf8"; ctx.beginPath(); ctx.arc(230,325,7,0,Math.PI*2); ctx.fill(); // 타자
            ctx.strokeStyle = "#f97316"; ctx.lineWidth = 3.5; ctx.beginPath(); ctx.moveTo(230,325); ctx.lineTo(210,300); ctx.stroke(); // 배트

            // 중앙 경계 그리드
            ctx.strokeStyle = "rgba(51, 65, 85, 0.5)"; ctx.setLineDash([4, 4]);
            ctx.beginPath(); ctx.moveTo(455, 10); ctx.lineTo(455, 410); ctx.stroke(); ctx.setLineDash([]);

            // --- 2. 우측 UHD 방송용 3D 스트라이크 존 ---
            ctx.fillStyle = "rgba(0, 230, 118, 0.04)"; ctx.fillRect(580, 130, 180, 180);
            ctx.strokeStyle = "#00e676"; ctx.lineWidth = 3; ctx.strokeRect(580, 130, 180, 180);
            
            // 9분할 UHD 격자 매트릭스
            ctx.strokeStyle = "rgba(255,255,255,0.12)"; ctx.lineWidth = 1.5;
            for(let i=1; i<3; i++) {
                ctx.beginPath(); ctx.moveTo(580 + (i * 60), 130); ctx.lineTo(580 + (i * 60), 310); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(580, 130 + (i * 60)); ctx.lineTo(760, 130 + (i * 60)); ctx.stroke();
            }
            ctx.strokeStyle = "rgba(148, 163, 184, 0.3)"; ctx.strokeRect(520, 70, 300, 300);

            // 하이테크 레이저 조준경 크로스헤어 효과
            if (mouse.x > 480 && mouse.x < 860 && mouse.y > 40 && mouse.y < 380 && !ball.active) {
                ctx.strokeStyle = "rgba(0, 230, 118, 0.4)"; ctx.setLineDash([2, 3]);
                ctx.beginPath(); ctx.moveTo(mouse.x, 40); ctx.lineTo(mouse.x, 380); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(520, mouse.y); ctx.lineTo(820, mouse.y); ctx.stroke(); ctx.setLineDash([]);
                
                ctx.strokeStyle = "#eab308"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(mouse.x, mouse.y, 12, 0, Math.PI * 2); ctx.stroke();
            }

            // 투구 기록 마커 흔적 남기기
            pitchLog.forEach(p => {
                ctx.fillStyle = p.inside ? "#00e676" : "#ef4444";
                ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            });

            // 실시간 투구 비행 및 커스텀 무브먼트 가속도 물리 계산
            if (ball.active) {
                ball.x += (ball.tx - ball.x) * 0.15;
                ball.y += (ball.ty - ball.y) * 0.15;

                let gap = Math.abs(ball.x - ball.tx);
                if (currentSpec.type === "슬라이더" && gap > 12) ball.x += 1.6;
                if (currentSpec.type === "커브" && gap > 12) ball.y += 2.2;

                let currentRadius = 3 + (1 - gap / 450) * 5.5;
                ctx.fillStyle = "#ffffff"; ctx.shadowBlur = 15; ctx.shadowColor = "#38bdf8";
                ctx.beginPath(); ctx.arc(ball.x, ball.y, currentRadius, 0, Math.PI * 2); ctx.fill();
                ctx.shadowBlur = 0;

                if (gap < 2) {
                    ball.active = false;
                    calculatePlay();
                }
            }

            requestAnimationFrame(engineLoop);
        }

        refreshDashboard();
        engineLoop();
    </script>
    """

    # ----------------------------------------------------
    # [위치 3] 가장 하단: 요청하신 구종 및 구속 설정 배치
    # ----------------------------------------------------
    st.markdown("### ⚙️ 3. PITCH SPECIFICATION (구종 및 세부 스탯 설정)")
    bot_col1, bot_col2 = st.columns([1, 2])
    
    with bot_col1:
        selected_pitch = st.radio(
            "🔮 던질 구종 선택", 
            ["포심 직구", "슬라이더", "커브"], 
            horizontal=False
        )
    
    with bot_col2:
        if selected_pitch == "포심 직구":
            fb_speed = st.slider("🔥 직구 최고 구속 (mph)", 85, 105, 99)
            fb_control = st.slider("🎯 직구 제구력 (1-100)", 1, 100, 88)
            current_speed, current_control = fb_speed, fb_control
        elif selected_pitch == "슬라이더":
            sl_speed = st.slider("🔮 슬라이더 구속 (mph)", 75, 95, 89)
            sl_control = st.sidebar.slider("🎯 슬라이더 제구력 (1-100)", 1, 100, 78) if 'fb_c' in st.session_state else st.slider("🎯 슬라이더 제구력 (1-100)", 1, 100, 78)
            current_speed, current_control = sl_speed, sl_control
        else:
            cb_speed = st.slider("🟢 커브 구속 (mph)", 65, 88, 77)
            cb_control = st.slider("🎯 커브 제구력 (1-100)", 1, 100, 72)
            current_speed, current_control = cb_speed, cb_control

    # ----------------------------------------------------
    # 데이터 매핑 최종 주입 후 캔버스 출력
    # ----------------------------------------------------
    final_html = (
        raw_game_html
        .replace("__AWAY_TEAM__", away_team)
        .replace("__HOME_TEAM__", home_team)
        .replace("__PITCHER_NAME__", pitcher_name)
        .replace("__PITCH_TYPE__", selected_pitch)
        .replace("__PITCH_SPEED__", str(current_speed))
        .replace("__PITCH_CONTROL__", str(current_control))
    )

    st.components.v1.html(final_html, height=660)

if __name__ == "__main__":
    main()
