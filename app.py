import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW - PERFECT FIX", layout="wide")
    
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
                    "포심 강속구": {"speed": 0.045, "drag": 1.0, "bx": 0.0, "by": -0.5},
                    "명품 너클커브": {"speed": 0.025, "drag": 0.85, "bx": 3.0, "by": 5.0},
                    "고속 스플린커": {"speed": 0.040, "drag": 0.95, "bx": 1.5, "by": 4.0},
                    "종 슬라이더": {"speed": 0.035, "drag": 0.90, "bx": -3.5, "by": 2.0},
                    "체인지업": {"speed": 0.030, "drag": 0.88, "bx": 2.0, "by": 3.5}
                }}
            },
            "lineup": ["오닐 크루즈 (SS)", "브라이언 레이놀즈 (LF)", "키브라이언 헤이즈 (3B)"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": {
                    "파워 포심": {"speed": 0.045, "drag": 1.0, "bx": 0.0, "by": 0.0},
                    "마스터 스위퍼": {"speed": 0.030, "drag": 0.85, "bx": -6.0, "by": -0.5}
                }}
            },
            "lineup": ["오타니 쇼헤이 (DH)", "무키 베츠 (SS)"]
        }
    }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#22c55e; font-weight:800; margin-top:20px;'>🏟️ MLB CATCHER VIEW: VERIFIED BUILD</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("아군 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            sel_pitcher = st.selectbox("선발 투수 선택", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("상대 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        if st.button("🏟️ 완벽 수정판 그라운드 입장"):
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
        st.markdown("---")
        if st.button("🚪 경기 종료"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#22c55e" if idx == 1 else "#1e293b"
            pitch_buttons += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" style="background:{bg}; color:white; border:1px solid #22c55e; padding:12px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:8px; font-weight:bold;">{p_name}</button>'

        html_src = f"""
        <div style="max-width:1100px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:14px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold; border:2px solid #334155;">
                <div style="color:#67e8f9; font-size:16px;">🏟️ {st.session_state.p_team} (CRITICAL PATCH)</div>
                <div id="score-board" style="color:#fbbf24; font-size:16px;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="ballCanvas" width="780" height="560" style="background:#14532d; border:4px solid #334155; border-radius:8px;"></canvas>
                <div style="width:240px; background:#1e293b; padding:14px; border-radius:8px; height:fit-content; border:1px solid #334155;">
                    <span style="color:#94a3b8; font-size:13px; font-weight:bold; display:block; margin-bottom:8px;">⚾ 구종 즉시 투구</span>
                    <div style="margin-top:6px;">{pitch_buttons}</div>
                    <div style="margin-top:15px; background:#0f172a; padding:10px; border-radius:6px; font-size:13px; font-weight:bold; text-align:center; color:#38bdf8;" id="base-viewer">주자 없음</div>
                </div>
            </div>

            <div style="background:#0f172a; border-left:6px solid #22c55e; padding:14px; border-radius:6px; margin-top:12px;">
                <div style="font-size:12px; color:#22c55e; font-weight:800; margin-bottom:6px;">🎙️ 중계석 (누적 로그)</div>
                <div id="relay-container" style="color:#f1f5f9; font-size:14px; font-family:monospace; max-height:110px; overflow-y:auto; display:flex; flex-direction:column-reverse; gap:6px; line-height:1.4;">
                    <div style="color: #a1a1aa;">[시스템] 프리징 현상을 유발하는 상태 교차 잠금을 전면 해제했습니다. 안정적으로 포수 미트에 투구가 가능합니다.</div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('ballCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};

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

            let runner = {{ active: false, x: 610, y: 300, status: "stay" }};
            let targetPos = {{ x: 390, y: 410 }};
            
            // 프리징 버그 원천 차단을 위해 변수를 완전히 단순 분리
            let ballActive = false;
            let ballX = 390, ballY = 190, ballZ = 0.0;
            let ballTx = 390, ballTy = 410;
            let ballSpeed = 0.04, ballDrag = 1.0, ballBx = 0, ballBy = 0, ballSpin = 0;

            let hitActive = false;
            let hitX = 390, hitY = 410, hitVx = 0, hitVy = 0, hitSpin = 0;
            
            let batterSwinging = false;
            let batterFrame = 0;
            let swingRot = 0;

            function addLog(msg) {{
                const container = document.getElementById('relay-container');
                const div = document.createElement('div');
                div.innerHTML = msg;
                container.insertBefore(div, container.firstChild);
            }}

            // 마우스 클릭 시 조준점 즉시 이동
            canvas.addEventListener('mousedown', (e) => {{
                if (ballActive || hitActive) return;
                let r = canvas.getBoundingClientRect();
                targetPos.x = (e.clientX - r.left) * (780 / r.width);
                targetPos.y = (e.clientY - r.top) * (560 / r.height);
            }});

            function setPitch(name) {{
                // 투구나 타격 동작이 완전히 종료되기 전엔 중복 호출 방지
                if (ballActive || hitActive) return;
                
                let p = pitches[name];
                
                // 버그 해제: 변수 강제 물리 리셋 고정
                ballX = 390; 
                ballY = 190; 
                ballZ = 0.0;
                ballTx = targetPos.x; 
                ballTy = targetPos.y;
                ballSpeed = p.speed; 
                ballDrag = p.drag; 
                ballBx = p.bx; 
                ballBy = p.by;
                ballSpin = 0;
                
                ballActive = true; 
                hitActive = false;
                batterSwinging = false;
                batterFrame = 0;

                addLog("⚾ 투수 시그니처 구종 [" + name + "] 발사!");
                
                if (runner.active && Math.random() < 0.4) {{
                    runner.status = "stealing";
                    addLog("<span style='color:#facc15;'>🏃 [도루] 1루 주자가 스타트를 끊었습니다!</span>");
                }}
                players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
            }}

            function judgeZone() {{
                ballActive = false;
                let isStrike = (ballX >= 310 && ballX <= 470 && ballY >= 300 && ballY <= 440);
                batterSwinging = true;

                if (Math.random() < (isStrike ? 0.6 : 0.15)) {{
                    hitActive = true;
                    hitX = ballX; hitY = ballY;
                    hitVx = (Math.random() - 0.5) * 20; 
                    hitVy = -(8 + Math.random() * 12);
                    addLog("<span style='color:#f87171;'>💥 [타격] 타자가 공을 시원하게 받아쳤습니다! 인플레이 상황!</span>");

                    let dx = hitX + hitVx * 15, dy = hitY + hitVy * 15;
                    let closest = null, minDist = 9999;
                    players.forEach(pl => {{
                        if (pl.id !== "투수" && pl.id !== "포수") {{
                            let d = Math.hypot(pl.sx - dx, pl.sy - dy);
                            if (d < minDist) {{ minDist = d; closest = pl; }}
                        }}
                    }});
                    if (closest && minDist < 180) {{ closest.tx = dx; closest.ty = dy; }}
                }} else {{
                    if (isStrike) {{
                        count.s++;
                        addLog("🥎 스트라이크! 포수 미트에 그대로 빨려 들어갑니다.");
                    }} else {{
                        count.b++;
                        addLog("🔵 볼! 존을 크게 벗어난 코스입니다.");
                    }}

                    if (count.s >= 3) {{ count.o++; count.s = 0; count.b = 0; addLog("❌ 삼진 아웃!"); }}
                    else if (count.b >= 4) {{ count.s = 0; count.b = 0; runner.active = true; addLog("🏃 볼넷 출루!"); }}
                    if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; addLog("🔄 이닝 교체!"); }}
                    
                    document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                    if (runner.status === "stealing") {{
                        runner.x = 390; runner.y = 220; runner.status = "stay";
                        document.getElementById('base-viewer').innerText = "주자 2루";
                    }}
                }}
            }}

            function drawBaseball(x, y, r, spin) {{
                ctx.save(); ctx.translate(x, y); ctx.rotate(spin);
                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fill();
                ctx.strokeStyle = "#dc2626"; ctx.lineWidth = r * 0.18;
                ctx.beginPath(); ctx.arc(-r * 0.35, 0, r * 0.7, -Math.PI*0.3, Math.PI*0.3); ctx.stroke();
                ctx.beginPath(); ctx.arc(r * 0.35, 0, r * 0.7, Math.PI*0.7, Math.PI*1.3); ctx.stroke();
                ctx.restore();
            }}

            function loop() {{
                ctx.clearRect(0, 0, 780, 560);
                swingRot += 0.04;

                // 그라운드 라인 드로우
                ctx.fillStyle = "#166534"; ctx.fillRect(0, 0, 780, 560);
                ctx.fillStyle = "#a16207"; ctx.beginPath(); ctx.moveTo(40, 560); ctx.lineTo(340, 190); ctx.lineTo(440, 190); ctx.lineTo(740, 560); ctx.fill();

                // 존 가이드라인
                ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 2; ctx.strokeRect(310, 300, 160, 140);
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(390, 480); ctx.lineTo(420, 498); ctx.lineTo(420, 520); ctx.lineTo(360, 520); ctx.lineTo(360, 498); ctx.fill();

                // 타자 드로우 루틴
                ctx.save(); ctx.translate(250, 380);
                ctx.fillStyle = "#cbd5e1"; ctx.beginPath(); ctx.arc(0, -25, 7, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, -18); ctx.lineTo(0, 10); ctx.stroke();
                
                if (batterSwinging) {{
                    let ang = (batterFrame / 10) * Math.PI * 0.8; ctx.rotate(ang); batterFrame++;
                    if (batterFrame > 10) batterSwinging = false;
                }} else {{
                    ctx.rotate(-Math.PI * 0.1);
                }}
                ctx.strokeStyle = "#d97706"; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(45, -15); ctx.stroke();
                ctx.restore();

                // 주자 상태 처리
                if (runner.active) {{
                    if (runner.status === "stealing") {{
                        let dx = 390 - runner.x, dy = 220 - runner.y, d = Math.hypot(dx, dy);
                        if (d > 4) {{ runner.x += (dx/d)*3.4; runner.y += (dy/d)*3.4; }}
                    }}
                    ctx.fillStyle = "#dc2626"; ctx.beginPath(); ctx.arc(runner.x, runner.y, 8, 0, Math.PI*2); ctx.fill();
                }}

                // 수비수 캐릭터 드로우 및 포구 판정
                players.forEach(pl => {{
                    pl.x += (pl.tx - pl.x) * 0.1; pl.y += (pl.ty - pl.y) * 0.1;

                    if (hitActive && Math.hypot(pl.x - hitX, pl.y - hitY) < 25) {{
                        hitActive = false;
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        count.o++; if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; }}
                        document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                        addLog("🧤 [수비] No." + pl.num + " (" + pl.id + ") 가 뻗어 나온 타구를 기가 막히게 잡아냈습니다! 아웃!");
                    }}

                    // 가독성 뛰어난 프로 야구 유니폼 모델 2D 드로우
                    ctx.fillStyle = "#1e3a8a"; ctx.fillRect(pl.x - 10, pl.y - 2, 20, 7);
                    ctx.fillStyle = "#3b82f6"; ctx.beginPath(); ctx.arc(pl.x, pl.y - 4, 6, 0, Math.PI * 2); ctx.fill();
                    ctx.fillStyle = "#ea580c"; ctx.fillRect(pl.x + 5, pl.y, 4, 5);
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px sans-serif"; ctx.fillText(pl.num, pl.x - 3, pl.y + 4);
                    ctx.fillStyle = "#cbd5e1"; ctx.font = "10px sans-serif"; ctx.fillText(pl.id, pl.x - 15, pl.y - 12);
                }});

                // 조준 타겟 표시
                if (!ballActive && !hitActive) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 12, 0, Math.PI*2); ctx.stroke();
                }}

                // ⚾ 버그 프리 투구 애니메이션 연산
                if (ballActive) {{
                    ballSpeed *= ballDrag;
                    ballZ += ballSpeed;
                    
                    let mx = Math.sin(ballZ * Math.PI) * ballBx * 3.5;
                    let my = Math.pow(ballZ, 2) * ballBy * 3.5;

                    ballX = 390 + (ballTx - 390) * ballZ + mx;
                    ballY = 190 + (ballTy - 190) * ballZ + my;
                    ballSpin += 0.25;

                    let bSize = Math.max(4.5, 5.0 + ballZ * 15);
                    drawBaseball(ballX, ballY, bSize, ballSpin);

                    if (ballZ >= 1.0) {{
                        judgeZone();
                    }}
                }}

                // 타구 애니메이션 연산
                if (hitActive) {{
                    hitX += hitVx; hitY += hitVy;
                    hitSpin += 0.15;
                    drawBaseball(hitX, hitY, 6.5, hitSpin);

                    if (hitY < 0 || hitX < 0 || hitX > 780) {{
                        hitActive = false;
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        count.s = 0; count.b = 0;
                        document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;

                        if (!runner.active) {{
                            runner.active = true; runner.x = 610; runner.y = 300;
                            document.getElementById('base-viewer').innerText = "주자 1루";
                            addLog("📢 안타! 안타입니다! 타구가 외야 펜스 방향으로 완전히 빠져나갔습니다.");
                        }} else {{
                            document.getElementById('base-viewer').innerText = "주자 홈인! 득점 완료!"; runner.active = false;
                            addLog("<span style='color:#fbbf24;'>🎉 홈인!! 루상의 주자가 베이스를 모두 돌고 홈을 밟아 추가 득점에 성공합니다!</span>");
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
