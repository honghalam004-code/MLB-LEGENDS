import streamlit as st
import json

def main():
    # 🏟️ 화면을 넓게 쓰기 위해 와이드 모드 강제 고정 및 타이틀 설정
    st.set_page_config(page_title="MLB CATCHER VIEW - MEGA WIDE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #090d16; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; }
        .stSelectbox > div > div { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #22c55e !important; }
        .stButton > button {
            background: linear-gradient(135deg, #22c55e 0%, #15803d 100%) !important;
            color: white !important; font-weight: bold !important; border: none !important; padding: 14px; border-radius: 8px; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # =========================================================================
    # 📊 MLB 30개 전 구단 마스터 데이터베이스 (정교한 고유 스펙 유지)
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

    # 30개 구단 자동 연계 가동 파이프라인
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
        st.markdown("<h2 style='text-align:center; color:#22c55e; font-weight:800; margin-top:20px;'>🏟️ MLB CATCHER VIEW: MEGA WIDE EDITION</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("아군 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            sel_pitcher = st.selectbox("선발 투수 선택", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("상대 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        if st.button("🏟️ 와이드 그라운드 정식 입장"):
            st.session_state.p_team = u_team
            st.session_state.a_team = a_team
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.p_data = mlb_mega_db[u_team]["pitchers"][sel_pitcher]
            st.session_state.a_data = mlb_mega_db[a_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    # 🖥️ 와이드 스크린 비율 최적화 배치 (그라운드를 압도적으로 크게 설정)
    col_canvas, col_panel = st.columns([3.8, 1.2])

    with col_panel:
        st.markdown("### 📊 LIVE DASHBOARD")
        st.success(f"**투수:** {st.session_state.pitcher_name}\n\n**구단:** {st.session_state.p_team}")
        st.warning(f"**상대 공격:** {st.session_state.a_team}")
        st.selectbox("🙋 현재 타석", st.session_state.a_data["lineup"])
        st.markdown("---")
        if st.button("🚪 경기 종료 및 퇴장"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#22c55e" if idx == 1 else "#1e293b"
            pitch_buttons += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" id="p{idx}" style="background:{bg}; color:white; border:1px solid #22c55e; padding:12px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:8px; font-weight:bold; font-size:14px;">{p_name}</button>'

        # 가로 780px, 세로 560px로 캔버스를 크게 키운 하이엔드 하이브리드 엔진
        html_src = f"""
        <div style="max-width:1100px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:14px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold; border:2px solid #334155; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="color:#67e8f9; font-size:16px;">🏟️ {st.session_state.p_team} GRAND STADIUM</div>
                <div id="abs-box" style="color:#22c55e; background:#0f172a; padding:2px 12px; border:1px solid #22c55e; border-radius:4px; font-size:13px; font-weight:800;">ABS READY</div>
                <div id="score-board" style="color:#fbbf24; font-size:16px; letter-spacing:1px;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="ballCanvas" width="780" height="560" style="background:#14532d; border:4px solid #334155; border-radius:8px; box-shadow: inset 0 0 50px rgba(0,0,0,0.6);"></canvas>
                
                <div style="width:240px; background:#1e293b; padding:14px; border-radius:8px; height:fit-content; border:1px solid #334155; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
                    <span style="color:#94a3b8; font-size:13px; font-weight:bold; display:block; margin-bottom:8px;">⚾ 포수 사인 완료 (SET)</span>
                    <div style="margin-top:6px;">{pitch_buttons}</div>
                    <div style="margin-top:15px; background:#0f172a; padding:10px; border-radius:6px; font-size:13px; font-weight:bold; text-align:center; color:#38bdf8; border:1px solid #1e293b;" id="base-viewer">주자 없음</div>
                </div>
            </div>

            <div style="background:#0f172a; border-left:6px solid #22c55e; padding:14px; border-radius:6px; margin-top:12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="font-size:12px; color:#22c55e; font-weight:800; margin-bottom:6px; letter-spacing:1px;">🎙️ REAL-TIME LIVE COMMENTARY LOG (누적 중계)</div>
                <div id="relay-container" style="color:#f1f5f9; font-size:14px; font-family:monospace; max-height:110px; overflow-y:auto; display:flex; flex-direction:column-reverse; gap:6px; line-height:1.4;">
                    <div style="color: #a1a1aa;">[현장 중계석] 구단주님, 초대형 와이드 경기장에 오신 것을 환영합니다! 미트 조준 후 투구 사인을 입력하세요.</div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('ballCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitches)[0];

            // 🏟️ 확대된 와이드 화면 좌표계에 맞춘 9인 정식 포메이션 정밀 재조정
            let players = [
                {{ id: "투수", x: 390, y: 190, sx: 390, sy: 190, tx: 390, ty: 190 }},
                {{ id: "포수", x: 390, y: 520, sx: 390, sy: 520, tx: 390, ty: 520 }},
                {{ id: "1루수", x: 610, y: 300, sx: 610, sy: 300, tx: 610, ty: 300 }},
                {{ id: "2루수", x: 500, y: 220, sx: 500, sy: 220, tx: 500, ty: 220 }},
                {{ id: "3루수", x: 170, y: 300, sx: 170, sy: 300, tx: 170, ty: 300 }},
                {{ id: "유격수", x: 280, y: 220, sx: 280, sy: 220, tx: 280, ty: 220 }},
                {{ id: "좌익수", x: 120, y: 100, sx: 120, sy: 100, tx: 120, ty: 100 }},
                {{ id: "중견수", x: 390, y: 70, sx: 390, sy: 70, tx: 390, ty: 70 }},
                {{ id: "우익수", x: 660, y: 100, sx: 660, sy: 100, tx: 660, ty: 100 }}
            ];

            let runner = {{ active: false, x: 610, y: 300, status: "stay", speed: 3.2 }};
            let isTargeting = false;
            let targetPos = {{ x: 390, y: 410 }};
            
            let ball = {{ active: false, status: "ready", x: 390, y: 190, z: 0.0, tx: 390, ty: 410, speed: 0, drag: 1.0, bx: 0, by: 0 }};
            let hitBall = {{ active: false, x: 390, y: 410, vx: 0, vy: 0, isBunt: false }};
            let batter = {{ swinging: false, frame: 0, mode: "normal", swingRot: 0 }};
            let catcherThrow = {{ active: false, x: 390, y: 520, vx: 0, vy: 0 }};

            // 🎙️ 누적형 해설 출력 함수 (기존 메시지를 밀어내며 쌓임)
            function addLog(msg) {{
                const container = document.getElementById('relay-container');
                const div = document.createElement('div');
                div.innerHTML = msg;
                container.insertBefore(div, container.firstChild);
            }}

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
                    catcherThrow.x = 390; catcherThrow.y = 520;
                    let dx = 390 - 390, dy = 220 - 520;
                    let d = Math.hypot(dx, dy);
                    catcherThrow.vx = (dx/d)*14; catcherThrow.vy = (dy/d)*14;
                    addLog("<span style='color:#67e8f9;'>⚡ [송구] 포수가 2루 정면으로 레이저 송구를 격발했습니다!</span>");
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
                ball.z = 0.0; ball.x = 390; ball.y = 190;
                ball.tx = targetPos.x; ball.ty = targetPos.y;
                ball.speed = p.speed; ball.drag = p.drag; ball.bx = p.bx; ball.by = p.by;
                ball.active = true; ball.status = "go";
                
                batter.swinging = false; batter.frame = 0;
                batter.mode = (Math.random() < 0.24) ? "bunt" : "normal";

                if (runner.active && Math.random() < 0.48) {{
                    runner.status = "stealing";
                    addLog("<span style='color:#facc15;'>🏃 [도루] 1루 주자가 2루를 향해 거칠게 스타트를 끊습니다!</span>");
                }}
                players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
            }}

            function judgeZone() {{
                ball.active = false;
                // 와이드 스크린에 맞춰 스트라이크 존 박스 정밀 좌표 스케일링 판정
                let isStrike = (ball.x >= 310 && ball.x <= 470 && ball.y >= 300 && ball.y <= 440);
                batter.swinging = true;

                let chance = isStrike ? 0.64 : 0.14;
                if (batter.mode === "bunt") chance = isStrike ? 0.84 : 0.34;

                if (Math.random() < chance) {{
                    ball.status = "hit"; hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y;
                    
                    if (batter.mode === "bunt") {{
                        hitBall.isBunt = true; hitBall.vx = (Math.random() - 0.5) * 4.5; hitBall.vy = -(2.0 + Math.random() * 2);
                        addLog("<span style='color:#fbbf24;'>🥎 [번트] 기습 번트! 타구가 내야 마운드 옆 흙바닥으로 천천히 구릅니다!</span>");
                    }} else {{
                        hitBall.isBunt = false; hitBall.vx = (Math.random() - 0.5) * 18; hitBall.vy = -(7 + Math.random() * 12);
                        addLog("<span style='color:#f87171;'>💥 [타격] 깡!! 정타 작렬! 타구가 총알 같은 속도로 뻗어 나갑니다!</span>");
                    }}

                    let dx = hitBall.x + hitBall.vx * 15, dy = hitBall.y + hitBall.vy * 15;
                    let closest = null, minDist = 9999;
                    players.forEach(pl => {{
                        if (pl.id !== "투수" && pl.id !== "포수") {{
                            let d = Math.hypot(pl.sx - dx, pl.sy - dy);
                            if (d < minDist) {{ minDist = d; closest = pl; }}
                        }}
                    }});

                    let maxRange = hitBall.isBunt ? 200 : 160;
                    if (closest && minDist < maxRange) {{ closest.tx = dx; closest.ty = dy; }}
                }} else {{
                    let box = document.getElementById('abs-box');
                    if (isStrike) {{
                        count.s++; box.innerText = "ABS: STRIKE"; box.style.color = "#ef4444"; box.style.borderColor = "#ef4444";
                        addLog("⚾ [ABS 판정] 스트라이크! 정밀 보간 궤적이 보더라인을 통과했습니다.");
                    }} else {{
                        count.b++; box.innerText = "ABS: BALL"; box.style.color = "#3b82f6"; box.style.borderColor = "#3b82f6";
                        addLog("🔵 [ABS 판정] 볼! 포수 미트가 바깥쪽으로 크게 빠졌습니다.");
                    }}

                    if (count.s >= 3) {{ count.o++; count.s=0; count.b=0; addLog("❌ [아웃] 삼진 아웃!! 완벽한 결정구로 타자를 돌려세웁니다!"); }}
                    else if (count.b >= 4) {{ count.s=0; count.b=0; runner.active = true; addLog("🏃 [출루] 볼넷! 타자가 베이스로 걸어 나갑니다."); }}
                    if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; addLog("🔄 [이닝 교체] 공수대교가 선언됩니다."); }}
                    
                    document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                    if (runner.status === "stealing") {{
                        runner.x = 390; runner.y = 220; runner.status = "stay";
                        document.getElementById('base-viewer').innerText = "주자 2루";
                    }}
                    ball.status = "ready";
                }}
            }}

            function loop() {{
                ctx.clearRect(0,0,780,560);
                batter.swingRot += 0.04;

                // 🏟️ 시원하게 확장된 정통 와이드 야구장 필드라인 드로우
                ctx.fillStyle = "#15803d"; ctx.fillRect(0,0,780,560);
                ctx.fillStyle = "#b45309"; ctx.beginPath(); ctx.moveTo(40,560); ctx.lineTo(340,190); ctx.lineTo(440,190); ctx.lineTo(740,560); ctx.fill();

                // ABS 트랙킹 스트라이크 존 박스 정밀 드로우 (확대 반영)
                ctx.strokeStyle = "rgba(255,255,255,0.35)"; ctx.lineWidth = 2; ctx.strokeRect(310, 300, 160, 140);

                // 홈플레이트 형상 마스터링
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(390,480); ctx.lineTo(420,498); ctx.lineTo(420,520); ctx.lineTo(360,520); ctx.lineTo(360,498); ctx.fill();

                // 🧑 리얼 배트 전환 타자 시스템 타격 모션
                ctx.save(); ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3.5;
                let tx = 250, ty = 380, wb = Math.sin(batter.swingRot)*1.5;
                ctx.beginPath(); ctx.arc(tx, ty-25+wb, 7, 0, Math.PI*2); ctx.fillStyle="#ffffff"; ctx.fill(); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty-18+wb); ctx.lineTo(tx, ty+10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty+10); ctx.lineTo(tx-10, ty+30); ctx.moveTo(tx, ty+10); ctx.lineTo(tx+10, ty+30); ctx.stroke();

                ctx.translate(tx, ty-8);
                if (batter.mode === "bunt") {{
                    ctx.rotate(Math.PI * 0.42); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(-10, -3); ctx.lineTo(38, -3); ctx.stroke();
                }} else if (batter.swinging) {{
                    let ang = (batter.frame / 12) * Math.PI * 0.85; ctx.rotate(ang); batter.frame++;
                    if(batter.frame > 12) batter.swinging = false;
                    ctx.strokeStyle = "#d97706"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(48, -16); ctx.stroke();
                }} else {{
                    ctx.rotate(-Math.PI * 0.12 + Math.sin(batter.swingRot)*0.03);
                    ctx.strokeStyle = "#d97706"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(48, -16); ctx.stroke();
                }}
                ctx.restore();

                // 🏃 주자 트래킹 가동
                if (runner.active) {{
                    if (runner.status === "stealing") {{
                        let dx = 390 - runner.x, dy = 220 - runner.y, d = Math.hypot(dx, dy);
                        if (d > 4) {{ runner.x += (dx/d)*runner.speed; runner.y += (dy/d)*runner.speed; }}
                    }}
                    ctx.fillStyle = "#facc15"; ctx.beginPath(); ctx.arc(runner.x, runner.y, 8, 0, Math.PI*2); ctx.fill();
                }}

                // 🧤 포수 송구 레이저 물리
                if (catcherThrow.active) {{
                    catcherThrow.x += catcherThrow.vx; catcherThrow.y += catcherThrow.vy;
                    ctx.fillStyle = "#22d3ee"; ctx.beginPath(); ctx.arc(catcherThrow.x, catcherThrow.y, 6, 0, Math.PI*2); ctx.fill();
                    if (catcherThrow.y <= 220) {{
                        catcherThrow.active = false;
                        if (Math.hypot(runner.x - 390, runner.y - 220) < 30) {{
                            runner.active = false; runner.status = "stay"; count.o++;
                            if (count.o >= 3) count.o = 0;
                            document.getElementById('base-viewer').innerText = "주자 없음";
                            document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                            addLog("<span style='color:#ef4444;'>🧤 [태그아웃] 포수 견제 대성공! 완벽한 송구로 주자를 지워버립니다!</span>");
                        }} else {{
                            runner.x = 390; runner.y = 220; runner.status = "stay";
                            document.getElementById('base-viewer').innerText = "주자 2루";
                            addLog("<span style='color:#34d399;'>⚡ [세이프] 야구 타이밍의 한 끗 차이! 슬라이딩 주자가 세이프 판정을 얻어냅니다!</span>");
                        }}
                    }}
                }}

                // 🏃 9인 정식 대형 수비진 렌더링 및 복귀 기믹
                players.forEach(pl => {{
                    pl.x += (pl.tx - pl.x) * 0.08; pl.y += (pl.ty - pl.y) * 0.08;

                    if (hitBall.active && Math.hypot(pl.x - hitBall.x, pl.y - hitBall.y) < 25) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }}); // 전 수비수 상황 종료 즉시 칼복귀 리셋
                        if (runner.status === "stealing") {{ runner.status = "stay"; runner.x = 390; runner.y = 220; }}
                        
                        count.o++; if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                        addLog("🧤 [수비 성공] " + pl.id + "수가 엄청난 반사신경으로 낙구 지점에 다이빙하여 아웃카운트를 선사합니다!");
                    }}

                    ctx.fillStyle = (pl.id === "투수" || pl.id === "포수") ? "#475569" : (pl.tx !== pl.sx ? "#ef4444" : "#2563eb");
                    ctx.beginPath(); ctx.arc(pl.x, pl.y, 9, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 10px sans-serif"; ctx.fillText(pl.id, pl.x-14, pl.y-12);
                }});

                if (isTargeting) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 11, 0, Math.PI*2); ctx.stroke();
                }}

                // ⚾ 5대 시그니처 구종 변화 물리 연산
                if (ball.active && ball.status === "go") {{
                    ball.speed *= ball.drag; ball.z += ball.speed;
                    let mx = Math.sin(ball.z * Math.PI) * ball.bx * 3.6;
                    let my = Math.pow(ball.z, 2) * ball.by * 3.8;

                    ball.x = 390 + (ball.tx - 390)*ball.z + mx;
                    ball.y = 190 + (ball.ty - 190)*ball.z + my;

                    let bSize = Math.max(4.0, 4.5 + ball.z * 16);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, bSize, 0, Math.PI*2); ctx.fill();
                    if (ball.z >= 1.0) {{ ball.z = 1.0; judgeZone(); }}
                }}

                // 🥎 타구 비행 및 경기 종료 연계 시스템
                if (hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 6.5, 0, Math.PI*2); ctx.fill();

                    if (hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 780) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        count.s = 0; count.b = 0;
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;

                        if (!runner.active) {{
                            runner.active = true; runner.x = 610; runner.y = 300;
                            document.getElementById('base-viewer').innerText = "주자 1루";
                            addLog("📢 [안타] 수비진 포위망을 뚫었습니다! 안타로 주자가 1루 베이스를 점령합니다.");
                        }} else {{
                            document.getElementById('base-viewer').innerText = "주자 홈인! 득점 대성공!"; runner.active = false;
                            addLog("<span style='color:#fbbf24;'>🎉 [득점] 주자가 모든 베이스를 돌아 홈플레이트를 강타합니다! 1득점 성공!</span>");
                        }}
                    }}
                }}

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(html_src, height=720)

if __name__ == "__main__":
    main()
