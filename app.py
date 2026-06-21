import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB PERFECT SLUGGER", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox { background: #1c2541 !important; color: #f8fafc !important; border-radius: 8px; border: 2px solid #3b82f6 !important; }
        label { color: #cbd5e1 !important; font-weight: 700; }
        .stButton>button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: white !important; font-weight: bold; border-radius: 6px !important; width: 100%;
        }
        .tactical-btn>button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # MLB 30개 전 구단 고증 데이터 (구속 단위: MPH)
    mlb_30_teams = {
        "LA Dodgers (로스앤젤레스 다저스)": {"pitcher": "오타니 쇼헤이", "speed": 99, "pitches": ["포심 직구", "스위퍼", "커브"], "lineup": [{"name": "오타니 쇼헤이", "power": 99}, {"name": "무키 베츠", "power": 85}, {"name": "프레디 프리먼", "power": 88}]},
        "NY Yankees (뉴욕 양키스)": {"pitcher": "게릿 콜", "speed": 97, "pitches": ["포심 직구", "너클 커브", "슬라이더"], "lineup": [{"name": "애런 저지", "power": 100}, {"name": "후안 소토", "power": 94}, {"name": "지안카를로 스탠튼", "power": 92}]},
        "SD Padres (샌디에이고 파드리스)": {"pitcher": "딜런 시즈", "speed": 96, "pitches": ["슬라이더", "포심 직구"], "lineup": [{"name": "페르난도 타티스 Jr.", "power": 92}, {"name": "매니 마차도", "power": 88}, {"name": "김하성", "power": 78}]},
        "SF Giants (샌프란시스코 자이언츠)": {"pitcher": "로건 웹", "speed": 93, "pitches": ["싱커", "체인지업"], "lineup": [{"name": "이정후", "power": 70}, {"name": "맷 채프먼", "power": 84}, {"name": "헬리오트 라모스", "power": 80}]},
        "Philadelphia Phillies (필라델피아 필리스)": {"pitcher": "잭 휠러", "speed": 96, "pitches": ["포심 직구", "스위퍼"], "lineup": [{"name": "브라이스 하퍼", "power": 95}, {"name": "카일 슈와버", "power": 98}, {"name": "트레이 터너", "power": 82}]},
        "Atlanta Braves (애틀랜타 브레이브스)": {"pitcher": "크리스 세일", "speed": 94, "pitches": ["슬라이더", "포심 직구"], "lineup": [{"name": "로날드 아쿠냐 Jr.", "power": 94}, {"name": "오스틴 라일리", "power": 89}, {"name": "마르셀 오즈나", "power": 91}]},
        "Houston Astros (휴스턴 애스트로스)": {"pitcher": "프램버 발데스", "speed": 94, "pitches": ["싱커", "커브"], "lineup": [{"name": "요단 알바레즈", "power": 98}, {"name": "카일 터커", "power": 91}, {"name": "호세 알투베", "power": 80}]},
        "Baltimore Orioles (볼티모어 오리올스)": {"pitcher": "코빈 번스", "speed": 95, "pitches": ["커터", "체인지업"], "lineup": [{"name": "건너 허더슨", "power": 89}, {"name": "애들리 러치맨", "power": 80}, {"name": "앤서니 산탄데르", "power": 88}]},
        "Boston Red Sox (보스턴 레드삭스)": {"pitcher": "루카스 지올리토", "speed": 93, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "라파엘 데버스", "power": 92}, {"name": "재런 두란", "power": 75}, {"name": "타일러 오닐", "power": 85}]},
        "Toronto Blue Jays (토론토 블루제이스)": {"pitcher": "케빈 가우스먼", "speed": 94, "pitches": ["포심 직구", "스플리터"], "lineup": [{"name": "블라디미르 게레로 Jr.", "power": 91}, {"name": "보 비셋", "power": 70}, {"name": "조지 스프링어", "power": 78}]},
        "Cleveland Guardians (클리블랜드 가디언스)": {"pitcher": "태너 바이비", "speed": 94, "pitches": ["포심 직구", "체인지업"], "lineup": [{"name": "호세 라미레즈", "power": 93}, {"name": "조시 네일러", "power": 86}, {"name": "스티븐 관", "power": 65}]},
        "Kansas City Royals (캔자스시티 로열스)": {"pitcher": "콜 레이간스", "speed": 96, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "바비 위트 Jr.", "power": 92}, {"name": "살바도르 페레즈", "power": 84}, {"name": "비니 파스콴티노", "power": 78}]},
        "Detroit Tigers (디트로이트 타이거스)": {"pitcher": "타릭 스쿠발", "speed": 96, "pitches": ["포심 직구", "싱커"], "lineup": [{"name": "라일리 그린", "power": 85}, {"name": "케리 카펜터", "power": 82}, {"name": "콜트 키스", "power": 70}]},
        "Minnesota Twins (미네소타 트윈스)": {"pitcher": "파블로 로페즈", "speed": 94, "pitches": ["포심 직구", "스위퍼"], "lineup": [{"name": "바이런 벅스턴", "power": 88}, {"name": "로이스 루이스", "power": 90}, {"name": "카를로스 코레아", "power": 80}]},
        "Chicago White Sox (시카고 화이트삭스)": {"pitcher": "가렛 크로셰", "speed": 97, "pitches": ["포심 직구", "커터"], "lineup": [{"name": "루이스 로베르트 Jr.", "power": 83}, {"name": "앤드류 본", "power": 75}, {"name": "개빈 시트", "power": 68}]},
        "Seattle Mariners (시애틀 매리너스)": {"pitcher": "루이스 카스티요", "speed": 95, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "훌리오 로드리게스", "power": 86}, {"name": "칼 라일리", "power": 87}, {"name": "랜디 아로자레나", "power": 82}]},
        "Texas Rangers (텍사스 레인저스)": {"pitcher": "제이콥 디그롬", "speed": 98, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "코리 시거", "power": 91}, {"name": "아돌리스 가르시아", "power": 85}, {"name": "마커스 시미언", "power": 80}]},
        "LA Angels (로스앤젤레스 에인절스)": {"pitcher": "타일러 앤더슨", "speed": 90, "pitches": ["체인지업", "커터"], "lineup": [{"name": "마이크 트라웃", "power": 94}, {"name": "로건 오호피", "power": 78}, {"name": "테일러 워드", "power": 81}]},
        "Oakland Athletics (오클랜드 애슬레틱스)": {"pitcher": "JP 시어스", "speed": 92, "pitches": ["포심 직구", "스위퍼"], "lineup": [{"name": "브렌트 루커", "power": 94}, {"name": "로렌스 버틀러", "power": 82}, {"name": "셰이 랭겔리어스", "power": 80}]},
        "NY Mets (뉴욕 메츠)": {"pitcher": "센가 코다이", "speed": 96, "pitches": ["포심 직구", "포크볼"], "lineup": [{"name": "프란시스코 린도어", "power": 88}, {"name": "피트 알론소", "power": 96}, {"name": "브랜든 니모", "power": 78}]},
        "Washington Nationals (워싱턴 내셔널스)": {"pitcher": "맥켄지 고어", "speed": 95, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "CJ 에이브람스", "power": 75}, {"name": "제임스 우드", "power": 81}, {"name": "딜런 크루즈", "power": 72}]},
        "Miami Marlins (마이애미 말린스)": {"pitcher": "샌디 알칸타라", "speed": 98, "pitches": ["싱커", "체인지업"], "lineup": [{"name": "제이크 버거", "power": 85}, {"name": "헤수스 산체스", "power": 78}, {"name": "자비에 에드워즈", "power": 55}]},
        "Milwaukee Brewers (밀워키 브루어스)": {"pitcher": "프레디 페랄타", "speed": 94, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "윌리 아다메스", "power": 88}, {"name": "윌리엄 콘트레라스", "power": 82}, {"name": "잭슨 چو리오", "power": 80}]},
        "St. Louis Cardinals (세인트루이스 카디널스)": {"pitcher": "소니 그레이", "speed": 93, "pitches": ["스위퍼", "커브"], "lineup": [{"name": "놀란 아레나도", "power": 80}, {"name": "폴 골드슈미트", "power": 82}, {"name": "윌슨 콘트레라스", "power": 81}]},
        "Chicago Cubs (시카고 컵스)": {"pitcher": "이마나가 쇼타", "speed": 92, "pitches": ["포심 직구", "스플리터"], "lineup": [{"name": "코디 벨린저", "power": 80}, {"name": "스즈키 세이야", "power": 84}, {"name": "이안 햅", "power": 80}]},
        "Cincinnati Reds (신시내티 레즈)": {"pitcher": "헌터 그린", "speed": 99, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "엘리 데 라 크루즈", "power": 90}, {"name": "스펜서 스티어", "power": 78}, {"name": "조나단 인디아", "power": 72}]},
        "Pittsburgh Pirates (피츠버그 파이리츠)": {"pitcher": "폴 스킨스", "speed": 100, "pitches": ["싱커", "슬라이더"], "lineup": [{"name": "오닐 크루즈", "power": 88}, {"name": "브라이언 레이놀즈", "power": 84}, {"name": "키브라이언 헤이즈", "power": 65}]},
        "Arizona Diamondbacks (애리조나 다이아몬드백스)": {"pitcher": "잭 갤런", "speed": 94, "pitches": ["포심 직구", "너클 커브"], "lineup": [{"name": "케텔 마르테", "power": 90}, {"name": "크리스찬 워커", "power": 88}, {"name": "코빈 캐롤", "power": 75}]},
        "Colorado Rockies (콜로라도 로키스)": {"pitcher": "카일 프리랜드", "speed": 91, "pitches": ["슬라이더", "체인지업"], "lineup": [{"name": "에제키엘 토바", "power": 76}, {"name": "브렌턴 도일", "power": 78}, {"name": "라이언 맥맨", "power": 77}]},
        "Tampa Bay Rays (탬파베이 레이스)": {"pitcher": "셰인 바즈", "speed": 96, "pitches": ["포심 직구", "슬라이더"], "lineup": [{"name": "얀디 디아즈", "power": 72}, {"name": "브랜든 로우", "power": 82}, {"name": "크리스토퍼 모렐", "power": 84}]}
    }

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 900;">⚾ MLB 리얼 타격 매니저 (낮은 포수 뷰)</h1>
                <p style="color: #94a3b8; margin-top: 5px;">실제 구속(MPH), 구종 무빙 고증 완료! 자동 투구를 타이밍 맞춰 타격하세요.</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            team_player = st.selectbox("🏃 내 타자 팀 선택", list(mlb_30_teams.keys()), index=0)
        with c2:
            team_ai = st.selectbox("🤖 AI 투수 팀 선택", list(mlb_30_teams.keys()), index=1)
            
        if st.button("🏟️ 경기 시작 (타석 입장)"):
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

    # 경기 관리 및 작전 레이아웃
    col_ctrl, col_canvas = st.columns([1, 3])
    
    with col_ctrl:
        st.markdown("### 📝 작전 및 교대실")
        
        # 주자 여부는 JS에서 전광판 제어하므로 세션 간소화용 가이드 버튼 제공
        st.markdown('<div class="tactical-btn">', unsafe_allow_html=True)
        if st.button("🏃 기습 도루 지시 (주자 있을 시)"):
            st.toast("도루 예약 완료! 다음 투구 때 주자가 달립니다.")
            st.session_state.action_cmd = "steal"
        if st.button("📐 번트 자세 잡기"):
            st.toast("번트 자세 장착! 다음 클릭 시 번트를 시도합니다.")
            st.session_state.action_cmd = "bunt"
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("🔄 **대타 요원 교체**")
        sub_bench = ["조지프 (파워: 85)", "마르티네즈 (파워: 92)", "곤잘레스 (파워: 78)"]
        selected_sub = st.selectbox("대타 선택", sub_bench)
        if st.button("🔥 대타 기용"):
            st.success(f"타자가 {selected_sub.split(' ')[0]}(으)로 교체되었습니다!")
            st.session_state.sub_player = selected_sub.split(' ')[0]

    with col_canvas:
        sub_name = st.session_state.get("sub_player", "")
        action_cmd = st.session_state.get("action_cmd", "normal")
        # 작전 수행 후 초기화 리셋 처리용
        st.session_state.action_cmd = "normal"

        game_html = f"""
        <div style="background: #0b1329; padding: 10px; border-radius: 12px; border: 2px solid #1c2541; max-width: 780px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 6px; padding: 10px; margin-bottom: 8px; font-family: monospace; display: flex; justify-content: space-between; color: white;">
                <div>
                    <span style="color: #3a86ff; font-weight: bold;">{st.session_state.player_title}</span> <span id="score-player" style="font-size: 18px; font-weight: 900; color: #3a86ff;">0</span> 
                    <span style="color: #64748b; margin: 0 10px;">VS</span> 
                    <span style="color: #f72585; font-weight: bold;">{st.session_state.ai_title}</span> <span id="score-ai" style="font-size: 18px; font-weight: 900; color: #f72585;">0</span>
                </div>
                <div>
                    <span id="runners-status" style="color: #10b981; font-weight: bold; margin-right: 15px;">주자: 없음</span>
                    <span id="sb-count" style="font-weight: bold; color: #ffb703;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <canvas id="baseballCanvas" width="760" height="380" style="background: #143615; border: 2px solid #3a86ff; display: block; border-radius: 6px; cursor: pointer;"></canvas>
            
            <div style="background: #020c1b; color: #f8fafc; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: 700; margin-top: 6px; border-left: 5px solid #3a86ff;">
                <span id="ticker" style="color: #4cc9f0;">⚾ 투수가 세트포지션에 들어갔습니다. 공이 오면 화면을 클릭해 타격하세요!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('baseballCanvas');
            const ctx = canvas.getContext('2d');

            let ROSTER = {player_lineup_json};
            const PITCHES = {ai_pitches_json};
            const MAX_SPEED_MPH = {st.session_state.ai_speed};
            
            // 대타 시스템 동적 반영
            if ("{sub_name}" !== "") {{
                ROSTER[0] = {{ name: "{sub_name}", power: 90 }};
            }}

            let game = {{ score: 0, aiScore: 0, b: 0, s: 0, o: 0, batterIdx: 0, onBase: false }};
            let ball = {{ active: false, x: 380, y: 180, z: 0, tx: 380, ty: 290, size: 2, speed: 0, pitchName: "" }};
            
            let swingTimer = 0;
            let pitchDelay = 100; 
            let isSwung = false;
            let currentTactics = "{action_cmd}"; // steal, bunt, normal

            canvas.addEventListener('mousedown', () => {{
                if (ball.active && !isSwung) {{
                    isSwung = true;
                    swingTimer = 10;
                    
                    if (currentTactics === "bunt") {{
                        checkBuntHit();
                    }} else {{
                        checkTimingHit();
                    }}
                }}
            }});

            function aiLauncher() {{
                if (!ball.active) {{
                    pitchDelay--;
                    if (pitchDelay <= 0) {{
                        let pIdx = Math.floor(Math.random() * PITCHES.length);
                        ball.pitchName = PITCHES[pIdx];
                        // 고증 속도 배정 (오타니 97~100마일 스케일링)
                        ball.speed = MAX_SPEED_MPH - Math.floor(Math.random() * 4);
                        
                        ball.tx = 340 + Math.random() * 80;
                        ball.ty = 260 + Math.random() * 60;
                        ball.x = 380; ball.y = 180; ball.z = 0; ball.size = 2;
                        isSwung = false;
                        ball.active = true;
                        
                        document.getElementById('ticker').innerHTML = "🔥 {st.session_state.ai_pitcher} 투수, <b>" + ball.pitchName + "</b> 투구했습니다!!";
                    }}
                }}
            }}

            // 타이밍 일치 기반 타격 판정 코어
            function checkTimingHit() {{
                // 도루 처리 선 반영
                if (currentTactics === "steal" && game.onBase) {{
                    if (Math.random() > 0.4) {{
                        document.getElementById('ticker').innerText = "🏃 대성공! 주자가 다음 베이스를 훔쳤습니다!";
                    }} else {{
                        game.o++;
                        game.onBase = false;
                        document.getElementById('ticker').innerText = "🚨 아웃! 포수가 칼송구로 도루를 저지했습니다!";
                    }}
                }}

                // 오직 공이 홈플레이트 타이밍(z축 0.83 ~ 0.95)에 도달했는가로 안타 결정!
                if (ball.z >= 0.83 && ball.z <= 0.96) {{
                    let dice = Math.random() * 100;
                    
                    // 수비수가 막아내는 호수비 확률 시스템 (15% 확률)
                    if (dice < 15) {{
                        game.o++;
                        document.getElementById('ticker').innerHTML = "🧤 <span style='color:#ef4444;'>아웃!</span> 상대 수비수가 몸을 날려 미친 호수비를 보여줍니다!";
                    }} else if (dice > 75) {{
                        let runs = game.onBase ? 2 : 1;
                        game.score += runs;
                        game.onBase = false;
                        document.getElementById('ticker').innerHTML = "💥 <span style='color:#ff007f;'>장외 홈런!!!</span> " + ball.speed + " MPH 강속구를 완벽히 받아쳤습니다!";
                    }} else {{
                        if (game.onBase) game.score++;
                        game.onBase = true;
                        document.getElementById('ticker').innerHTML = "⚾ <span style='color:#4cc9f0;'>안타 성공!</span> 깨끗하게 밀어쳐 외야 앞으로 공을 보냅니다.";
                    }}
                    ball.active = false;
                    settlePlate();
                }} else {{
                    game.s++;
                    document.getElementById('ticker').innerHTML = "❌ <span style='color:#f72585;'>헛스윙!</span> 타이밍이 완전히 빗나갔습니다.";
                    ball.active = false;
                    settlePlate();
                }}
            }}

            // 번트용 전용 판정 함수
            function checkBuntHit() {{
                if (ball.z >= 0.75 && ball.z <= 0.96) {{
                    if (game.onBase) game.score++; // 작전 성공 주자 홈인 또는 진루
                    game.onBase = false;
                    game.o++; // 타자 주자는 아웃
                    document.getElementById('ticker').innerHTML = "📐 <span style='color:#10b981;'>희생번트 성공!</span> 안전하게 주자를 다음 베이스로 보냅니다.";
                }} else {{
                    game.s++;
                    document.getElementById('ticker').innerText = "파울! 번트 타이밍을 놓쳤습니다.";
                }}
                currentTactics = "normal";
                ball.active = false;
                settlePlate();
            }}

            function settlePlate() {{
                pitchDelay = 90; // 투구 리셋 텀
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('ticker').innerText = "🎯 스트라이크 아웃 삼진!!"; }}
                if (game.b >= 4) {{ game.score++; game.s = 0; game.b = 0; game.onBase = true; document.getElementById('ticker').innerText = "🚶 밀어내기 볼넷 출루!"; }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; game.onBase = false;
                    game.aiScore += Math.floor(Math.random() * 2);
                    game.batterIdx = (game.batterIdx + 1) % ROSTER.length;
                    document.getElementById('ticker').innerText = "🔄 공수교대 및 타석 교체 진행!";
                }}
                
                // 전술 초기화
                currentTactics = "normal";
                updateDisplay();
            }}

            function updateDisplay() {{
                document.getElementById('score-player').innerText = game.score;
                document.getElementById('score-ai').innerText = game.aiScore;
                document.getElementById('sb-count').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
                document.getElementById('runners-status').innerText = game.onBase ? "주자: 1, 2루 대기" : "주자: 없음";
            }}

            function drawField() {{
                ctx.clearRect(0, 0, 760, 380);

                // 고정된 낮은 앵글의 내야 패널 그라운드 흙
                ctx.fillStyle = "#a26a42"; ctx.beginPath();
                ctx.moveTo(0, 380); ctx.lineTo(760, 380); ctx.lineTo(430, 180); ctx.lineTo(330, 180);
                ctx.closePath(); ctx.fill();

                // 가라앉은 스트라이크 가이드라인 박스 (낮은 눈높이 매칭)
                ctx.strokeStyle = "rgba(255, 255, 255, 0.35)"; ctx.lineWidth = 3;
                ctx.strokeRect(320, 240, 120, 90);

                // 마운드 위 투수 (정확히 고정되어 부르르 떨리지 않음)
                ctx.fillStyle = "#60a5fa";
                ctx.beginPath(); ctx.arc(380, 165, 6, 0, Math.PI*2); ctx.fill();
                ctx.fillRect(376, 171, 8, 12);

                // 타석 좌측에 서서 대기하는 타자 실루엣
                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.arc(490, 280, 11, 0, Math.PI*2); ctx.fill();
                ctx.fillRect(482, 291, 16, 32);

                // ⚾ 구종별 고증 실제 무빙 궤적 엔진
                if (ball.active) {{
                    ball.z += 0.026 + (ball.speed / 100) * 0.008;

                    ball.x = 380 + (ball.tx - 380) * ball.z;
                    ball.y = 175 + (ball.ty - 175) * ball.z;
                    ball.size = 2 + (Math.pow(ball.z, 3.8) * 32);

                    // 1. 포심 직구: 휘지 않고 중앙 레이저 송구
                    // 2. 슬라이더/스위퍼: 옆으로 꺾임
                    if (ball.pitchName === "슬라이더" || ball.pitchName === "스위퍼") {{
                        ball.x += Math.sin(ball.z * Math.PI) * 45;
                    }}
                    // 3. 커브: 종으로 뚝 떨어짐
                    if (ball.pitchName === "커브") {{
                        ball.y += Math.sin(ball.z * Math.PI) * 40;
                    }}

                    // 야구공 드로잉
                    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    // 포수 미트 도달 시 루킹 판정
                    if (ball.z >= 1.0) {{
                        ball.active = false;
                        let inZone = (ball.tx >= 320 && ball.tx <= 440 && ball.ty >= 240 && ball.ty <= 330);
                        if (inZone) {{ game.s++; document.getElementById('ticker').innerText = "⚠️ 루킹 스트라이크!"; }}
                        else {{ game.b++; document.getElementById('ticker').innerText = "✋ 볼을 잘 골라냈습니다."; }}
                        settlePlate();
                    }}
                }}

                // 배트 스윙 타격 이펙트 애니메이션
                if (swingTimer > 0) {{
                    ctx.save();
                    let ratio = (swingTimer / 10) * Math.PI;
                    ctx.translate(460, 300);
                    ctx.rotate(-ratio + Math.PI/3);
                    ctx.strokeStyle = "#ff007f"; ctx.lineWidth = 9; ctx.lineCap = "round";
                    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-75, -25); ctx.stroke();
                    ctx.restore();
                    swingTimer--;
                }} else {{
                    // 기본 타격 대기 자세
                    ctx.strokeStyle = "#ffb703"; ctx.lineWidth = 4;
                    ctx.beginPath(); ctx.moveTo(485, 290); ctx.lineTo(465, 255); ctx.stroke();
                }}

                aiLauncher();

                ctx.fillStyle = "#ffffff"; ctx.font = "bold 13px sans-serif";
                ctx.fillText("현재 타자: " + ROSTER[game.batterIdx].name + " (파워: " + ROSTER[game.batterIdx].power + ")", 20, 365);

                requestAnimationFrame(drawField);
            }}

            updateDisplay();
            drawField();
        </script>
        """
        st.components.v1.html(game_html, height=520)

    st.markdown("---")
    if st.button("🏟️ 다른 구단 라인업 보러 나가기 (리셋)"):
        st.session_state.game_active = False
        st.session_state.pop("sub_player", None)
        st.rerun()

if __name__ == "__main__":
    main()
