import streamlit as st
import random

def main():
    # ----------------------------------------------------------------
    # 1. 고해상도 시네마틱 와이드 레이아웃 및 화이트 UI 스타일링
    # ----------------------------------------------------------------
    st.set_page_config(page_title="EA SPORTS: MVP BASEBALL PRO 2026", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        .stSelectbox, .stTextInput, .stSlider, .stRadio { 
            background: #ffffff !important; color: #0f172a !important; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        div[data-testid="stBlock"] { padding: 12px; }
        h2, h3 { color: #0f172a !important; font-weight: 800 !important; letter-spacing: -0.5px; }
        .stButton>button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important; font-weight: 800 !important; padding: 12px 24px !important; border-radius: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # 2. 게임 상태 관리 (세션 데이터 오케스트레이션)
    # ----------------------------------------------------------------
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'away_team' not in st.session_state: st.session_state.away_team = "NY Yankees"
    if 'home_team' not in st.session_state: st.session_state.home_team = "LA Dodgers"
    if 'pitcher_name' not in st.session_state: st.session_state.pitcher_name = "C. Kershaw"

    # --- MLB 30개 전체 구단 데이터셋 완벽 탑재 ---
    mlb_teams = [
        "AZ Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", 
        "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians", 
        "Colorado Rockies", "Detroit Tigers", "Houston Astros", "KC Royals", 
        "LA Angels", "LA Dodgers", "Miami Marlins", "Milwaukee Brewers", 
        "Minnesota Twins", "NY Mets", "NY Yankees", "Oakland Athletics", 
        "Philadelphia Phillies", "Pittsburgh Pirates", "SD Padres", "SF Giants", 
        "Seattle Mariners", "STL Cardinals", "Tampa Bay Rays", "Texas Rangers", 
        "Toronto Blue Jays", "Washington Nationals"
    ]

    # ----------------------------------------------------------------
    # [위치 1] 초기 설정 화면 (아무것도 못하고 고르는 빌드 마크업)
    # ----------------------------------------------------------------
    if not st.session_state.game_started:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%); padding: 60px; border-radius: 24px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.05); border: 2px solid #e2e8f0; max-width: 800px; margin: 40px auto;">
                <div style="background: #ef4444; color: white; font-family: 'Arial Black', sans-serif; font-size: 14px; font-weight: 900; display: inline-block; padding: 4px 12px; border-radius: 4px; margin-bottom: 15px; letter-spacing: 2px;">EA SPORTS</div>
                <h1 style="color: #0f172a; margin: 0; font-family: 'Impact', sans-serif; font-size: 56px; letter-spacing: 1px;">MVP BASEBALL <span style="color:#2563eb;">2026</span></h1>
                <p style="color: #475569; margin-top: 10px; font-size: 16px; font-weight: 500;">경기 시작 전, 대진할 구단과 선발 투수를 등록하십시오.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sel_away = st.selectbox("⚾ 원정 팀 (AWAY TEAM)", mlb_teams, index=18)
        with col2:
            sel_home = st.selectbox("🏠 홈 팀 (HOME TEAM)", mlb_teams, index=13)
        with col3:
            sel_pitcher = st.text_input("👤 등판할 투수 이름 입력", "C. Sale")
            
        st.markdown("<div style='text-align:center; margin-top:30px;'>", unsafe_allow_html=True)
        if st.button("🎮 ENTER STADIUM (경기장 입장)", use_container_width=True):
            st.session_state.away_team = sel_away
            st.session_state.home_team = sel_home
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.game_started = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop() # 조건 충족 시까지 하단 코드를 차단하는 가드레일

    # ----------------------------------------------------------------
    # [위치 2] 중간: 포수 시점 리얼 3D 궤적 그래픽 시뮬레이션 엔진
    # ----------------------------------------------------------------
    st.markdown(f"## 🏟️ LIVE MATCHUP: {st.session_state.away_team} VS {st.session_state.home_team}")

    # 스트림릿 수명주기 데이터 바인딩 우회 연산
    away_abbr = st.session_state.away_team[:3].upper()
    home_abbr = st.session_state.home_team[:3].upper()
    p_name = st.session_state.pitcher_name

    # ----------------------------------------------------------------
    # [위치 3] 최하단: 정밀 제어 구종 커맨드 센터 설계
    # ----------------------------------------------------------------
    st.markdown("---")
    st.markdown("### ⚙️ PITCH COMMAND CENTER (구종 및 투구 매커니즘 튜닝)")
    
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.2, 2, 2])
    
    with ctrl_col1:
        selected_pitch = st.radio(
            "🔮 던질 구질 선택 (Pitch Selection)", 
            ["포심 직구 (Fastball)", "슬라이더 (Slider)", "체인지업 (Changeup)", "파워 커브 (Curve)"], 
            horizontal=False
        )
    
    with ctrl_col2:
        if "포심 직구" in selected_pitch:
            speed = st.slider("🔥 최고 구속 설정 (Velocity - mph)", 92, 106, 99)
            break_val = 0.0 # 직구는 자체 무브먼트 최소화
        elif "슬라이더" in selected_pitch:
            speed = st.slider("🔮 슬라이더 구속 (Velocity - mph)", 84, 96, 88)
            break_val = st.slider("횡방향 무브먼트 (Horizontal Break)", 1.0, 4.0, 2.5)
        elif "체인지업" in selected_pitch:
            speed = st.slider("💤 체인지업 구속 (Velocity - mph)", 80, 92, 84)
            break_val = st.slider("종방향 하강 무브먼트 (Sink)", 1.0, 3.5, 2.0)
        else:
            speed = st.slider("🟢 파워 커브 구속 (Velocity - mph)", 70, 86, 76)
            break_val = st.slider("폭포수 낙차 무브먼트 (Vertical Drop)", 2.0, 6.0, 4.5)

    with ctrl_col3:
        control_stat = st.slider("🎯 핀포인트 커맨드 제구 스탯", 1, 100, 85)
        st.markdown(f"""
            <div style="background:#f1f5f9; padding:15px; border-radius:12px; border:1px solid #cbd5e1; margin-top:10px;">
                <b style="color:#1e3a8a;">[선택된 구질 요약 스펙]</b><br>
                • 타입: {selected_pitch.split(' ')[0]}<br>
                • 회전 속도: {int(speed * 26.3)} RPM<br>
                • 제구 허용 오차 반경: {round((100-control_stat)*0.35, 2)} cm
            </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------
    # 4. 코어 그래픽스 렌더링 파이프라인 (HTML5 Canvas + Embedded Core JS)
    # ----------------------------------------------------------------
    # 화이트 스타일 테마 및 리얼 포수 시점 물리 그래픽 탑재
    core_game_engine_html = """
    <div style="background: #ffffff; padding: 25px; border-radius: 24px; box-shadow: 0 15px 45px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; max-width: 960px; margin: 0 auto; font-family: system-ui, sans-serif;">
        
        <div style="background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 16px; display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <div>
                    <span style="font-size: 10px; color: #64748b; display:block; font-weight:800; letter-spacing:1px;">AWAY</span>
                    <span style="font-size: 20px; font-weight: 900; color: #0f172a;">__AWAY__</span>
                </div>
                <div id="score-away" style="font-size: 36px; font-weight: 900; color: #2563eb; background: #fff; padding: 2px 14px; border-radius: 8px; border: 1px solid #cbd5e1;">0</div>
            </div>
            
            <div style="text-align: center;">
                <div id="match-inning" style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #fff; font-size: 13px; font-weight: 800; padding: 5px 18px; border-radius: 20px; letter-spacing: 0.5px;">1회초 (TOP 1ST)</div>
                <div style="display: flex; justify-content: center; gap: 12px; margin-top: 10px; font-family: monospace; font-size: 13px; font-weight:900;">
                    <div style="color:#334155;">B <span id="b-indicators"></span></div>
                    <div style="color:#334155;">S <span id="s-indicators"></span></div>
                    <div style="color:#334155;">O <span id="o-indicators"></span></div>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; gap: 20px;">
                <div id="score-home" style="font-size: 36px; font-weight: 900; color: #2563eb; background: #fff; padding: 2px 14px; border-radius: 8px; border: 1px solid #cbd5e1;">0</div>
                <div style="text-align: right;">
                    <span style="font-size: 10px; color: #64748b; display:block; font-weight:800; letter-spacing:1px;">HOME</span>
                    <span style="font-size: 20px; font-weight: 900; color: #0f172a;">__HOME__</span>
                </div>
            </div>
        </div>

        <canvas id="mvpCanvas" width="910" height="440" style="border-radius: 16px; background: #ffffff; border: 2px solid #cbd5e1; display: block; margin: 0 auto; box-shadow: inset 0 2px 10px rgba(0,0,0,0.02);"></canvas>
        
        <div id="live-audio-board" style="margin-top: 15px; background: #0f172a; border: 1px solid #1e293b; color: #f8fafc; font-family: sans-serif; padding: 15px; height: 65px; overflow-y: auto; font-size: 14px; border-radius: 12px; line-height: 1.6;">
            [🎙️ EA SPORTS BROADCAST] 포수 시점 카메라 중계가 켜졌습니다. 선발 투수 __PITCHER__ 선수가 사인을 교환하고 투구 모션에 들어갑니다. 우측 K-ZONE 에 마우스를 올리고 클릭하여 볼끝을 조절해 보세요!
        </div>
    </div>

    <script>
        const canvas = document.getElementById('mvpCanvas');
        const ctx = canvas.getContext('2d');

        // 동적 연동용 JSON 모델 인젝션
        const runtimeSpecs = {
            pName: "__PITCHER__",
            type: "__TYPE__",
            speed: __SPEED__,
            control: __CONTROL__,
            break: __BREAK__
        };

        let db = {
            awayScore: 0, homeScore: 0, inning: 1, isTop: true,
            b: 0, s: 0, o: 0,
            bases: [false, false, false],
            batterName: "M. Trout"
        };

        let pointer = { x: 0, y: 0 };
        // 포수 시점 물리 초기 좌표 (투수 마운드는 먼 배경 상단 중앙 240, 160)
        let ballSim = { active: false, x: 240, y: 160, tx: 0, ty: 0, pct: 0, size: 2.5, startX: 240, startY: 160 };
        let pitHistory = [];

        canvas.addEventListener('mousemove', (e) => {
            const boundary = canvas.getBoundingClientRect();
            pointer.x = (e.clientX - boundary.left) * (canvas.width / boundary.width);
            pointer.y = (e.clientY - boundary.top) * (canvas.height / boundary.height);
        });

        canvas.addEventListener('mousedown', () => {
            if (ballSim.active) return;
            // 우측의 하이 콘트라스트 K-ZONE 정밀 타겟팅 세팅 바운더리 검증
            if (pointer.x > 490 && pointer.x < 870 && pointer.y > 40 && pointer.y < 400) {
                let rngError = (100 - runtimeSpecs.control) * 0.45;
                ballSim.tx = pointer.x + (Math.random() - 0.5) * rngError;
                ballSim.ty = pointer.y + (Math.random() - 0.5) * rngError;
                
                ballSim.x = 240; ballSim.y = 160;
                ballSim.pct = 0; ballSim.size = 2.5;
                ballSim.active = true;
            }
        });

        function pushCommentary(msg) {
            const board = document.getElementById('live-audio-board');
            board.innerHTML = `<span style="color:#3b82f6; font-weight:bold;">[LIVE]</span> ${msg}<br>` + board.innerHTML;
        }

        function updateHUD() {
            document.getElementById('score-away').innerText = db.awayScore;
            document.getElementById('score-home').innerText = db.homeScore;
            document.getElementById('match-inning').innerText = `${db.inning}회${db.isTop ? '초' : '말'} (TOP 1ST)`;
            
            const renderLamps = (c, m, col) => '<span style="color:'+col+'; margin-right:4px;">●</span>'.repeat(c) + '<span style="color:#e2e8f0; margin-right:4px;">○</span>'.repeat(m-c);
            document.getElementById('b-indicators').innerHTML = renderLamps(db.b, 3, '#22c55e');
            document.getElementById('s-indicators').innerHTML = renderLamps(db.s, 2, '#eab308');
            document.getElementById('o-indicators').innerHTML = renderLamps(db.o, 3, '#ef4444');
        }

        function runAIEngine() {
            const insideStrike = (ballSim.tx >= 580 && ballSim.tx <= 760 && ballSim.ty >= 130 && ballSim.ty <= 310);
            const dynamicSpeed = runtimeSpecs.speed + Math.floor(Math.random() * 4) - 2;
            
            let pitchWeight = (dynamicSpeed - 85) * 0.015;
            const batterSwingProbability = insideStrike ? (0.64 - pitchWeight) : (0.22 + pitchWeight);
            const triggeredSwing = Math.random() < batterSwingProbability;

            if (triggeredSwing) {
                let missRate = 0.47 + pitchWeight;
                if (Math.random() > missRate) {
                    const hitResolution = Math.random();
                    if (hitResolution < 0.12) {
                        let activeRunners = db.bases.filter(x=>x).length + 1;
                        if(db.isTop) db.awayScore += activeRunners; else db.homeScore += activeRunners;
                        db.bases = [false, false, false];
                        pushCommentary(`<span style="color:#ef4444; font-weight:800;">[GRAND SLAM HOMERUN]</span> 완벽하게 받쳐놓고 쳤습니다! 담장을 훌쩍 넘기는 초대형 아치를 그립니다! (${dynamicSpeed} mph)`);
                    } else if (hitResolution < 0.46) {
                        let homeIn = db.bases[2] ? 1 : 0;
                        db.bases[2] = db.bases[1]; db.bases[1] = db.bases[0]; db.bases[0] = true;
                        if(db.isTop) db.awayScore += homeIn; else db.homeScore += homeIn;
                        pushCommentary(`[HIT] 클린 히트! 우중간을 꿰뚫는 안타가 터집니다. 주자 스피드업! (${dynamicSpeed} mph)`);
                    } else {
                        db.outs++; pushCommentary(`[OUT] 2루수 땅볼! 2루수가 잡아서 안전하게 1루로 송구하여 아웃 카운트를 올립니다.`);
                    }
                    db.s = 0; db.b = 0;
                } else {
                    db.strikes++; db.s++; pushCommentary(`[STRIKE] 헛스윙! 볼끝의 무브먼트에 배트 타이밍이 완전히 밀렸습니다. (${dynamicSpeed} mph)`);
                }
            } else {
                if (insideStrike) {
                    db.s++; pushCommentary(`[STRIKE] 루킹 스트라이크! 존 구석에 완벽히 꽂히는 스트라이크 판정입니다. (${dynamicSpeed} mph)`);
                } else {
                    db.b++; pushCommentary(`[BALL] 타자가 예리하게 볼을 골라내며 출루 싸움을 벌입니다.`);
                }
            }

            if(db.s >= 3) { db.o++; db.s = 0; db.b = 0; pushCommentary(`[삼진 아웃] 투수의 삼진 결정구가 완벽하게 작동했습니다!`); }
            if(db.b >= 4) { db.bases[0] = true; db.s = 0; db.b = 0; pushCommentary(`[베이스 포볼] 제구가 흔들리며 주자를 볼넷으로 내보냅니다.`); }
            if(db.o >= 3) { db.o = 0; db.s = 0; db.b = 0; db.bases = [false,false,false]; db.isTop = !db.isTop; if(db.isTop) db.inning++; pushCommentary(`[이닝 교대] 공수교대, 야수조가 덕아웃으로 복귀합니다.`); }
            
            pitHistory.push({ x: ballSim.tx, y: ballSim.ty, strikeFlag: insideStrike });
            if(pitHistory.length > 7) pitHistory.shift();
            updateHUD();
        }

        function gameGraphicsLoop() {
            // 화이트 스타일 캔버스 베이스 초기화 리셋
            ctx.fillStyle = "#ffffff"; ctx.fillRect(0, 0, canvas.width, canvas.height);

            // --- [1] 좌측 구역: EA Retro 야구장 (원근법 포수 시점 배치) ---
            let grassPalette = ctx.createLinearGradient(240, 360, 240, 100);
            grassPalette.addColorStop(0, '#16a34a'); grassPalette.addColorStop(1, '#166534');
            ctx.fillStyle = grassPalette;
            
            // 포수 마스크 뷰 부채꼴 시야각 드로잉
            ctx.beginPath();
            ctx.moveTo(240, 380); // 포수 홈 플레이트 백스탑
            ctx.lineTo(410, 110); // 우측 외야 펜스 방향 라인
            ctx.lineTo(70, 110);  // 좌측 외야 펜스 방향 라인
            ctx.closePath(); ctx.fill();

            // 리얼 마운드 흙 및 플레이트 마킹
            ctx.fillStyle = "#b45309"; ctx.beginPath(); ctx.ellipse(240, 160, 25, 8, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#ffffff"; ctx.fillRect(232, 158, 16, 2); // 투수 투판 고화질 렌더

            // 원근법 다이아몬드 베이스 라인 가공
            const buildCatcherBase = (bx, by, stateFlag) => {
                ctx.fillStyle = stateFlag ? "#ef4444" : "#f1f5f9";
                ctx.strokeStyle = stateFlag ? "#f87171" : "#94a3b8";
                ctx.lineWidth = 2;
                ctx.save(); ctx.translate(bx, by); ctx.rotate(45 * Math.PI / 180);
                ctx.fillRect(-6, -6, 12, 12); ctx.strokeRect(-6, -6, 12, 12); ctx.restore();
            };
            buildCatcherBase(310, 225, db.bases[0]); // 1루
            buildCatcherBase(240, 140, db.bases[1]); // 2루
            buildCatcherBase(170, 225, db.bases[2]); // 3루

            // 포수 앞 홈플레이트 오각형 시네마틱 화이트 마킹
            ctx.fillStyle = "#e2e8f0";
            ctx.beginPath(); ctx.moveTo(240, 350); ctx.lineTo(255, 362); ctx.lineTo(255, 370); ctx.lineTo(225, 370); ctx.lineTo(225, 362);
            ctx.closePath(); ctx.fill();

            // 마운드 위의 투수 엔티티 실루엣 (원근 축소)
            ctx.fillStyle = "#1e293b"; ctx.beginPath(); ctx.arc(240, 150, 4, 0, Math.PI*2); ctx.fill();
            ctx.fillRect(238, 154, 4, 8);

            // 우타자 시네마틱 스탠딩 위젯 배팅 기어
            ctx.fillStyle = "#2563eb"; ctx.beginPath(); ctx.arc(195, 340, 8, 0, Math.PI*2); ctx.fill(); // 타자 머리
            ctx.strokeStyle = "#78350f"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(195, 342); ctx.lineTo(215, 315); ctx.stroke(); // 배트 라인

            // 센트럴 디바이더 파티션 라인
            ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(455, 10); ctx.lineTo(455, 430); ctx.stroke();

            // --- [2] 우측 구역: UHD 디지털 브로드캐스트 스트라이크 존 ---
            ctx.fillStyle = "rgba(37, 99, 235, 0.02)"; ctx.fillRect(580, 130, 180, 180);
            ctx.strokeStyle = "#2563eb"; ctx.lineWidth = 4; ctx.strokeRect(580, 130, 180, 180); // 주 스트라이크 사각형
            
            // 9분할 인디케이터 라인 처리
            ctx.strokeStyle = "rgba(37, 99, 235, 0.15)"; ctx.lineWidth = 1.5;
            for(let i=1; i<3; i++) {
                ctx.beginPath(); ctx.moveTo(580 + (i * 60), 130); ctx.lineTo(580 + (i * 60), 310); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(580, 130 + (i * 60)); ctx.lineTo(760, 130 + (i * 60)); ctx.stroke();
            }
            ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 1; ctx.strokeRect(510, 60, 320, 320); // 외곽 보더 존

            // 레이저 조준 크로스헤어 피드백 메커니즘
            if (pointer.x > 490 && pointer.x < 870 && pointer.y > 40 && pointer.y < 400 && !ballSim.active) {
                ctx.strokeStyle = "rgba(37, 99, 235, 0.25)"; ctx.setLineDash([3, 4]);
                ctx.beginPath(); ctx.moveTo(pointer.x, 40); ctx.lineTo(pointer.x, 380);
                ctx.beginPath(); ctx.moveTo(510, pointer.y); ctx.lineTo(830, pointer.y); ctx.stroke(); ctx.setLineDash([]);
                
                ctx.strokeStyle = "#ea580c"; ctx.lineWidth = 2.5;
                ctx.beginPath(); ctx.arc(pointer.x, pointer.y, 14, 0, Math.PI * 2); ctx.stroke();
            }

            // 히스토리 점 투구 맵 출력
            pitHistory.forEach(p => {
                ctx.fillStyle = p.strikeFlag ? "#22c55e" : "#ef4444";
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(p.x, p.y, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            });

            // --- [3] 리얼타임 물리 변화구 시뮬레이션 물리 모델 연산 ---
            if (ballSim.active) {
                ballSim.pct += 0.045; // 비행 속도 가속 프레임 비율
                
                // 베지에 형태의 원근 보간 가중치 수학 연산
                ballSim.x = ballSim.startX + (ballSim.tx - ballSim.startX) * ballSim.pct;
                ballSim.y = ballSim.startY + (ballSim.ty - ballSim.startY) * ballSim.pct;
                
                // 포수 시점 3D 입체 변형: 공이 다가올수록 크기가 기하급수적으로 팽창
                ballSim.size = 2.0 + (ballSim.pct * 8.5);

                // 구종별 고유의 실제 낙차/커브 브레이킹 효과 주입 연산
                if (ballSim.pct < 0.85) {
                    if (runtimeSpecs.type.includes("Slider")) ballSim.x += runtimeSpecs.break * 0.9;
                    if (runtimeSpecs.type.includes("Changeup")) ballSim.y += runtimeSpecs.break * 0.7;
                    if (runtimeSpecs.type.includes("Curve")) {
                        ballSim.y += runtimeSpecs.break * 1.3;
                        ballSim.x -= runtimeSpecs.break * 0.4; // 종/횡 동시 브레이킹 야구 역학
                    }
                }

                // 공 3D 글로우 화이트 쉐이딩 처리
                ctx.fillStyle = "#ffffff";
                ctx.strokeStyle = "#64748b"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(ballSim.x, ballSim.y, ballSim.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

                if (ballSim.pct >= 1.0) {
                    ballSim.active = false;
                    runAIEngine();
                }
            }

            requestAnimationFrame(gameGraphicsLoop);
        }

        updateHUD();
        gameGraphicsLoop();
    </script>
    """

    # --- 데이터 문자열 교체 조립 및 샌드박스 컴포넌트 렌더링 ---
    assembled_engine = (
        core_game_engine_html
        .replace("__AWAY__", away_abbr)
        .replace("__HOME__", home_abbr)
        .replace("__PITCHER__", p_name)
        .replace("__TYPE__", selected_pitch)
        .replace("__SPEED__", str(speed))
        .replace("__CONTROL__", str(control_stat))
        .replace("__BREAK__", str(break_val))
    )

    st.components.v1.html(assembled_engine, height=680)

    # 경기 전면 초기화 리셋 제어 장치
    st.write("")
    if st.button("🔄 RETURN TO MATCH CONFIG (구단 및 투수 재설정)"):
        st.session_state.game_started = False
        st.rerun()

if __name__ == "__main__":
    main()
