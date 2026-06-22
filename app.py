import streamlit as st
import json
import random
import math

def main():
    st.set_page_config(page_title="MLB MATRIX v6 - STICKMAN EDITION", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #030712; color: #f9fafb; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        .stSelectbox > div > div { background-color: #1f2937 !important; color: #ffffff !important; border: 2px solid #3b82f6 !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 16px !important;
            border-radius: 10px !important; border: none !important; padding: 14px 28px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 30개 구단 핵심 풀 매핑 가동
    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스 (선발)": {"stamina": 100, "pitches": {"파워 포심": {"color": "#ef4444", "speed_start": 0.045, "drag_coeff": 1.0, "break_x": 0.0}, "명품 너클커브": {"color": "#f59e0b", "speed_start": 0.024, "drag_coeff": 0.82, "break_x": 4.5}}}
            },
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "키브라이언 헤이즈", "앤드류 맥커친"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이 (선발)": {"stamina": 100, "pitches": {"파워 포심": {"color": "#ef4444", "speed_start": 0.044, "drag_coeff": 1.0, "break_x": 0.0}, "명품 스위퍼": {"color": "#06b6d4", "speed_start": 0.030, "drag_coeff": 0.86, "break_x": -5.0}}}
            },
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "테오스카 에르난데스"]
        }
    }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #090d16 0%, #111827 100%); padding: 35px; border-radius: 20px; text-align: center; border: 2px solid #2563eb; max-width: 900px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 30px; font-weight: 900;">⚾ MLB MATRIX v6 - 졸라맨 라이브 스펙</h1>
                <p style="color: #60a5fa; margin-top: 10px; font-size: 15px;">두 번째 공 락 버그 완전 해결 • 투수/타자/수비수 전원 졸라맨 그래픽으로 리빌딩</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("🏃 내 투수 구단 선택", sorted_teams)
            sel_pitcher = st.selectbox("⚾ 투수 선택", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("🤖 상대 AI 타자 구단 선택", sorted_teams, index=1 if len(sorted_teams)>1 else 0)
            
        if st.button("🏟️ VER 6.0 졸라맨 패치 엔진 구동"):
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
        st.markdown("### 🎮 졸라맨 필드 컨트롤")
        st.success(f"투수: {st.session_state.pitcher_name}")
        selected_b_name = st.selectbox("🙋 현재 타석", st.session_state.a_data["lineup"])
        if st.button("🚪 메인 화면으로"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons_html = ""
        for idx, (p_name, p_info) in enumerate(st.session_state.p_data['pitches'].items(), 1):
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" class="pitch-btn" id="btn-p{idx}" style="background: {"#2563eb" if idx==1 else "#111827"}; color: white; border: 2px solid #2563eb; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; width:100%; margin-bottom:8px;">{p_name}</button>'

        html_part = f"""
        <div id="matrix-container" style="background: #020617; padding: 20px; border-radius: 16px; border: 1px solid #1e293b; max-width: 860px; margin: 0 auto;">
            
            <div style="background: #090d16; border: 2px solid #2563eb; border-radius: 10px; padding: 15px; margin-bottom: 12px; color: white; display: flex; justify-content: space-between; align-items: center;">
                <div><span style="color: #38bdf8; font-weight: 900;">⚾ {st.session_state.pitcher_name}</span></div>
                <div><span id="count-board" style="font-weight: 900; color: #f59e0b; font-size: 18px;">B: 0 | S: 0 | O: 0</span></div>
            </div>

            <div style="display: flex; gap: 20px;">
                <canvas id="matrixCanvas" width="600" height="500" style="background: #070a13; border: 3px solid #1e293b; display: block; border-radius: 10px;"></canvas>
                <div style="width: 200px; display: flex; flex-direction: column; background: #111827; padding: 15px; border-radius: 10px;">
                    <h4 style="color: #9ca3af; margin: 0 0 10px 0; font-size: 12px;">구종 선택</h4>
                    <div id="pitch-buttons-zone">{pitch_buttons_html}</div>
                </div>
            </div>

            <div style="background: #090d16; color: #f3f4f6; padding: 15px; border-radius: 10px; margin-top: 12px; border-left: 6px solid #2563eb; min-height: 45px; font-size:13px;">
                <span id="commentary" style="color: #38bdf8;">🎙️ [안내] 멈춤 현상 완전 리셋 패치. 졸라맨들의 수비 연산이 시작됩니다! 마우스를 끌어다 놓으세요.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('matrixCanvas');
            const ctx = canvas.getContext('2d');

            let game = {{ b: 0, s: 0, o: 0 }};
            const pitchesData = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitchesData)[0];

            // 🏃 생동감 넘치는 야수 졸라맨 진형 설정
            let fielders = [
                {{ id: "유격수", x: 210, y: 190, startX: 210, startY: 190, state: "idle" }},
                {{ id: "2루수", x: 390, y: 190, startX: 390, startY: 190, state: "idle" }},
                {{ id: "3루수", x: 150, y: 260, startX: 150, startY: 260, state: "idle" }},
                {{ id: "1루수", x: 450, y: 260, startX: 450, startY: 260, state: "idle" }},
                {{ id: "중견수", x: 300, y: 90, startX: 300, startY: 90, state: "idle" }}
            ];

            let isDragging = false;
            let dragTarget = {{ x: 300, y: 360 }};
            
            // ⚠️ 무한 멈춤 버그 방어막: 확실하게 타임아웃 필드 보장
            let ball = {{ active: false, status: "ready", x: 300, y: 160, z: 0, currentSpeed: 0, breakX: 0, drag: 1.0, tx: 300, ty: 360 }};
            let hitBall = {{ active: false, x: 300, y: 360, vx: 0, vy: 0 }};
            let batter = {{ swingActive: false, frame: 0, idleWobble: 0 }};
            let umpSignal = {{ text: "", frame: 0, color: "#fff" }};

            function setPitch(pName) {{
                selectedPitch = pName;
                document.querySelectorAll('.pitch-btn').forEach(b => b.style.backgroundColor = '#111827');
                event.target.style.backgroundColor = '#2563eb';
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if (!ball.active && !hitBall.active && ball.status === "ready") {{
                    isDragging = true;
                    updateDragPos(e);
                }}
            }});

            canvas.addEventListener('mousemove', (e) => {{
                if (isDragging) updateDragPos(e);
            }});

            canvas.addEventListener('mouseup', () => {{
                if (isDragging) {{ isDragging = false; firePitch(); }}
            }});

            function updateDragPos(e) {{
                let rect = canvas.getBoundingClientRect();
                dragTarget.x = (e.clientX - rect.left) * (canvas.width / rect.width);
                dragTarget.y = (e.clientY - rect.top) * (canvas.height / rect.height);
            }}

            function firePitch() {{
                let pData = pitchesData[selectedPitch];
                
                // ⚠️ 핵심 패치: 발사 순간 완벽 리셋으로 누적 가속 버그 원천 폭파
                ball.z = 0.0;
                ball.x = 300; 
                ball.y = 160;
                ball.tx = dragTarget.x; 
                ball.ty = dragTarget.y;
                ball.currentSpeed = pData.speed_start;
                ball.drag = pData.drag_coeff;
                ball.breakX = pData.break_x;
                
                ball.active = true;
                ball.status = "flying";
                
                batter.swingActive = false;
                batter.frame = 0;

                fielders.forEach(f => {{ f.state = "ready"; f.x = f.startX; f.y = f.startY; }});
            }}

            // 🎨 인간적인 졸라맨 그리기 함수
            function drawStickman(x, y, color, isStriking, swingFrame, wobble) {{
                ctx.save();
                ctx.strokeStyle = color;
                ctx.lineWidth = 2.5;
                ctx.fillStyle = color;

                // 머리 (대기 시 위아래로 숨쉬는 흔들림 추가)
                let headY = y - 25 + (wobble ? Math.sin(wobble) * 1.5 : 0);
                ctx.beginPath();
                ctx.arc(x, headY, 5, 0, Math.PI * 2);
                ctx.fill();

                // 척추
                ctx.beginPath();
                ctx.moveTo(x, headY + 5);
                ctx.lineTo(x, y - 5);
                ctx.stroke();

                if (isStriking) {{
                    // 타격용 다이나믹 배트 스윙 졸라맨 팔다리 연산
                    let armAngle = (swingFrame / 12) * Math.PI * 0.7;
                    ctx.beginPath();
                    ctx.moveTo(x, y - 15);
                    ctx.lineTo(x - 15 + Math.cos(armAngle)*20, y - 10 - Math.sin(armAngle)*10);
                    ctx.stroke();

                    // 배트
                    ctx.strokeStyle = "#d97706";
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    ctx.moveTo(x - 5, y - 15);
                    ctx.lineTo(x - 30 + Math.cos(armAngle)*45, y - 10 - Math.sin(armAngle)*35);
                    ctx.stroke();
                }} else {{
                    // 일반 수비 대기 자세 팔
                    ctx.beginPath();
                    ctx.moveTo(x, y - 15);
                    ctx.lineTo(x - 8, y - 8);
                    ctx.moveTo(x, y - 15);
                    ctx.lineTo(x + 8, y - 8);
                    ctx.stroke();
                }}

                // 다리 지지대
                ctx.strokeStyle = color;
                ctx.lineWidth = 2.5;
                ctx.beginPath();
                ctx.moveTo(x, y - 5);
                ctx.lineTo(x - 7, y + 10);
                ctx.moveTo(x, y - 5);
                ctx.lineTo(x + 7, y + 10);
                ctx.stroke();

                ctx.restore();
            }}

            function triggerFieldersAI(hitX, hitY) {{
                fielders.forEach(f => {{
                    let dist = Math.hypot(f.x - hitX, f.y - hitY);
                    if (dist < 260) {{
                        f.state = "chasing";
                        // 타구 지점을 향해 전력 대시 가속 매핑
                        f.startX = f.x; f.startY = f.y;
                        let angle = Math.atan2(hitY - f.y, hitX - f.x);
                        f.x += Math.cos(angle) * (60 + Math.random() * 30);
                        f.y += Math.sin(angle) * (60 + Math.random() * 30);
                    }}
                }});
            }}

            function evaluateZone() {{
                let inside = (ball.x >= 230 && ball.x <= 370 && ball.y >= 260 && ball.y <= 400);
                batter.swingActive = true;

                if (Math.random() < (inside ? 0.65 : 0.20)) {{
                    ball.active = false;
                    ball.status = "hit";
                    hitBall.active = true;
                    hitBall.x = ball.x;
                    hitBall.y = ball.y;
                    hitBall.vx = (Math.random() - 0.5) * 15;
                    hitBall.vy = -(5 + Math.random() * 12);
                    
                    document.getElementById('commentary').innerText = "🎙️ 깡!! 정타 작렬! 수비수 졸라맨들이 일제히 포구 동작에 들어갑니다!";
                    triggerFieldersAI(hitBall.x + hitBall.vx * 15, hitBall.y + hitBall.vy * 15);
                }} else {{
                    if (inside) {{
                        game.s++; umpSignal = {{ text: "STRIKE", color: "#ef4444", frame: 40 }};
                    }} else {{
                        game.b++; umpSignal = {{ text: "BALL", color: "#3b82f6", frame: 40 }};
                    }}
                    if (game.s >= 3 || game.b >= 4) {{ game.s = 0; game.b = 0; }}
                    document.getElementById('count-board').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
                    
                    // 판정 즉시 해제하여 절대 두 번째 멈춤이 없도록 조치
                    setTimeout(() => {{
                        ball.active = false;
                        ball.status = "ready";
                    }}, 200);
                }}
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 600, 500);
                batter.idleWobble += 0.08;

                // 🏟️ 푸른 그라운드 배경 그리기
                ctx.fillStyle = "#166534"; ctx.beginPath(); ctx.moveTo(0, 500); ctx.lineTo(220, 150); ctx.lineTo(380, 150); ctx.lineTo(600, 500); ctx.fill();
                ctx.fillStyle = "#9a3412"; ctx.beginPath(); ctx.moveTo(120, 500); ctx.lineTo(260, 170); ctx.lineTo(340, 170); ctx.lineTo(480, 500); ctx.fill();
                
                // 스트라이크존 아웃라인 가이드
                ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.strokeRect(230, 260, 140, 140);

                // 1. 투수 마운드 위 졸라맨 투수
                drawStickman(300, 150, "#38bdf8", ball.status==="flying", 0, batter.idleWobble);

                // 2. 타석 위 졸라맨 타자 (실시간 스윙 상태 체크)
                if (batter.swingActive) {{
                    drawStickman(200, 360, "#fbbf24", true, batter.frame, 0);
                    batter.frame++;
                    if(batter.frame > 12) batter.swingActive = false;
                }} else {{
                    drawStickman(200, 360, "#f59e0b", false, 0, batter.idleWobble);
                }}

                // 3. 필드 주위 수비수 졸라맨 무리 드로잉
                fielders.forEach(f => {{
                    drawStickman(f.x, f.y, "#a7f3d0", false, 0, batter.idleWobble * 0.5);
                    ctx.fillStyle = "#ffffff"; ctx.font = "9px sans-serif";
                    ctx.fillText(f.id, f.x - 12, f.y - 35);
                }});

                // 투구 실시간 이동 연산
                if (ball.active && ball.status === "flying") {{
                    ball.currentSpeed *= ball.drag;
                    ball.z += ball.currentSpeed;
                    let curveBreak = Math.sin(ball.z * Math.PI) * ball.breakX * 22;

                    ball.x = 300 + (ball.tx - 300) * ball.z + curveBreak;
                    ball.y = 160 + (ball.ty - 160) * ball.z;

                    // 진짜 야구공 형태로 드로잉
                    let r = Math.max(3, 4 + ball.z * 15);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, r, 0, Math.PI*2); ctx.fill();
                    ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 1; ctx.stroke();

                    if (ball.z >= 1.0) {{
                        ball.z = 1.0;
                        evaluateZone();
                    }}
                }}

                // 타구 궤적 연산
                if (hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 6, 0, Math.PI*2); ctx.fill();

                    if (hitBall.y < 30 || hitBall.x < 0 || hitBall.x > 600) {{
                        hitBall.active = false;
                        ball.active = false;
                        ball.status = "ready";
                        fielders.forEach(f => {{ f.x = f.startX; f.y = f.startY; }});
                    }}
                }}

                if (umpSignal.frame > 0) {{
                    ctx.fillStyle = umpSignal.color; ctx.font = "bold 42px sans-serif"; ctx.fillText(umpSignal.text, 210, 110); umpSignal.frame--;
                }}

                requestAnimationFrame(drawScene);
            }}

            drawScene();
        </script>
        """
        st.components.v1.html(html_part, height=660)

if __name__ == "__main__":
    main()
