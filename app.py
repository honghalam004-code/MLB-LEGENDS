import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB MATRIX v4 - CATCHER CORE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox > div > div { background-color: #1c2541 !important; color: #ffffff !important; border: 2px solid #3a86ff !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #e63946 0%, #b7094c 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 16px !important;
            border-radius: 8px !important; border: none !important; padding: 12px 20px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 8종 고유 변화구 및 물리 계수가 완벽하게 매핑된 투수 데이터셋
    pitcher_db = {
        "폴 스킨스 (PIT)": {
            "stamina": 100,
            "pitches": {
                "파워 포심": {"type": "fast", "color": "#e63946", "speed_start": 0.035, "drag_coeff": 1.0, "break_x": 0.0},
                "101마일 스플린커": {"type": "splinker", "color": "#f72585", "speed_start": 0.033, "drag_coeff": 0.92, "break_x": -1.8},
                "명품 슬라이더": {"type": "slider", "color": "#3a86ff", "speed_start": 0.028, "drag_coeff": 0.88, "break_x": 3.2},
                "너클 커브": {"type": "curve", "color": "#ffb703", "speed_start": 0.022, "drag_coeff": 0.82, "break_x": 0.5}
            }
        },
        "오타니 쇼헤이 (LAD)": {
            "stamina": 100,
            "pitches": {
                "파워 포심": {"type": "fast", "color": "#e63946", "speed_start": 0.035, "drag_coeff": 1.0, "break_x": 0.0},
                "명품 스위퍼": {"type": "sweeper", "color": "#00f5d4", "speed_start": 0.027, "drag_coeff": 0.85, "break_x": -4.5},
                "스플리터": {"type": "splitter", "color": "#7209b7", "speed_start": 0.031, "drag_coeff": 0.90, "break_x": 0.0},
                "고속 커터": {"type": "cutter", "color": "#9b5de5", "speed_start": 0.033, "drag_coeff": 0.96, "break_x": 1.2}
            }
        },
        "로건 웹 (SF)": {
            "stamina": 100,
            "pitches": {
                "명품 싱커": {"type": "sinker", "color": "#f15bb5", "speed_start": 0.032, "drag_coeff": 0.93, "break_x": -2.2},
                "체인지업": {"type": "changeup", "color": "#06d6a0", "speed_start": 0.026, "drag_coeff": 0.84, "break_x": -1.5}
            }
        }
    }

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 30px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 700px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 900;">⚾ MLB MATRIX v4 - CORE ENGINE</h1>
                <p style="color: #06d6a0; margin-top: 10px; font-size: 14px;">STEP 1: 포수 시점 리얼 변화구 물리 감속 및 ABS 판정 시뮬레이터</p>
            </div>
        """, unsafe_allow_html=True)
        
        selected_p = st.selectbox("🔥 테스트할 투수 선택", list(pitcher_db.keys()))
        
        if st.button("🏟️ 포수 시점 캔버스 가동"):
            st.session_state.pitcher_name = selected_p
            st.session_state.pitcher_data = pitcher_db[selected_p]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_screen, col_ctrl = st.columns([3, 1])

    with col_ctrl:
        st.markdown("### 🎮 PITCHING CONTROL")
        st.caption("원하는 구종을 선택하고 아래 캔버스의 **스트라이크 존 경계면(보더라인)**을 마우스 드래그로 조준해 던지세요!")
        
        pitch_buttons_html = ""
        for idx, (p_name, p_info) in enumerate(st.session_state.pitcher_data['pitches'].items(), 1):
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" id="btn-p{idx}" style="background: {"#e63946" if idx==1 else "#1c2541"}; color: white; border: 1px solid #3a86ff; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size:13px; width:100%; margin-bottom:6px;">{p_name}</button>'
        
        st.components.v1.html(f"""
            <div style="display: flex; flex-direction: column; gap: 2px;">
                {pitch_buttons_html}
            </div>
            <script>
                function setPitch(name) {{
                    window.parent.postMessage({{type: 'SET_PITCH', val: name}}, '*');
                }}
            </script>
        """, height=240)

        st.markdown("---")
        if st.button("🚪 메인 화면으로"):
            st.session_state.game_active = False
            st.rerun()

    with col_screen:
        html_part = f"""
        <div id="matrix-container" style="background: #0b1329; padding: 10px; border-radius: 14px; max-width: 740px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 10px; margin-bottom: 8px; color: white; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #4cc9f0; font-weight: bold; font-size: 15px;">🔥 투수: {st.session_state.pitcher_name}</span>
                    <span style="margin-left: 15px; font-size: 13px; color: #ff4757;">🔋 체력: <span id="stamina-val">100</span>%</span>
                </div>
                <div><span id="count-board" style="font-weight: bold; color: #ffb703; font-size: 15px;">B: 0 | S: 0 | O: 0</span></div>
            </div>

            <canvas id="catcherCanvas" width="700" height="460" style="background: #1e272e; border: 3px solid #1c2541; display: block; border-radius: 8px; cursor: crosshair;"></canvas>

            <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 6px; border-left: 5px solid #06d6a0; min-height: 48px; font-size:13px;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 포수 시점 마운드가 정렬되었습니다. 마우스 드래그로 타겟을 지정하세요.</span>
            </div>
        </div>
        """

        js_part = f"""
        <script>
            const canvas = document.getElementById('catcherCanvas');
            const ctx = canvas.getContext('2d');

            let stamina = 100;
            let game = {{ b: 0, s: 0, o: 0 }};
            const pitchesData = {json.dumps(st.session_state.pitcher_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitchesData)[0];

            // 조작 물리계 데이터 변수
            let isDragging = false;
            let dragTarget = {{ x: 350, y: 300 }};
            
            // 3D 볼 변수 (Z축이 0이면 투수 손, 1이면 포수 미트 도달)
            let ball = {{ active: false, status: "ready", x: 350, y: 160, z: 0, startX: 350, startY: 160, tx: 350, ty: 300, currentSpeed: 0, breakX: 0, drag: 1.0 }};
            
            let umpSignal = {{ text: "", frame: 0, color: "#fff" }};
            let absSignal = {{ text: "", frame: 0 }};

            // Streamlit 버튼 연동 통신 핸들러
            window.addEventListener('message', function(e) {{
                if (e.data.type === 'SET_PITCH') {{
                    selectedPitch = e.data.val;
                }}
            }});

            canvas.addEventListener('mousedown', (e) => {{
                if (!ball.active && ball.status === "ready") {{
                    isDragging = true;
                    updateDragCoords(e);
                }}
            }});

            canvas.addEventListener('mousemove', (e) => {{
                if (isDragging) updateDragCoords(e);
            }});

            canvas.addEventListener('mouseup', () => {{
                if (isDragging) {{
                    isDragging = false;
                    firePitch();
                }}
            }});

            function updateDragCoords(e) {{
                let rect = canvas.getBoundingClientRect();
                dragTarget.x = e.clientX - rect.left;
                dragTarget.y = e.clientY - rect.top;
            }}

            function firePitch() {{
                let pData = pitchesData[selectedPitch];
                
                // 체력 감소에 따른 미세한 제구 흔들림(Variance) 기믹
                let staminaFactor = (100 - stamina) * 0.2;
                let randomErrorX = (Math.random() - 0.5) * staminaFactor;
                let randomErrorY = (Math.random() - 0.5) * staminaFactor;

                ball.startX = 350; ball.startY = 140; // 저 멀리 마운드 투수 릴리즈 포인트
                ball.x = 350; ball.y = 140;
                ball.tx = dragTarget.x + randomErrorX; ball.ty = dragTarget.y + randomErrorY;
                
                ball.z = 0;
                ball.currentSpeed = pData.speed_start;
                ball.drag = pData.drag_coeff; // 변화구 고유 감속 계수
                ball.breakX = pData.break_x;
                ball.active = true;
                ball.status = "flying";

                stamina = Math.max(0, stamina - 1);
                document.getElementById('stamina-val').innerText = stamina;
                document.getElementById('commentary').innerText = "🎙️ 투수 손을 떠났습니다! 구종: " + selectedPitch;
            }}

            function evaluateZone() {{
                ball.active = false;
                ball.status = "ready";

                // ⚠️ 포수 정면 시점의 리얼 스트라이크 존 규격 (280~420가 존 내부)
                let insideStrike = (ball.x >= 280 && ball.x <= 420 && ball.y >= 230 && ball.y <= 370);
                let insideBorder = (ball.x >= 265 && ball.x <= 435 && ball.y >= 215 && ball.y <= 385);
                
                let isRealStrike = insideStrike;
                let callStrike = isRealStrike;

                // 보더라인 영역(존의 가장자리 띠)에 걸칠 때 인간 심판 25% 확률 오심 발생
                if (!insideStrike && insideBorder) {{
                    if (Math.random() < 0.25) {{
                        callStrike = !callStrike; // 오심 판정 유도
                    }}
                }}

                if (callStrike) {{
                    game.s++; umpSignal = {{ text: "STRIKE!", color: "#e63946", frame: 45 }};
                }} else {{
                    game.b++; umpSignal = {{ text: "BALL", color: "#3a86ff", frame: 45 }};
                }}

                // ABS(로봇심판) 정밀 추적 교정 시스템 시각화
                if (callStrike !== isRealStrike) {{
                    absSignal = {{ text: "📢 ABS 판정 교정: 주심 오심 추적됨 [실제 판정: " + (isRealStrike?"STRIKE":"BALL") + "]", frame: 65 }};
                }} else {{
                    absSignal = {{ text: "📢 ABS 판정 추적: 주심 판정과 100% 일치", frame: 30 }};
                }}

                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; }}
                if (game.b >= 4) {{ game.s = 0; game.b = 0; }}
                if (game.o >= 3) {{ game.o = 0; game.s = 0; game.b = 0; }}

                document.getElementById('count-board').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 700, 460);

                // 1. 포수 시점 투수 마운드 원근 가이드 라인
                ctx.strokeStyle = "#3c40c6"; ctx.lineWidth = 1;
                ctx.beginPath(); ctx.moveTo(0, 460); ctx.lineTo(300, 140); ctx.moveTo(700, 460); ctx.lineTo(400, 140); ctx.stroke();

                // 2. 스트라이크 존 & 보더라인 가이드 시각화
                ctx.strokeStyle = "rgba(255, 255, 255, 0.15)"; ctx.lineWidth = 2;
                ctx.strokeRect(265, 215, 170, 170); // 바깥 노란색 보더라인 매핑존
                
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3;
                ctx.strokeRect(280, 230, 140, 140); // 리얼 스트라이크 존 정면라인

                // 3. 드래그 타겟 조준점 렌더링
                if (isDragging) {{
                    ctx.strokeStyle = "#00f5d4"; ctx.lineWidth = 1;
                    ctx.beginPath(); ctx.arc(dragTarget.x, dragTarget.y, 8, 0, Math.PI*2); ctx.stroke();
                }}

                // 4. 공의 3D 비행 및 물리 감속 메커니즘
                if (ball.active && ball.status === "flying") {{
                    // 공이 포수 눈앞으로 올수록 점점 감속비(drag) 적용
                    ball.currentSpeed *= ball.drag;
                    ball.z += ball.currentSpeed;

                    // 변화구 고유 사인파 횡/종 무브먼트 곡선 연출
                    let breakEffect = Math.sin(ball.z * Math.PI) * ball.breakX * 22;

                    ball.x = ball.startX + (ball.tx - ball.startX) * ball.z + breakEffect;
                    ball.y = ball.startY + (ball.ty - ball.startY) * ball.z;

                    // 포수 시점 원근법: Z축이 커질수록 공의 크기가 커짐
                    let ballRadius = 2 + (ball.z * 16);
                    
                    ctx.fillStyle = pitchesData[selectedPitch]?.color || "#ffffff";
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2); ctx.fill();

                    // 미트 안착 시점
                    if (ball.z >= 1.0) evaluateZone();
                }}

                // 판정 텍스트 오버레이
                if (umpSignal.frame > 0) {{
                    ctx.fillStyle = umpSignal.color; ctx.font = "bold 42px sans-serif"; ctx.fillText(umpSignal.text, 260, 120); umpSignal.frame--;
                }}
                if (absSignal.frame > 0) {{
                    ctx.fillStyle = "rgba(2, 12, 27, 0.95)"; ctx.fillRect(10, 10, 460, 30);
                    ctx.fillStyle = "#06d6a0"; ctx.font = "bold 12px sans-serif"; ctx.fillText(absSignal.text, 20, 30); absSignal.frame--;
                }}

                requestAnimationFrame(drawScene);
            }}

            drawScene();
        </script>
        """
        st.components.v1.html(html_part + js_part, height=580)
