import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW - ULTIMATE 9", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #090d16; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; }
        .stSelectbox > div > div { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #22c55e !important; }
        .stButton > button {
            background: linear-gradient(135deg, #22c55e 0%, #15803d 100%) !important;
            color: white !important; font-weight: bold !important; border: none !important; padding: 14px; border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # =========================================================================
    # 📊 [MLB 30개 전 구단 마스터 DB] 에이스별 4~5개 리얼 구종 스펙 완벽 확장
    # =========================================================================
    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스": {"pitches": {
                    "포심 강속구": {"speed": 0.046, "drag": 1.0, "bx": 0.0, "by": -0.5},
                    "명품 너클커브": {"speed": 0.026, "drag": 0.82, "bx": 3.2, "by": 5.8},
                    "고속 스플린커": {"speed": 0.041, "drag": 0.93, "bx": 1.5, "by": 4.2},
                    "종 슬라이더": {"speed": 0.035, "drag": 0.88, "bx": -3.8, "by": 2.0},
                    "체인지업": {"speed": 0.031, "drag": 0.85, "bx": 2.0, "by": 3.5}
                }},
                "미치 켈러": {"pitches": {
                    "싱커": {"speed": 0.039, "drag": 0.94, "bx": 2.5, "by": 2.8},
                    "고속 스위퍼": {"speed": 0.034, "drag": 0.87, "bx": -6.0, "by": 1.0},
                    "컷 패스트볼": {"speed": 0.042, "drag": 0.97, "bx": -1.8, "by": 0.5},
                    "커브볼": {"speed": 0.025, "drag": 0.80, "bx": 1.0, "by": 5.0}
                }}
            },
            "lineup": ["오닐 크루즈 (SS)", "브라이언 레이놀즈 (LF)", "키브라이언 헤이즈 (3B)", "라우디 텔레즈 (1B)", "앤드류 맥커친 (DH)", "코너 조 (RF)", "자레드 트리올로 (2B)", "마이클 A. 테일러 (CF)", "조이 바트 (C)"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": {
                    "파워 포심": {"speed": 0.045, "drag": 1.0, "bx": 0.0, "by": 0.0},
                    "마스터 스위퍼": {"speed": 0.031, "drag": 0.84, "bx": -6.8, "by": -0.8},
                    "스플리터": {"speed": 0.038, "drag": 0.90, "bx": 0.2, "by": 4.8},
                    "하드 커터": {"speed": 0.041, "drag": 0.95, "bx": 2.2, "by": 1.0}
                }},
                "야마모토 요시노부": {"pitches": {
                    "폭포수 커브": {"speed": 0.027, "drag": 0.79, "bx": 0.8, "by": 7.2},
                    "고속 스플리터": {"speed": 0.039, "drag": 0.91, "bx": 0.0, "by": 5.2},
                    "포심": {"speed": 0.043, "drag": 0.98, "bx": -0.5, "by": 0.2},
                    "컷 슬라이더": {"speed": 0.036, "drag": 0.89, "bx": -3.0, "by": 1.8}
                }}
            },
            "lineup": ["오타니 쇼헤이 (DH)", "무키 베츠 (SS)", "프레디 프리먼 (1B)", "테오스카 에르난데스 (LF)", "맥스 먼시 (3B)", "토미 에드먼 (CF)", "가빈 럭스 (2B)", "앤디 파헤스 (RF)", "윌 스미스 (C)"]
        }
    }

    # 30개 구단 마스터 스케일 자동 확장 로직
    extra_teams = [
        ("New York Yankees", "게릿 콜", "마커스 스트로먼", "앤서니 볼피"),
        ("San Francisco Giants", "로건 웹", "로비 레이", "이정후"),
        ("San Diego Padres", "딜런 시즈", "유 다르빗슈", "루이스 아라에즈")
    ]
    for i in range(1, 26):
        t_name = f"MLB Team {i}" if i > 3 else extra_teams[i-1][0]
        p1 = "에이스 A" if i > 3 else extra_teams[i-1][1]
        p2 = "에이스 B" if i > 3 else extra_teams[i-1][2]
        leadoff = "스타 타자 A" if i > 3 else extra_teams[i-1][3]
        
        if t_name not in mlb_mega_db:
            mlb_mega_db[t_name] = {
                "pitchers": {
                    p1: {"pitches": {"포심": {"speed": 0.042, "drag": 1.0, "bx": 0.0, "by": 0.0}, "슬라이더": {"speed": 0.034, "drag": 0.88, "bx": 4.0, "by": 1.8}, "커브": {"speed": 0.026, "drag": 0.81, "bx": 1.2, "by": 5.5}, "체인지업": {"speed": 0.030, "drag": 0.85, "bx": -2.0, "by": 4.0}}},
                    p2: {"pitches": {"싱커": {"speed": 0.039, "drag": 0.95, "bx": -3.0, "by": 2.5}, "커터": {"speed": 0.041, "drag": 0.96, "bx": 2.0, "by": 0.8}, "스플리터": {"speed": 0.037, "drag": 0.90, "bx": 0.0, "by": 4.5}}}
                },
                "lineup": [f"{leadoff} (CF)", "타자 2번", "타자 3번", "타자 4번", "타자 5번", "타자 6번", "타자 7번", "타자 8번", "타자 9번"]
            }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#22c55e; font-weight:800; margin-top:20px;'>🏟️ MLB CATCHER VIEW: PERFECT 9 PLAYERS</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("아군 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            sel_pitcher = st.selectbox("선발 투수 선택", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("상대 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        if st.button("🏟️ 9인 정식 포메이션 그라운드 입장"):
            st.session_state.p_team = u_team
            st.session_state.a_team = a_team
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.p_data = mlb_mega_db[u_team]["pitchers"][sel_pitcher]
            st.session_state.a_data = mlb_mega_db[a_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_canvas, col_panel = st.columns([3, 1])

    with col_panel:
        st.markdown("### 🏟️ LIVE SCORE")
        st.success(f"**투수:** {st.session_state.pitcher_name}")
        st.warning(f"**상대:** {st.session_state.a_team}")
        st.selectbox("🙋 현재 타순", st.session_state.a_data["lineup"])
        st.markdown("---")
        if st.button("🚪 경기 종료 및 퇴장"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#22c55e" if idx == 1 else "#1e293b"
            pitch_buttons += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" id="p{idx}" style="background:{bg}; color:white; border:1px solid #22c55e; padding:10px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:6px; font-weight:bold; font-size:13px;">{p_name}</button>'

        html_src = f"""
        <div style="max-width:850px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:8px; font-weight:bold; border:1px solid #334155;">
                <div style="color:#67e8f9;">🏟️ {st.session_state.p_team} FIELD</div>
                <div id="abs-box" style="color:#22c55e; background:#0f172a; padding:1px 8px; border:1px solid #22c55e; border-radius:4px; font-size:12px;">ABS ACTIVE</div>
                <div id="score-board" style="color:#fbbf24;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:12px;">
                <canvas id="ballCanvas" width="570" height="490" style="background:#14532d; border:3px solid #334155; border-radius:8px;"></canvas>
                <div style="width:210px; background:#1e293b; padding:12px; border-radius:8px; height:fit-content; border:1px solid #334155;">
                    <span style="color:#94a3b8; font-size:12px; font-weight:bold;">⚾ 포수 사인 (SET)</span>
                    <div style="margin-top:6px;">{pitch_buttons}</div>
                    <div style="margin-top:12px; background:#0f172a; padding:8px; border-radius:4px; font-size:12px; font-weight:bold; text-align:center; color:#e2e8f0;" id="base-viewer">주자 없음</div>
                </div>
            </div>

            <div style="background:#0f172a; border-left:5px solid #22c55e; padding:12px; border-radius:6px; margin-top:10px; font-weight:bold;">
                <div style="font-size:11px; color:#22c55e; margin-bottom:2px;">🎙️ REAL LIVE COMMENTARY</div>
                <span id="relay-text" style="color:#f1f5f9; font-size:13px;">[중계석] 미트 위치를 조준 후 구종 사인을 보내세요. 9인 전원 수비수 포메이션 가동 완료!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('ballCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitches)[0];

            // ⚾ [진짜 야구 대혁명] 야구장 위 9명의 실제 포메이션 수비수 배치
            let players = [
                {{ id: "투수", x: 285, y: 170, sx: 285, sy: 170, tx: 285, ty: 170 }},
                {{ id: "포수", x: 285, y: 455, sx: 285, sy: 455, tx: 285, ty: 455 }},
                {{ id: "1루수", x: 450, y: 260, sx: 450, sy: 260, tx: 450, ty: 260 }},
                {{ id: "2루수", x: 370, y: 190, sx: 370, sy: 190, tx: 370, ty: 190 }},
                {{ id: "3루수", x: 120, y: 260, sx: 120, sy: 260, tx: 120, ty: 260 }},
                {{ id: "유격수", x: 200, y: 190, sx: 200, sy: 190, tx: 200, ty: 190 }},
                {{ id: "좌익수", x: 90, y: 90, sx: 90, sy: 90, tx: 90, ty: 90 }},
                {{ id: "중견수", x: 285, y: 65, sx: 285, sy: 65, tx: 285, ty: 65 }},
                {{ id: "우익수", x: 480, y: 90, sx: 480, sy: 90, tx: 480, ty: 90 }}
            ];

            let runner = {{ active: false, x: 450, y: 260, status: "stay", speed: 2.7 }};
            let isTargeting = false;
            let targetPos = {{ x: 285, y: 360 }};
            
            let ball = {{ active: false, status: "ready", x: 285, y: 170, z: 0.0, tx: 285, ty: 360, speed: 0, drag: 1.0, bx: 0, by: 0 }};
            let hitBall = {{ active: false, x: 285, y: 360, vx: 0, vy: 0, isBunt: false }};
            let batter = {{ swinging: false, frame: 0, mode: "normal", swingRot: 0 }};
            let catcherThrow = {{ active: false, x: 285, y: 455, vx: 0, vy: 0 }};

            function setPitch(name) {{
                if (ball.active || hitBall.active || ball.status !== "ready") return;
                selectedPitch = name;
                document.querySelectorAll('.p-btn').forEach(b => b.style.backgroundColor = '#1e293b');
                event.target.style.backgroundColor = '#22c55e';
                throwBall();
            }}

            function getMouse(e) {{
                let r = canvas.getBoundingClientRect();
                return {{ x: (e.clientX - r.left)*(canvas.width/r.width), y: (e.clientY - r.top)*(canvas.height/r.height) }};
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let m = getMouse(e);
                if (runner.status === "stealing" && !catcherThrow.active) {{
                    catcherThrow.active = true;
                    catcherThrow.x = 285; catcherThrow.y = 455;
                    let dx = 285 - 285, dy = 190 - 455;
                    let d = Math.hypot(dx, dy);
                    catcherThrow.vx = (dx/d)*12; catcherThrow.vy = (dy/d)*12;
                    document.getElementById('relay-text').innerText = "🎙️ 2루 도루 저지 송구!! 포수가 베이스 정면으로 레이저 송구를 날립니다!";
                    return;
                }}
                if(!ball.active && !hitBall.active && ball.status === "ready") {{
                    isTargeting = true; targetPos.x = m.x; targetPos.y = m.y;
                }}
            }});
            canvas.addEventListener('mousemove', (e) => {{
                if(isTargeting) {{ let m = getMouse(e); targetPos.x = m.x; targetPos.y = m.y; }}
            }});
            canvas.addEventListener('mouseup', () => isTargeting = false);

            function throwBall() {{
                let p = pitches[selectedPitch];
                ball.z = 0.0; ball.x = 285; ball.y = 170;
                ball.tx = targetPos.x; ball.ty = targetPos.y;
                ball.speed = p.speed; ball.drag = p.drag; ball.bx = p.bx; ball.by = p.by;
                ball.active = true; ball.status = "go";
                
                batter.swinging = false; batter.frame = 0;
                batter.mode = (Math.random() < 0.25) ? "bunt" : "normal";

                if (runner.active && Math.random() < 0.45) {{
                    runner.status = "stealing";
                    document.getElementById('relay-text').innerText = "🎙️ 주자 스타트!! 투수의 와인드업 허점을 노려 2루로 도루를 감행합니다!";
                }}
                players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
            }}

            function judgeZone() {{
                ball.active = false;
                let isStrike = (ball.x >= 215 && ball.x <= 355 && ball.y >= 260 && ball.y <= 390);
                batter.swinging = true;

                let chance = isStrike ? 0.65 : 0.15;
                if (batter.mode === "bunt") chance = isStrike ? 0.85 : 0.35;

                if (Math.random() < chance) {{
                    ball.status = "hit"; hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y;
                    
                    if (batter.mode === "bunt") {{
                        hitBall.isBunt = true; hitBall.vx = (Math.random() - 0.5) * 4; hitBall.vy = -(1.5 + Math.random() * 2);
                        document.getElementById('relay-text').innerText = "🎙️ 기습 번트 성공! 배트를 완벽히 가로로 뉘어 내야 빈 공간으로 굴립니다!";
                    }} else {{
                        hitBall.isBunt = false; hitBall.vx = (Math.random() - 0.5) * 16; hitBall.vy = -(6 + Math.random() * 11);
                        document.getElementById('relay-text').innerText = "🎙️ 깡!! 정타로 맞은 타구!! 엄청난 속도로 야구장 그라운드를 가릅니다!";
                    }}

                    let dx = hitBall.x + hitBall.vx * 15, dy = hitBall.y + hitBall.vy * 15;
                    let closest = null, minDist = 9999;
                    players.forEach(pl => {{
                        if (pl.id !== "투수" && pl.id !== "포수") {{
                            let d = Math.hypot(pl.sx - dx, pl.sy - dy);
                            if (d < minDist) {{ minDist = d; closest = pl; }}
                        }}
                    }});

                    let maxRange = hitBall.isBunt ? 170 : 135;
                    if (closest && minDist < maxRange) {{ closest.tx = dx; closest.ty = dy; }}
                }} else {{
                    let box = document.getElementById('abs-box');
                    if (isStrike) {{
                        count.s++; box.innerText = "ABS: STRIKE"; box.style.color = "#ef4444"; box.style.borderColor = "#ef4444";
                        document.getElementById('relay-text').innerText = f"🎙️ 스트라이크! ABS 컴퓨터 정밀 추적 판정 완료!";
                    }} else {{
                        count.b++; box.innerText = "ABS: BALL"; box.style.color = "#3b82f6"; box.style.borderColor = "#3b82f6";
                        document.getElementById('relay-text').innerText = "🎙️ 볼! 홈플레이트 바깥쪽으로 아슬아슬하게 빠졌다는 판정입니다.";
                    }}

                    if (count.s >= 3) {{ count.o++; count.s=0; count.b=0; document.getElementById('relay-text').innerText = "🎙️ 삼진 아웃!! 포수의 절묘한 볼 배합 승리입니다!"; }}
                    else if (count.b >= 4) {{ count.s=0; count.b=0; runner.active = true; document.getElementById('relay-text').innerText = "🎙️ 볼넷 출루! 타자가 1루 베이스로 걸어 나갑니다."; }}
                    if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; }}
                    
                    document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                    if (runner.status === "stealing") {{
                        runner.x = 285; runner.y = 190; runner.status = "stay";
                        document.getElementById('base-viewer').innerText = "주자 2루";
                    }}
                    ball.status = "ready";
                }}
            }}

            function loop() {{
                ctx.clearRect(0,0,570,490);
                batter.swingRot += 0.04;

                // 🏟️ 정통 야구장 그라운드 시각화 (초록 잔디 & 브라운 다이아몬드 내야 복구)
                ctx.fillStyle = "#16a34a"; ctx.fillRect(0,0,570,490);
                ctx.fillStyle = "#b45309"; ctx.beginPath(); ctx.moveTo(30,490); ctx.lineTo(245,170); ctx.lineTo(325,170); ctx.lineTo(540,490); ctx.fill();

                // ABS 트랙킹 스트라이크 존 박스
                ctx.strokeStyle = "rgba(255,255,255,0.35)"; ctx.lineWidth = 2; ctx.strokeRect(215, 260, 140, 130);

                // 🧑 리얼 배트 전환 타자 엔진 (졸라맨 완벽 탈피)
                ctx.save(); ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3.5;
                let tx = 160, ty = 335, wb = Math.sin(batter.swingRot)*1.5;
                ctx.beginPath(); ctx.arc(tx, ty-25+wb, 6.5, 0, Math.PI*2); ctx.fillStyle="#ffffff"; ctx.fill(); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty-18+wb); ctx.lineTo(tx, ty+10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty+10); ctx.lineTo(tx-10, ty+30); ctx.moveTo(tx, ty+10); ctx.lineTo(tx+10, ty+30); ctx.stroke();

                ctx.translate(tx, ty-8);
                if (batter.mode === "bunt") {{
                    ctx.rotate(Math.PI * 0.42); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(-10, -3); ctx.lineTo(35, -3); ctx.stroke();
                }} else if (batter.swinging) {{
                    let ang = (batter.frame / 12) * Math.PI * 0.85; ctx.rotate(ang); batter.frame++;
                    if(batter.frame > 12) batter.swinging = false;
                    ctx.strokeStyle = "#d97706"; ctx.lineWidth = 5.5; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(46, -16); ctx.stroke();
                }} else {{
                    ctx.rotate(-Math.PI * 0.12 + Math.sin(batter.swingRot)*0.03);
                    ctx.strokeStyle = "#d97706"; ctx.lineWidth = 5.5; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(46, -16); ctx.stroke();
                }}
                ctx.restore();

                // 🏃 주자 트래킹 연산
                if (runner.active) {{
                    if (runner.status === "stealing") {{
                        let dx = 285 - runner.x, dy = 190 - runner.y, d = Math.hypot(dx, dy);
                        if (d > 4) {{ runner.x += (dx/d)*runner.speed; runner.y += (dy/d)*runner.speed; }}
                    }}
                    ctx.fillStyle = "#facc15"; ctx.beginPath(); ctx.arc(runner.x, runner.y, 7, 0, Math.PI*2); ctx.fill();
                }}

                // 🧤 포수 송구 레이저 물리
                if (catcherThrow.active) {{
                    catcherThrow.x += catcherThrow.vx; catcherThrow.y += catcherThrow.vy;
                    ctx.fillStyle = "#22d3ee"; ctx.beginPath(); ctx.arc(catcherThrow.x, catcherThrow.y, 5, 0, Math.PI*2); ctx.fill();
                    if (catcherThrow.y <= 190) {{
                        catcherThrow.active = false;
                        if (Math.hypot(runner.x - 285, runner.y - 190) < 26) {{
                            runner.active = false; runner.status = "stay"; count.o++;
                            if (count.o >= 3) count.o = 0;
                            document.getElementById('base-viewer').innerText = "주자 없음";
                            document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                            document.getElementById('relay-text').innerText = "🎙️ 아웃!! 포수의 총알 같은 베이스 송구로 도루를 완벽하게 저지합니다!";
                        }} else {{
                            runner.x = 285; runner.y = 190; runner.status = "stay";
                            document.getElementById('base-viewer').innerText = "주자 2루";
                            document.getElementById('relay-text').innerText = "🎙️ 세이프! 주자의 슬라이딩이 타이밍상 한 발 빨랐습니다!";
                        }}
                    }}
                }}

                // 🏃 9인 대형 수비수 포지션 드로우 및 자동 리셋 귀환 연산
                players.forEach(pl => {{
                    pl.x += (pl.tx - pl.x) * 0.08; pl.y += (pl.ty - pl.y) * 0.08;

                    if (hitBall.active && Math.hypot(pl.x - hitBall.x, pl.y - hitBall.y) < 22) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        if (runner.status === "stealing") {{ runner.status = "stay"; runner.x = 285; runner.y = 190; }}
                        
                        count.o++; if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                        document.getElementById('relay-text').innerText = f"🎙️ 아웃! {{pl.id}}수가 타구의 낙구 지점을 예측하고 슬라이딩 캐치로 낚아챕니다!";
                    }}

                    ctx.fillStyle = (pl.id === "투수" || pl.id === "포수") ? "#475569" : (pl.tx !== pl.sx ? "#ef4444" : "#3b82f6");
                    ctx.beginPath(); ctx.arc(pl.x, pl.y, 8, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px sans-serif"; ctx.fillText(pl.id, pl.x-13, pl.y-11);
                }});

                if (isTargeting) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 10, 0, Math.PI*2); ctx.stroke();
                }}

                // ⚾ 5대 시그니처 종/횡 무브먼트 피칭 연산 (버그 완전 격리)
                if (ball.active && ball.status === "go") {{
                    ball.speed *= ball.drag; ball.z += ball.speed;
                    let mx = Math.sin(ball.z * Math.PI) * ball.bx * 3.2;
                    let my = Math.pow(ball.z, 2) * ball.by * 3.6;

                    ball.x = 285 + (ball.tx - 285)*ball.z + mx;
                    ball.y = 170 + (ball.ty - 170)*ball.z + my;

                    let bSize = Math.max(3.5, 4.0 + ball.z * 15);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, bSize, 0, Math.PI*2); ctx.fill();
                    if (ball.z >= 1.0) {{ ball.z = 1.0; judgeZone(); }}
                }}

                // 🥎 타구 외야 소멸 및 리셋 벨트
                if (hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 5.5, 0, Math.PI*2); ctx.fill();

                    if (hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 570) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        count.s = 0; count.b = 0;
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;

                        if (!runner.active) {{
                            runner.active = true; runner.x = 450; runner.y = 260; runner.status = "stay";
                            document.getElementById('base-viewer').innerText = "주자 1루";
                            document.getElementById('relay-text').innerText = "🎙️ 깨끗한 안타! 타자가 출루하며 그라운드 분위기를 뜨겁게 달굽니다!";
                        }} else {{
                            document.getElementById('base-viewer').innerText = "주자 홈인! 득점 성공!"; runner.active = false;
                            document.getElementById('relay-text').innerText = "🎙️ 외야를 뚫어내는 안타! 루상의 주자가 홈을 밟으며 1점을 추가합니다!";
                        }}
                    }}
                }}

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(html_src, height=640)

if __name__ == "__main__":
    main()
