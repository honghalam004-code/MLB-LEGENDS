import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB MATRIX v4 - CATCHER CORE FIX", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 8종 고유 변화구 물리 데이터베이스
    pitcher_db = {
        "폴 스킨스 (PIT)": {
            "pitches": {
                "파워 포심": {"color": "#e63946", "speed_start": 0.038, "drag_coeff": 1.0, "break_x": 0.0},
                "101마일 스플린커": {"color": "#f72585", "speed_start": 0.035, "drag_coeff": 0.93, "break_x": -1.8},
                "명품 슬라이더": {"color": "#3a86ff", "speed_start": 0.030, "drag_coeff": 0.89, "break_x": 3.2},
                "너클 커브": {"color": "#ffb703", "speed_start": 0.024, "drag_coeff": 0.84, "break_x": 0.5}
            }
        },
        "오타니 쇼헤이 (LAD)": {
            "pitches": {
                "파워 포심": {"color": "#e63946", "speed_start": 0.038, "drag_coeff": 1.0, "break_x": 0.0},
                "명품 스위퍼": {"color": "#00f5d4", "speed_start": 0.029, "drag_coeff": 0.86, "break_x": -4.5},
                "스플리터": {"color": "#7209b7", "speed_start": 0.033, "drag_coeff": 0.91, "break_x": 0.0},
                "고속 커터": {"color": "#9b5de5", "speed_start": 0.035, "drag_coeff": 0.97, "break_x": 1.2}
            }
        }
    }

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 25px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 600px; margin: 40px auto;">
                <h2 style="color: #ffffff; margin: 0; font-weight: 900;">⚾ MLB MATRIX v4 - CATCHER FIX</h2>
                <p style="color: #06d6a0; margin-top: 10px; font-size: 14px;">인라인 버튼 구조 전환으로 무브먼트 통신 오류 완전 해결</p>
            </div>
        """, unsafe_allow_html=True)
        
        selected_p = st.selectbox("🔥 투수 선택", list(pitcher_db.keys()))
        if st.button("🏟️ 포수 시점 캔버스 가동"):
            st.session_state.pitcher_name = selected_p
            st.session_state.pitcher_data = pitcher_db[selected_p]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    # 안전하게 100% HTML5 내부 통합 구조로 렌더링
    html_part = f"""
    <div id="matrix-container" style="background: #0b1329; padding: 15px; border-radius: 14px; max-width: 850px; margin: 0 auto; font-family: sans-serif;">
        
        <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 12px; margin-bottom: 10px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: #4cc9f0; font-weight: bold; font-size: 16px;">🔥 투수: {st.session_state.pitcher_name}</span>
                <span style="margin-left: 20px; font-size: 14px; color: #ff4757;">🔋 체력: <span id="stamina-val">100</span>%</span>
            </div>
            <div><span id="count-board" style="font-weight: bold; color: #ffb703; font-size: 16px;">B: 0 | S: 0 | O: 0</span></div>
        </div>

        <div style="display: flex; gap: 15px;">
            <canvas id="catcherCanvas" width="640" height="460" style="background: #1e272e; border: 3px solid #1c2541; display: block; border-radius: 8px; cursor: crosshair;"></canvas>
            
            <div style="flex: 1; display: flex; flex-direction: column; gap: 8px; background: #1c2541; padding: 12px; border-radius: 8px; height: 460px; box-sizing: border-box;">
                <h4 style="color: #fff; margin: 0 0 5px 0; font-size: 14px;">🎯 구종 선택</h4>
                <div id="pitch-buttons-zone" style="display: flex; flex-direction: column; gap: 8px;"></div>
                <div style="margin-top: auto; background: #020c1b; padding: 8px; border-radius: 6px; font-size: 11px; color: #a4b1cd; line-height: 1.4;">
                    <strong>💡 조작법:</strong><br>
                    구종 클릭 후, 스트라이크 존(흰색 칸) 근처를 <strong>마우스로 드래그 앤 드롭</strong>하여 조준 후 놓으세요!
                </div>
            </div>
        </div>

        <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 10px; border-left: 5px solid #06d6a0; min-height: 48px; font-size:13px; box-sizing: border-box;">
            <span id="commentary" style="color: #90e0ef;">🎙️ 시스템 교정 완료. 구종을 선택하고 드래그해 보세요!</span>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('catcherCanvas');
        const ctx = canvas.getContext('2d');

        let stamina = 100;
        let game = {{ b: 0, s: 0, o: 0 }};
        const pitchesData = {json.dumps(st.session_state.pitcher_data['pitches'], ensure_ascii=False)};
        let selectedPitch = Object.keys(pitchesData)[0];

        // UI 버튼 동적 생성 (통신 오류 원천 차단)
        const btnZone = document.getElementById('pitch-buttons-zone');
        Object.keys(pitchesData).forEach((pName, idx) => {{
            const btn = document.createElement('button');
            btn.innerText = pName;
            btn.style.width = '100%';
            btn.style.padding = '10px';
            btn.style.borderRadius = '6px';
            btn.style.border = '1px solid #3a86ff';
            btn.style.fontWeight = 'bold';
            btn.style.cursor = 'pointer';
            btn.style.fontSize = '12px';
            btn.style.backgroundColor = idx === 0 ? '#e63946' : '#0b1329';
            btn.style.color = '#ffffff';
            btn.className = 'pitch-btn';
            
            btn.onclick = () => {{
                selectedPitch = pName;
                document.querySelectorAll('.pitch-btn').forEach(b => b.style.backgroundColor = '#0b1329');
                btn.style.backgroundColor = '#e63946';
            }};
            btnZone.appendChild(btn);
        }});

        let isDragging = false;
        let dragTarget = {{ x: 320, y: 300 }};
        let ball = {{ active: false, status: "ready", x: 320, y: 160, z: 0, startX: 320, startY: 160, tx: 320, ty: 300, currentSpeed: 0, breakX: 0, drag: 1.0 }};
        
        let umpSignal = {{ text: "", frame: 0, color: "#fff" }};
        let absSignal = {{ text: "", frame: 0 }};

        // 스크롤 및 프레임 위치 보정된 정확한 마우스 좌표 계산식
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

            ball.startX = 320; ball.startY = 140; // 원거리 마운드 중심
            ball.x = 320; ball.y = 140;
            ball.tx = dragTarget.x + errX; ball.ty = dragTarget.y + errY;
            ball.z = 0;
            ball.currentSpeed = pData.speed_start;
            ball.drag = pData.drag_coeff;
            ball.breakX = pData.break_x;
            ball.active = true;
            ball.status = "flying";

            stamina = Math.max(0, stamina - 1);
            document.getElementById('stamina-val').innerText = stamina;
            document.getElementById('commentary').innerText = "🎙️ 투구 시작: " + selectedPitch;
        }}

        function evaluateZone() {{
            ball.active = false;
            ball.status = "ready";

            // 640x460 해상도 맞춤 정밀 스트라이크 존 판정선 (중심: 320, 300)
            let insideStrike = (ball.x >= 250 && ball.x <= 390 && ball.y >= 230 && ball.y <= 370);
            let insideBorder = (ball.x >= 235 && ball.x <= 405 && ball.y >= 215 && ball.y <= 385);
            
            let isRealStrike = insideStrike;
            let callStrike = isRealStrike;

            if (!insideStrike && insideBorder) {{
                if (Math.random() < 0.25) callStrike = !callStrike; // 25% 심판 오심 기믹
            }}

            if (callStrike) {{
                game.s++; umpSignal = {{ text: "STRIKE!", color: "#e63946", frame: 45 }};
            }} else {{
                game.b++; umpSignal = {{ text: "BALL", color: "#3a86ff", frame: 45 }};
            }}

            if (callStrike !== isRealStrike) {{
                absSignal = {{ text: "📢 ABS 보정 완료: 심판의 시각 왜곡을 교정했습니다. [실제 판정: " + (isRealStrike?"STRIKE":"BALL") + "]", frame: 65 }};
            }} else {{
                absSignal = {{ text: "📢 ABS 트래킹: 심판 판정 일치", frame: 30 }};
            }}

            if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; }}
            if (game.b >= 4) {{ game.s = 0; game.b = 0; }}
            if (game.o >= 3) {{ game.o = 0; game.s = 0; game.b = 0; }}

            document.getElementById('count-board').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
        }}

        function drawScene() {{
            ctx.clearRect(0, 0, 640, 460);

            // 1. 포수 시점 원근 가이드라인
            ctx.strokeStyle = "rgba(60, 64, 198, 0.4)"; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(0, 460); ctx.lineTo(280, 140); ctx.moveTo(640, 460); ctx.lineTo(360, 140); ctx.stroke();

            // 2. 가상 보더라인 대역 & 흰색 실선 스트라이크 존 드로잉
            ctx.strokeStyle = "rgba(255, 255, 255, 0.12)"; ctx.lineWidth = 2;
            ctx.strokeRect(235, 215, 170, 170);
            
            ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3;
            ctx.strokeRect(250, 230, 140, 140);

            // 3. 조준선 렌더
            if (isDragging) {{
                ctx.strokeStyle = "#00f5d4"; ctx.lineWidth = 1;
                ctx.beginPath(); ctx.arc(dragTarget.x, dragTarget.y, 8, 0, Math.PI*2); ctx.stroke();
            }}

            // 4. 물리 법칙 (감속 공기저항 + 횡 무브먼트 곡선)
            if (ball.active && ball.status === "flying") {{
                ball.currentSpeed *= ball.drag; // 프레임 진행될수록 속도가 감소 (변화구 특성)
                ball.z += ball.currentSpeed;

                let breakEffect = Math.sin(ball.z * Math.PI) * ball.breakX * 22;
                ball.x = ball.startX + (ball.tx - ball.startX) * ball.z + breakEffect;
                ball.y = ball.startY + (ball.ty - ball.startY) * ball.z;

                let ballRadius = 2 + (ball.z * 16); // 3D 다가오는 효과
                
                ctx.fillStyle = pitchesData[selectedPitch]?.color || "#ffffff";
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2); ctx.fill();

                if (ball.z >= 1.0) evaluateZone();
            }}

            // 상단 자막 레이아웃
            if (umpSignal.frame > 0) {{
                ctx.fillStyle = umpSignal.color; ctx.font = "bold 40px sans-serif"; ctx.fillText(umpSignal.text, 240, 110); umpSignal.frame--;
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
    st.components.v1.html(html_part, height=580)

if __name__ == "__main__":
    main()
