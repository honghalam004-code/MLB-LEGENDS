import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW - FIX EDITION", layout="wide")
    
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

    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스": {"pitches": {
                    "포심 강속구": {"speed": 0.046, "drag": 1.0, "bx": 0.0, "by": -0.5},
                    "명품 너클커브": {"speed": 0.026, "drag": 0.82, "bx": 3.2, "by": 5.8},
                    "고속 스플린커": {"speed": 0.041, "drag": 0.93, "bx": 1.5, "by": 4.2},
                    "종 슬라이더": {"speed": 0.035, "drag": 0.88, "bx": -3.8, "by": 2.0},
                    "체인지업": {"speed": 0.031, "drag": 0.85, "bx": 2.0, "by": 3.5}
                }}
            },
            "lineup": ["오닐 크루즈 (SS)", "브라이언 레이놀즈 (LF)", "키브라이언 헤이즈 (3B)", "라우디 텔레즈 (1B)"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": {
                    "파워 포심": {"speed": 0.045, "drag": 1.0, "bx": 0.0, "by": 0.0},
                    "마스터 스위퍼": {"speed": 0.031, "drag": 0.84, "bx": -6.8, "by": -0.8}
                }}
            },
            "lineup": ["오타니 쇼헤이 (DH)", "무키 베츠 (SS)", "프레디 프리먼 (1B)"]
        }
    }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#22c55e; font-weight:800; margin-top:20px;'>🏟️ MLB CATCHER VIEW: BUG FIX & NO-DOT</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("아군 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            sel_pitcher = st.selectbox("선발 투수 선택", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("상대 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        if st.button("🏟️ 엔진 수정판 그라운드 입장"):
            st.session_state.p_team = u_team
            st.session_state.a_team = a_team
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.p_data = mlb_mega_db[u_team]["pitchers"][sel_pitcher]
            st.session_state.a_data = mlb_mega_db[a_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

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

        html_src = f"""
        <div style="max-width:1100px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:14px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold; border:2px solid #334155;">
                <div style="color:#67e8f9; font-size:16px;">🏟️ {st.session_state.p_team} (BUG FIXED BUILD)</div>
                <div id="abs-box" style="color:#22c55e; background:#0f172a; padding:2px 12px; border:1px solid #22c55e; border-radius:4px; font-size:13px; font-weight:800;">ABS LIVE</div>
                <div id="score-board" style="color:#fbbf24; font-size:16px;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="ballCanvas" width="780" height="560" style="background:#114d22; border:4px solid #334155; border-radius:8px;"></canvas>
                <div style="width:240px; background:#1e293b; padding:14px; border-radius:8px; height:fit-content; border:1px solid #334155;">
                    <span style="color:#94a3b8; font-size:13px; font-weight:bold; display:block; margin-bottom:8px;">⚾ 포수 구종 결정</span>
                    <div style="margin-top:6px;">{pitch_buttons}</div>
                    <div style="margin-top:15px; background:#0f172a; padding:10px; border-radius:6px; font-size:13px; font-weight:bold; text-align:center; color:#38bdf8;" id="base-viewer">주자 없음</div>
                </div>
            </div>

            <div style="background:#0f172a; border-left:6px solid #22c55e; padding:14px; border-radius:6px; margin-top:12px;">
                <div style="font-size:12px; color:#22c55e; font-weight:800; margin-bottom:6px;">🎙️ REAL-TIME LIVE COMMENTARY LOG (누적 중계)</div>
                <div id="relay-container" style="color:#f1f5f9; font-size:14px; font-family:monospace; max-height:110px; overflow-y:auto; display:flex; flex-direction:column-reverse; gap:6px; line-height:1.4;">
                    <div style="color: #a1a1aa;">[중계석] 락업(Lock-up) 프리징 버그 완전 패치 완료! 멈춤 없이 9인 리얼 그래픽 플레이가 전개됩니다.</div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('ballCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitches)[0];

            let players = [
                {{ id: "투수", num: "1", x: 390, y: 190, sx: 390, sy: 190, tx: 390, ty: 190 }},
                {{ id: "포수", num: "2", x: 390, y: 520, sx: 390, sy: 520, tx: 390, ty: 520 }},
                {{ id: "1루수", num: "3", x: 610, y: 300, sx: 610, sy: 300, tx: 610, ty: 300 }},
                {{ id: "2루수", num: "4", x: 500, y: 220, sx: 500, sy: 220, tx: 500, ty: 220 }},
                {{ id: "3루수", num: "5", x: 170, y: 300, sx: 170, sy: 300, tx: 170, ty: 300 }},
                {{ id: "유격수", num: "6", x: 280, y: 220, sx: 280, sy: 220, tx: 280, ty: 220 }},
                {{ id: "좌익수", num: "7", x: 120, y: 100, sx: 120, sy: 100, tx: 120, ty: 100 }},
                {{ id: "중견수", num: "8", x: 390, y: 70, sx: 390, sy: 70, tx: 390, ty: 70 }},
                {{ id: "우익수", num: "9", x: 660, y: 100, sx: 660, sy: 100, tx: 660, ty: 100 }}
            ];

            let runner = {{ active: false, x: 610, y: 300, status: "stay", speed: 3.4 }};
            let isTargeting = false;
            let targetPos = {{ x: 390, y: 410 }};
            
            let ball = {{ active: false, status: "ready", x: 390, y: 190, z: 0.0, tx: 390, ty: 410, speed: 0, drag: 1.0, bx: 0, by: 0, spin: 0 }};
            let hitBall = {{ active: false, x: 390, y: 410, vx: 0, vy: 0, isBunt: false, spin: 0 }};
            let batter = {{ swinging: false, frame: 0, mode: "normal", swingRot: 0 }};
            let catcherThrow = {{ active: false, x: 390, y: 520, vx: 0, vy: 0 }};

            function addLog(msg) {{
                const container = document.getElementById('relay-container');
                const div = document.createElement('div');
                div.innerHTML = msg;
                container.insertBefore(div, container.firstChild);
            }}

            function setPitch(name) {{
                // 공이 도는 중이거나 타구가 날아가는 중이면 입력 잠금 차단
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
                    let dx = 390 - 390, dy = 220 - 520; let d = Math.hypot(dx, dy);
                    catcherThrow.vx = (dx/d)*14; catcherThrow.vy = (dy/d)*14;
                    addLog("<span style='color:#67e8f9;'>⚡ [송구 가동] 포수가 2루 베이스 커버진을 향해 저격 탄환을 던졌습니다!</span>");
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
                ball.speed = p.speed; ball.drag = p.drag; ball.bx = p.bx; ball.by = p.by; ball.spin = 0;
                ball.active = true; ball.status = "go";
                
                batter.swinging = false; batter.frame = 0;
                batter.mode = (Math.random() < 0.25) ? "bunt" : "normal";

                if (runner.active && Math.random() < 0.5) {{
                    runner.status = "stealing";
                    addLog("<span style='color:#facc15;'>🏃 [도루 감행] 루상의 주자가 스킵 동작 이후 완전히 베이스를 훔치려 달립니다!</span>");
                }}
                players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
            }}

            // ⚠️ 프리징 버그를 유발하던 비동기 흐름 제어 로직 완전 개조
            function judgeZone() {{
                ball.active = false;
                let isStrike = (ball.x >= 310 && ball.x <= 470 && ball.y >= 300 && ball.y <= 440);
                batter.swinging = true;
                batter.frame = 0; // 프레임 초기화로 루프 락 예방

                let chance = isStrike ? 0.62 : 0.12;
                if (batter.mode === "bunt") chance = isStrike ? 0.82 : 0.32;

                if (Math.random() < chance) {{
                    ball.status = "hit"; hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y; hitBall.spin = 0;
                    
                    if (batter.mode === "bunt") {{
                        hitBall.isBunt = true; hitBall.vx = (Math.random() - 0.5) * 5; hitBall.vy = -(2.5 + Math.random() * 2);
                        addLog("<span style='color:#fbbf24;'>🥎 [인플레이] 번트 타구가 내야 라인 안쪽에 절묘하게 떨어집니다!</span>");
                    }} else {{
                        hitBall.isBunt = false; hitBall.vx = (Math.random() - 0.5) * 19; hitBall.vy = -(8 + Math.random() * 13);
                        addLog("<span style='color:#f87171;'>💥 [인플레이] 콰앙!! 배트 중심에 제대로 맞은 타구가 외야 상공으로 뿜어집니다!</span>");
                    }}

                    let dx = hitBall.x + hitBall.vx * 15, dy = hitBall.y + hitBall.vy * 15;
                    let closest = null, minDist = 9999;
                    players.forEach(pl => {{
                        if (pl.id !== "투수" && pl.id !== "포수") {{
                            let d = Math.hypot(pl.sx - dx, pl.sy - dy);
                            if (d < minDist) {{ minDist = d; closest = pl; }}
                        }}
                    }});

                    let maxRange = hitBall.isBunt ? 210 : 170;
                    if (closest && minDist < maxRange) {{ closest.tx = dx; closest.ty = dy; }}
                }} else {{
                    let box = document.getElementById('abs-box');
                    if (isStrike) {{
                        count.s++; box.innerText = "ABS: STRIKE"; box.style.color = "#ef4444"; box.style.borderColor = "#ef4444";
                        addLog("⚾ [ABS 판정] 스트라이크! 정확한 하이 패스트볼 보더라인 관통.");
                    }} else {{
                        count.b++; box.innerText = "ABS: BALL"; box.style.color = "#3b82f6"; box.style.borderColor = "#3b82f6";
                        addLog("🔵 [ABS 판정] 볼! 베이스 플레이트 옆으로 크게 날아갔습니다.");
                    }}

                    if (count.s >= 3) {{ count.o++; count.s=0; count.b=0; addLog("❌ [아웃] 삼진 아웃! 타자가 고개를 저으며 퇴장합니다."); }}
                    else if (count.b >= 4) {{ count.s=0; count.b=0; runner.active = true; addLog("🏃 [출루] 사구(볼넷)로 베이스가 채워집니다."); }}
                    if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; addLog("🔄 [체인지] 클리닝 타임, 이닝이 완전히 종료됩니다."); }}
                    
                    document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                    if (runner.status === "stealing") {{
                        runner.x = 390; runner.y = 220; runner.status = "stay";
                        document.getElementById('base-viewer').innerText = "주자 2루";
                    }}
                    // 리셋 보증 상태 전이
                    ball.status = "ready";
                }}
            }}

            // 🎨 [점 그래픽 영구 파괴] 실밥 야구공 렌더러
            function drawRealBall(x, y, r, spin) {{
                ctx.save(); ctx.translate(x, y); ctx.rotate(spin);
                ctx.fillStyle = "#ffffff"; ctx.shadowBlur = 8; ctx.shadowColor = "rgba(255,255,255,0.4)";
                ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fill();
                ctx.shadowBlur = 0; 
                ctx.strokeStyle = "#dc2626"; ctx.lineWidth = r * 0.15;
                ctx.beginPath(); ctx.arc(-r * 0.35, 0, r * 0.7, -Math.PI*0.35, Math.PI*0.35); ctx.stroke();
                ctx.beginPath(); ctx.arc(r * 0.35, 0, r * 0.7, Math.PI*0.65, Math.PI*1.35); ctx.stroke();
                ctx.restore();
            }}

            // 🎨 [점 그래픽 영구 파괴] 헬멧+어깨+글러브 조합 2D 선수 렌더러
            function drawPlayerSprite(pl) {{
                ctx.save();
                // 1) 어깨 라인 유니폼 (베이스 레이어)
                ctx.fillStyle = "#1e3a8a"; 
                ctx.fillRect(pl.x - 12, pl.y - 3, 24, 8);
                
                // 2) 야구 헬멧 & 캡 챙 (상단 레이어)
                ctx.fillStyle = "#3b82f6";
                ctx.beginPath(); ctx.arc(pl.x, pl.y - 4, 7, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#1d4ed8"; // 챙 색상 분리
                ctx.fillRect(pl.x - 6, pl.y - 11, 12, 3);

                // 3) 글러브 시각화 (수비 동적 묘사)
                ctx.fillStyle = "#ea580c"; // 가죽 글러브 브라운 브릭
                ctx.fillRect(pl.x + (pl.tx !== pl.sx ? 8 : 6), pl.y, 5, 6);

                // 4) 등번호 프린팅
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px sans-serif";
                ctx.fillText(pl.num, pl.x - 3, pl.y + 4);

                // 5) 포지션 명칭 레이블
                ctx.fillStyle = "#cbd5e1"; ctx.font = "10px sans-serif";
                ctx.fillText(pl.id, pl.x - 16, pl.y - 14);
                ctx.restore();
            }}

            function loop() {{
                ctx.clearRect(0,0,780,560);
                batter.swingRot += 0.04;

                // 그라운드 필드 고화질 드로우
                ctx.fillStyle = "#166534"; ctx.fillRect(0,0,780,560);
                ctx.fillStyle = "#9a3412"; ctx.beginPath(); ctx.moveTo(40,560); ctx.lineTo(340,190); ctx.lineTo(440,190); ctx.lineTo(740,560); ctx.fill();

                // 스트라이크 판정 박스 및 홈플레이트
                ctx.strokeStyle = "rgba(255,255,255,0.4)"; ctx.lineWidth = 2; ctx.strokeRect(310, 300, 160, 140);
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(390,480); ctx.lineTo(420,498); ctx.lineTo(420,520); ctx.lineTo(360,520); ctx.lineTo(360,498); ctx.fill();

                // 타자 렌더러 (메탈 배트 하이라이팅 포함)
                ctx.save(); ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3.5;
                let tx = 250, ty = 380, wb = Math.sin(batter.swingRot)*1.5;
                ctx.beginPath(); ctx.arc(tx, ty-25+wb, 7, 0, Math.PI*2); ctx.fillStyle="#e2e8f0"; ctx.fill(); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty-18+wb); ctx.lineTo(tx, ty+10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty+10); ctx.lineTo(tx-10, ty+30); ctx.moveTo(tx, ty+10); ctx.lineTo(tx+10, ty+30); ctx.stroke();

                ctx.translate(tx, ty-8);
                if (batter.mode === "bunt") {{
                    ctx.rotate(Math.PI * 0.42); ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(-10, -3); ctx.lineTo(38, -3); ctx.stroke();
                }} else if (batter.swinging) {{
                    let ang = (batter.frame / 12) * Math.PI * 0.85; ctx.rotate(ang); batter.frame++;
                    if(batter.frame > 12) batter.swinging = false;
                    ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(48, -16); ctx.stroke();
                }} else {{
                    ctx.rotate(-Math.PI * 0.12 + Math.sin(batter.swingRot)*0.03);
                    ctx.strokeStyle = "#64748b"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(48, -16); ctx.stroke();
                }}
                ctx.restore();

                // 🏃 주자 캐릭터화 스프라이트
                if (runner.active) {{
                    if (runner.status === "stealing") {{
                        let dx = 390 - runner.x, dy = 220 - runner.y, d = Math.hypot(dx, dy);
                        if (d > 4) {{ runner.x += (dx/d)*runner.speed; runner.y += (dy/d)*runner.speed; }}
                    }}
                    ctx.fillStyle = "#dc2626"; ctx.beginPath(); ctx.arc(runner.x, runner.y, 8, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#facc15"; ctx.fillRect(runner.x - 4, runner.y + 4, 8, 4); // 러닝 레그 묘사
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px Arial"; ctx.fillText("RUN", runner.x-9, runner.y-12);
                }}

                // 포수 견제 송구
                if (catcherThrow.active) {{
                    catcherThrow.x += catcherThrow.vx; catcherThrow.y += catcherThrow.vy;
                    drawRealBall(catcherThrow.x, catcherThrow.y, 5, batter.swingRot * 4);
                    if (catcherThrow.y <= 220) {{
                        catcherThrow.active = false;
                        if (Math.hypot(runner.x - 390, runner.y - 220) < 32) {{
                            runner.active = false; runner.status = "stay"; count.o++;
                            if (count.o >= 3) count.o = 0;
                            document.getElementById('base-viewer').innerText = "주자 없음";
                            document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                            addLog("<span style='color:#ef4444;'>🧤 [태그 아웃] 자동 송구 프로세스 완벽 도킹! 주자를 완벽하게 베이스에서 태그아웃 처리합니다.</span>");
                        }} else {{
                            runner.x = 390; runner.y = 220; runner.status = "stay";
                            document.getElementById('base-viewer').innerText = "주자 2루";
                            addLog("<span style='color:#34d399;'>⚡ [세이프] 베이스 터치가 간발의 차이로 빨랐습니다!</span>");
                        }}
                    }}
                }}

                // 🏃 9인 수비 캐릭터 일괄 드로우 및 연산 (점 그래픽 완벽 격리)
                players.forEach(pl => {{
                    pl.x += (pl.tx - pl.x) * 0.08; pl.y += (pl.ty - pl.y) * 0.08;

                    if (hitBall.active && Math.hypot(pl.x - hitBall.x, pl.y - hitBall.y) < 26) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        if (runner.status === "stealing") {{ runner.status = "stay"; runner.x = 390; runner.y = 220; }}
                        
                        count.o++; if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                        addLog("🧤 [다이내믹 수비] No." + pl.num + " (" + pl.id + ") 캐릭터가 몸을 던져 야구공 텍스처를 완전히 움켜쥐었습니다!");
                    }}

                    // 개조된 그래픽 스프라이트 호출
                    drawPlayerSprite(pl);
                }});

                if (isTargeting) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 11, 0, Math.PI*2); ctx.stroke();
                }}

                // ⚾ 버그 프리 투구 구동 부스터 벨트
                if (ball.active && ball.status === "go") {{
                    ball.speed *= ball.drag; ball.z += ball.speed;
                    ball.spin += 0.28;

                    let mx = Math.sin(ball.z * Math.PI) * ball.bx * 3.6;
                    let my = Math.pow(ball.z, 2) * ball.by * 3.8;

                    ball.x = 390 + (ball.tx - 390)*ball.z + mx;
                    ball.y = 190 + (ball.ty - 190)*ball.z + my;

                    let bSize = Math.max(4.5, 5.0 + ball.z * 16);
                    
                    // 버그 없이 끝까지 날아가서 꽂히는 공 드로우
                    drawRealBall(ball.x, ball.y, bSize, ball.spin);
                    
                    if (ball.z >= 1.0) {{ 
                        ball.z = 1.0; 
                        judgeZone(); 
                    }}
                }}

                // 타구 물리 및 아웃/안타 루틴
                if (hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    hitBall.spin += 0.18;
                    drawRealBall(hitBall.x, hitBall.y, 7, hitBall.spin);

                    if (hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 780) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        count.s = 0; count.b = 0;
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;

                        if (!runner.active) {{
                            runner.active = true; runner.x = 610; runner.y = 300;
                            document.getElementById('base-viewer').innerText = "주자 1루";
                            addLog("📢 [라인 드라이브 안타] 완벽한 궤적으로 외야 펜스를 직격하는 안타가 터집니다!");
                        }} else {{
                            document.getElementById('base-viewer').innerText = "주자 홈인! 득점 성공!"; runner.active = false;
                            addLog("<span style='color:#fbbf24;'>🎉 [홈인] 3루를 돈 주자가 전력 질주로 홈플레이트를 쓸어 담으며 추가 점수를 뽑아냅니다!</span>");
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
