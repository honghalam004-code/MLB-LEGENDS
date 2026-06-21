import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB REAL SLUGGER", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox { background: #1c2541 !important; color: #f8fafc !important; border-radius: 8px; border: 2px solid #3b82f6 !important; }
        label { color: #cbd5e1 !important; font-weight: 700; }
        .stButton>button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: white !important; font-weight: 900; padding: 12px 24px !important; border-radius: 8px !important; border: none !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    # MLB 30개 전 구단 완벽 리스트
    mlb_30_teams = {
        "NY Yankees (뉴욕 양키스)": {"pitcher": "게릿 콜", "speed": 96, "pitches": ["포심 직구", "너클 커브", "슬라이더"], "lineup": [{"name": "애런 저지", "power": 100}, {"name": "후안 소토", "power": 94}]},
        "Baltimore Orioles (볼티모어 오리올스)": {"pitcher": "코빈 번스", "speed": 95, "pitches": ["커터", "체인지업"], "lineup": [{"name": "건너 허더슨", "power": 89}, {"name": "애들리 러치맨", "power": 78}]},
        "Boston Red Sox (보스턴 레드삭스)": {"pitcher": "루카스 지올리토", "speed": 93, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "라파엘 데버스", "power": 92}, {"name": "재런 두란", "power": 71}]},
        "Tampa Bay Rays (탬파베이 레이스)": {"pitcher": "셰인 바즈", "speed": 96, "pitches": ["포심 직구", "커브"], "lineup": [{"name": "얀디 디아즈", "power": 68}, {"name": "브랜든 로우", "power": 81}]},
        "Toronto Blue Jays (토론토 블루제이스)": {"pitcher": "케빈 가우스먼", "speed": 94, "pitches": ["포심 직구", "스플리터"], "lineup": [{"name": "블라디미르 게레로 Jr.", "power": 91}, {"name": "보 비셋", "power": 65}]},
        "Cleveland Guardians (클리블랜드 가디언스)": {"pitcher": "태너 바이비", "speed": 94, "pitches": ["포심 직구", "체인지업"], "lineup": [{"name": "호세 라미레즈", "power": 93}, {"name": "조시 네일러", "power": 86}]},
        "Kansas City Royals (캔자스시티 로열스)": {"pitcher": "콜 레이간스", "speed": 96, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "바비 위트 Jr.", "power": 92}, {"name": "살바도르 페레즈", "power": 84}]},
        "Detroit Tigers (디트로이트 타이거스)": {"pitcher": "타릭 스쿠발", "speed": 96, "pitches": ["포심 직구", "싱커"], "lineup": [{"name": "라일리 Greene", "power": 82}, {"name": "케리 카펜터", "power": 80}]},
        "Minnesota Twins (미네소타 트윈스)": {"pitcher": "파블로 로페즈", "speed": 94, "pitches": ["포심 직구", "스위퍼"], "lineup": [{"name": "바이런 벅스턴", "power": 87}, {"name": "로이스 루이스", "power": 90}]},
        "Chicago White Sox (시카고 화이트삭스)": {"pitcher": "가렛 크로셰", "speed": 97, "pitches": ["포심 직구", "커터"], "lineup": [{"name": "루이스 로베르트 Jr.", "power": 83}, {"name": "앤드류 본", "power": 71}]},
        "Houston Astros (휴스턴 애스트로스)": {"pitcher": "프램버 발데스", "speed": 94, "pitches": ["싱커", "커브"], "lineup": [{"name": "요단 알바레즈", "power": 98}, {"name": "카일 터커", "power": 91}]},
        "Seattle Mariners (시애틀 매리너스)": {"pitcher": "루이스 카스티요", "speed": 95, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "훌리오 로드리게스", "power": 86}, {"name": "칼 라일리", "power": 87}]},
        "Texas Rangers (텍사스 레인저스)": {"pitcher": "제이콥 디그롬", "speed": 98, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "코리 시거", "power": 91}, {"name": "아돌리스 가르시아", "power": 85}]},
        "LA Angels (로스앤젤레스 에인절스)": {"pitcher": "타일러 앤더슨", "speed": 90, "pitches": ["체인지업", "커터"], "lineup": [{"name": "마이크 트라웃", "power": 94}, {"name": "테일러 워드", "power": 81}]},
        "Oakland Athletics (오클랜드 애슬레틱스)": {"pitcher": "JP 시어스", "speed": 92, "pitches": ["포심 직구", "스위퍼"], "lineup": [{"name": "브렌트 루커", "power": 94}, {"name": "로렌스 버틀러", "power": 82}]},
        "Philadelphia Phillies (필라델피아 필리스)": {"pitcher": "잭 휠러", "speed": 95, "pitches": ["포심 직구", "스위퍼"], "lineup": [{"name": "브라이스 하퍼", "power": 95}, {"name": "카일 슈와버", "power": 98}]},
        "Atlanta Braves (애틀랜타 브레이브스)": {"pitcher": "크리스 세일", "speed": 94, "pitches": ["슬라이더", "포심 직구"], "lineup": [{"name": "로날드 아쿠냐 Jr.", "power": 94}, {"name": "오스틴 라일리", "power": 89}]},
        "NY Mets (뉴욕 메츠)": {"pitcher": "센가 코다이", "speed": 96, "pitches": ["포심 직구", "포크볼"], "lineup": [{"name": "프란시스코 린도어", "power": 88}, {"name": "피트 알론소", "power": 96}]},
        "Washington Nationals (워싱턴 내셔널스)": {"pitcher": "맥켄지 고어", "speed": 95, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "CJ 에이브람스", "power": 73}, {"name": "제임스 우드", "power": 81}]},
        "Miami Marlins (마이애미 말린스)": {"pitcher": "샌디 알칸타라", "speed": 98, "pitches": ["싱커", "체인지업"], "lineup": [{"name": "제이크 버거", "power": 85}, {"name": "헤수스 산체스", "power": 78}]},
        "Milwaukee Brewers (밀워키 브루어스)": {"pitcher": "프레디 페랄타", "speed": 94, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "윌리 아다메스", "power": 88}, {"name": "윌리엄 콘트레라스", "power": 81}]},
        "St. Louis Cardinals (세인트루이스 카디널스)": {"pitcher": "소니 그레이", "speed": 93, "pitches": ["스위퍼", "커브"], "lineup": [{"name": "놀란 아레나도", "power": 76}, {"name": "폴 골드슈미트", "power": 79}]},
        "Chicago Cubs (시카고 컵스)": {"pitcher": "이마나가 쇼타", "speed": 92, "pitches": ["포심 직구", "스플리터"], "lineup": [{"name": "코디 벨린저", "power": 78}, {"name": "스즈키 세이야", "power": 83}]},
        "Cincinnati Reds (신시내티 레즈)": {"pitcher": "헌터 그린", "speed": 98, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "엘리 데 라 크루즈", "power": 89}, {"name": "스펜서 스티어", "power": 78}]},
        "Pittsburgh Pirates (피츠버그 파이리츠)": {"pitcher": "폴 스킨스", "speed": 99, "pitches": ["싱커", "슬라이더"], "lineup": [{"name": "브라이언 레이놀즈", "power": 82}, {"name": "오닐 크루즈", "power": 86}]},
        "LA Dodgers (로스앤젤레스 다저스)": {"pitcher": "오타니 쇼헤이", "speed": 97, "pitches": ["포심 직구", "스위퍼"], "lineup": [{"name": "오타니 쇼헤이", "power": 99}, {"name": "무키 베츠", "power": 79}]},
        "SD Padres (샌디에이고 파드리스)": {"pitcher": "딜런 시즈", "speed": 96, "pitches": ["슬라이더", "포심 직구"], "lineup": [{"name": "페르난도 타티스 Jr.", "power": 92}, {"name": "매니 마차도", "power": 88}]},
        "Arizona Diamondbacks (애리조나 다이아몬드백스)": {"pitcher": "잭 갤런", "speed": 93, "pitches": ["포심 직구", "너클 커브"], "lineup": [{"name": "케텔 마르테", "power": 90}, {"name": "크리스찬 워커", "power": 87}]},
        "SF Giants (샌프란시스코 자이언츠)": {"pitcher": "로건 웹", "speed": 92, "pitches": ["체인지업", "싱커"], "lineup": [{"name": "이정후", "power": 65}, {"name": "맷 채프먼", "power": 84}]},
        "Colorado Rockies (콜로라도 로키스)": {"pitcher": "카일 프리랜드", "speed": 90, "pitches": ["슬라이더", "체인지업"], "lineup": [{"name": "에제키엘 토바", "power": 74}, {"name": "브렌턴 도일", "power": 78}]}
    }

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 30px; font-weight: 900;">⚾ MLB 포수 시점 리얼 슬러거</h1>
                <p style="color: #64748b; margin-top: 5px;">투수는 가만히 대기하다 자동 투구합니다. 타이밍 맞춰 캔버스를 클릭해 타격하세요!</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            team_player = st.selectbox("🏃 플레이어 타자 팀 선택", list(mlb_30_teams.keys()), index=25)
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

    st.markdown(f"### 🏟️ {st.session_state.player_title} 타석 (상대 투수: {st.session_state.ai_pitcher})")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("### 🎮 규칙 안내")
        st.info("💡 **자동 투구 대기**\n가만히 있으면 AI 투수가 알아서 와인드업 후 공을 던집니다!\n\n**🎯 타격 방법**\n공이 스트라이크 박스를 통과하는 찰나의 순간에 **화면 아무 곳이나 클릭**하면 타자가 배트를 휘두릅니다!")

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

            <canvas id="mainCanvas" width="760" height="400" style="background: #143615; border: 2px solid #3a86ff; display: block; border-radius: 6px;"></canvas>
            
            <div style="background: #020c1b; color: #f8fafc; padding: 15px; border-radius: 6px; font-size: 16px; font-weight: 700; margin-top: 6px; border-left: 5px solid #3a86ff; text-align: left;">
                <span id="ticker" style="color: #4cc9f0;">⚾ 투수가 사인을 교환하고 있습니다. 곧 자동으로 투구합니다!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('mainCanvas');
            const ctx = canvas.getContext('2d');

            const ROSTER = {player_lineup_json};
            const PITCHES = {ai_pitches_json};
            const BASE_SPEED = {st.session_state.ai_speed};

            let game = {{ score: 0, aiScore: 0, b: 0, s: 0, o: 0, batterIdx: 0 }};
            let ball = {{ active: false, x: 380, y: 140, z: 0, tx: 380, ty: 280, size: 2, speed: 0, pitchName: "" }};
            
            let swingTimer = 0;
            let pitcherState = "idle"; // idle, windup, release
            let pitcherTimer = 90; // 자동 투구 간격 타이머 프레임 수
            let isSwung = false;

            // 유저 마우스 클릭 -> 배트 스윙
            canvas.addEventListener('mousedown', () => {{
                if (ball.active && !isSwung) {{
                    isSwung = true;
                    swingTimer = 12; // 배트 궤적 루프 시작
                    checkHit();
                }}
            }});

            // 자동 투구 인공지능 루틴 코어
            function aiAutoPitch() {{
                if (!ball.active && pitcherState === "idle") {{
                    pitcherTimer--;
                    if (pitcherTimer <= 0) {{
                        pitcherState = "windup";
                        document.getElementById('ticker').innerText = "🔮 투수 와인드업 돌입! 집중하세요!";
                        
                        setTimeout(() => {{
                            pitcherState = "release";
                            let pIdx = Math.floor(Math.random() * PITCHES.length);
                            ball.pitchName = PITCHES[pIdx];
                            ball.speed = BASE_SPEED + Math.floor(Math.random() * 5) - 2;
                            
                            // 스트라이크존 내부 및 경계선 흩뿌리기 조준
                            ball.tx = 330 + Math.random() * 100;
                            ball.ty = 240 + Math.random() * 80;
                            
                            ball.x = 380; ball.y = 140; ball.z = 0; ball.size = 2;
                            isSwung = false;
                            ball.active = true;
                        }}, 600); // 윈드업 모션 시간
                    }}
                }}
            }}

            function checkHit() {{
                // 리얼 배트 타격 인정 구간 (z가 포수 홈플레이트 진입 타임라인일 때)
                if (ball.z >= 0.82 && ball.z <= 0.95) {{
                    let rand = Math.random() * 100;
                    let inZone = (ball.x >= 320 && ball.x <= 440 && ball.y >= 220 && ball.y <= 320);
                    
                    if (inZone) {{
                        if (rand > 75) {{
                            game.score += 1 + Math.floor(Math.random()*2);
                            document.getElementById('ticker').innerHTML = "<span style='color:#ff007f;'>💥 홈런!!!</span> 완벽한 배럴 타구로 펜스를 크게 넘겼습니다!";
                        }} else {{
                            game.score += 1;
                            document.getElementById('ticker').innerHTML = "<span style='color:#4cc9f0;'>⚾ 안타 장렬!</span> 깨끗한 라인드라이브 안타!";
                        }}
                    }} else {{
                        document.getElementById('ticker').innerText = "⚠️ 유인구에 속았습니다! 빗맞은 타구가 내야 땅볼 처리됩니다.";
                        game.o++;
                    }}
                    ball.active = false;
                    resetAfterPitch();
                }} else {{
                    game.s++;
                    document.getElementById('ticker').innerHTML = "<span style='color:#f72585;'>헛스윙!!</span> 타이밍이 전혀 맞지 않았습니다.";
                    ball.active = false;
                    resetAfterPitch();
                }}
            }}

            function resetAfterPitch() {{
                pitcherState = "idle";
                pitcherTimer = 100; // 던진 후 리셋 시간 부여
                
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('ticker').innerText = "🎯 삼진 아웃 처리!!"; }}
                if (game.b >= 4) {{ game.score++; game.s = 0; game.b = 0; document.getElementById('ticker').innerText = "🚶 볼넷 출루 성공."; }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0;
                    game.aiScore += Math.floor(Math.random() * 2); 
                    game.batterIdx = (game.batterIdx + 1) % ROSTER.length;
                    document.getElementById('ticker').innerText = "🔄 스리 아웃 체인지! 다음 타자 타석에 진입합니다.";
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

                // 원근감 있는 내야 흙 필드 브러시
                ctx.fillStyle = "#8c562b"; ctx.beginPath();
                ctx.moveTo(0, 400); ctx.lineTo(760, 400); ctx.lineTo(440, 140); ctx.lineTo(320, 140);
                ctx.closePath(); ctx.fill();

                // 스트라이크 박스
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 3;
                ctx.strokeRect(320, 220, 120, 100);

                // 정중앙 마운드 투수 그래픽 (떨림 현상 완전 버그 픽스 완료)
                ctx.save();
                ctx.fillStyle = "#60a5fa";
                let pX = 380;
                let pY = 125;
                if (pitcherState === "windup") {{ pY -= 4; ctx.fillStyle = "#f43f5e"; }} // 윈드업 시 슬쩍 일어나는 비주얼
                ctx.beginPath(); ctx.arc(pX, pY, 7, 0, Math.PI*2); ctx.fill(); // 머리
                ctx.fillRect(pX - 5, pY + 7, 10, 15); // 몸판
                ctx.restore();

                // 우타석 대기 중인 타자 실루엣 그래픽 상시 배치
                ctx.save();
                ctx.fillStyle = "#ffffff";
                let bX = 490, bY = 300;
                ctx.beginPath(); ctx.arc(bX, bY, 12, 0, Math.PI*2); ctx.fill(); // 머리
                ctx.fillRect(bX - 8, bY + 12, 16, 30); // 몸통
                
                // 대기용 고정 배트 렌더
                if (swingTimer === 0) {{
                    ctx.strokeStyle = "#ffb703"; ctx.lineWidth = 5; ctx.lineCap = "round";
                    ctx.beginPath(); ctx.moveTo(bX - 5, bY + 10); ctx.lineTo(bX - 25, bY - 20); ctx.stroke();
                }}
                ctx.restore();

                // ⚾ 실시간 날아오는 야구공 렌더링 루틴
                if (ball.active) {{
                    ball.z += 0.024 + (ball.speed / 120) * 0.013;

                    ball.x = 380 + (ball.tx - 380) * ball.z;
                    ball.y = 135 + (ball.ty - 135) * ball.z;
                    ball.size = 2 + (Math.pow(ball.z, 4) * 35); // 다가올수록 증폭 가속

                    // 구종 궤적 무빙
                    if (ball.pitchName.includes("슬라이더")) ball.x += Math.sin(ball.z * Math.PI) * 45;
                    if (ball.pitchName.includes("커브")) ball.y += Math.sin(ball.z * Math.PI) * 30;

                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.5;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    // 루킹 상황 판정
                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let inZone = (ball.tx >= 320 && ball.tx <= 440 && ball.ty >= 220 && ball.ty <= 320);
                        if (inZone) {{
                            game.s++;
                            document.getElementById('ticker').innerText = "👌 스트라이크 판정! 공을 그냥 지켜봤습니다.";
                        }} else {{
                            game.b++;
                            document.getElementById('ticker').innerText = "✋ 볼! 잘 골라내어 카운트를 늘립니다.";
                        }}
                        resetAfterPitch();
                    }}
                }}

                // 유저 클릭 시 배트 휘두르는 타격 이펙트 애니메이션
                if (swingTimer > 0) {{
                    ctx.save();
                    let swingAngle = (swingTimer / 12) * Math.PI;
                    ctx.translate(450, 320);
                    ctx.rotate(-swingAngle + Math.PI/4);
                    ctx.strokeStyle = "#ff007f"; ctx.lineWidth = 10; ctx.lineCap = "round";
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-80, -30); ctx.stroke();
                    ctx.restore();
                    swingTimer--;
                }}

                aiAutoPitch();

                ctx.fillStyle = "#ffffff"; ctx.font = "bold 13px sans-serif";
                ctx.fillText("현재 타자: " + ROSTER[game.batterIdx].name + " [파워: " + ROSTER[game.batterIdx].power + "]", 20, 385);

                requestAnimationFrame(draw);
            }}

            updateScoreboard();
            draw();
        </script>
        """
        st.components.v1.html(game_html, height=540)

    st.markdown("---")
    if st.button("🔄 구단 선택 메인 로비로 완전 리셋"):
        st.session_state.game_active = False
        st.rerun()

if __name__ == "__main__":
    main()
