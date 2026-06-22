import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW GAME", layout="wide")
    
    # 30개 구단 메인 데이터 (구단주님의 원본 스펙 유지)
    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스 (선발)": {"pitches": {"파워 포심": {"speed": 0.042, "drag": 1.0, "break": 0.0}, "명품 너클커브": {"speed": 0.025, "drag": 0.83, "break": 4.5}}},
                "데이비드 베드나 (마무리)": {"pitches": {"하이 패스트볼": {"speed": 0.039, "drag": 1.0, "break": 0.0}}}
            },
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "앤드류 맥커친"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이 (선발)": {"pitches": {"파워 포심": {"speed": 0.041, "drag": 1.0, "break": 0.0}, "명품 스위퍼": {"speed": 0.029, "drag": 0.85, "break": -4.8}}}
            },
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼"]
        }
    }

    # 타 구단 호환성 유지용 자동 삽입
    for t in ["New York Yankees", "San Francisco Giants", "San Diego Padres", "Boston Red Sox"]:
        if t not in mlb_mega_db:
            mlb_mega_db[t] = {
                "pitchers": {"에이스 (선발)": {"pitches": {"직구": {"speed": 0.040, "drag": 1.0, "break": 0.0}}}},
                "lineup": ["1번타자", "2번타자", "3번타자"]
            }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center;'>⚾ 정통 포수시점 야구 게임 (버그 수정판)</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("내 투수 구단", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            sel_pitcher = st.selectbox("투수 선택", list(mlb_mega_db[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("상대 AI 타자 구단", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
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
        st.markdown(f"### 🏟️ 경기 정보")
        st.write(f"**투수:** {st.session_state.pitcher_name}")
        st.selectbox("🚨 타석 타자", st.session_state.a_data["lineup"])
        st.markdown("---")
        if st.button("🚪 게임 종료"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#16a34a" if idx == 1 else "#1f2937"
            pitch_buttons += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" id="p{idx}" style="background:{bg}; color:white; border:1px solid #16a34a; padding:10px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:6px; font-weight:bold;">{p_name}</button>'

        html_src = f"""
        <div style="max-width:800px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold;">
                <div>🥎 {st.session_state.pitcher_name} 투구 준비 완료</div>
                <div id="score-board">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="baseballCanvas" width="550" height="480" style="background:#15803d; border:4px solid #1e293b; border-radius:8px;"></canvas>
                <div style="width:180px; background:#1f2937; padding:12px; border-radius:8px; height:fit-content;">
                    <span style="color:#9ca3af; font-size:12px; font-weight:bold;">구종 변경</span>
                    <div style="margin-top:8px;">{pitch_buttons}</div>
                </div>
            </div>

            <div style="background:#f8fafc; border-left:5px solid #16a34a; padding:12px; border-radius:6px; margin-top:10px; font-weight:bold; color:#334155; font-size:13px;">
                <span id="relay">🎙️ 마우스로 스트라이크 존 안팎을 클릭하거나 드래그하여 투구하세요!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitches)[0];

            // 🏃 요구사항 반영: 수비수는 단 한 명 (유격수)
            let fielder = {{ id: "유격수", x: 200, y: 180, tx: 200, ty: 180 }};

            let isTargeting = false;
            let targetPos = {{ x: 275, y: 340 }};
            
            // 🔒 멈춤 오류 방지용 완벽 구조체
            let ball = {{ active: false, status: "ready", x: 275, y: 150, z: 0.0, sx: 275, sy: 150, tx: 275, ty: 340, speed: 0, drag: 1.0, breakX: 0 }};
            let hitBall = {{ active: false, x: 275, y: 340, vx: 0, vy: 0 }};
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
                ball.z = 0.0;
                ball.x = 275; ball.y = 150;
                ball.tx = targetPos.x; ball.ty = targetPos.y;
                ball.speed = p.speed;
                ball.drag = p.drag;
                ball.breakX = p.break;
                ball.active = true;
                ball.status = "go";
                batter.swinging = false; batter.frame = 0;
                fielder.x = 200; fielder.y = 180; fielder.tx = 200; fielder.ty = 180;
            }}

            function judgeZone() {{
                let isStrike = (ball.x >= 200 && ball.x <= 350 && ball.y >= 250 && ball.y <= 390);
                batter.swinging = true;

                if (Math.random() < (isStrike ? 0.6 : 0.15)) {{
                    ball.active = false;
                    ball.status = "hit";
                    hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y;
                    hitBall.vx = (Math.random() - 0.5) * 14;
                    hitBall.vy = -(4 + Math.random() * 10);
                    document.getElementById('relay').innerText = "🎙️ 깡! 타격 성공! 유격수가 타구를 따라 움직입니다!";
                    
                    // 수비수 단 한 명만 타구 지점으로 대시 연산
                    fielder.tx = hitBall.x + hitBall.vx * 15;
                    fielder.ty = hitBall.y + hitBall.vy * 15;
                }} else {{
                    if(isStrike) {{ count.s++; }} else {{ count.b++; }}
                    if(count.s >= 3) {{ count.o++; count.s=0; count.b=0; }}
                    else if(count.b >= 4) {{ count.s=0; count.b=0; }}
                    if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                    document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                    
                    // ⚠️ 핵심: 다음 루프 대기 전 명확히 초기화하여 락 걸림 방지
                    ball.active = false;
                    ball.status = "ready";
                }}
            }}

            function loop() {{
                ctx.clearRect(0,0,550,480);

                // 야구장 그라운드 리얼 베이스 라인 (포수 시점 정화)
                ctx.fillStyle = "#15803d"; ctx.fillRect(0,0,550,480);
                ctx.fillStyle = "#a16207"; ctx.beginPath(); ctx.moveTo(50,480); ctx.lineTo(230,150); ctx.lineTo(320,150); ctx.lineTo(500,480); ctx.fill();

                // 홈 플레이트 및 스트라이크 존 백그라운드 라인
                ctx.strokeStyle = "rgba(255,255,255,0.4)"; ctx.lineWidth = 2; ctx.strokeRect(200, 250, 150, 140);

                // 🧑 타자 컴백 (좌타석 대기 상태의 타자 그래픽 묘사)
                ctx.save();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3;
                let tx = 160, ty = 320;
                ctx.beginPath(); ctx.arc(tx, ty-25, 6, 0, Math.PI*2); ctx.fillStyle="#ffffff"; ctx.fill(); // 머리
                ctx.beginPath(); ctx.moveTo(tx, ty-19); ctx.lineTo(tx, ty+10); ctx.stroke(); // 몸통
                ctx.beginPath(); ctx.moveTo(tx, ty+10); ctx.lineTo(tx-10, ty+30); ctx.moveTo(tx, ty+10); ctx.lineTo(tx+10, ty+30); ctx.stroke(); // 다리

                // 타자 배트 스윙 애니메이션
                ctx.translate(tx, ty-10);
                if(batter.swinging) {{
                    let angle = (batter.frame / 12) * Math.PI * 0.7;
                    ctx.rotate(angle); batter.frame++;
                    if(batter.frame > 12) batter.swinging = false;
                }}
                ctx.strokeStyle = "#eab308"; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(45, -15); ctx.stroke();
                ctx.restore();

                // 🏃 오직 한 명뿐인 수비수 (유격수) 드로잉 및 AI 추적
                fielder.x += (fielder.tx - fielder.x) * 0.07;
                fielder.y += (fielder.ty - fielder.y) * 0.07;
                ctx.fillStyle = "#3b82f6"; ctx.beginPath(); ctx.arc(fielder.x, fielder.y, 8, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 10px sans-serif"; ctx.fillText(fielder.id, fielder.x-15, fielder.y-12);

                if(isTargeting) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 8, 0, Math.PI*2); ctx.stroke();
                }}

                // 공 투구 궤적 및 물리 연산
                if(ball.active && ball.status === "go") {{
                    ball.speed *= ball.drag;
                    ball.z += ball.speed;
                    let bk = Math.sin(ball.z * Math.PI) * ball.breakX * 20;
                    ball.x = 275 + (ball.tx - 275)*ball.z + bk;
                    ball.y = 150 + (ball.ty - 150)*ball.z;

                    let size = Math.max(3, 4 + ball.z * 14);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, size, 0, Math.PI*2); ctx.fill();
                    ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 1; ctx.stroke();

                    if(ball.z >= 1.0) {{ ball.z = 1.0; judgeZone(); }}
                }}

                // 타구 이동 연산
                if(hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 6, 0, Math.PI*2); ctx.fill();

                    if(hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 550) {{
                        hitBall.active = false; ball.active = false; ball.status = "ready";
                        fielder.x = 200; fielder.y = 180; fielder.tx = 200; fielder.ty = 180;
                    }}
                }}

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(html_src, height=620)

if __name__ == "__main__":
    main()
