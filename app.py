import streamlit as st
import json

def main():
    st.set_page_config(page_title="REAL CATCHER EYE", layout="wide")
    
    # 눈이 시원해지는 고대비 화이트 가이드 스타일
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; color: #0f172a; font-family: sans-serif; }
        .stSelectbox, .stRadio { background: #ffffff !important; color: #0f172a !important; border-radius: 8px; border: 2px solid #cbd5e1 !important; }
        div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #0f172a !important; }
        label { color: #334155 !important; font-weight: 700 !important; }
        .stButton>button {
            background: #0f172a !important; color: white !important; font-weight: 900 !important; 
            padding: 14px 24px !important; border-radius: 8px !important; border: none !important; width: 100%;
        }
        .stat-box { background: #ffffff; padding: 14px; border-radius: 10px; border: 2px solid #e2e8f0; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)

    # 8대 구단 및 라인업 싱크 데이터
    mlb_roster_db = {
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitchers": {"오타니 쇼헤이": {"pitches": ["포심 직구", "스위퍼", "스플리터"], "speed": 101, "control": 82}, "야마모토 요시노부": {"pitches": ["포심 직구", "명품 커브"], "speed": 97, "control": 93}},
            "lineup": [{"name": "무키 베츠", "contact": 94, "power": 78}, {"name": "프레디 프리먼", "contact": 95, "power": 83}, {"name": "오타니 쇼헤이", "contact": 91, "power": 99}]
        },
        "NY Yankees (뉴욕 양키스)": {
            "pitchers": {"게릿 콜": {"pitches": ["포심 직구", "너클 커브"], "speed": 99, "control": 92}},
            "lineup": [{"name": "후안 소토", "contact": 93, "power": 94}, {"name": "애런 저지", "contact": 89, "power": 100}]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitchers": {"유 다르빗슈": {"pitches": ["포심 직구", "슬라이더"], "speed": 95, "control": 89}},
            "lineup": [{"name": "페르난도 타티스 Jr.", "contact": 87, "power": 92}, {"name": "김하성", "contact": 80, "power": 68}]
        }
    }

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # 1. 경기 셋업 로비
    if not st.session_state.game_started:
        st.title("⚾ 1인칭 리얼 포수 시점 매치업")
        col1, col2 = st.columns(2)
        with col1:
            away_team_sel = st.selectbox("🎯 AWAY 공격 구단", list(mlb_roster_db.keys()), index=1)
        with col2:
            home_team_sel = st.selectbox("🏠 HOME 수비 구단", list(mlb_roster_db.keys()), index=0)
            pitcher_sel = st.selectbox("👤 등판 투수 선택", list(mlb_roster_db[home_team_sel]['pitchers'].keys()))
            
        if st.button("🏟️ 포수 마스크 착용 (게임 시작)"):
            st.session_state.away_title = away_team_sel.split(" (")[0]
            st.session_state.home_title = home_team_sel.split(" (")[0]
            st.session_state.active_pitcher = pitcher_sel
            st.session_state.pitcher_spec = mlb_roster_db[home_team_sel]['pitchers'][pitcher_sel]
            st.session_state.away_lineup = mlb_roster_db[away_team_sel]['lineup']
            st.session_state.game_started = True
            st.rerun()
        st.stop()

    # 2. 전력투구 vs 정밀제구 시소 시스템 변수 제어
    st.markdown(f"### 🎛️ {st.session_state.active_pitcher} 투구 컨트롤 보드")
    
    col_ctrl1, col_ctrl2 = st.columns([1, 2])
    with col_ctrl1:
        selected_pitch = st.radio("🔮 구종 선택", st.session_state.pitcher_spec['pitches'])
    with col_ctrl2:
        balance_ratio = st.slider("⚖️ 피칭 밸런스 지표 [ ◀ 구속 우선 (실투 확률 폭등) ─── 정밀 제구 (구속 감소) ▶ ]", 0, 100, 50)

    # 시소 스탯 공식 연산
    max_sp = st.session_state.pitcher_spec['speed'] + 4
    min_sp = st.session_state.pitcher_spec['speed'] - 14
    live_speed = int(max_sp - (balance_ratio / 100.0) * (max_sp - min_sp))
    live_control = int(5 + (balance_ratio / 100.0) * 92)

    st.markdown(f"📈 **현재 스펙:** 구속 **{live_speed} mph** | 제구력 **{live_control} / 100**")

    # 무브먼트 계수 가중치
    if "직구" in selected_pitch: h_break, v_break = (0.0, -1.5)
    elif "스위퍼" in selected_pitch or "슬라이더" in selected_pitch: h_break, v_break = (14.0, 2.0)
    elif "커브" in selected_pitch: h_break, v_break = (4.0, 15.0)
    else: h_break, v_break = (-1.0, 10.0) # 오프스피드

    # 3. [화이트 고대비] 1인칭 포수 시점 캔버스 파이프라인
    lineup_json = json.dumps(st.session_state.away_lineup, ensure_ascii=False)

    catcher_view_html = f"""
    <div style="background: #ffffff; padding: 10px; border-radius: 12px; border: 3px solid #0f172a; max-width: 940px; margin: 0 auto;">
        
        <div style="background: #0f172a; color: #ffffff; padding: 10px 20px; border-radius: 6px; display: flex; justify-content: space-between; font-weight: 900; font-family: monospace;">
            <div>[AWAY] {st.session_state.away_title.upper()} : <span id="txt-away-score" style="color:#ef4444;">0</span></div>
            <div id="txt-bso" style="color:#fbbf24;">B○○ S○○ O○○</div>
            <div>[HOME] {st.session_state.home_title.upper()} : <span id="txt-home-score" style="color:#3b82f6;">0</span></div>
        </div>

        <canvas id="catcherCanvas" width="900" height="500" style="background: #ffffff; border: 2px solid #0f172a; display: block; margin: 10px auto; cursor: none;"></canvas>
        
        <div style="background: #f1f5f9; color: #0f172a; padding: 12px; border-radius: 6px; font-size: 14px; font-weight: bold; border-left: 5px solid #0f172a;">
            <div id="ticker-board">💡 [포수 가이드] 화면 전체가 내 시야입니다! 마우스를 움직여 투구 예상 지점에 '포수 미트'를 대고 클릭하여 공을 받아내세요!</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('catcherCanvas');
        const ctx = canvas.getContext('2d');

        const P_NAME = "{st.session_state.active_pitcher}";
        const P_TYPE = "{selected_pitch}";
        const P_SPEED = {live_speed};
        const P_CONTROL = {live_control};
        const P_H_BREAK = {h_break};
        const P_V_BREAK = {v_break};
        const ATTACK_LINEUP = {lineup_json};

        let game = {{ awayScore: 0, homeScore: 0, b: 0, s: 0, o: 0, batterIdx: 0 }};
        let mouse = {{ x: 450, y: 250 }};
        let ball = {{ active: false, x: 450, y: 160, tx: 450, ty: 250, time: 0, size: 3 }};
        
        let trail = [];
        let isMistake = false;
        let nX = 0, nY = 0;
        let historyDots = [];

        canvas.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            mouse.x = (e.clientX - rect.left) * (canvas.width / rect.width);
            mouse.y = (e.clientY - rect.top) * (canvas.height / rect.height);
        }});

        canvas.addEventListener('mousedown', () => {{
            if (ball.active) return;

            // 제구력 기반 오차 범주 계산
            let mistakeChance = (100 - P_CONTROL) * 0.5;
            isMistake = Math.random() * 100 < mistakeChance;

            if (isMistake) {{
                // 타겟을 벗어나 정중앙 혹은 완전 엉뚱한 곳으로 실투
                ball.tx = 450 + (Math.random() - 0.5) * 60;
                ball.ty = 250 + (Math.random() - 0.5) * 60;
            }} else {{
                // 마우스로 조준한 포수 미트 위치가 곧 투구 타겟 지점
                let errorRange = (100 - P_CONTROL) * 0.4;
                ball.tx = mouse.x + (Math.random() - 0.5) * errorRange;
                ball.ty = mouse.y + (Math.random() - 0.5) * errorRange;
            }}

            // 사진 형태의 큰 포물선 궤적 유도용 무작위 회전 스핀
            nX = (Math.random() - 0.5) * 7.0;
            nY = (Math.random() - 0.5) * 7.0;

            ball.x = 450; ball.y = 160; // 저 멀리 마운드 투수 위치에서 출발
            ball.time = 0; ball.size = 3;
            trail = [];
            ball.active = true;
        }});

        function logComment(msg) {{
            document.getElementById('ticker-board').innerHTML = `💬 ${{msg}}`;
        }}

        function evalPitch() {{
            const batter = ATTACK_LINEUP[game.batterIdx];
            // 대형 스트라이크 존 판정 바운더리
            const insideSz = (ball.tx >= 320 && ball.tx <= 580 && ball.ty >= 140 && ball.ty <= 380);
            
            let swing = insideSz ? 0.70 : 0.25;
            if (isMistake) swing = 0.92;

            if (Math.random() < swing) {{
                let miss = 0.40 - (batter.contact - 70) * 0.005;
                if (isMistake) miss = 0.02;

                if (Math.random() > miss) {{
                    let pwr = (batter.power - 70) * 0.008;
                    if (isMistake) pwr += 0.55;
                    const roll = Math.random() + pwr;

                    if (roll > 1.1) {{
                        game.awayScore += 1; game.s = 0; game.b = 0;
                        logComment(`<span style="color:#ef4444;">🔥 홈런!</span> 타자 ${{batter.name}}이 실투를 받아쳐 백스크린을 넘겼습니다!`);
                    }} else if (roll > 0.45) {{
                        game.awayScore += 0; game.s = 0; game.b = 0;
                        logComment(`[안타] 시원한 타구음과 함께 외야로 뻗어나가는 안타가 됩니다.`);
                    }} else {{
                        game.o++; game.s = 0; game.b = 0;
                        logComment(`[아웃] 타이밍이 밀려 평범한 내야 땅볼로 처리됩니다.`);
                    }}
                }} else {{
                    game.s++; logComment(`[헛스윙] 무시무시하게 휘어 들어오는 볼끝에 헛방망이가 나갑니다.`);
                }}
            }} else {{
                if (insideSz) {{ game.s++; logComment(`[스트라이크] 포수 미트에 꽂히는 꽉 찬 스트라이크 주입.`); }}
                else {{ game.b++; logComment(`[볼] 원바운드성 볼을 타자가 잘 골라냈습니다.`); }}
            }}

            if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; logComment(`⚠️ 삼진 아웃! 투수 ${{P_NAME}}의 완벽한 결정구 성공.`); }}
            if (game.b >= 4) {{ game.s = 0; game.b = 0; logComment(`[볼넷] 베이스 출루를 허용합니다.`); }}
            if (game.o >= 3) {{ game.o = 0; game.s = 0; game.b = 0; logComment(`🔄 쓰리아웃 이닝 종료, 공수가 교대됩니다.`); }}

            document.getElementById('txt-away-score').innerText = game.awayScore;
            document.getElementById('txt-home-score').innerText = game.homeScore;
            document.getElementById('txt-bso').innerText = `B${{ "●".repeat(game.b) }} S${{ "●".repeat(game.s) }} O${{ "●".repeat(game.o) }}`;

            historyDots.push({{ x: ball.tx, y: ball.ty, strike: insideSz, msk: isMistake }});
            if (historyDots.length > 7) historyDots.shift();
        }}

        function drawLoop() {{
            // 눈이 부시도록 선명한 화이트 고대비 배경 청소
            ctx.fillStyle = "#ffffff"; ctx.fillRect(0,0,900,500);

            // 1. 포수 눈앞의 대형 스트라이크 존 렌더링 (화이트와 대비되는 검은 실선 구조)
            ctx.fillStyle = "#f8fafc"; ctx.fillRect(320, 140, 260, 240);
            ctx.strokeStyle = "#0f172a"; ctx.lineWidth = 4; ctx.strokeRect(320, 140, 260, 240);
            
            // 스트라이크존 가로세로 9분할 격자선
            ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 2;
            for(let i=1; i<3; i++) {{
                ctx.beginPath(); ctx.moveTo(320 + (i * 86.6), 140); ctx.lineTo(320 + (i * 86.6), 380); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(320, 140 + (i * 80)); ctx.lineTo(580, 140 + (i * 80)); ctx.stroke();
            }}

            // 저 멀리 보이는 미니어처 투수 마운드 플레이트 표시
            ctx.fillStyle = "#cbd5e1"; ctx.fillRect(435, 155, 30, 6);

            // 과거 투구 기록 히트맵 표시 (초록=스트라이크, 빨강=볼)
            historyDots.forEach(h => {{
                ctx.fillStyle = h.msk ? "#f59e0b" : (h.strike ? "#10b981" : "#ef4444");
                ctx.beginPath(); ctx.arc(h.x, h.y, 8, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.stroke();
            }});

            // 2. [주문하신 아크 포물선] 공의 물리학 연산 기믹
            if (ball.active) {{
                ball.time += 0.045;

                // 사진처럼 위로 솟구쳤다가 아래로 뚝 떨어지며 휘어지는 거대 3D 아크 포물선 궤적 수식
                let arcX = Math.sin(ball.time * Math.PI) * 70.0; 
                let arcY = -Math.sin(ball.time * Math.PI) * 45.0; 

                let lx = 450 + (ball.tx - 450) * ball.time;
                let ly = 160 + (ball.ty - 160) * ball.time;

                // 포수 시야 앞으로 올수록 공 크기가 극대화 (3D 공간 원근감)
                ball.size = 3.0 + (Math.pow(ball.time, 3.5) * 32.0);

                let breakPower = Math.pow(ball.time, 2.5);
                ball.x = lx + arcX + ((P_H_BREAK + nX) * breakPower * 2.5);
                ball.y = ly + arcY + ((P_V_BREAK + nY) * breakPower * 2.5);

                trail.push({{ x: ball.x, y: ball.y }});

                // [가장 중요] 화이트 배경 위에 칼같이 선명하게 찍히는 고대비 볼 트랙 궤적선
                ctx.beginPath();
                ctx.strokeStyle = isMistake ? "#f43f5e" : "#1e293b"; // 실투는 핑크, 일반은 먹색 선
                ctx.lineWidth = 5;
                for (let i = 0; i < trail.length; i++) {{
                    if (i === 0) ctx.moveTo(trail[i].x, trail[i].y);
                    else ctx.lineTo(trail[i].x, trail[i].y);
                }}
                ctx.stroke();

                // 야구공 본체 드로잉
                ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#0f172a"; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

                if (ball.time >= 1.0) {{
                    ball.active = false;
                    evalPitch();
                }}
            }}

            // 3. 포수 1인칭 전용 '가죽 포수 미트' 마우스 트래커 드로잉
            if (!ball.active) {{
                ctx.fillStyle = "rgba(120, 53, 4, 0.85)"; // 세련된 가죽 갈색 미트 색상
                ctx.strokeStyle = "#451a03"; ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(mouse.x, mouse.y, 25, 0, Math.PI*2); // 커다란 포수 미트 타겟
                ctx.fill(); ctx.stroke();
                
                // 미트 정중앙 크로스헤어 타겟선
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.moveTo(mouse.x - 12, mouse.y); ctx.lineTo(mouse.x + 12, mouse.y);
                ctx.moveTo(mouse.x, mouse.y - 12); ctx.lineTo(mouse.x, mouse.y + 12); ctx.stroke();
            }}

            // 타석 정보 안내 텍스트
            ctx.fillStyle = "#0f172a"; ctx.font = "bold 14px sans-serif";
            ctx.fillText(`현재 타자: ${{ATTACK_LINEUP[game.batterIdx].name}}`, 30, 450);
            ctx.fillStyle = "#475569"; ctx.font = "13px sans-serif";
            ctx.fillText(`PITCHER: ${{P_NAME}} (${{P_TYPE}} 대기 중)`, 30, 475);

            requestAnimationFrame(drawLoop);
        }}
        drawLoop();
    </script>
    """

    st.components.v1.html(catcher_view_html, height=620)

    if st.button("🔄 처음 구단 로비 리셋 화면으로 나가기"):
        st.session_state.game_started = False
        st.rerun()

if __name__ == "__main__":
    main()
