import streamlit as st

def main():
    # 1. 와이드 레이아웃 및 깔끔한 화이트 테마 전용 스타일 적용
    st.set_page_config(page_title="MLB PRO: Catcher's View HD", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; color: #0f172a; }
        .stSelectbox, .stTextInput, .stSlider, .stRadio { 
            background: #ffffff !important; 
            color: #0f172a !important; 
            border-radius: 12px;
        }
        div[data-testid="stBlock"] { padding: 10px; }
        h3 { color: #1e3a8a !important; font-weight: 800 !important; }
        </style>
    """, unsafe_allow_html=True)

    # 럭셔리 화이트 스포츠 헤더
    st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 50%, #1e3a8a 100%); padding: 18px; border-radius: 14px; text-align: center; box-shadow: 0 4px 20px rgba(30,58,138,0.15); margin-bottom: 25px;">
            <h1 style="color: #ffffff; margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 3px; font-size: 36px;">⚾ MLB LEGENDS <span style="color:#6ee7b7;">CATCHER'S VIEW</span></h1>
            <p style="color: #e2e8f0; margin: 5px 0 0 0; font-size: 14px; font-weight: 500;">프리미엄 화이트 중계 가시성 업그레이드 버전</p>
        </div>
    """, unsafe_allow_html=True)

    # --- [구단 데이터 목록 완벽 복원] ---
    mlb_teams = [
        "애리조나 다이아몬드백스", "애틀랜타 브레이브스", "볼티모어 오리올스", "보스턴 레드삭스", 
        "시카고 컵스", "시카고 화이트삭스", "신시내티 레즈", "클리블랜드 가디언스", 
        "콜로라도 로키스", "디트로이트 타이거스", "휴스턴 애스트로스", "캔자스시티 로열스", 
        "로스앤젤레스 에인절스", "로스앤젤레스 다저스", "마이애미 말린스", "밀워키 브루어스", 
        "미네소타 트윈스", "뉴욕 메츠", "뉴욕 양키스", "오클랜드 애슬레틱스", 
        "필라델피아 Φ리스", "피츠버그 파이어리츠", "샌디에이고 파드리스", "샌프란시스코 자이언츠", 
        "시애틀 매리너스", "세인트루이스 카디널스", "탬파베이 레이스", "텍사스 레인저스", 
        "토론토 블루제이스", "워싱턴 내셔널스"
    ]

    # ----------------------------------------------------
    # [1단계] 최상단: 팀 선택 및 투수 이름 설정
    # ----------------------------------------------------
    st.markdown("### 📋 1. 경기 매치업 및 라인업 구성")
    top_col1, top_col2, top_col3 = st.columns([1, 1, 1])
    with top_col1:
        away_team = st.selectbox("⚾ 원정 팀 (AWAY TEAM)", mlb_teams, index=18) # 양키스 기본
    with top_col2:
        home_team = st.selectbox("🏠 홈 팀 (HOME TEAM)", mlb_teams, index=13)  # 다저스 기본
    with top_col3:
        pitcher_name = st.text_input("👤 투수 이름 등록", "디그롬")

    st.markdown("---")

    # ----------------------------------------------------
    # [하단 수치 선행 정의] 스트림릿 구조상 아래 컨트롤러 값을 미리 받아오기 위함
    # ----------------------------------------------------
    if 'current_speed' not in st.session_state:
        current_speed, current_control, selected_pitch = 98, 85, "포심 직구"

    # ----------------------------------------------------
    # [2단계] 중앙: 포수 시점 초고화질 화이트 그래픽 엔진
    # ----------------------------------------------------
    st.markdown("### 🎮 2. LIVE STADIUM (포수 시점 리얼 피칭 존)")

    raw_game_html = """
    <div style="background: #ffffff; padding: 25px; border-radius: 24px; box-shadow: 0 15px 40px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; max-width: 960px; margin: 0 auto;">
        
        <div style="background: #f1f5f9; border: 2px solid #cbd5e1; border-radius: 16px; display: flex; justify-content: space-between; align-items: center; padding: 18px 30px; margin-bottom: 20px; font-family: system-ui, sans-serif;">
            <div>
                <span style="font-size: 11px; color: #64748b; display:block; font-weight:800;">AWAY</span>
                <span style="font-size: 20px; font-weight: 800; color: #0f172a;">__AWAY_TEAM__</span>
                <span id="sb-away" style="font-size: 30px; font-weight: 900; color: #1d4ed8; margin-left: 15px;">0</span>
            </div>
            
            <div style="text-align: center; background: #ffffff; padding: 8px 25px; border-radius: 30px; border: 1px solid #cbd5e1; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);">
                <div id="sb-inning" style="color: #1e3a8a; font-size: 15px; font-weight: 900; letter-spacing: 1px;">1회 초</div>
                <div style="display: flex; justify-content: center; gap: 14px; margin-top: 8px; font-family: monospace; font-size: 14px; font-weight:bold;">
                    <div style="color:#475569;">B <span id="lamp-b"></span></div>
                    <div style="color:#475569;">S <span id="lamp-s"></span></div>
                    <div style="color:#475569;">O <span id="lamp-o"></span></div>
                </div>
            </div>
            
            <div style="text-align: right;">
                <span id="sb-home" style="font-size: 30px; font-weight: 900; color: #1d4ed8; margin-right: 15px;">0</span>
                <span style="font-size: 11px; color: #64748b; display:block; font-weight:800;">HOME</span>
                <span style="font-size: 20px; font-weight: 800; color: #0f172a;">__HOME_TEAM__</span>
            </div>
        </div>

        <canvas id="catcherCanvas" width="910" height="420" style="border-radius: 16px; background: #f8fafc; border: 2px solid #cbd5e1; display: block; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.03);"></canvas>
        
        <div id="broadcast-ticker" style="margin-top: 15px; background: #0f172a; border: 1px solid #1e293b; color: #38bdf8; font-family: sans-serif; padding: 15px; height: 65px; overflow-y: auto; font-size: 14px; border-radius: 12px; line-height: 1.6; font-weight: 500;">
            [중계석] 캐처스 뷰 모드 가동 완료. __PITCHER_NAME__ 투수가 와인드업을 준비합니다. 우측 스트라이크 존을 겨냥하세요!
        </div>
    </div>

    <script>
        const canvas = document.getElementById('catcherCanvas');
        const ctx = canvas.getContext('2d');

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
        // 포수 시점: 공이 투수 마운드(멀리서, 작게)에서 포수 미트(가까이, 커지면서)로 날아옴
        let ball = { active: false, x: 230, y: 150, tx: 0, ty: 0, startX: 230, startY: 150 };
        let pitchLog = [];

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = (e.clientX - rect.left) * (canvas.width / rect.width);
            mouse.y = (e.clientY - rect.top) * (canvas.height / rect.height);
        });

        canvas.addEventListener('mousedown', () => {
            if (ball.active) return;
            // 우측의 가시성 높은 투구 조준 영역 잠금 클릭
            if (mouse.x > 490 && mouse.x < 860 && mouse.y > 40 && mouse.y < 380) {
                let precisionError = (100 - currentSpec.control) * 0.42;
                ball.tx = mouse.x + (Math.random() - 0.5) * precisionError;
                ball.ty = mouse.y + (Math.random() - 0.5) * precisionError;
                
                // 포수 시점 원근감 투구 시작점 세팅 (저 멀리 마운드 센터)
                ball.x = 230; ball.y = 150;
                ball.active = true;
            }
        });

        function printLog(text) {
            const ticker = document.getElementById('broadcast-ticker');
            ticker.innerHTML = `<span style="color:#2563eb;">✓</span> ${text}<br>` + ticker.innerHTML;
        }

        function refreshDashboard() {
            document.getElementById('sb-away').innerText = game.awayScore;
            document.getElementById('sb-home').innerText = game.homeScore;
            document.getElementById('sb-inning').innerText = `${game.inning}회 ${game.isTop ? '초' : '말'}`;
            
            const makeLamps = (cnt, max, color) => '<span style="color:'+color+'; margin-right:3px;">●</span>'.repeat(cnt) + '<span style="color:#cbd5e1; margin-right:3px;">○</span>'.repeat(max-cnt);
            document.getElementById('lamp-b').innerHTML = makeLamps(game.balls, 3, '#22c55e');
            document.getElementById('lamp-s').innerHTML = makeLamps(game.strikes, 2, '#eab308');
            document.getElementById('lamp-o').innerHTML = makeLamps(game.outs, 3, '#ef4444');
        }

        function calculatePlay() {
            const inZone = (ball.tx >= 580 && ball.tx <= 760 && ball.ty >= 130 && ball.ty <= 310);
            const displaySpeed = currentSpec.speed + Math.floor(Math.random() * 5) - 2;
            
            let advantage = (displaySpeed - 85) * 0.012;
            const swingChance = inZone ? (0.60 - advantage) : (0.25 + advantage);
            const isSwing = Math.random() < swingChance;

            if (isSwing) {
                let missPercent = 0.45 + advantage;
                if (Math.random() > missPercent) {
                    const hitSeed = Math.random();
                    if (hitSeed < 0.13) {
                        let runners = game.bases.filter(b=>b).length + 1;
                        if(game.isTop) game.awayScore += runners; else game.homeScore += runners;
                        game.bases = [false, false, false];
                        printLog(`<span style="color:#dc2626; font-weight:bold;">[HOME RUN]</span> 타자 배트 중심에 정확히 맞았습니다! 장외 홈런 대폭발!! (${displaySpeed} mph)`);
                    } else if (hitSeed < 0.46) {
                        let scoreIn = game.bases[2] ? 1 : 0;
                        game.bases[2] = game.bases[1]; game.bases[1] = game.bases[0]; game.bases[0] = true;
                        if(game.isTop) game.awayScore += scoreIn; else game.homeScore += scoreIn;
                        printLog(`[HIT] 안타! 주자들이 한 루씩 안전하게 진루합니다. (${displaySpeed} mph)`);
                    } else {
                        game.outs++; printLog(`[OUT] 범타 아웃! 타이밍을 뺏긴 빗맞은 공이 야수 정면으로 향합니다.`);
                    }
                    game.strikes = 0; game.balls = 0;
                } else {
                    game.strikes++; printLog(`[STRIKE] 호쾌한 헛스윙! ${currentSpec.type}의 강력한 구위에 타자가 당했습니다. (${displaySpeed} mph)`);
                }
            } else {
                if (inZone) {
                    game.strikes++; printLog(`[STRIKE] 루킹 스트라이크 존 안쪽 보더라인을 완벽히 관통합니다! (${displaySpeed} mph)`);
                } else {
                    game.balls++; printLog(`[BALL] 볼! 아슬아슬하게 빠져나간 공을 타자가 잘 골라냈습니다.`);
                }
            }

            if(game.strikes >= 3) { game.outs++; game.strikes = 0; game.balls = 0; printLog(`[삼진] 💥 삼진 아웃! 포수가 완벽한 프레이밍으로 삼진을 이끌어냅니다!`); }
            if(game.balls >= 4) { game.bases[0] = true; game.strikes = 0; game.balls = 0; printLog([`[볼넷] 베이스 포볼 출루 허용.`]); }
            if(game.outs >= 3) { game.outs = 0; game.strikes = 0; game.balls = 0; game.bases = [false,false,false]; game.isTop = !game.isTop; if(game.isTop) game.inning++; printLog(`[이닝 교대] 공수교대! 투수와 타자가 교체됩니다.`); }
            
            pitchLog.push({ x: ball.tx, y: ball.ty, inside: inZone });
            if(pitchLog.length > 6) pitchLog.shift();
            refreshDashboard();
        }

        function engineLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 디바이더 및 화이트 세련된 가이드 디자인 배경 처리
            ctx.fillStyle = "#ffffff"; ctx.fillRect(0,0,canvas.width,canvas.height);

            // --- 1. 좌측: 실제 포수 시점 (Catcher's View) 입체 이펙트 필드 ---
            // 야구장 원근감 잔디 라인 표현
            let fieldGrad = ctx.createLinearGradient(230, 350, 230, 80);
            fieldGrad.addColorStop(0, '#22c55e'); fieldGrad.addColorStop(1, '#15803d');
            ctx.fillStyle = fieldGrad;
            
            // 포수 시점 원근 부채꼴 필드
            ctx.beginPath();
            ctx.moveTo(230, 370); // 포수 위치 (홈)
            ctx.lineTo(400, 100); // 원경 1루 방향 우측 외야
            ctx.lineTo(60, 100);  // 원경 3루 방향 좌측 외야
            ctx.closePath(); ctx.fill();

            // 리얼 베이스 다이아몬드 (포수 시점 정렬)
            const drawCatcherBase = (bx, by, active) => {
                ctx.fillStyle = active ? "#ef4444" : "#e2e8f0";
                ctx.strokeStyle = active ? "#f87171" : "#94a3b8";
                ctx.lineWidth = 2;
                ctx.save(); ctx.translate(bx, by); ctx.rotate(45 * Math.PI / 180);
                ctx.fillRect(-6, -6, 12, 12); ctx.strokeRect(-6, -6, 12, 12); ctx.restore();
            };
            drawCatcherBase(295, 210, game.bases[0]); // 1루
            drawCatcherBase(230, 120, game.bases[1]); // 2루
            drawCatcherBase(165, 210, game.bases[2]); // 3루

            // 포수 마스크 바로 앞의 홈플레이트 (화이트 베이스)
            ctx.fillStyle = "#64748b";
            ctx.beginPath();
            ctx.moveTo(230, 345); ctx.lineTo(245, 355); ctx.lineTo(245, 362);
            ctx.lineTo(215, 362); ctx.lineTo(215, 355);
            ctx.closePath(); ctx.fill();

            // 저 멀리 보이는 투수 실루엣 위젯 (원근감 축소)
            ctx.fillStyle = "#0f172a"; ctx.beginPath(); ctx.arc(230, 140, 4, 0, Math.PI*2); ctx.fill(); 
            ctx.fillRect(228, 144, 4, 8); // 투수 몸통

            // 포수 앞 타자 위젯 디자인
            ctx.fillStyle = "#2563eb"; ctx.beginPath(); ctx.arc(185, 330, 8, 0, Math.PI*2); ctx.fill(); // 타자 머리
            ctx.strokeStyle = "#b45309"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(185, 332); ctx.lineTo(205, 305); ctx.stroke(); // 배트

            // 중앙 파티션 스플릿 라인 (가시성 높은 점선 가이드)
            ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
            ctx.beginPath(); ctx.moveTo(455, 10); ctx.lineTo(455, 410); ctx.stroke(); ctx.setLineDash([]);

            // --- 2. 우측: 방송용 고대비 스트라이크 존 ---
            // 명확하게 글씨와 라인이 보이는 화이트 하이테크 스타일 존
            ctx.fillStyle = "rgba(37, 99, 235, 0.03)"; ctx.fillRect(580, 130, 180, 180);
            ctx.strokeStyle = "#2563eb"; ctx.lineWidth = 3.5; ctx.strokeRect(580, 130, 180, 180);
            
            // 9분할 스트라이크 구분 실선
            ctx.strokeStyle = "rgba(37, 99, 235, 0.18)"; ctx.lineWidth = 1.5;
            for(let i=1; i<3; i++) {
                ctx.beginPath(); ctx.moveTo(580 + (i * 60), 130); ctx.lineTo(580 + (i * 60), 310); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(580, 130 + (i * 60)); ctx.lineTo(760, 130 + (i * 60)); ctx.stroke();
            }
            // 전체 가이드 보드 테두리
            ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 1; ctx.strokeRect(520, 70, 300, 300);

            // 레이저 크로스헤어 정밀 에임 가이드 피드백
            if (mouse.x > 490 && mouse.x < 860 && mouse.y > 40 && mouse.y < 380 && !ball.active) {
                ctx.strokeStyle = "rgba(37, 99, 235, 0.3)"; ctx.setLineDash([3, 3]);
                ctx.beginPath(); ctx.moveTo(mouse.x, 40); ctx.lineTo(mouse.x, 380); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(520, mouse.y); ctx.lineTo(820, mouse.y); ctx.stroke(); ctx.setLineDash([]);
                
                ctx.strokeStyle = "#d97706"; ctx.lineWidth = 2.5;
                ctx.beginPath(); ctx.arc(mouse.x, mouse.y, 14, 0, Math.PI * 2); ctx.stroke();
            }

            // 던져진 구질 히스토리 점 히트맵 시각화
            pitchLog.forEach(p => {
                ctx.fillStyle = p.inside ? "#22c55e" : "#ef4444";
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(p.x, p.y, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            });

            // 60FPS 포수 시점 리얼 3D 다이내믹 피칭 비행 물리 계산
            if (ball.active) {
                // 원근 효과 연산: 멀리서(투수) 가까이(포수 존) 오면서 속도가 가속되는 느낌 부여
                let distanceToTarget = Math.sqrt(Math.pow(ball.tx - ball.x, 2) + Math.pow(ball.ty - ball.y, 2));
                
                ball.x += (ball.tx - ball.x) * 0.14;
                ball.y += (ball.ty - ball.y) * 0.14;

                // 변화구 무브먼트 리얼 궤적 반영
                if (currentSpec.type === "슬라이더" && distanceToTarget > 15) ball.x += 1.8;
                if (currentSpec.type === "커브" && distanceToTarget > 15) ball.y += 2.4;

                // 포수 시점의 핵심: 다가올수록 공 크기가 극적으로 확대됨 (원근 구형 렌더링)
                let catcherPerspectiveRadius = 3 + (1 - distanceToTarget / 450) * 8;
                if(catcherPerspectiveRadius < 3) catcherPerspectiveRadius = 3;

                ctx.fillStyle = "#ffffff"; 
                ctx.strokeStyle = "#475569"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(ball.x, ball.y, catcherPerspectiveRadius, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

                if (distanceToTarget < 3) {
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
    # [3단계] 최하단 배치: 완전히 밑으로 내려온 구종 및 구속 선택 컨트롤러
    # ----------------------------------------------------
    st.markdown("### ⚙️ 3. PITCH COMMAND CENTER (구종 및 세부 능력치 튜닝)")
    bot_col1, bot_col2 = st.columns([1, 2])
    
    with bot_col1:
        selected_pitch = st.radio(
            "🔮 실시간 구종 장착", 
            ["포심 직구", "슬라이더", "커브"], 
            horizontal=True
        )
    
    with bot_col2:
        if selected_pitch == "포심 직구":
            fb_speed = st.slider("🔥 직구 최고 구속 설정 (mph)", 85, 105, 98)
            fb_control = st.slider("🎯 직구 핀포인트 제구력 (1-100)", 1, 100, 85)
            current_speed, current_control = fb_speed, fb_control
        elif selected_pitch == "슬라이더":
            sl_speed = st.slider("🔮 슬라이더 변화구 구속 (mph)", 75, 95, 87)
            sl_control = st.slider("🎯 슬라이더 핀포인트 제구력 (1-100)", 1, 100, 76)
            current_speed, current_control = sl_speed, sl_control
        else:
            cb_speed = st.slider("🟢 낙차 커브 구속 설정 (mph)", 65, 88, 76)
            cb_control = st.slider("🎯 커브 핀포인트 제구력 (1-100)", 1, 100, 72)
            current_speed, current_control = cb_speed, cb_control

    # ----------------------------------------------------
    # 데이터 치환 가공 작업 후 렌더링 완료
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

    st.components.v1.html(final_html, height=670)

if __name__ == "__main__":
    main()
