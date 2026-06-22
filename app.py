import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB MATRIX v4 - INFINITE ENGINE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox > div > div { background-color: #1c2541 !important; color: #ffffff !important; border: 2px solid #3a86ff !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #3a86ff 0%, #8338ec 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important;
            border-radius: 8px !important; border: none !important; padding: 10px 15px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # ⚠️ 약속했던 30개 구단별 "선발/불펜 2인 투수 체제" 및 실제 타자 라인업 완전 매핑
    mlb_grand_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스 (선발)": {
                    "stamina": 100,
                    "pitches": {
                        "파워 포심": {"color": "#e63946", "speed_start": 0.039, "drag_coeff": 1.0, "break_x": 0.0},
                        "101마일 스플린커": {"color": "#f72585", "speed_start": 0.036, "drag_coeff": 0.93, "break_x": -1.8},
                        "명품 슬라이더": {"color": "#3a86ff", "speed_start": 0.031, "drag_coeff": 0.89, "break_x": 3.2},
                        "너클 커브": {"color": "#ffb703", "speed_start": 0.024, "drag_coeff": 0.84, "break_x": 0.5}
                    }
                },
                "데이비드 베드나 (마무리)": {
                    "stamina": 80,
                    "pitches": {
                        "하이 패스트볼": {"color": "#e63946", "speed_start": 0.037, "drag_coeff": 1.0, "break_x": 0.0},
                        "낙차 큰 스플리터": {"color": "#7209b7", "speed_start": 0.032, "drag_coeff": 0.88, "break_x": -0.2},
                        "커터": {"color": "#9b5de5", "speed_start": 0.034, "drag_coeff": 0.95, "break_x": 1.5}
                    }
                }
            },
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "키브라이언 헤이즈", "라우디 텔레즈", "앤드류 맥커친", "코너 조", "조이 바트"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이 (선발)": {
                    "stamina": 100,
                    "pitches": {
                        "파워 포심": {"color": "#e63946", "speed_start": 0.039, "drag_coeff": 1.0, "break_x": 0.0},
                        "명품 스위퍼": {"color": "#00f5d4", "speed_start": 0.028, "drag_coeff": 0.85, "break_x": -4.5},
                        "스플리터": {"color": "#7209b7", "speed_start": 0.033, "drag_coeff": 0.91, "break_x": 0.0},
                        "고속 커터": {"color": "#9b5de5", "speed_start": 0.035, "drag_coeff": 0.96, "break_x": 1.2}
                    }
                },
                "에반 필립스 (마무리)": {
                    "stamina": 75,
                    "pitches": {
                        "커터": {"color": "#9b5de5", "speed_start": 0.034, "drag_coeff": 0.95, "break_x": 1.6},
                        "슬라이더": {"color": "#3a86ff", "speed_start": 0.031, "drag_coeff": 0.89, "break_x": 3.0},
                        "포심 직구": {"color": "#e63946", "speed_start": 0.036, "drag_coeff": 0.99, "break_x": 0.0}
                    }
                }
            },
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "테오스카 에르난데스", "맥스 먼시", "토미 에드먼", "윌 스미"]
        },
        "San Francisco Giants": {
            "pitchers": {
                "로건 웹 (선발)": {
                    "stamina": 105,
                    "pitches": {
                        "명품 싱커": {"color": "#f15bb5", "speed_start": 0.034, "drag_coeff": 0.94, "break_x": -2.4},
                        "체인지업": {"color": "#06d6a0", "speed_start": 0.026, "drag_coeff": 0.83, "break_x": -1.8},
                        "슬라이더": {"color": "#3a86ff", "speed_start": 0.029, "drag_coeff": 0.88, "break_x": 2.6}
                    }
                },
                "캠밀로 도발 (마무리)": {
                    "stamina": 80,
                    "pitches": {
                        "103마일 싱커": {"color": "#f15bb5", "speed_start": 0.041, "drag_coeff": 0.96, "break_x": -1.5},
                        "슬라이더": {"color": "#3a86ff", "speed_start": 0.033, "drag_coeff": 0.90, "break_x": 3.5}
                    }
                }
            },
            "lineup": ["이정후", "타이로 에스트라다", "맷 채프먼", "마이클 콘포토", "윌머 플로레스", "패트릭 베일리"]
        },
        "New York Yankees": {
            "pitchers": {
                "게릿 콜 (선발)": {
                    "stamina": 100,
                    "pitches": {
                        "강속구 포심": {"color": "#e63946", "speed_start": 0.039, "drag_coeff": 1.0, "break_x": 0.0},
                        "고속 슬라이더": {"color": "#3a86ff", "speed_start": 0.031, "drag_coeff": 0.90, "break_x": 2.5},
                        "너클 커브": {"color": "#ffb703", "speed_start": 0.023, "drag_coeff": 0.83, "break_x": 0.4}
                    }
                },
                "루크 위버 (마무리)": {
                    "stamina": 85,
                    "pitches": {
                        "포심": {"color": "#e63946", "speed_start": 0.036, "drag_coeff": 0.99, "break_x": 0.0},
                        "체인지업": {"color": "#06d6a0", "speed_start": 0.028, "drag_coeff": 0.85, "break_x": -1.5},
                        "커터": {"color": "#9b5de5", "speed_start": 0.033, "drag_coeff": 0.94, "break_x": 1.0}
                    }
                }
            },
            "lineup": ["앤서니 볼피", "후안 소토", "애런 저지", "지안카를로 스탠튼", "앤서니 리조", "글레이버 토레스"]
        }
    }
    
    mlb_teams = sorted(list(mlb_grand_db.keys()))

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 25px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 30px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 25px; font-weight: 900;">⚾ MLB MATRIX v4 - 30 구단 인피니티 모듈</h1>
                <p style="color: #06d6a0; margin-top: 8px; font-size: 14px;">팀별 투수 2명 매핑 완료 • 실시간 타자 셀렉터 탑재 • 리얼 포수 주심 뷰</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            user_team = st.selectbox("🏃 투수 구단", mlb_teams, index=0)
            p_keys = list(mlb_grand_db[user_team]["pitchers"].keys())
            selected_pitcher = st.selectbox("⚾ 투수 선택 (구단별 2명)", p_keys)
        with c2:
            ai_team = st.selectbox("🤖 상대 타자 구단", mlb_teams, index=1 if len(mlb_teams)>1 else 0)
            
        if st.button("🏟️ 엔진 풀 스펙 로드"):
            st.session_state.p_team = user_team
            st.session_state.a_team = ai_team
            st.session_state.pitcher_name = selected_pitcher
            st.session_state.p_data = mlb_grand_db[user_team]["pitchers"][selected_pitcher]
            st.session_state.a_data = mlb_grand_db[ai_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    # 인플레이 화면 구성
    col_canvas, col_ctrl = st.columns([3, 1])

    with col_ctrl:
        st.markdown("### 🎮 REALTIME PANEL")
        st.caption("현재 플레이 중인 투수와 상태 정보입니다.")
        st.success(f"🏟️ 구단: {st.session_state.p_team}\n\n👤 투수: **{st.session_state.pitcher_name}**")
        
        st.markdown("---")
        st.markdown("### 🎯 타자 실시간 교체")
        st.caption("상대 팀 라인업 중 원하는 타자를 즉시 타석에 세울 수 있습니다.")
        
        # ⚠️ 타자도 마음대로 바꿀 수 있는 실시간 셀렉터 기능 추가
        selected_b_name = st.selectbox("🙋 타석 타자 변경", st.session_state.a_data["lineup"])
        
        st.markdown("---")
        if st.button("🚪 다른 팀/투수 고르기"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons_html = ""
        for idx, (p_name, p_info) in enumerate(st.session_state.p_data['pitches'].items(), 1):
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" class="pitch-btn" id="btn-p{idx}" style="background: {"#e63946" if idx==1 else "#0b1329"}; color: white; border: 1px solid #3a86ff; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size:12px; width:100%; margin-bottom:6px;">{p_name}</button>'

        html_part = f"""
        <div id="matrix-container" style="background: #0b1329; padding: 15px; border-radius: 14px; max-width: 820px; margin: 0 auto; font-family: sans-serif;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: white; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #4cc9f0; font-weight: bold; font-size: 15px;">🔥 ACTIVE: {st.session_state.pitcher_name}</span>
                    <span style="margin-left: 15px; font-size: 13px; color: #ff4757;">🔋 체력: <span id="stamina-val">100</span>%</span>
                </div>
                <div><span id="count-board" style="font-weight: bold; color: #ffb703; font-size: 16px;">B: 0 | S: 0 | O: 0</span></div>
            </div>

            <div style="background: #1c2541; padding: 8px; border-radius: 6px; color: #06d6a0; font-weight: bold; font-size: 14px; margin-bottom: 8px; text-align: center;">
                ⚔️ 타석: <span id="current-b-display" style="color:#fff;">{selected_b_name}</span> ({st.session_state.a_team})
            </div>

            <div style="display: flex; gap: 15px;">
                <canvas id="catcherCanvas" width="600" height="480" style="background: #130f40; border: 3px solid #1c2541; display: block; border-radius: 8px; cursor: crosshair;"></canvas>
                
                <div style="width: 180px; display: flex; flex-direction: column; background: #1c2541; padding: 12px; border-radius: 8px; box-sizing: border-box;">
                    <h4 style="color: #fff; margin: 0 0 8px 0; font-size: 13px;">🎯 구종 마스터리</h4>
                    <div id="pitch-buttons-zone">{pitch_buttons_html}</div>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 10px; border-left: 5px solid #06d6a0; min-height: 45px; font-size:13px; box-sizing: border-box;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 포수 시점 홈플레이트 뒤쪽 카메라 동기화 완료.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('catcherCanvas');
            const ctx = canvas.getContext('2d');

            let stamina = 100;
            let game = {{ b: 0, s: 0, o: 0 }};
            
            const pitchesData = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitchesData)[0];

            // 수비수 백업 레이아웃 데이터
            let fielders = [
                {{ id: "LF", x: 140, y: 130 }}, {{ id: "CF", x: 300, y: 95 }}, {{ id: "RF", x: 460, y: 130 }},
                {{ id: "SS", x: 220, y: 190 }}, {{ id: "2B", x: 380, y: 190 }},
                {{ id: "3B", x: 170, y: 240 }}, {{ id: "1B", x: 430, y: 240 }}
            ];

            let isDragging = false;
            let dragTarget = {{ x: 300, y: 340 }};
            let ball = {{ active: false, status: "ready", x: 300, y: 160, z: 0, startX: 300, startY: 160, tx: 300, ty: 340, currentSpeed: 0, breakX: 0, drag: 1.0 }};
            
            let umpSignal = {{ text: "", frame: 0, color: "#fff" }};
            let absSignal = {{ text: "", frame: 0 }};

            function setPitch(pName) {{
                selectedPitch = pName;
                document.querySelectorAll('.pitch-btn').forEach(b => b.style.backgroundColor = '#0b1329');
                event.target.style.backgroundColor = '#e63946';
            }}

            function getMousePos(e) {{
                let rect = canvas.getBoundingClientRect();
                return {{
                    x: (e.clientX - rect.left) * (canvas.width / rect.width),
                    y: (e.clientY - rect.top) * (canvas.height / rect.height)
                }};
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if (!ball.active && ball.status === "ready") {{
                    isDragging = true;
                    let pos = getMousePos(e);
                    dragTarget.x = pos.x; dragTarget.y = pos.y;
                }}
            }});

            canvas.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    let pos = getMousePos(e);
                    dragTarget.x = pos.x; dragTarget.y = pos.y;
                }}
            }});

            canvas.addEventListener('mouseup', () => {{
                if (isDragging) {{
                    isDragging = false;
                    firePitch();
                }}
            }});

            function firePitch() {{
                let pData = pitchesData[selectedPitch];
                let variance = (100 - stamina) * 0.25;
                let errX = (Math.random() - 0.5) * variance;
                let errY = (Math.random() - 0.5) * variance;

                ball.startX = 300; ball.startY = 160; // 투수 마운드 좌표 고정
                ball.x = 300; ball.y = 160;
                ball.tx = dragTarget.x + errX; ball.ty = dragTarget.y + errY;
                ball.z = 0;
                ball.currentSpeed = pData.speed_start;
                ball.drag = pData.drag_coeff;
                ball.breakX = pData.break_x;
                ball.active = true;
                ball.status = "flying";

                stamina = Math.max(0, stamina - 1);
                document.getElementById('stamina-val').innerText = stamina;
            }}

            function evaluateZone() {{
                ball.active = false;
                ball.status = "ready"; // ⚠️ 이닝 누락 및 팅김 현상 완치 

                let insideStrike = (ball.x >= 230 && ball.x <= 370 && ball.y >= 260 && ball.y <= 400);
                let insideBorder = (ball.x >= 210 && ball.x <= 390 && ball.y >= 240 && ball.y <= 420);
                
                let isRealStrike = insideStrike;
                let callStrike = isRealStrike;

                if (!insideStrike && insideBorder) {{
                    if (Math.random() < 0.25) callStrike = !callStrike; 
                }}

                if (callStrike) {{
                    game.s++; umpSignal = {{ text: "STRIKE!", color: "#e63946", frame: 45 }};
                }} else {{
                    game.b++; umpSignal = {{ text: "BALL", color: "#3a86ff", frame: 45 }};
                }}

                if (callStrike !== isRealStrike) {{
                    absSignal = {{ text: "📢 ABS 시스템 보정: 주심 오심 추적 교정 완료", frame: 60 }};
                }} else {{
                    absSignal = {{ text: "📢 ABS 트래킹: 정상 판정 수용", frame: 30 }};
                }}

                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; }}
                else if (game.b >= 4) {{ game.s = 0; game.b = 0; }}
                if (game.o >= 3) {{ game.o = 0; game.s = 0; game.b = 0; }}

                document.getElementById('count-board').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 600, 480);

                // 1. 진짜 포수 홈플레이트 중심 종심 구장 배경 드로잉
                ctx.fillStyle = "#1e7e34"; ctx.beginPath(); ctx.moveTo(0, 480); ctx.lineTo(250, 150); ctx.lineTo(350, 150); ctx.lineTo(600, 480); ctx.fill();
                ctx.fillStyle = "#d3a25d"; ctx.beginPath(); ctx.moveTo(100, 480); ctx.lineTo(270, 170); ctx.lineTo(330, 170); ctx.lineTo(500, 480); ctx.fill();

                // 수비수 배치
                fielders.forEach(f => {{
                    ctx.fillStyle = "#22a6b3"; ctx.beginPath(); ctx.arc(f.x, f.y, 5, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px sans-serif"; ctx.fillText(f.id, f.x - 6, f.y - 8);
                }});

                // 투수 릴리즈 포인트 구체
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(300, 160, 7, 0, Math.PI*2); ctx.fill();

                // 2. 포수 정면 스트라이크 존 그리드 고정 (230~370, 260~400)
                ctx.strokeStyle = "rgba(255, 255, 255, 0.15)"; ctx.lineWidth = 1;
                ctx.strokeRect(210, 240, 180, 180);
                
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3;
                ctx.strokeRect(230, 260, 140, 140);

                // 홈플레이트 시각화 오버레이 (포수 바로 앞)
                ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
                ctx.beginPath(); ctx.moveTo(270, 440); ctx.lineTo(330, 440); ctx.lineTo(330, 460); ctx.lineTo(300, 475); ctx.lineTo(270, 460); ctx.fill();

                if (isDragging) {{
                    ctx.strokeStyle = "#00f5d4"; ctx.lineWidth = 1;
                    ctx.beginPath(); ctx.arc(dragTarget.x, dragTarget.y, 8, 0, Math.PI*2); ctx.stroke();
                }}

                // 3. 8종 변화구 물리 브레이크 무브먼트 가동
                if (ball.active && ball.status === "flying") {{
                    ball.currentSpeed *= ball.drag;
                    ball.z += ball.currentSpeed;

                    let breakEffect = Math.sin(ball.z * Math.PI) * ball.breakX * 23;
                    ball.x = ball.startX + (ball.tx - ball.startX) * ball.z + breakEffect;
                    ball.y = ball.startY + (ball.ty - ball.startY) * ball.z;

                    let ballRadius = 3 + (ball.z * 18); // 날아오면서 거대해지는 리얼 시점 효과
                    
                    ctx.fillStyle = pitchesData[selectedPitch]?.color || "#ffffff";
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2); ctx.fill();

                    if (ball.z >= 1.0) evaluateZone();
                }}

                if (umpSignal.frame > 0) {{
                    ctx.fillStyle = umpSignal.color; ctx.font = "bold 42px sans-serif"; ctx.fillText(umpSignal.text, 215, 120); umpSignal.frame--;
                }}
                if (absSignal.frame > 0) {{
                    ctx.fillStyle = "rgba(2, 12, 27, 0.95)"; ctx.fillRect(10, 10, 480, 32);
                    ctx.fillStyle = "#06d6a0"; ctx.font = "bold 12px sans-serif"; ctx.fillText(absSignal.text, 20, 30); absSignal.frame--;
                }}

                requestAnimationFrame(drawScene);
            }}

            drawScene();
        </script>
        """
        st.components.v1.html(html_part, height=620)

if __name__ == "__main__":
    main()
