import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB FIRST-PERSON BATTER", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox { background: #1c2541 !important; color: #f8fafc !important; border-radius: 8px; border: 2px solid #3b82f6 !important; }
        label { color: #cbd5e1 !important; font-weight: 700 !important; }
        .stButton>button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: white !important; font-weight: 900 !important; padding: 12px 24px !important; 
            border-radius: 8px !important; border: none !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    # 30개 구단 데이터
    mlb_30_teams = {
        "NY Yankees (뉴욕 양키스)": {
            "pitcher": "게릿 콜", "speed": 96, "pitches": ["포심 직구", "너클 커브", "슬라이더"],
            "lineup": [{"name": "애런 저지", "power": 100}, {"name": "후안 소토", "power": 94}]
        },
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitcher": "오타니 쇼헤이", "speed": 97, "pitches": ["포심 직구", "스위퍼", "스플리터"],
            "lineup": [{"name": "오타니 쇼헤이", "power": 99}, {"name": "무키 베츠", "power": 79}]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitcher": "딜런 시즈", "speed": 96, "pitches": ["슬라이더", "포심 직구"],
            "lineup": [{"name": "페르난도 타티스 Jr.", "power": 92}, {"name": "김하성", "power": 75}]
        },
        "SF Giants (샌프란시스코 자이언츠)": {
            "pitcher": "로건 웹", "speed": 92, "pitches": ["체인지업", "싱커"],
            "lineup": [{"name": "이정후", "power": 65}, {"name": "맷 채프먼", "power": 84}]
        }
    }

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 30px; font-weight: 900;">⚾ 1인칭 타자 시점 리얼 배틀</h1>
                <p style="color: #64748b; margin-top: 5px;">AI 투수가 던지는 공을 내 눈으로 직접 보고 갈기세요!</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            team_player = st.selectbox("🏃 나의 타자 팀 선택", list(mlb_30_teams.keys()), index=1)
        with c2:
            team_ai = st.selectbox("🤖 AI 투수 팀 선택", list(mlb_30_teams.keys()), index=0)
            
        if st.button("🏟️ 타석 입장하기"):
            st.session_state.player_title = team_player.split(" (")[0]
            st.session_state.ai_title = team_ai.split(" (")[0]
            st.session_state.ai_pitcher = mlb_30_teams[team_ai]['pitcher']
            st.session_state.ai_pitches = mlb_30_teams[team_ai]['pitches']
            st.session_state.ai_speed = mlb_30_teams[team_ai]['speed']
            st.session_state.player_lineup = mlb_30_teams[team_player]['lineup']
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    player_lineup_json = json.dumps(st.session_state.player_lineup, ensure_ascii=False)
    ai_pitches_json = json.dumps(st.session_state.ai_pitches, ensure_ascii=False)

    st.markdown(f"### 🏟️ {st.session_state.player_title} 타석 (AI 투수: {st.session_state.ai_pitcher})")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("### 🎮 조작법")
        st.warning("⚠️ **필독!**\n\n1. 화면(게임판)을 클릭하면 AI 투수가 와인드업 후 공을 던집니다.\n\n2. 공이 내 눈앞으로 날아와 **스트라이크 존 사각형에 겹치며 커지는 순간** 타이밍을 맞춰 한 번 더 클릭하면 배트를 휘두릅니다!")
        st.info("💡 공이 포수 미트에 꽂히기 직전, 공이 커졌을 때 쳐야 안타가 됩니다!")

    with col2:
        game_html = f"""
        <div style="background: #0b1329; padding: 10px; border-radius: 12px; border: 2px solid #1c2541; max-width: 800px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; display: flex; justify-content: space-between; color: white;">
                <div>
                    <span style="color: #3a86ff; font-weight: bold;">{st.session_state.player_title}</span> <span id="score-player" style="font-size: 18px; font-weight: 900; color: #3a86ff;">0</span> 
                    <span style="color: #64748b; margin: 0 10px;">VS</span> 
                    <span style="color: #f72585; font-weight: bold;">{st.session_state.ai_title}</span> <span id="score-ai" style="font-size: 18px; font-weight: 900; color: #f72585;">0</span>
                </div>
                <div>
                    <span id="sb-count" style="font-weight: bold; color: #ffb703;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="batterCanvas" width="760" height="400" style="background: #132a13; border: 2px solid #3a86ff; display: block; border-radius: 6px; cursor: crosshair;"></canvas>
            
            <div style="background: #020c1b; color: #f8fafc; padding: 15px; border-radius: 6px; font-size: 16px; font-weight: 700; margin-top: 6px; border-left: 5px solid #3a86ff; text-align: left;">
                <span id="ticker" style="color: #4cc9f0;">⚾ 투수가 와인드업 대기 중입니다. 화면을 클릭하면 공을 던집니다!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('batterCanvas');
            const ctx = canvas.getContext('2d');

            const ROSTER = {player_lineup_json};
            const PITCHES = {ai_pitches_json};
            const BASE_SPEED = {st.session_state.ai_speed};

            let game = {{ score: 0, aiScore: 0, b: 0, s: 0, o: 0, batterIdx: 0 }};
            let ball = {{ active: false, x: 380, y: 150, z: 0, tx: 380, ty: 250, size: 2, speed: 0, pitchName: "" }};
            let swingTimer = 0;
            let pitcherMotion = 0;
            let isSwung = false;

            canvas.addEventListener('mousedown', () => {{
                // 공이 날아오는 중이면 -> 스윙 시도!
                if (ball.active) {{
                    if (!isSwung) {{
                        isSwung = true;
                        swingTimer = 10; // 배트 애니메이션 프레임 시작
                        checkHit();
                    }}
                    return;
                }}

                // 공이 없는 상태면 -> AI 투수에게 투구 명령 지시
                if (pitcherMotion === 0) {{
                    pitcherMotion = 20; // 투수 모션 작동
                    document.getElementById('ticker').innerText = "🔮 투수 와인드업 개시! 타이밍을 잡으세요...";
                    
                    setTimeout(() => {{
                        let pIdx = Math.floor(Math.random() * PITCHES.length);
                        ball.pitchName = PITCHES[pIdx];
                        ball.speed = BASE_SPEED + Math.floor(Math.random() * 6) - 3;
                        
                        // 스트라이크존 부근 무작위 타겟 설정
                        ball.tx = 340 + Math.random() * 80;
                        ball.ty = 220 + Math.random() * 60;
                        
                        ball.x = 380; ball.y = 150; ball.z = 0; ball.size = 2;
                        isSwung = false;
                        ball.active = true;
                    }}, 400);
                }}
            }});

            function checkHit() {{
                // 타자 1인칭 타이밍 체크 (z가 0.82 ~ 0.95 사이일 때가 배트와 공이 만나는 리얼 타이밍)
                if (ball.z >= 0.81 && ball.z <= 0.96) {{
                    let power = ROSTER[game.batterIdx].power;
                    let rand = Math.random() * 100;
                    
                    // 존 안에 정확히 들어왔는지 여부
                    let inZone = (ball.x >= 320 && ball.x <= 440 && ball.y >= 200 && ball.y <= 280);
                    
                    if (inZone) {{
                        if (rand > 80) {{
                            game.score += 1;
                            document.getElementById('ticker').innerHTML = "<span style='color:#ff007f;'>💥 대형 홈런 브레이크!!</span> 담장을 완전히 넘겨버렸습니다!";
                        }} else {{
                            game.score += 1;
                            document.getElementById('ticker').innerHTML = "<span style='color:#4cc9f0;'>⚾ 안타 쾅!!</span> 수비수 키를 넘기는 시원한 안타!";
                        }}
                    }} else {{
                        document.getElementById('ticker').innerText = "💪 나쁜 공을 억지로 때려 내야 플라이 아웃 되었습니다.";
                        game.o++;
                    }}
                    ball.active = false;
                    resetInning();
                }} else {{
                    game.s++;
                    document.getElementById('ticker').innerHTML = "<span style='color:#f72585;'>헛스윙!!</span> 타이밍이 너무 빠르거나 늦었습니다.";
                    ball.active = false;
                    resetInning();
                }}
            }}

            function resetInning() {{
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('ticker').innerText = "🎯 삼진 아웃! 투수의 결정구에 완패했습니다."; }}
                if (game.b >= 4) {{ game.score++; game.s = 0; game.b = 0; document.getElementById('ticker').innerText = "🚶 밀어내기 볼넷 출루 성공!"; }}
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0;
                    game.aiScore += Math.floor(Math.random() * 2); // AI 점수 시뮬레이션
                    game.batterIdx = (game.batterIdx + 1) % ROSTER.length;
                    document.getElementById('ticker').innerText = "🔄 다음 타자가 타석에 들어섭니다!";
                }}
                updateScoreboard();
            }}

            function updateScoreboard() {{
                document.getElementById('score-player').innerText = game.score;
                document.getElementById('score-ai').innerText = game.aiScore;
                document.getElementById('sb-count').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function draw() {{
                ctx.clearRect(0, 0, 760, 400);

                // 1. 경기장 내야 흙 원근 표현 (타자 시점 1인칭 그라운드)
                ctx.fillStyle = "#a66a38"; ctx.beginPath();
                ctx.moveTo(0, 400); ctx.lineTo(760, 400); ctx.lineTo(430, 150); ctx.lineTo(330, 150);
                ctx.closePath(); ctx.fill();

                // 저 멀리 외야 잔디와 담장 배경
                ctx.fillStyle = "#1e4620"; ctx.fillRect(0, 0, 760, 150);
                ctx.fillStyle = "#0d1b2a"; ctx.fillRect(0, 0, 760, 110); // 펜스 너머 하늘

                // 2. 스트라이크 존 사각형 (내 눈앞 투수패널 박스 고정)
                ctx.strokeStyle = "rgba(255, 255, 255, 0.3)"; ctx.lineWidth = 3;
                ctx.strokeRect(320, 200, 120, 80);

                // 3. 저 멀리 서 있는 AI 투수 그리기 (마운드 시점 원근 축소)
                ctx.save();
                ctx.fillStyle = "#ffffff";
                let tOffset = 0;
                if (pitcherMotion > 0) {{
                    tOffset = Math.sin(pitcherMotion * 0.5) * 5;
                    pitcherMotion--;
                }}
                ctx.beginPath(); ctx.arc(380 + tOffset, 135, 5, 0, Math.PI*2); ctx.fill(); // 머리
                ctx.fillRect(377 + tOffset, 140, 6, 12); // 몸체
                ctx.restore();

                // 4. ⚾ 투수가 던진 공이 내 눈앞으로 다가오는 효과 (z축 가속 애니메이션)
                if (ball.active) {{
                    ball.z += 0.025 + (ball.speed / 120) * 0.012; // 공 구속 속도 가중

                    // 원근 이동 계산 공식
                    ball.x = 380 + (ball.tx - 380) * ball.z;
                    ball.y = 145 + (ball.ty - 145) * ball.z;
                    ball.size = 1.5 + (Math.pow(ball.z, 4.5) * 45); // 눈앞으로 올수록 미친듯이 커짐

                    // 구종별 무빙 커브 궤적 렌더링
                    if (ball.pitchName.includes("슬라이더") || ball.pitchName.includes("스위퍼")) {{
                        ball.x += Math.sin(ball.z * Math.PI) * 40;
                    }} else if (ball.pitchName.includes("커브")) {{
                        ball.y += Math.sin(ball.z * Math.PI) * 35;
                    }}

                    // 야구공 실물 드로잉
                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.5;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    // 포수 미트 뒤로 지나쳐 버린 경우 (루킹 판정)
                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let inZone = (ball.tx >= 320 && ball.tx <= 440 && ball.ty >= 200 && ball.ty <= 280);
                        if (inZone) {{
                            game.s++;
                            document.getElementById('ticker').innerText = "⚠️ 꽉 찬 스트라이크! 공을 그냥 보내버렸습니다.";
                        }} else {{
                            game.b++;
                            document.getElementById('ticker').innerText = "👀 완벽하게 빠진 볼! 참아내기 성공.";
                        }}
                        resetInning();
                    }}
                }}

                // 5. 🏏 타자 1인칭 배트 휘두르기 애니메이션 (클릭 시 아래에서 위로 회전 타격)
                if (swingTimer > 0) {{
                    ctx.save();
                    let angle = (swingTimer / 10) * Math.PI / 2; // 스윙 회전각
                    ctx.translate(500, 380);
                    ctx.rotate(-angle);
                    ctx.strokeStyle = "#ffb703"; ctx.lineWidth = 14; ctx.lineCap = "round";
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-120, -60); ctx.stroke();
                    ctx.restore();
                    swingTimer--;
                }} else {{
                    // 평소 대기할 때 배트 그립 하단 대기 모습
                    ctx.strokeStyle = "#cd853f"; ctx.lineWidth = 12; ctx.lineCap = "round";
                    ctx.beginPath(); ctx.moveTo(560, 400); ctx.lineTo(500, 320); ctx.stroke();
                }}

                ctx.fillStyle = "#ffffff"; ctx.font = "bold 13px sans-serif";
                ctx.fillText("현재 타자: " + ROSTER[game.batterIdx].name + " (파워: " + ROSTER[game.batterIdx].power + ")", 20, 380);

                requestAnimationFrame(draw);
            }}

            updateScoreboard();
            draw();
        </script>
        """
        st.components.v1.html(game_html, height=540)

    st.markdown("---")
    if st.button("🔄 라운지 복귀 및 게임 초기화"):
        st.session_state.game_active = False
        st.rerun()

if __name__ == "__main__":
    main()
