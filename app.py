import streamlit as st
import json

def main():
    # 1. 고대비 다크 테마 & 전광판 야구장 스타일 적용
    st.set_page_config(page_title="MLB STATCAST REAL GAME", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox, .stRadio { background: #1e293b !important; color: #f8fafc !important; border-radius: 8px; border: 2px solid #334155 !important; }
        label { color: #94a3b8 !important; font-weight: 800 !important; font-size: 15px !important; }
        .stButton>button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important; font-weight: 900 !important; padding: 14px 28px !important; 
            border-radius: 10px !important; border: none !important; font-size: 16px !important;
            width: 100%; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    # MLB 30개 구단 실제 Statcast 데이터 기반 빌드
    mlb_30_teams = {
        "NY Yankees (뉴욕 양키스)": {
            "pitcher": "게릿 콜", "speed": 96, "control": 92, "pitches": ["포심 직구", "너클 커브", "슬라이더"],
            "lineup": [{"name": "후안 소토", "contact": 93, "power": 94}, {"name": "애런 저지", "contact": 89, "power": 100}, {"name": "지안카를로 스탠튼", "contact": 72, "power": 95}]
        },
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitcher": "오타니 쇼헤이", "speed": 97, "control": 82, "pitches": ["포심 직구", "스위퍼", "스플리터"],
            "lineup": [{"name": "무키 베츠", "contact": 93, "power": 79}, {"name": "프레디 프리먼", "contact": 94, "power": 84}, {"name": "오타니 쇼헤이", "contact": 91, "power": 99}]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitcher": "딜런 시즈", "speed": 96, "control": 83, "pitches": ["슬라이더", "포심 직구", "너클 커브"],
            "lineup": [{"name": "루이스 아라에즈", "contact": 99, "power": 45}, {"name": "페르난도 타티스 Jr.", "contact": 88, "power": 92}, {"name": "매니 마차도", "contact": 85, "power": 88}]
        },
        "SF Giants (샌프란시스코 자이언츠)": {
            "pitcher": "로건 웹", "speed": 92, "control": 93, "pitches": ["체인지업", "싱커", "슬라이더"],
            "lineup": [{"name": "이정후", "contact": 88, "power": 55}, {"name": "맷 채프먼", "contact": 80, "power": 84}, {"name": "헬리오트 라모스", "contact": 82, "power": 79}]
        }
    }

    # 기본 구단 외 간소화를 위해 주요 4개 구단으로 예시 구성 (원하면 이전 리스트 복사 가능)
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 2. 게임 셋업 로비
    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #111827; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #2563eb; max-width: 900px; margin: 30px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB STATCAST 리얼 이닝 시뮬레이터</h1>
                <p style="color: #94a3b8; font-weight: 600; margin-top: 5px;">공격(타격)과 수비(투구)가 실제로 교대되는 리얼 나인 이닝 경기</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            team_away = st.selectbox("🎯 플레이어 팀 선택 (초 공격 시작)", list(mlb_30_teams.keys()), index=1)
        with c2:
            team_home = st.selectbox("🏠 상대 AI 팀 선택 (말 공격 시작)", list(mlb_30_teams.keys()), index=0)
            
        if st.button("🏟️ 경기 시작 (스타디움 입장)"):
            st.session_state.away_title = team_away.split(" (")[0]
            st.session_state.home_title = team_home.split(" (")[0]
            
            # 플레이어 팀 데이터
            st.session_state.user_pitcher = mlb_30_teams[team_away]['pitcher']
            st.session_state.user_pitches = mlb_30_teams[team_away]['pitches']
            st.session_state.user_speed = mlb_30_teams[team_away]['speed']
            st.session_state.user_lineup = mlb_30_teams[team_away]['lineup']
            
            # AI 팀 데이터
            st.session_state.ai_pitcher = mlb_30_teams[team_home]['pitcher']
            st.session_state.ai_pitches = mlb_30_teams[team_home]['pitches']
            st.session_state.ai_speed = mlb_30_teams[team_home]['speed']
            st.session_state.ai_lineup = mlb_30_teams[team_home]['lineup']
            
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    # 3. 인게임 데이터 변수 바인딩
    user_lineup_json = json.dumps(st.session_state.user_lineup, ensure_ascii=False)
    ai_lineup_json = json.dumps(st.session_state.ai_lineup, ensure_ascii=False)
    user_pitches_json = json.dumps(st.session_state.user_pitches, ensure_ascii=False)
    ai_pitches_json = json.dumps(st.session_state.ai_pitches, ensure_ascii=False)

    st.markdown(f"### 🏟️ 현재 경기: {st.session_state.away_title} (USER) vs {st.session_state.home_title} (AI)")

    # UI 조절 사이드 패널
    col_ctrl1, col_ctrl2 = st.columns([1, 3])
    with col_ctrl1:
        st.markdown("### 🎮 작전 지시 룸")
        st.info("💡 **공수교대 자동 제어:**\n3아웃이 되면 화면이 '수비(투수)' 모드와 '공격(타자)' 모드로 자동 전환됩니다!")
        user_select_pitch = st.selectbox("🔮 [수비 시] 내가 던질 구종 선택", st.session_state.user_pitches)
        user_style = st.slider("⚖️ 피칭 스타일 (제구 vs 구속)", 0, 100, 50)
    
    with col_ctrl2:
        # 4. 자바스크립트 통합 엔진 (리얼 전광판 + 주자 다이아몬드 + 공수교대 루프)
        game_canvas_html = f"""
        <div style="background: #111827; padding: 15px; border-radius: 12px; border: 2px solid #334155; max-width: 900px; margin: 0 auto;">
            
            <div style="background: #020617; border: 2px solid #1e293b; border-radius: 8px; padding: 12px; margin-bottom: 10px; font-family: monospace;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <table style="color: #ffffff; font-size: 16px; text-align: center; border-collapse: collapse; width: 45%;">
                        <tr style="color: #64748b; font-size: 12px;">
                            <th style="width: 40%; text-align: left;">TEAM</th><th style="width: 15%;">R</th><th style="width: 15%;">H</th><th style="width: 15%;">E</th>
                        </tr>
                        <tr>
                            <td style="text-align: left; font-weight: bold; color: #3b82f6;">{st.session_state.away_title[:8]} (플레이어)</td>
                            <td id="sb-r-away" style="font-weight: 900; color: #3b82f6;">0</td><td id="sb-h-away">0</td><td>0</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; font-weight: bold; color: #f43f5e;">{st.session_state.home_title[:8]} (AI)</td>
                            <td id="sb-r-home" style="font-weight: 900; color: #f43f5e;">0</td><td id="sb-h-home">0</td><td>0</td>
                        </tr>
                    </table>

                    <div style="width: 20%; text-align: center;">
                        <div id="sb-inning" style="color: #38bdf8; font-size: 18px; font-weight: 900; margin-bottom: 5px;">1회 초</div>
                        <div id="sb-turn-badge" style="background: #2563eb; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px; font-weight: bold;">공격 모드</div>
                    </div>

                    <div style="display: flex; width: 30%; justify-content: space-around; align-items: center;">
                        <div style="font-size: 14px; line-height: 1.4; font-weight: bold; text-align: left;">
                            <span style="color: #64748b;">B</span> <span id="b-dots" style="color: #10b981;">○○</span><br>
                            <span style="color: #64748b;">S</span> <span id="s-dots" style="color: #fbbf24;">○○</span><br>
                            <span style="color: #64748b;">O</span> <span id="o-dots" style="color: #ef4444;">○○</span>
                        </div>
                        <canvas id="diamondCanvas" width="70" height="70" style="background: transparent;"></canvas>
                    </div>
                </div>
            </div>

            <canvas id="gameCanvas" width="880" height="420" style="background: #0f172a; border: 1px solid #1e293b; display: block; border-radius: 6px;"></canvas>
            
            <div style="background: #020617; color: #f8fafc; padding: 18px; border-radius: 6px; font-size: 18px; font-weight: 700; margin-top: 8px; border-left: 6px solid #2563eb; text-align: left;">
                <span id="game-ticker" style="color: #38bdf8;">🏟️ 경기장에 불이 켜졌습니다. 플레이어 팀의 1회초 공격으로 경기를 시작합니다! 화면을 클릭해 타격하세요.</span>
            </div>
        </div>

        <script>
            const cv = document.getElementById('gameCanvas');
            const cx = cv.getContext('2d');
            const dCv = document.getElementById('diamondCanvas');
            const dCx = dCv.getContext('2d');

            // 파이썬 데이터 연동
            const USER_ROSTER = {user_lineup_json};
            const AI_ROSTER = {ai_lineup_json};
            const USER_PITCHES = {user_pitches_json};
            const AI_PITCHES = {ai_pitches_json};
            
            const USER_BASE_SPEED = {st.session_state.user_speed};
            const AI_BASE_SPEED = {st.session_state.ai_speed};

            // 전역 야구 엔진 핵심 상태 변수
            let match = {{
                inning: 1,
                isTop: true, // true: 초(플레이어 공격), false: 말(플레이어 수비-투수)
                scoreAway: 0, scoreHome: 0,
                hitsAway: 0, hitsHome: 0,
                b: 0, s: 0, o: 0,
                user_idx: 0, ai_idx: 0,
                bases: [false, false, false], // 1루, 2루, 3루 주자 여부
                isPlayerTurn: true // true: 타자 스윙 유도, false: 투수 피칭 유도
            }};

            let ball = {{ active: false, x: 440, y: 120, tx: 440, ty: 240, time: 0, size: 2, currentSpeed: 0 }};
            let pointer = {{ x: 440, y: 240 }};
            let isActionDone = false;
            let currentPitchName = "";
            let trail = [];

            // 마우스 추적 (수비 투수 모드 시 조준용)
            cv.addEventListener('mousemove', (e) => {{
                const r = cv.getBoundingClientRect();
                pointer.x = (e.clientX - r.left) * (cv.width / r.width);
                pointer.y = (e.clientY - r.top) * (cv.height / r.height);
            }});

            // 메인 인게임 클릭 액션 (공격일 땐 타이밍 스윙 / 수비일 땐 피칭 배달)
            cv.addEventListener('mousedown', () => {{
                if (ball.active) {{
                    // [공격 모드] 공이 날아오는 도중 클릭하면 스윙 판단
                    if (match.isTop && !isActionDone) {{
                        isActionDone = true;
                        evaluateSwing();
                    }}
                    return;
                }}

                // 공이 없을 때 클릭하면 공 배달 스타트
                if (match.isTop) {{
                    // AI가 투구 던짐 (공격 모드)
                    let pIndex = Math.floor(Math.random() * AI_PITCHES.length);
                    currentPitchName = AI_PITCHES[pIndex];
                    ball.currentSpeed = AI_BASE_SPEED + Math.floor(Math.random() * 5) - 2;
                    
                    // 투구 목표 지점 랜덤 설정
                    ball.tx = 380 + Math.random() * 120;
                    ball.ty = 180 + Math.random() * 120;
                    
                    initBallReady();
                }} else {{
                    // 플레이어가 투구 던짐 (수비 모드)
                    currentPitchName = "{user_select_pitch}";
                    ball.currentSpeed = USER_BASE_SPEED + Math.floor((100 - {user_style})*0.05);
                    
                    // 플레이어가 조준한 마우스 커서 위치로 피칭 타겟 고정
                    ball.tx = pointer.x;
                    ball.ty = pointer.y;
                    
                    initBallReady();
                    document.getElementById('game-ticker').innerText = "⚾ 플레이어가 " + ball.currentSpeed + " mph " + currentPitchName + " 투구를 시작했습니다!";
                }}
            }});

            function initBallReady() {{
                ball.x = 440; ball.y = 120;
                ball.time = 0; ball.size = 2;
                trail = []; isActionDone = false;
                ball.active = true;
            }}

            // 공격 모드: 플레이어 스윙 타이밍 정밀 채점
            function evaluateSwing() {{
                const batter = USER_ROSTER[match.user_idx];
                let t = ball.time;
                
                // 최적의 정타 타이밍 존 (0.83 ~ 0.95)
                if (t >= 0.83 && t <= 0.95) {{
                    let dice = Math.random() + (batter.power - 70) * 0.01;
                    if (dice > 1.05) {{
                        triggerHit(4, "💥 대형 홈런!! 타자 " + batter.name + "가 복판에 몰린 공을 놓치지 않고 담장 밖으로 넘깁니다!");
                    }} else if (dice > 0.4) {{
                        triggerHit(1, "⚾ 안타!! 깔끔한 밀어치기로 수비 벽을 뚫어내는 안타를 기록합니다.");
                    }} else {{
                        triggerHit(2, "🔥 2루타 장타 폭발!! 우중간을 완전히 갈라놓는 웰컴 안타!");
                    }}
                }} else {{
                    match.s++;
                    document.getElementById('game-ticker').innerHTML = "<span style='color:#f59e0b;'>헛스윙!!</span> 타이밍이 어긋나며 공기를 갈랐습니다.";
                    updateCounts();
                }}
            }}

            // 수비 모드: AI 타자 루틴 자동화 채점
            function evaluateAIAtBat() {{
                const batter = AI_ROSTER[match.ai_idx];
                const inZone = (ball.tx >= 360 && ball.tx <= 520 && ball.ty >= 160 && ball.ty <= 320);
                
                let swingProb = inZone ? 0.65 : 0.25;
                if (Math.random() < swingProb) {{
                    // 스윙함
                    if (Math.random() > 0.35) {{
                        // 안타성
                        let dice = Math.random();
                        if (dice > 0.85) triggerHit(4, "🚨 AI 홈런 경보!! " + batter.name + "에게 일격을 당해 실점합니다.");
                        else triggerHit(1, "🏃 AI 안타: 빠른 유격수 키를 넘기는 안타로 주자가 출루합니다.");
                    }} else {{
                        match.s++;
                        document.getElementById('game-ticker').innerText = "🎯 헛스윙 삼진 유도! 플레이어의 볼끝이 예리했습니다.";
                        updateCounts();
                    }}
                }} else {{
                    // 지켜봄
                    if (inZone) {{
                        match.s++;
                        document.getElementById('game-ticker').innerText = "👌 루킹 스트라이크! 존 구석을 정밀 타격했습니다.";
                    }} else {{
                        match.b++;
                        document.getElementById('game-ticker').innerText = "✋ 볼 판정: 타자가 속지 않고 차분히 골라냅니다.";
                    }}
                    updateCounts();
                }}
            }}

            // 안타 및 진루 베이스 연산 유닛 (실제 야구 로직 구현)
            function triggerHit(basesCount, msg) {{
                document.getElementById('game-ticker').innerHTML = "<span style='color:#10b981; font-weight:900;'>" + msg + "</span>";
                
                if (match.isTop) match.hitsAway++; else match.hitsHome++;
                
                let runsScored = 0;
                // 주자 이동 시뮬레이션
                if (basesCount === 4) {{ // 홈런
                    runsScored = 1 + match.bases.filter(b => b).length;
                    match.bases = [false, false, false];
                }} else {{
                    // 안타 진루 연산 반복 수행
                    for (let h = 0; h < basesCount; h++) {{
                        if (match.bases[2]) {{ runsScored++; match.bases[2] = false; }}
                        if (match.bases[1]) {{ match.bases[2] = true; match.bases[1] = false; }}
                        if (match.bases[0]) {{ match.bases[1] = true; match.bases[0] = false; }}
                        if (h === 0) match.bases[0] = true;
                    }}
                }}

                if (match.isTop) match.scoreAway += runsScored; else match.scoreHome += runsScored;
                
                // 아웃카운트 제외 볼카운트 초기화
                match.b = 0; match.s = 0;
                updateCounts();
            }}

            // 아웃카운트 및 이닝 스위칭(공수교대) 로직 핵심 조율기
            function updateCounts() {{
                if (match.s >= 3) {{ match.o++; match.s = 0; match.b = 0; document.getElementById('game-ticker').innerText += " 🎯 삼진 아웃!!"; }}
                if (match.b >= 4) {{ triggerHit(1, "🚶 볼넷 출루 성공! 밀어내기 찬스가 다가옵니다."); }}
                
                if (match.o >= 3) {{
                    // 🚨 쓰리아웃 공수교대 발동!!
                    match.o = 0; match.s = 0; match.b = 0;
                    match.bases = [false, false, false]; // 루상 주자 리셋
                    
                    if (match.isTop) {{
                        match.isTop = false; // 초 -> 말 (유저 수비 전환)
                        match.user_idx = (match.user_idx + 1) % USER_ROSTER.length;
                        document.getElementById('game-ticker').innerHTML = "🔄 <b>공수교대!</b> 플레이어가 이제 투수가 되어 마우스로 조준 투구(수비)합니다.";
                    }} else {{
                        match.isTop = true; // 말 -> 다음이닝 초 (유저 공격 전환)
                        match.ai_idx = (match.ai_idx + 1) % AI_ROSTER.length;
                        match.inning++;
                        document.getElementById('game-ticker').innerHTML = "🔄 <b>공수교대! " + match.inning + "회초 공격 시작</b> 화면을 클릭해 배트를 휘두르세요!";
                    }}
                }}

                // HTML 하드웨어 스코어 업데이트 보정
                document.getElementById('sb-r-away').innerText = match.scoreAway;
                document.getElementById('sb-r-home').innerText = match.scoreHome;
                document.getElementById('sb-h-away').innerText = match.hitsAway;
                document.getElementById('sb-h-home').innerText = match.hitsHome;
                document.getElementById('sb-inning').innerText = match.inning + "회 " + (match.isTop ? "초" : "말");
                document.getElementById('sb-turn-badge').innerText = match.isTop ? "공격 모드 (타자)" : "수비 모드 (투수)";
                
                document.getElementById('b-dots').innerText = "●".repeat(match.b) + "○".repeat(2-match.b);
                document.getElementById('s-dots').innerText = "●".repeat(match.s) + "○".repeat(2-match.s);
                document.getElementById('o-dots').innerText = "●".repeat(match.o) + "○".repeat(2-match.o);
                
                drawDiamond();
            }}

            // 미니 주자 다이아몬드 실시간 렌더러
            function drawDiamond() {{
                dCx.clearRect(0,0,70,70);
                const pts = [{{x:50, y:35}}, {{x:35, y:20}}, {{x:20, y:35}}]; // 1루, 2루, 3루 배치 좌표
                
                // 외곽 다이아몬드 선
                dCx.strokeStyle = "#334155"; dCx.lineWidth = 2;
                dCx.beginPath(); dCx.moveTo(35, 5); dCx.lineTo(65, 35); dCx.lineTo(35, 65); dCx.lineTo(5, 35); dCx.closePath(); dCx.stroke();
                
                // 베이스 채우기 활성화 체크
                for(let i=0; i<3; i++) {{
                    dCx.fillStyle = match.bases[i] ? "#38bdf8" : "#1e293b";
                    dCx.fillRect(pts[i].x-5, pts[i].y-5, 10, 10);
                    dCx.strokeStyle = "#475569"; dCx.strokeRect(pts[i].x-5, pts[i].y-5, 10, 10);
                }}
            }}

            // 애니메이션 루프 스크린
            function drawScene() {{
                cx.clearRect(0, 0, 880, 420);
                
                // 야구장 원근 필드 가이드라인 그리기
                cx.fillStyle = "#1e293b"; cx.beginPath();
                cx.moveTo(360, 420); cx.lineTo(520, 420); cx.lineTo(470, 120); cx.lineTo(410, 120);
                cx.closePath(); cx.fill();

                // 스트라이크 스트라이프 사각형 그리드 포지셔닝
                cx.strokeStyle = "rgba(255, 255, 255, 0.25)"; cx.lineWidth = 2;
                cx.strokeRect(360, 160, 160, 160);

                if (ball.active) {{
                    let speedStep = 0.026 + (ball.currentSpeed / 100) * 0.015;
                    ball.time += speedStep;

                    let lx = 440 + (ball.tx - 440) * ball.time;
                    let ly = 120 + (ball.ty - 120) * ball.time;
                    ball.size = 2 + (Math.pow(ball.time, 3.5) * 30);

                    // 구종별 무브먼트 궤적 튜닝 파트
                    let curveOffsetX = 0;
                    if(currentPitchName.includes("슬라이더") || currentPitchName.includes("스위퍼")) {{
                        curveOffsetX = Math.sin(ball.time * Math.PI) * 45;
                    }} else if(currentPitchName.includes("커브")) {{
                        curveOffsetX = Math.sin(ball.time * Math.PI) * 20;
                        ly += Math.sin(ball.time * Math.PI) * 25;
                    }}

                    ball.x = lx + curveOffsetX;
                    ball.y = ly;
                    trail.push({{ x: ball.x, y: ball.y }});

                    // 궤적 자취 드로잉
                    cx.beginPath(); cx.strokeStyle = "rgba(56, 189, 248, 0.5)"; cx.lineWidth = 3;
                    for (let i = 0; i < trail.length; i++) {{
                        if (i === 0) cx.moveTo(trail[i].x, trail[i].y); else cx.lineTo(trail[i].x, trail[i].y);
                    }}
                    cx.stroke();

                    // 야구공 본체
                    cx.fillStyle = "#ffffff"; cx.strokeStyle = "#000000"; cx.lineWidth = 2;
                    cx.beginPath(); cx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); cx.fill(); cx.stroke();

                    if (ball.time >= 1.0) {{
                        ball.active = false;
                        if (!match.isTop) {{
                            // 수비 모드일 때는 공이 다 오면 AI 타격 채점 작동
                            evaluateAIAtBat();
                        }} else {{
                            // 공격 모드인데 플레이어가 안 쳤을 때 지켜본 루킹 카운트 처리
                            if (!isActionDone) {{
                                const inZone = (ball.tx >= 360 && ball.tx <= 520 && ball.ty >= 160 && ball.ty <= 320);
                                if (inZone) {{ match.s++; document.getElementById('game-ticker').innerText = "⚠️ 루킹 스트라이크 존 통과!"; }}
                                else {{ match.b++; document.getElementById('game-ticker').innerText = "👀 잘 골라냈습니다! 볼 판정."; }}
                                updateCounts();
                            }}
                        }}
                    }}
                }}

                // 수비 모드 전용 십자 조준선 미트 가이드 활성화
                if (!match.isTop && !ball.active) {{
                    cx.strokeStyle = "#f43f5e"; cx.lineWidth = 2;
                    cx.beginPath();
                    cx.arc(pointer.x, pointer.y, 18, 0, Math.PI*2);
                    cx.moveTo(pointer.x-25, pointer.y); cx.lineTo(pointer.x+25, pointer.y);
                    cx.moveTo(pointer.x, pointer.y-25); cx.lineTo(pointer.x, pointer.y+25);
                    cx.stroke();
                }}

                // 하단 타석 정보 인디케이터 라벨링텍스트
                cx.fillStyle = "#94a3b8"; cx.font = "bold 13px sans-serif";
                if (match.isTop) {{
                    cx.fillText("현재 타자(플레이어): " + USER_ROSTER[match.user_idx].name + " [파워: " + USER_ROSTER[match.user_idx].power + "]", 20, 395);
                    cx.fillText("상대 AI 투수: {st.session_state.ai_pitcher} (평속 " + AI_BASE_SPEED + " mph)", 20, 411);
                }} else {{
                    cx.fillText("현재 타자(AI): " + AI_ROSTER[match.ai_idx].name + " [파워: " + AI_ROSTER[match.ai_idx].power + "]", 20, 395);
                    cx.fillText("내 투수: {st.session_state.user_pitcher} | 마우스 클릭 지점으로 제구 투구 발사 가능", 20, 411);
                }}

                requestAnimationFrame(drawScene);
            }}

            // 초기 보드 세팅 구동
            drawDiamond();
            drawScene();
        </script>
        """
        st.components.v1.html(game_canvas_html, height=620)

    st.markdown("---")
    if st.button("🔄 게임 초기화 및 구단 선택 화면으로 가기"):
        st.session_state.game_active = False
        st.rerun()

if __name__ == "__main__":
    main()
