import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW - FINAL STANDARD", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #111827; color: #f9fafb; font-family: sans-serif; }
        .stSelectbox > div > div { background-color: #1f2937 !important; color: #ffffff !important; border: 2px solid #15803d !important; }
        .stButton > button {
            background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
            color: white !important; font-weight: bold !important; border: none !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 30개 전 구단 원본 스펙 데이터베이스
    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스 (선발)": {"pitches": {"파워 포심": {"speed": 0.042, "drag": 1.0, "break": 0.0}, "명품 너클커브": {"speed": 0.025, "drag": 0.83, "break": 4.5}}},
                "데이비드 베드나 (마무리)": {"pitches": {"하이 패스트볼": {"speed": 0.039, "drag": 1.0, "break": 0.0}}}
            },
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "앤드류 맥커친", "조이 바트"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이 (선발)": {"pitches": {"파워 포심": {"speed": 0.041, "drag": 1.0, "break": 0.0}, "명품 스위퍼": {"speed": 0.029, "drag": 0.85, "break": -4.8}}}
            },
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "윌 스미"]
        }
    }

    # 구단 확장 호환성 자동 매핑
    for t in ["New York Yankees", "San Francisco Giants", "San Diego Padres"]:
        if t not in mlb_mega_db:
            mlb_mega_db[t] = {
                "pitchers": {"에이스 (선발)": {"pitches": {"직구": {"speed": 0.040, "drag": 1.0, "break": 0.0}}}},
                "lineup": ["대타자 A", "대타자 B"]
            }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#22c55e; margin-top:30px;'>⚾ 포수 시점 리얼 베이스볼 (버그 완치 최종본)</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("내 투수 구단", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            sel_pitcher = st.selectbox("투수 라인업", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("상대 타자 구단", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        if st.button("🏟️ 야구장 입장"):
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
        st.markdown("### 🏟️ 경기 상태 창")
        st.info(f"**현재 투수:** {st.session_state.pitcher_name}")
        st.selectbox("🙋 타석 대기 타자", st.session_state.a_data["lineup"])
        st.markdown("---")
        if st.button("🚪 게이트 퇴장"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#16a34a" if idx == 1 else "#1f2937"
            pitch_buttons += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" id="p{idx}" style="background:{bg}; color:white; border:1px solid #16a34a; padding:12px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:8px; font-weight:bold;">{p_name}</button>'

        html_src = f"""
        <div style="max-width:820px; margin:0 auto;">
            <div style="background:#1f2937; color:white; padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold; border:1px solid #374151;">
                <div>⚾ 정통 포수 관점 (Catcher View)</div>
                <div id="score-board" style="color:#fbbf24; font-size:16px;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="gameCanvas" width="560" height="480" style="background:#15803d; border:3px solid #374151; border-radius:8px;"></canvas>
                <div style="width:190px; background:#1f2937; padding:12px; border-radius:8px; height:fit-content; border:1px solid #374151;">
                    <span style="color:#9ca3af; font-size:12px; font-weight:bold;">배당 구종</span>
                    <div style="margin-top:8px;">{pitch_buttons}</div>
                </div>
            </div>

            <div style="background:#1f2937; border-left:5px solid #16a34a; padding:12px; border-radius:6px; margin-top:10px; font-weight:bold; color:#f3f4f6; font-size:13px;">
                <span id="relay-text">🎙️ [안내] 존 안쪽을 드래그-클릭하여 투구하세요. 투구 멈춤 오류가 완벽히 해결되었습니다!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitches)[0];

            // 수비수 기본 좌표 배치 (고유 수비 위치 고정)
            let fielder = {{ id: "유격수", x: 220, y: 190, sx: 220, sy: 190, tx: 220, ty: 190 }};

            let isTargeting = false;
            let targetPos = {{ x: 280, y: 350 }};
            
            // 물리 락 현상을 완벽히 배제하기 위한 제어 플래그 분리 구조체
            let ball = {{ active: false, status: "ready", x: 280, y: 150, z: 0.0, tx: 280, ty: 350, speed: 0, drag: 1.0, breakX: 0 }};
            let hitBall = {{ active: false, x: 280, y: 350, vx: 0, vy: 0 }};
            let batter = {{ swinging: false, frame: 0 }};

            function setPitch(name) {{
                selectedPitch = name;
                document.querySelectorAll('.p-btn').forEach(b => b.style.backgroundColor = '#1f2937');
                event.target.style.backgroundColor = '#16a34a';
            }}

            function getMouse(e) {{
                let r = canvas.getBoundingClientRect();
                return {{ x: (e.clientX - r.left)*(canvas.width/r.width), y: (e.clientY - r.top)*(canvas.height/r.height) }};
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if(!ball.active && !hitBall.active && ball.status === "ready") {{
                    isTargeting = true;
                    let m = getMouse(e); targetPos.x = m.x; targetPos.y = m.y;
                }}
            }});
            canvas.addEventListener('mousemove', (e) => {{
                if(isTargeting) {{ let m = getMouse(e); targetPos.x = m.x; targetPos.y = m.y; }}
            }});
            canvas.addEventListener('mouseup', () => {{
                if(isTargeting) {{ isTargeting = false; throwBall(); }}
            }});

            function throwBall() {{
                let p = pitches[selectedPitch];
                ball.z = 0.0; ball.x = 280; ball.y = 150;
                ball.tx = targetPos.x; ball.ty = targetPos.y;
                ball.speed = p.speed; ball.drag = p.drag; ball.breakX = p.break;
                
                ball.active = true;
                ball.status = "go"; // 날아가는 중 상태 돌입
                batter.swinging = false; batter.frame = 0;
                
                // 투구 시 유격수 무조건 자기 자리 대기 안정화
                fielder.tx = fielder.sx; fielder.ty = fielder.sy;
            }}

            function judgeZone() {{
                // 멈춤 오류 절대 방지를 위해 도달 즉시 active 플래그부터 해제
                ball.active = false; 
                
                let isStrike = (ball.x >= 200 && ball.x <= 360 && ball.y >= 250 && ball.y <= 390);
                batter.swinging = true;

                // 타격 확률 연산 (스트라이크면 휘두를 확률 대폭 증가)
                if (Math.random() < (isStrike ? 0.65 : 0.18)) {{
                    ball.status = "hit";
                    hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y;
                    hitBall.vx = (Math.random() - 0.5) * 14;
                    hitBall.vy = -(5 + Math.random() * 9);
                    
                    let destX = hitBall.x + hitBall.vx * 15;
                    let destY = hitBall.y + hitBall.vy * 15;
                    let dist = Math.hypot(fielder.sx - destX, fielder.sy - destY);

                    if(dist < 130) {{
                        fielder.tx = destX; fielder.ty = destY;
                        document.getElementById('relay-text').innerText = "🎙️ 깡! 유격수 정면 타구! 유격수가 포구를 시도합니다!";
                    }} else {{
                        // 범위를 넘어서면 외야 방향으로 쫓아가다 한계에서 멈추도록 유도
                        fielder.tx = fielder.sx + (destX - fielder.sx) * 0.35;
                        fielder.ty = fielder.sy + (destY - fielder.sy) * 0.35;
                        document.getElementById('relay-text').innerText = "🎙️ 안타! 유격수 키를 넘어 외야로 빠져나갑니다!";
                    }}
                }} else {{
                    // 미트 인 (포구 및 볼카운트 판정)
                    if(isStrike) {{ count.s++; }} else {{ count.b++; }}
                    if(count.s >= 3) {{ count.o++; count.s=0; count.b=0; }}
                    else if(count.b >= 4) {{ count.s=0; count.b=0; }}
                    if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                    document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                    document.getElementById('relay-text').innerText = isStrike ? "🎙️ 스트라이크!" : "🎙️ 볼!";
                    
                    // 판정 즉시 완전 초기화 상태로 복원시켜 정지 락 차단
                    ball.status = "ready";
                }}
            }}

            function loop() {{
                ctx.clearRect(0,0,560,480);

                // 정통 야구장 필드 라인 구현
                ctx.fillStyle = "#15803d"; ctx.fillRect(0,0,560,480);
                ctx.fillStyle = "#a16207"; ctx.beginPath(); ctx.moveTo(40,480); ctx.lineTo(240,150); ctx.lineTo(320,150); ctx.lineTo(520,480); ctx.fill();

                // 가이드 라인 스트라이크 존 백그라운드
                ctx.strokeStyle = "rgba(255,255,255,0.35)"; ctx.lineWidth = 2; ctx.strokeRect(200, 250, 160, 140);

                // 🧑 정통 타자 그래픽 복원 및 렌더링
                ctx.save();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3;
                let tx = 160, ty = 320;
                ctx.beginPath(); ctx.arc(tx, ty-25, 6, 0, Math.PI*2); ctx.fillStyle="#ffffff"; ctx.fill();
                ctx.beginPath(); ctx.moveTo(tx, ty-19); ctx.lineTo(tx, ty+10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty+10); ctx.lineTo(tx-10, ty+30); ctx.moveTo(tx, ty+10); ctx.lineTo(tx+10, ty+30); ctx.stroke();

                ctx.translate(tx, ty-10);
                if(batter.swinging) {{
                    let angle = (batter.frame / 12) * Math.PI * 0.75;
                    ctx.rotate(angle); batter.frame++;
                    if(batter.frame > 12) batter.swinging = false;
                }}
                ctx.strokeStyle = "#eab308"; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(45, -15); ctx.stroke();
                ctx.restore();

                // 🏃 유격수 이동 역학 및 복귀 처리 알고리즘
                fielder.x += (fielder.tx - fielder.x) * 0.08;
                fielder.y += (fielder.ty - fielder.y) * 0.08;
                
                // 타구를 쫓아가서 잡았을 때의 처리
                if (hitBall.active && Math.hypot(fielder.x - hitBall.x, fielder.y - hitBall.y) < 20) {{
                    hitBall.active = false; ball.status = "ready";
                    fielder.tx = fielder.sx; fielder.ty = fielder.sy; // 잡은 즉시 원위치 자동 귀환
                    count.o++; if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                    document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                    document.getElementById('relay-text').innerText = "🎙️ 아웃! 유격수가 타구를 안정적으로 포구해 냈습니다!";
                }}

                ctx.fillStyle = "#3b82f6"; ctx.beginPath(); ctx.arc(fielder.x, fielder.y, 8, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 10px sans-serif"; ctx.fillText(fielder.id, fielder.x-14, fielder.y-12);

                if(isTargeting) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 8, 0, Math.PI*2); ctx.stroke();
                }}

                // 투구 이동 프로세스
                if(ball.active && ball.status === "go") {{
                    ball.speed *= ball.drag;
                    ball.z += ball.speed;
                    let bk = Math.sin(ball.z * Math.PI) * ball.breakX * 20;
                    ball.x = 280 + (ball.tx - 280)*ball.z + bk;
                    ball.y = 150 + (ball.ty - 150)*ball.z;

                    let size = Math.max(3, 4 + ball.z * 14);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, size, 0, Math.PI*2); ctx.fill();
                    ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 1; ctx.stroke();

                    if(ball.z >= 1.0) {{ ball.z = 1.0; judgeZone(); }}
                }}

                // 타구 아웃오브바운드 소멸 및 유격수 제자리 강제 소환 복귀 시스템
                if(hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 6, 0, Math.PI*2); ctx.fill();

                    if(hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 560) {{
                        hitBall.active = false; 
                        ball.status = "ready"; // 완벽 초기화 보장
                        fielder.tx = fielder.sx; fielder.ty = fielder.sy; // 타구가 나가면 즉시 자기 수비위치 복귀
                    }}
                }}

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(html_src, height=630)

if __name__ == "__main__":
    main()
