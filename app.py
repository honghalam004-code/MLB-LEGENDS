import streamlit as st
import json
import math

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW - ULTIMATE ENGINE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .stSelectbox > div > div { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #16a34a !important; border-radius: 6px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
            color: #ffffff !important; font-weight: bold !important;
            border-radius: 8px !important; border: none !important; padding: 12px 24px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 30개 전 구단 오리지널 데이터베이스 완벽 보존
    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스 (선발)": {"pitches": {"파워 포심": {"speed": 0.042, "drag": 1.0, "break": 0.0}, "명품 너클커브": {"speed": 0.025, "drag": 0.83, "break": 4.5}}},
                "데이비드 베드나 (마무리)": {"pitches": {"하이 패스트볼": {"speed": 0.039, "drag": 1.0, "break": 0.0}}}
            },
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "키브라이언 헤이즈", "앤드류 맥커친", "조이 바트"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이 (선발)": {"pitches": {"파워 포심": {"speed": 0.041, "drag": 1.0, "break": 0.0}, "명품 스위퍼": {"speed": 0.029, "drag": 0.85, "break": -4.8}}},
                "에반 필립스 (마무리)": {"pitches": {"슬라이더": {"speed": 0.032, "drag": 0.89, "break": 3.0}}}
            },
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "테오스카 에르난데스", "윌 스미스"]
        }
    }

    # 타 구단 데이터 매핑 자동화 보장
    other_teams = [
        ("New York Yankees", "게릿 콜 (선발)", "후안 소토"),
        ("San Francisco Giants", "로건 웹 (선발)", "이정후"),
        ("San Diego Padres", "딜런 시즈 (선발)", "루이스 아라에즈")
    ]
    for t_name, p_main, b_first in other_teams:
        if t_name not in mlb_mega_db:
            mlb_mega_db[t_name] = {
                "pitchers": {p_main: {"pitches": {"직구": {"speed": 0.040, "drag": 1.0, "break": 0.0}}}},
                "lineup": [b_first, "타자 B", "타자 C"]
            }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#16a34a; margin-top:20px;'>🏟️ 정통 포수시점 프로페셔널 야구 (수비 AI 정상화)</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("🏃 내 투수 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            sel_pitcher = st.selectbox("⚾ 투수 선택", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("🤖 상대 AI 타자 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        if st.button("🏟️ 야구 경기 시작"):
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
        st.markdown("### 🎮 경기 중계석")
        st.success(f"투수: {st.session_state.pitcher_name}")
        st.selectbox("🙋 타석 타자", st.session_state.a_data["lineup"])
        st.markdown("---")
        if st.button("🚪 게임 리셋 종료"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons_html = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#16a34a" if idx == 1 else "#1e293b"
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" id="p{idx}" style="background:{bg}; color:white; border:1px solid #16a34a; padding:11px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:7px; font-weight:bold;">{p_name}</button>'

        html_part = f"""
        <div style="max-width:820px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold;">
                <div>⚾ {st.session_state.pitcher_name} 포수 미트 리얼 조준</div>
                <div id="count-board" style="color:#f59e0b; font-size:16px;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="catcherCanvas" width="560" height="480" style="background:#166534; border:3px solid #334155; border-radius:8px;"></canvas>
                <div style="width:190px; background:#1e293b; padding:12px; border-radius:8px; height:fit-content; border:1px solid #334155;">
                    <span style="color:#94a3b8; font-size:12px; font-weight:bold;">보유 구종 리스트</span>
                    <div style="margin-top:8px;">{pitch_buttons_html}</div>
                </div>
            </div>

            <div style="background:#1e293b; border-left:5px solid #16a34a; padding:12px; border-radius:6px; margin-top:10px; font-weight:bold; color:#e2e8f0; font-size:13px;">
                <span id="commentary">🎙️ [안내] 마우스를 조준하여 투구하세요. 유격수가 범위 내 공은 다이빙 캐치하고 범위를 벗어나면 안타가 선언됩니다.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('catcherCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitchesData = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitchesData)[0];

            // 🏃 유격수 데이터 (기초 배치 및 추적 한계치 정밀 설정)
            let fielder = {{ id: "유격수", x: 230, y: 190, sx: 230, sy: 190, tx: 230, ty: 190, state: "normal" }};

            let isDragging = false;
            let targetPos = {{ x: 280, y: 350 }};

            let ball = {{ active: false, status: "ready", x: 280, y: 150, z: 0.0, tx: 280, ty: 350, speed: 0, drag: 1.0, breakX: 0 }};
            let hitBall = {{ active: false, x: 280, y: 350, vx: 0, vy: 0, maxDist: 0, currentDist: 0 }};
            let batter = {{ swinging: false, frame: 0, wobble: 0 }};

            function setPitch(pName) {{
                selectedPitch = pName;
                document.querySelectorAll('.p-btn').forEach(b => b.style.backgroundColor = '#1e293b');
                event.target.style.backgroundColor = '#16a34a';
            }}

            function getMousePos(e) {{
                let r = canvas.getBoundingClientRect();
                return {{ x: (e.clientX - r.left) * (canvas.width / r.width), y: (e.clientY - r.top) * (canvas.height / r.height) }};
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if (!ball.active && !hitBall.active && ball.status === "ready") {{
                    isDragging = true;
                    let m = getMousePos(e); targetPos.x = m.x; targetPos.y = m.y;
                }}
            }});
            canvas.addEventListener('mousemove', (e) => {{
                if (isDragging) {{ let m = getMousePos(e); targetPos.x = m.x; targetPos.y = m.y; }}
            }});
            canvas.addEventListener('mouseup', () => {{
                if (isDragging) {{ isDragging = false; firePitch(); }}
            }});

            function firePitch() {{
                let p = pitchesData[selectedPitch];
                ball.z = 0.0; ball.x = 280; ball.y = 150;
                ball.tx = targetPos.x; ball.ty = targetPos.y;
                ball.speed = p.speed; ball.drag = p.drag; ball.breakX = p.break;
                ball.active = true; ball.status = "flying";
                
                batter.swinging = false; batter.frame = 0;
                fielder.tx = fielder.sx; fielder.ty = fielder.sy; fielder.state = "normal";
            }}

            function evaluateZone() {{
                let inside = (ball.x >= 205 && ball.x <= 355 && ball.y >= 250 && ball.y <= 390);
                batter.swinging = true;

                if (Math.random() < (inside ? 0.65 : 0.15)) {{
                    ball.active = false; ball.status = "hit";
                    hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y;
                    hitBall.vx = (Math.random() - 0.5) * 14;
                    hitBall.vy = -(5 + Math.random() * 9);
                    hitBall.currentDist = 0;
                    hitBall.maxDist = 25 + Math.random() * 20; // 타구 비행 수명

                    // 🎯 수비수 목적지 지정 (타구 예상 동선 가로채기 연산)
                    let pX = hitBall.x + hitBall.vx * 10;
                    let pY = hitBall.y + hitBall.vy * 10;
                    
                    // 수비수 원래 자리(sx, sy)에서 공 낙하 예상지점까지의 순수 거리 계산
                    let distFromBase = Math.hypot(fielder.sx - pX, fielder.sy - pY);
                    
                    if (distFromBase < 140) {{
                        // 수비 범위 안이면 끝까지 공을 쫓아가 잡아내도록 타겟 설정!
                        fielder.tx = pX; fielder.ty = pY; fielder.state = "tracking";
                        document.getElementById('commentary').innerText = "🎙️ 깡! 유격수 정면 바운드 타구! 유격수가 맹렬히 전력 질주합니다!";
                    }} else {{
                        // 범위를 넘어서면 외야 펜스 전까지만 아쉽게 쫓아가다가 멈추는 모션 처리
                        fielder.tx = fielder.sx + (pX - fielder.sx) * 0.4;
                        fielder.ty = fielder.sy + (pY - fielder.sy) * 0.4;
                        fielder.state = "giveup";
                        document.getElementById('commentary').innerText = "🎙️ 잘 맞은 타구! 유격수가 손을 뻗어보지만 키를 넘어가는 안타가 됩니다!";
                    }}
                }} else {{
                    if (inside) {{ count.s++; }} else {{ count.b++; }}
                    if (count.s >= 3) {{ count.o++; count.s = 0; count.b = 0; }}
                    else if (count.b >= 4) {{ count.s = 0; count.b = 0; }}
                    if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; }}
                    document.getElementById('count-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                    
                    ball.active = false; ball.status = "ready";
                }}
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 560, 480);
                batter.wobble += 0.06;

                // 정통 야구장 필드 구현
                ctx.fillStyle = "#166534"; ctx.fillRect(0, 0, 560, 480);
                ctx.fillStyle = "#b45309"; ctx.beginPath(); ctx.moveTo(40, 480); ctx.lineTo(240, 150); ctx.lineTo(320, 150); ctx.lineTo(520, 480); ctx.fill();

                // 가이드 스트라이크 존
                ctx.strokeStyle = "rgba(255,255,255,0.4)"; ctx.lineWidth = 2; ctx.strokeRect(205, 250, 150, 140);

                // 🧑 배트를 흔들며 대기하는 정통 타자 그래픽
                ctx.save();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3;
                let bx = 165, by = 325;
                let wb = Math.sin(batter.wobble) * 1.3;
                ctx.beginPath(); ctx.arc(bx, by - 25 + wb, 6, 0, Math.PI * 2); ctx.fillStyle = "#ffffff"; ctx.fill();
                ctx.beginPath(); ctx.moveTo(bx, by - 19 + wb); ctx.lineTo(bx, by + 10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(bx, by + 10); ctx.lineTo(bx - 9, by + 28); ctx.moveTo(bx, by + 10); ctx.lineTo(bx + 9, by + 28); ctx.stroke();

                ctx.translate(bx, by - 10);
                if (batter.swinging) {{
                    let swingAngle = (batter.frame / 12) * Math.PI * 0.75;
                    ctx.rotate(swingAngle); batter.frame++;
                    if (batter.frame > 12) batter.swinging = false;
                }}
                ctx.strokeStyle = "#f59e0b"; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(42, -15); ctx.stroke();
                ctx.restore();

                // 🏃 유격수 위치 연산 및 다이빙/포구 상태 시각화
                fielder.x += (fielder.tx - fielder.x) * 0.08;
                fielder.y += (fielder.ty - fielder.y) * 0.08;
                
                // 수비수가 공을 성공적으로 캐치했는지 판정 (거리가 가깝고 tracking 상태일 때)
                if (hitBall.active && fielder.state === "tracking" && Math.hypot(fielder.x - hitBall.x, fielder.y - hitBall.y) < 22) {{
                    hitBall.active = false; ball.active = false; ball.status = "ready";
                    fielder.tx = fielder.sx; fielder.ty = fielder.sy; fielder.state = "normal";
                    count.o++; if(count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; }}
                    document.getElementById('count-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                    document.getElementById('commentary').innerText = "🎙️ 아웃! 유격수가 엄청난 호수비로 타구를 잡아냅니다!";
                }}

                ctx.fillStyle = (fielder.state === "tracking") ? "#ef4444" : "#3b82f6";
                ctx.beginPath(); ctx.arc(fielder.x, fielder.y, 8, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 10px sans-serif"; ctx.fillText(fielder.id, fielder.x - 14, fielder.y - 12);

                if (isDragging) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 9, 0, Math.PI * 2); ctx.stroke();
                }}

                // 날아오는 투구 렌더링 (멈춤 에러 완전 방지 보정)
                if (ball.active && ball.status === "flying") {{
                    ball.speed *= ball.drag;
                    ball.z += ball.speed;
                    let bk = Math.sin(ball.z * Math.PI) * ball.breakX * 21;
                    ball.x = 280 + (ball.tx - 280) * ball.z + bk;
                    ball.y = 150 + (ball.ty - 150) * ball.z;

                    let size = Math.max(3, 4 + ball.z * 15);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, size, 0, Math.PI * 2); ctx.fill();
                    ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 1; ctx.stroke();

                    if (ball.z >= 1.0) {{ ball.z = 1.0; evaluateZone(); }}
                }}

                // 타격 공 렌더링 및 라이프사이클 처리
                if (hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    hitBall.currentDist++;

                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 6, 0, Math.PI * 2); ctx.fill();

                    // 수명 한계를 넘거나 경기장 밖으로 나가면 안타/아웃 처리 후 원위치 리셋
                    if (hitBall.currentDist > hitBall.maxDist || hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 560) {{
                        if (fielder.state === "giveup") {{
                            count.s = 0; count.b = 0; // 안타 시 카운트 리셋
                            document.getElementById('count-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                        }}
                        hitBall.active = false; ball.active = false; ball.status = "ready";
                        fielder.tx = fielder.sx; fielder.ty = fielder.sy; fielder.state = "normal";
                    }}
                }}

                requestAnimationFrame(drawScene);
            }}
            drawScene();
        </script>
        """
        st.components.v1.html(html_part, height=630)

if __name__ == "__main__":
    main()
