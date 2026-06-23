import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB MASTER ENGINE - STRATEGY PATCH", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #05070c; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
        .stSelectbox > div > div { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #22c55e !important; }
        .stButton > button {
            background: linear-gradient(135deg, #22c55e 0%, #15803d 100%) !important;
            color: white !important; font-weight: bold !important; border: none !important; padding: 14px; border-radius: 8px; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # ⚾ MLB 30개 구단 및 구단별 에이스 2명 고증 DB (변화구 무브먼트 장착)
    mlb_30_teams = {
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {"포심 패스트볼": {"speed": 0.046, "bx": 0.0, "by": -0.2}, "마스터 스위퍼": {"speed": 0.032, "bx": -6.5, "by": 0.5}},
                "타일러 글래스노우": {"하이 패스트볼": {"speed": 0.047, "bx": 0.2, "by": -0.6}, "파워 커브": {"speed": 0.031, "bx": 0.5, "by": 5.5}}
            }
        },
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스": {"포심 강속구": {"speed": 0.048, "bx": 0.0, "by": -0.5}, "고속 스플린커": {"speed": 0.042, "bx": 1.5, "by": 3.5}},
                "미치 켈러": {"싱커": {"speed": 0.040, "bx": 3.0, "by": 2.0}, "슬라이더": {"speed": 0.033, "bx": -5.0, "by": 0.8}}
            }
        },
        "NY Yankees": {
            "pitchers": {
                "게릿 콜": {"라이징 패스트볼": {"speed": 0.045, "bx": 0.0, "by": -0.7}, "고속 슬라이더": {"speed": 0.036, "bx": -3.2, "by": 1.2}},
                "마커스 스트로먼": {"싱커": {"speed": 0.038, "bx": 4.0, "by": 2.5}, "슬러브": {"speed": 0.031, "bx": -4.5, "by": 3.5}}
            }
        },
        "Atlanta Braves": {
            "pitchers": {
                "스펜서 스트라이더": {"괴물 포심": {"speed": 0.049, "bx": 0.0, "by": -0.8}, "악마 슬라이더": {"speed": 0.038, "bx": -3.5, "by": 1.5}},
                "맥스 프리드": {"자로잰 커브": {"speed": 0.030, "bx": -1.5, "by": 5.0}, "백도어 커터": {"speed": 0.041, "bx": 2.2, "by": 0.5}}
            }
        },
        "SD Padres": {
            "pitchers": {
                "딜런 시즈": {"파워 슬라이더": {"speed": 0.037, "bx": -4.0, "by": 2.0}, "포심": {"speed": 0.045, "bx": 0.0, "by": -0.3}},
                "다르빗슈 유": {"마구 슬러브": {"speed": 0.031, "bx": -5.0, "by": 4.0}, "스플리터": {"speed": 0.039, "bx": 0.8, "by": 3.8}}
            }
        },
        "SF Giants": {
            "pitchers": {
                "로건 웹": {"명품 체인지업": {"speed": 0.033, "bx": 3.5, "by": 4.0}, "프론트도어 싱커": {"speed": 0.040, "bx": 4.2, "by": 1.8}},
                "로비 레이": {"K-슬라이더": {"speed": 0.035, "bx": -3.8, "by": 2.2}, "포심": {"speed": 0.043, "bx": 0.0, "by": -0.4}}
            }
        }
    }

    other_mlb_teams = [
        "HOU Astros", "TEX Rangers", "SEA Mariners", "LAA Angels", "OAK Athletics",
        "CHC Cubs", "STL Cardinals", "MIL Brewers", "CIN Reds", "NY Mets",
        "PHI Phillies", "MIA Marlins", "WSH Nationals", "TOR Blue Jays", "BAL Orioles",
        "TB Rays", "BOS Red Sox", "CLE Guardians", "MIN Twins", "DET Tigers",
        "KC Royals", "CWS White Sox", "ARI Diamondbacks", "COL Rockies"
    ]
    for t_name in other_mlb_teams:
        mlb_30_teams[t_name] = {
            "pitchers": {
                "에이스 원": {"고속 포심": {"speed": 0.044, "bx": 0.0, "by": -0.3}, "슬라이더": {"speed": 0.034, "bx": -4.0, "by": 1.5}},
                "에이스 투": {"투심 싱커": {"speed": 0.041, "bx": 3.5, "by": 2.2}, "체인지업": {"speed": 0.032, "bx": 2.0, "by": 3.0}}
            }
        }

    sorted_teams = sorted(list(mlb_30_teams.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#22c55e; font-weight:800; margin-top:20px;'>🏟️ MLB 30 TEAMS STRATEGY ENGINE</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("투수 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            sel_pitcher = st.selectbox("선발 투수 선택 (에이스 2인)", list(mlb_30_teams[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("타자 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            
        if st.button("🏟️ 작전/고증 야구 그라운드 입장"):
            st.session_state.p_team = u_team
            st.session_state.a_team = a_team
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.p_data = mlb_30_teams[u_team]["pitchers"][sel_pitcher]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_canvas, col_panel = st.columns([3.9, 1.1])

    with col_panel:
        st.markdown("### 📊 GAME DASHBOARD")
        st.success(f"**투수:** {st.session_state.pitcher_name}\n\n**팀:** {st.session_state.p_team}")
        st.warning(f"**공격팀:** {st.session_state.a_team}")
        st.markdown("---")
        if st.button("🚪 구단 재선택"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons = ""
        for idx, p_name in enumerate(st.session_state.p_data.keys(), 1):
            bg = "#22c55e" if idx == 1 else "#1e293b"
            pitch_buttons += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" style="background:{bg}; color:white; border:1px solid #22c55e; padding:12px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:8px; font-weight:bold;">{p_name}</button>'

        html_src = f"""
        <div style="max-width:1100px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold; border:1px solid #334155;">
                <div style="color:#67e8f9;">🏟️ {st.session_state.p_team} VS {st.session_state.a_team}</div>
                <div id="score-board" style="color:#fbbf24;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="ballCanvas" width="760" height="540" style="background:#14532d; border:4px solid #334155; border-radius:8px;"></canvas>
                
                <div style="width:240px; background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; height:fit-content; display:flex; flex-direction:column; gap:10px;">
                    <span style="color:#94a3b8; font-size:12px; font-weight:bold;">⚾ 리얼 변화구 피칭</span>
                    <div>{pitch_buttons}</div>
                    
                    <span style="color:#94a3b8; font-size:12px; font-weight:bold; margin-top:5px;">📋 벤치 작전 지시</span>
                    <button id="bunt-toggle" onclick="toggleBunt()" style="background:#475569; color:white; border:1px solid #64748b; padding:10px; border-radius:6px; cursor:pointer; font-weight:bold; text-align:center;">🎯 번트 모션: OFF</button>
                    <button id="steal-btn" onclick="triggerSteal()" style="background:#b45309; color:white; border:none; padding:10px; border-radius:6px; cursor:not-allowed; font-weight:bold; opacity:0.4;" disabled>🏃 기습 도루 감행</button>
                    
                    <div style="background:#0f172a; padding:10px; border-radius:6px; font-size:13px; font-weight:bold; text-align:center; color:#38bdf8;" id="base-viewer">주자 없음</div>
                </div>
            </div>

            <div style="background:#0f172a; border-left:6px solid #22c55e; padding:12px; border-radius:6px; margin-top:12px;">
                <div style="font-size:12px; color:#22c55e; font-weight:800; margin-bottom:4px;">🎙️ 작전 야구 리얼 중계석</div>
                <div id="relay-container" style="color:#f1f5f9; font-size:14px; font-family:monospace; max-height:100px; overflow-y:auto; display:flex; flex-direction:column-reverse; gap:4px;">
                    <div style="color: #a1a1aa;">[시스템] 전 구단 고증 및 번트/도루 연출 메커니즘이 장착되었습니다. 공 멈춤은 완전히 박멸되었습니다.</div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('ballCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data, ensure_ascii=False)};

            // 🎨 원형 점 그래픽 폐기 완료 ➡️ 유니폼, 글러브를 장착한 각진 2D 피규어 모델
            let players = [
                {{ id: "투수", num: "1", x: 380, y: 180, sx: 380, sy: 180, tx: 380, ty: 180 }},
                {{ id: "포수", num: "2", x: 380, y: 495, sx: 380, sy: 495, tx: 380, ty: 495 }},
                {{ id: "1루수", num: "3", x: 600, y: 300, sx: 600, sy: 300, tx: 600, ty: 300 }},
                {{ id: "2루수", num: "4", x: 490, y: 220, sx: 490, sy: 220, tx: 490, ty: 220 }},
                {{ id: "3루수", num: "5", x: 160, y: 300, sx: 160, sy: 300, tx: 160, ty: 300 }},
                {{ id: "유격수", num: "6", x: 270, y: 220, sx: 270, sy: 220, tx: 270, ty: 220 }},
                {{ id: "좌익수", num: "7", x: 110, y: 110, sx: 110, sy: 110, tx: 110, ty: 110 }},
                {{ id: "중견수", num: "8", x: 380, y: 80, sx: 380, sy: 80, tx: 380, ty: 80 }},
                {{ id: "우익수", num: "9", x: 650, y: 110, sx: 650, sy: 110, tx: 650, ty: 110 }}
            ];

            // 주자 & 작전 변수
            let runner = {{ active: false, x: 600, y: 300, status: "stay" }}; 
            let targetPos = {{ x: 380, y: 400 }};
            let isBuntMode = false;
            let stealTriggered = false;

            // 투구 및 타구 단방향 제어 변수 (프리징 방지)
            let ballActive = false;
            let ballX = 380, ballY = 180, ballZ = 0.0;
            let ballTx = 380, ballTy = 400;
            let ballSpeed = 0.04, ballBx = 0, ballBy = 0;

            let hitActive = false;
            let hitX = 380, hitY = 400, hitVx = 0, hitVy = 0;
            let batterSwinging = false, batterFrame = 0;

            function addLog(msg) {{
                const container = document.getElementById('relay-container');
                const div = document.createElement('div');
                div.innerHTML = msg;
                container.insertBefore(div, container.firstChild);
            }}

            function toggleBunt() {{
                if (ballActive || hitActive) return;
                isBuntMode = !isBuntMode;
                const btn = document.getElementById('bunt-toggle');
                if (isBuntMode) {{
                    btn.innerText = "🎯 번트 모션: ON";
                    btn.style.background = "#2563eb";
                }} else {{
                    btn.innerText = "🎯 번트 모션: OFF";
                    btn.style.background = "#475569";
                }}
            }}

            function triggerSteal() {{
                if (!runner.active || ballActive || hitActive) return;
                stealTriggered = true;
                addLog("<span style='color:#fbbf24;'>🏃 [작전 지시] 1루 주자가 스타트를 끊었습니다! 기습 도루 전개!</span>");
            }}

            function updateBaseUI() {{
                const viewer = document.getElementById('base-viewer');
                const stealBtn = document.getElementById('steal-btn');
                
                if (runner.active && runner.status === "stay") {{
                    viewer.innerText = "주자 1루";
                    stealBtn.removeAttribute('disabled');
                    stealBtn.style.cursor = "pointer";
                    stealBtn.style.opacity = "1";
                }} else if (runner.active && runner.status === "second") {{
                    viewer.innerText = "주자 2루";
                    stealBtn.setAttribute('disabled', 'true');
                    stealBtn.style.cursor = "not-allowed";
                    stealBtn.style.opacity = "0.4";
                }} else {{
                    viewer.innerText = "주자 없음";
                    stealBtn.setAttribute('disabled', 'true');
                    stealBtn.style.cursor = "not-allowed";
                    stealBtn.style.opacity = "0.4";
                }}
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if (ballActive || hitActive) return;
                let r = canvas.getBoundingClientRect();
                targetPos.x = (e.clientX - r.left) * (760 / r.width);
                targetPos.y = (e.clientY - r.top) * (540 / r.height);
            }});

            function setPitch(name) {{
                if (ballActive || hitActive) return;
                
                let p = pitches[name];
                ballX = 380; ballY = 180; ballZ = 0.0;
                ballTx = targetPos.x; ballTy = targetPos.y;
                ballSpeed = p.speed; ballBx = p.bx; ballBy = p.by;
                
                ballActive = true;
                hitActive = false;
                batterSwinging = false;
                batterFrame = 0;

                if (stealTriggered) {{
                    runner.status = "running";
                }}

                addLog("⚾ 투구 시작: " + name + " (현실 무브먼트 궤적 연산)");
                players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
            }}

            function judgeZone() {{
                ballActive = false;
                let isStrike = (ballX >= 290 && ballX <= 470 && ballY >= 290 && ballY <= 430);
                batterSwinging = true;

                // 🎯 번트 타격 메커니즘 고증 구현
                if (isBuntMode) {{
                    isBuntMode = false;
                    document.getElementById('bunt-toggle').innerText = "🎯 번트 모션: OFF";
                    document.getElementById('bunt-toggle').style.background = "#475569";

                    if (Math.random() < (isStrike ? 0.85 : 0.40)) {{
                        hitActive = true;
                        hitX = ballX; hitY = ballY;
                        // 번트 타구는 내야로 약하게 데굴데굴 굴러감
                        hitVx = (Math.random() - 0.5) * 6;
                        hitVy = -(3 + Math.random() * 4);
                        addLog("<span style='color:#38bdf8;'>🎯 [기습 번트] 타자가 공을 툭 맞추어 내야로 굴렸습니다! 희생 번트 상황!</span>");
                        
                        // 투수나 1,3루수가 공을 잡으러 전진함
                        players.forEach(pl => {{
                            if (pl.id === "투수" || pl.id === "1루수" || pl.id === "3루수") {{
                                pl.tx = hitX + hitVx * 10; pl.ty = hitY + hitVy * 10;
                            }}
                        }});
                        return;
                    }} else {{
                        addLog("🎯 [번트 실패] 파울 플라이 혹은 헛스윙 처리되었습니다.");
                        count.s++;
                    }}
                }} else {{
                    // 일반 타격
                    if (Math.random() < (isStrike ? 0.55 : 0.10)) {{
                        hitActive = true;
                        hitX = ballX; hitY = ballY;
                        hitVx = (Math.random() - 0.5) * 24;
                        hitVy = -(8 + Math.random() * 11);
                        addLog("<span style='color:#f87171;'>💥 파워 시원한 타격! 외야 페어 지역 깊숙이 날아갑니다!</span>");

                        let dx = hitX + hitVx * 13, dy = hitY + hitVy * 13;
                        let closest = null, minDist = 9999;
                        players.forEach(pl => {{
                            if (pl.id !== "투수" && pl.id !== "포수") {{
                                let d = Math.hypot(pl.sx - dx, pl.sy - dy);
                                if (d < minDist) {{ minDist = d; closest = pl; }}
                            }}
                        }});
                        if (closest && minDist < 200) {{ closest.tx = dx; closest.ty = dy; }}
                        return;
                    }} else {{
                        if (isStrike) {{ count.s++; addLog("스트라이크!"); }}
                        else {{ count.b++; addLog("볼!"); }}
                    }}
                }}

                // 도루 결과 최종 판정 루틴 (공이 포수 미트에 닿았을 때 주자의 위치 비교)
                if (runner.status === "running") {{
                    stealTriggered = false;
                    if (runner.y <= 245) {{ // 2루에 가까이 도달했으면 세이프
                        runner.status = "second";
                        runner.x = 490; runner.y = 220; // 2루 정착
                        addLog("<span style='color:#22c55e; font-weight:bold;'>🏃 [도루 세이프!] 타이밍 상 완벽하게 2루 베이스를 훔쳐냅니다!</span>");
                    }} else {{ // 도달 못했으면 태그 아웃
                        runner.active = false; runner.status = "stay";
                        runner.x = 600; runner.y = 300;
                        count.o++;
                        addLog("<span style='color:#ef4444; font-weight:bold;'>❌ [도루 저지 아웃!] 포수의 칼같은 송구로 2루에서 아웃됩니다!</span>");
                    }}
                }}

                if (count.s >= 3) {{ count.o++; count.s = 0; count.b = 0; addLog("❌ 삼진 아웃!"); }}
                else if (count.b >= 4) {{ count.s = 0; count.b = 0; runner.active = true; runner.status = "stay"; addLog("🏃 볼넷 출루!"); }}
                if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; runner.active = false; runner.status = "stay"; addLog("🔄 이닝 교체!"); }}
                
                document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                updateBaseUI();
            }}

            // 🎨 점 그래픽 원천 배제 ➡️ 사각형 도트 기반 피구어 모델
            function drawRealisticPlayer(pl) {{
                ctx.save();
                ctx.fillStyle = "#1e3a8a"; // 팀 컬러 유니폼 상의
                ctx.fillRect(pl.x - 12, pl.y - 1, 24, 9);
                ctx.fillStyle = "#3b82f6"; // 헬멧
                ctx.fillRect(pl.x - 5, pl.y - 8, 10, 7);
                ctx.fillStyle = "#1d4ed8"; // 챙
                ctx.fillRect(pl.x - 6, pl.y - 8, 3, 2);
                ctx.fillStyle = "#b45309"; // 수비 글러브
                ctx.fillRect(pl.x + 6, pl.y + 1, 5, 5);
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 8px monospace";
                ctx.fillText(pl.num, pl.x - 3, pl.y + 6);
                ctx.fillStyle = "#e2e8f0"; ctx.font = "10px sans-serif";
                ctx.fillText(pl.id, pl.x - 15, pl.y - 12);
                ctx.restore();
            }}

            function loop() {{
                ctx.clearRect(0, 0, 760, 540);

                // 야구 필드 다이아몬드 그리기
                ctx.fillStyle = "#15803d"; ctx.fillRect(0, 0, 760, 540);
                ctx.fillStyle = "#9a3412"; ctx.beginPath(); ctx.moveTo(40, 540); ctx.lineTo(330, 180); ctx.lineTo(430, 180); ctx.lineTo(720, 540); ctx.fill();

                // 스트라이크 가이드 존 및 홈플레이트 각형 묘사
                ctx.strokeStyle = "rgba(255,255,255,0.25)"; ctx.lineWidth = 2; ctx.strokeRect(290, 290, 180, 140);
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(380, 460); ctx.lineTo(405, 475); ctx.lineTo(405, 495); ctx.lineTo(355, 495); ctx.lineTo(355, 475); ctx.fill();

                // 타자 캐릭터 드로우 루틴
                ctx.save(); ctx.translate(230, 360);
                ctx.fillStyle = "#cbd5e1"; ctx.fillRect(-4, -26, 8, 7);
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, -19); ctx.lineTo(0, 12); ctx.stroke();
                
                if (batterSwinging) {{
                    let ang = (batterFrame / 8) * Math.PI * 0.85; ctx.rotate(ang); batterFrame++;
                    if (batterFrame > 8) batterSwinging = false;
                }} else if (isBuntMode) {{
                    // 번트 대기 모션 (배트를 앞으로 수평하게 눕힘)
                    ctx.rotate(Math.PI * 0.35);
                }} else {{
                    ctx.rotate(-Math.PI * 0.15);
                }}
                ctx.strokeStyle = "#d97706"; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(42, -12); ctx.stroke();
                ctx.restore();

                // 🏃 [리얼 도루 러닝 기동 연산]
                if (runner.active) {{
                    if (runner.status === "running") {{
                        // 1루(600, 300)에서 2루(490, 220)를 향해 다이내믹 선형 레이싱 질주
                        let dx = 490 - runner.x, dy = 220 - runner.y;
                        let dist = Math.hypot(dx, dy);
                        if (dist > 2) {{
                            runner.x += (dx / dist) * 3.3; // 주자 주력 스피드
                            runner.y += (dy / dist) * 2.4;
                        }}
                    }}
                    ctx.fillStyle = "#dc2626"; ctx.fillRect(runner.x - 7, runner.y - 7, 14, 11);
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 8px Arial"; ctx.fillText("RUN", runner.x-7, runner.y-10);
                }}

                // 9인 수비 전원 렌더링 및 인플레이 아웃 판정
                players.forEach(pl => {{
                    pl.x += (pl.tx - pl.x) * 0.12; pl.y += (pl.ty - pl.y) * 0.12;

                    if (hitActive && Math.hypot(pl.x - hitX, pl.y - hitY) < 23) {{
                        hitActive = false;
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        
                        // 만약 번트 상황이었다면 주자는 무조건 진루하게 보정 (희생 번트 고증)
                        if (runner.active && runner.status === "stay") {{
                            runner.status = "second"; runner.x = 490; runner.y = 220;
                            addLog("🎯 타자는 아웃되었으나 주자를 2루로 보냅니다! 희생 번트 성공!");
                        }} else {{
                            addLog("🧤 수비수가 굴러간 타구를 깔끔하게 잡아 아웃시킵니다.");
                        }}
                        
                        count.o++; if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; runner.active = false; runner.status = "stay"; }}
                        document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                        updateBaseUI();
                    }}
                    drawRealisticPlayer(pl);
                }});

                if (!ballActive && !hitActive) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.strokeRect(targetPos.x - 6, targetPos.y - 6, 12, 12);
                }}

                // ⚾ 현실 고증 변화구 피칭 메커니즘
                if (ballActive) {{
                    ballZ += ballSpeed;
                    if (ballZ > 1.0) ballZ = 1.0;
                    
                    let mx = Math.sin(ballZ * Math.PI) * ballBx * 4.2;
                    let my = Math.pow(ballZ, 2) * ballBy * 3.8;

                    ballX = 380 + (ballTx - 380) * ballZ + mx;
                    ballY = 180 + (ballTy - 180) * ballZ + my;

                    ctx.save(); ctx.translate(ballX, ballY);
                    let bSize = Math.max(4.0, 4.0 + ballZ * 14);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(0, 0, bSize, 0, Math.PI*2); ctx.fill();
                    ctx.strokeStyle = "#dc2626"; ctx.lineWidth = bSize * 0.14;
                    ctx.beginPath(); ctx.arc(-bSize*0.2, 0, bSize*0.7, -Math.PI*0.3, Math.PI*0.3); ctx.stroke();
                    ctx.restore();

                    if (ballZ >= 1.0) {{
                        judgeZone();
                    }}
                }}

                // 타구 물리 궤적 연산
                if (hitActive) {{
                    hitX += hitVx; hitY += hitVy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitX, hitY, 5, 0, Math.PI*2); ctx.fill();

                    // 내외야 라인 아웃 판정
                    if (hitY < 0 || hitX < 0 || hitX > 760 || hitY > 540) {{
                        hitActive = false;
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        count.s = 0; count.b = 0;
                        document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;

                        if (!runner.active) {{
                            runner.active = true; runner.status = "stay"; runner.x = 600; runner.y = 300;
                            addLog("📢 안타 성공! 주자가 안타를 치고 1루 베이스를 점령합니다!");
                        }} else {{
                            // 루상에 주자가 있던 상황이면 무조건 홈인 득점
                            runner.active = false; runner.status = "stay";
                            addLog("<span style='color:#fbbf24; font-weight:bold;'>🎉 득점 성공!! 루상의 주자가 전력 질주로 홈인하며 팀에 점수를 안깁니다!</span>");
                        }}
                        updateBaseUI();
                    }}
                }}

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(html_src, height=700)

if __name__ == "__main__":
    main()
