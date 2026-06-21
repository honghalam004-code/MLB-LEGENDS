import streamlit as st
import json

def main():
    # 1. 고대비 다크 테마 & 전광판 야구장 스타일 적용
    st.set_page_config(page_title="MLB STATCAST 30 TEAMS REAL GAME", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox, .stRadio { background: #1e293b !important; color: #f8fafc !important; border-radius: 8px; border: 2px solid #334155 !important; }
        label { color: #94a3b8 !important; font-weight: 800 !important; font-size: 15px !important; }
        .stButton>button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important; font-weight: 900 !important; padding: 14px 28px !important; 
            border-radius: 10px !important; border: none !important; font-size: 16px !important;
            width: 100%; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. [현실 고증] MLB 30개 구단 전체 데이터셋 복원
    mlb_30_teams = {
        "NY Yankees (뉴욕 양키스)": {
            "pitcher": "게릿 콜", "speed": 96, "control": 92, "pitches": ["포심 직구", "너클 커브", "슬라이더"],
            "lineup": [{"name": "후안 소토", "contact": 93, "power": 94}, {"name": "애런 저지", "contact": 89, "power": 100}, {"name": "지안카를로 스탠튼", "contact": 72, "power": 95}]
        },
        "Baltimore Orioles (볼티모어 오리올스)": {
            "pitcher": "코빈 번스", "speed": 95, "control": 90, "pitches": ["커터", "커브", "체인지업"],
            "lineup": [{"name": "건너 허더슨", "contact": 88, "power": 89}, {"name": "애들리 러치맨", "contact": 85, "power": 78}, {"name": "앤서니 산탄데르", "contact": 79, "power": 91}]
        },
        "Boston Red Sox (보스턴 레드삭스)": {
            "pitcher": "루카스 지올리토", "speed": 93, "control": 83, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "라파엘 데버스", "contact": 89, "power": 92}, {"name": "재런 두란", "contact": 86, "power": 71}, {"name": "타일러 오닐", "contact": 76, "power": 87}]
        },
        "Tampa Bay Rays (탬파베이 레이스)": {
            "pitcher": "셰인 바즈", "speed": 96, "control": 85, "pitches": ["포심 직구", "슬라이더", "커브"],
            "lineup": [{"name": "얀디 디아즈", "contact": 90, "power": 68}, {"name": "브랜든 로우", "contact": 78, "power": 81}, {"name": "크리스토퍼 모렐", "contact": 71, "power": 83}]
        },
        "Toronto Blue Jays (토론토 블루제이스)": {
            "pitcher": "케빈 가우스먼", "speed": 94, "control": 89, "pitches": ["포심 직구", "스플리터", "슬라이더"],
            "lineup": [{"name": "블라디미르 게레로 Jr.", "contact": 94, "power": 91}, {"name": "보 비셋", "contact": 81, "power": 65}, {"name": "조지 스프링어", "contact": 77, "power": 74}]
        },
        "Cleveland Guardians (클리블랜드 가디언스)": {
            "pitcher": "태너 바이비", "speed": 94, "control": 87, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "스티븐 관", "contact": 95, "power": 52}, {"name": "호세 라미레즈", "contact": 88, "power": 93}, {"name": "조시 네일러", "contact": 82, "power": 86}]
        },
        "Kansas City Royals (캔자스시티 로열스)": {
            "pitcher": "콜 레이간스", "speed": 96, "control": 86, "pitches": ["포심 직구", "체인지업", "슬라이더"],
            "lineup": [{"name": "바비 위트 Jr.", "contact": 94, "power": 92}, {"name": "살바도르 페레즈", "contact": 80, "power": 84}, {"name": "비니 파스콴티노", "contact": 83, "power": 76}]
        },
        "Detroit Tigers (디트로이트 타이거스)": {
            "pitcher": "타릭 스쿠발", "speed": 96, "control": 94, "pitches": ["포심 직구", "체인지업", "싱커"],
            "lineup": [{"name": "라일리 그린", "contact": 85, "power": 82}, {"name": "콜트 키스", "contact": 78, "power": 64}, {"name": "케리 카펜터", "contact": 81, "power": 80}]
        },
        "Minnesota Twins (미네소타 트윈스)": {
            "pitcher": "파블로 로페즈", "speed": 94, "control": 89, "pitches": ["포심 직구", "체인지업", "스위퍼"],
            "lineup": [{"name": "바이런 벅스턴", "contact": 79, "power": 87}, {"name": "로이스 루이스", "contact": 86, "power": 90}, {"name": "카를로스 코레아", "contact": 84, "power": 75}]
        },
        "Chicago White Sox (시카고 화이트삭스)": {
            "pitcher": "가렛 크로셰", "speed": 97, "control": 88, "pitches": ["포심 직구", "커터", "슬라이더"],
            "lineup": [{"name": "루이스 로베르트 Jr.", "contact": 75, "power": 83}, {"name": "앤드류 본", "contact": 77, "power": 71}, {"name": "개빈 시트", "contact": 73, "power": 65}]
        },
        "Houston Astros (휴스턴 애스트로스)": {
            "pitcher": "프램버 발데스", "speed": 94, "control": 86, "pitches": ["싱커", "커브", "체인지업"],
            "lineup": [{"name": "호세 알투베", "contact": 91, "power": 75}, {"name": "요단 알바레즈", "contact": 93, "power": 98}, {"name": "카일 터커", "contact": 89, "power": 91}]
        },
        "Seattle Mariners (시애틀 매리너스)": {
            "pitcher": "루이스 카스티요", "speed": 95, "control": 88, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "훌리오 로드리게스", "contact": 84, "power": 86}, {"name": "랜디 아로자레나", "contact": 78, "power": 80}, {"name": "칼 라일리", "contact": 72, "power": 87}]
        },
        "Texas Rangers (텍사스 레인저스)": {
            "pitcher": "제이콥 디그롬", "speed": 98, "control": 95, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "코리 시거", "contact": 90, "power": 91}, {"name": "마커스 시미언", "contact": 81, "power": 78}, {"name": "아돌리스 가르시아", "contact": 74, "power": 85}]
        },
        "LA Angels (로스앤젤레스 에인절스)": {
            "pitcher": "타일러 앤더슨", "speed": 90, "control": 87, "pitches": ["체인지업", "커터", "싱커"],
            "lineup": [{"name": "마이크 트라웃", "contact": 85, "power": 94}, {"name": "로건 오호피", "contact": 78, "power": 77}, {"name": "테일러 워드", "contact": 80, "power": 81}]
        },
        "Oakland Athletics (오클랜드 애슬레틱스)": {
            "pitcher": "JP 시어스", "speed": 92, "control": 82, "pitches": ["포심 직구", "스위퍼", "체인지업"],
            "lineup": [{"name": "브렌트 루커", "contact": 83, "power": 94}, {"name": "로렌스 버틀러", "contact": 80, "power": 82}, {"name": "셰이 랭겔리어스", "contact": 72, "power": 85}]
        },
        "Philadelphia Phillies (필라델피아 필리스)": {
            "pitcher": "잭 휠러", "speed": 95, "control": 94, "pitches": ["포심 직구", "싱커", "스위퍼"],
            "lineup": [{"name": "트레이 터너", "contact": 90, "power": 76}, {"name": "브라이스 하퍼", "contact": 89, "power": 95}, {"name": "카일 슈와버", "contact": 72, "power": 98}]
        },
        "Atlanta Braves (애틀랜타 브레이브스)": {
            "pitcher": "크리스 세일", "speed": 94, "control": 91, "pitches": ["슬라이더", "포심 직구", "체인지업"],
            "lineup": [{"name": "로날드 아쿠냐 Jr.", "contact": 91, "power": 94}, {"name": "오스틴 라일리", "contact": 85, "power": 89}, {"name": "마르셀 오즈나", "contact": 84, "power": 93}]
        },
        "NY Mets (뉴욕 메츠)": {
            "pitcher": "센가 코다이", "speed": 96, "control": 82, "pitches": ["포심 직구", "포크볼", "컷패스트볼"],
            "lineup": [{"name": "프란시스코 린도어", "contact": 87, "power": 88}, {"name": "피트 알론소", "contact": 76, "power": 96}, {"name": "브랜든 니모", "contact": 83, "power": 74}]
        },
        "Washington Nationals (워싱턴 내셔널스)": {
            "pitcher": "맥켄지 고어", "speed": 95, "control": 81, "pitches": ["포심 직구", "슬라이더", "커브"],
            "lineup": [{"name": "CJ 에이브람스", "contact": 80, "power": 73}, {"name": "제임스 우드", "contact": 82, "power": 81}, {"name": "딜런 크루즈", "contact": 77, "power": 70}]
        },
        "Miami Marlins (마이애미 말린스)": {
            "pitcher": "샌디 알칸타라", "speed": 98, "control": 91, "pitches": ["싱커", "체인지업", "슬라이더"],
            "lineup": [{"name": "제이크 버거", "contact": 76, "power": 85}, {"name": "헤수스 산체스", "contact": 78, "power": 78}, {"name": "자비에 에드워즈", "contact": 81, "power": 52}]
        },
        "Milwaukee Brewers (밀워키 브루어스)": {
            "pitcher": "프레디 페랄타", "speed": 94, "control": 84, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "윌리 아다메스", "contact": 79, "power": 88}, {"name": "윌리엄 콘트레라스", "contact": 87, "power": 81}, {"name": "잭슨 چو리오", "contact": 83, "power": 79}]
        },
        "St. Louis Cardinals (세인트루이스 카디널스)": {
            "pitcher": "소니 그레이", "speed": 93, "control": 89, "pitches": ["스위퍼", "커브", "포심 직구"],
            "lineup": [{"name": "놀란 아레나도", "contact": 82, "power": 76}, {"name": "폴 골드슈미트", "contact": 80, "power": 79}, {"name": "윌슨 콘트레라스", "contact": 84, "power": 82}]
        },
        "Chicago Cubs (시카고 컵스)": {
            "pitcher": "이마나가 쇼타", "speed": 92, "control": 93, "pitches": ["포심 직구", "스플리터", "커브"],
            "lineup": [{"name": "코디 벨린저", "contact": 83, "power": 78}, {"name": "스즈키 세이야", "contact": 86, "power": 83}, {"name": "이안 햅", "contact": 80, "power": 80}]
        },
        "Cincinnati Reds (신시내티 레즈)": {
            "pitcher": "헌터 Greene (헌터 그린)", "speed": 98, "control": 85, "pitches": ["포심 직구", "슬라이더"],
            "lineup": [{"name": "엘리 데 라 크루즈", "contact": 81, "power": 89}, {"name": "스펜서 스티어", "contact": 80, "power": 78}, {"name": "조나단 인디아", "contact": 83, "power": 66}]
        },
        "Pittsburgh Pirates (피츠버그 파이리츠)": {
            "pitcher": "폴 스킨스", "speed": 99, "control": 92, "pitches": ["싱커", "슬라이더", "스플리터"],
            "lineup": [{"name": "브라이언 레이놀즈", "contact": 86, "power": 82}, {"name": "오닐 크루즈", "contact": 78, "power": 86}, {"name": "키브라이언 헤이즈", "contact": 79, "power": 62}]
        },
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitcher": "오타니 쇼헤이", "speed": 97, "control": 82, "pitches": ["포심 직구", "스위퍼", "스플리터"],
            "lineup": [{"name": "무키 베츠", "contact": 93, "power": 79}, {"name": "프레디 프리먼", "contact": 94, "power": 84}, {"name": "오타니 쇼헤이", "contact": 91, "power": 99}]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitcher": "딜런 시즈", "speed": 96, "control": 83, "pitches": ["슬라이더", "포심 직구", "너클 커브"],
            "lineup": [{"name": "루이스 아라에즈", "contact": 99, "power": 45}, {"name": "페르난도 타티스 Jr.", "contact": 88, "power": 92}, {"name": "매니 마차도", "contact": 85, "power": 88}]
        },
        "Arizona Diamondbacks (애리조나 다이아몬드백스)": {
            "pitcher": "잭 갤런", "speed": 93, "control": 90, "pitches": ["포심 직구", "너클 커브", "체인지업"],
            "lineup": [{"name": "코빈 캐롤", "contact": 82, "power": 70}, {"name": "케텔 마르테", "contact": 90, "power": 90}, {"name": "크리스찬 워커", "contact": 81, "power": 87}]
        },
        "SF Giants (샌프란시스코 자이언츠)": {
            "pitcher": "로건 웹", "speed": 92, "control": 93, "pitches": ["체인지업", "싱커", "슬라이더"],
            "lineup": [{"name": "이정후", "contact": 88, "power": 55}, {"name": "맷 채프먼", "contact": 80, "power": 84}, {"name": "헬리오트 라모스", "contact": 82, "power": 79}]
        },
        "Colorado Rockies (콜로라도 로키스)": {
            "pitcher": "카일 프리랜드", "speed": 90, "control": 84, "pitches": ["슬라이더", "체인지업", "싱커"],
            "lineup": [{"name": "에제키엘 토바", "contact": 83, "power": 74}, {"name": "브렌턴 도일", "contact": 79, "power": 78}, {"name": "라이언 맥맨", "contact": 77, "power": 76}]
        }
    }

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 3. 게임 셋업 로비
    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #111827; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #2563eb; max-width: 900px; margin: 30px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900; letter-spacing:-1px;">⚾ MLB STATCAST 30 TEAMS REAL GAME</h1>
                <p style="color: #94a3b8; font-weight: 600; margin-top: 5px;">30개 구단 전체 활성화 완료 • 이닝 기반 실시간 무한 공수교대 시스템</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            team_away = st.selectbox("🎯 원정 팀 선택 (초 공격/플레이어)", list(mlb_30_teams.keys()), index=25) # 다저스 기본값
        with c2:
            team_home = st.selectbox("🏠 홈 팀 선택 (말 공격/AI)", list(mlb_30_teams.keys()), index=0) # 양키스 기본값
            
        if st.button("🏟️ 스타디움 입장 (공수 교대 매치 개시)"):
            st.session_state.away_title = team_away.split(" (")[0]
            st.session_state.home_title = team_home.split(" (")[0]
            
            # 플레이어 팀 데이터셋 바인딩
            st.session_state.user_pitcher = mlb_30_teams[team_away]['pitcher']
            st.session_state.user_pitches = mlb_30_teams[team_away]['pitches']
            st.session_state.user_speed = mlb_30_teams[team_away]['speed']
            st.session_state.user_lineup = mlb_30_teams[team_away]['lineup']
            
            # AI 팀 데이터셋 바인딩
            st.session_state.ai_pitcher = mlb_30_teams[team_home]['pitcher']
            st.session_state.ai_pitches = mlb_30_teams[team_home]['pitches']
            st.session_state.ai_speed = mlb_30_teams[team_home]['speed']
            st.session_state.ai_lineup = mlb_30_teams[team_home]['lineup']
            
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    # 인게임 캔버스 전송용 데이터 마샬링
    user_lineup_json = json.dumps(st.session_state.user_lineup, ensure_ascii=False)
    ai_lineup_json = json.dumps(st.session_state.ai_lineup, ensure_ascii=False)
    user_pitches_json = json.dumps(st.session_state.user_pitches, ensure_ascii=False)
    ai_pitches_json = json.dumps(st.session_state.ai_pitches, ensure_ascii=False)

    st.markdown(f"### 📡 LIVE STADIUM: {st.session_state.away_title} vs {st.session_state.home_title}")

    col_ctrl1, col_ctrl2 = st.columns([1, 3])
    with col_ctrl1:
        st.markdown("### 🎮 구종 및 작전")
        user_select_pitch = st.selectbox("🔮 내 투수 구종 교체", st.session_state.user_pitches)
        user_style = st.slider("⚖️ 피칭 웨이트 (제구력 vs 최대구속)", 0, 100, 50)
        st.success("🚨 **플레이 가이드**\n* **공격(초):** 공이 날아올 때 캔버스를 타이밍 맞춰 클릭하세요!\n* **수비(말):** 스트라이크 존에 마우스를 대고 클릭하여 공을 던지세요!")
    
    with col_ctrl2:
        game_canvas_html = f"""
        <div style="background: #111827; padding: 15px; border-radius: 12px; border: 2px solid #334155; max-width: 900px; margin: 0 auto;">
            
            <div style="background: #020617; border: 2px solid #1e293b; border-radius: 8px; padding: 12px; margin-bottom: 10px; font-family: monospace;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <table style="color: #ffffff; font-size: 16px; text-align: center; border-collapse: collapse; width: 45%;">
                        <tr style="color: #64748b; font-size: 12px;">
                            <th style="width: 40%; text-align: left;">TEAM</th><th style="width: 15%;">R</th><th style="width: 15%;">H</th><th style="width: 15%;">E</th>
                        </tr>
                        <tr>
                            <td style="text-align: left; font-weight: bold; color: #3b82f6;">{st.session_state.away_title}</td>
                            <td id="sb-r-away" style="font-weight: 900; color: #3b82f6;">0</td><td id="sb-h-away">0</td><td>0</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; font-weight: bold; color: #f43f5e;">{st.session_state.home_title}</td>
                            <td id="sb-r-home" style="font-weight: 900; color: #f43f5e;">0</td><td id="sb-h-home">0</td><td>0</td>
                        </tr>
                    </table>

                    <div style="width: 20%; text-align: center;">
                        <div id="sb-inning" style="color: #38bdf8; font-size: 18px; font-weight: 900; margin-bottom: 5px;">1회 초</div>
                        <div id="sb-turn-badge" style="background: #2563eb; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px; font-weight: bold;">공격 모드</div>
                    </div>

                    <div style="display: flex; width: 30%; justify-content: space-around; align-items: center;">
                        <div style="font-size: 14px; line-height: 1.4; font-weight: bold; text-align: left;">
                            <span style="color: #64748b;">B</span> <span id="b-dots" style="color: #10b981;">○○</span><br>
                            <span style="color: #64748b;">S</span> <span id="s-dots" style="color: #fbbf24;">○○</span><br>
                            <span style="color: #64748b;">O</span> <span id="o-dots" style="color: #ef4444;">○○</span>
                        </div>
                        <canvas id="diamondCanvas" width="70" height="70" style="background: transparent;"></canvas>
                    </div>
                </div>
            </div>

            <canvas id="gameCanvas" width="880" height="420" style="background: #0f172a; border: 1px solid #1e293b; display: block; border-radius: 6px;"></canvas>
            
            <div style="background: #020617; color: #f8fafc; padding: 18px; border-radius: 6px; font-size: 18px; font-weight: 700; margin-top: 8px; border-left: 6px solid #2563eb; text-align: left;">
                <span id="game-ticker" style="color: #38bdf8;">🏟️ 전 경기장 셋업 완료. 플레이어 팀의 1회초 선두타자 타석 진입합니다!</span>
            </div>
        </div>

        <script>
            const cv = document.getElementById('gameCanvas');
            const cx = cv.getContext('2d');
            const dCv = document.getElementById('diamondCanvas');
            const dCx = dCv.getContext('2d');

            // 자바스크립트 스코프 내 데이터 구조화
            const USER_ROSTER = {user_lineup_json};
            const AI_ROSTER = {ai_lineup_json};
            const USER_PITCHES = {user_pitches_json};
            const AI_PITCHES = {ai_pitches_json};
            
            const USER_BASE_SPEED = {st.session_state.user_speed};
            const AI_BASE_SPEED = {st.session_state.ai_speed};

            let match = {{
                inning: 1,
                isTop: true, // true: 초(유저 타격), false: 말(유저 피칭 수비)
                scoreAway: 0, scoreHome: 0,
                hitsAway: 0, hitsHome: 0,
                b: 0, s: 0, o: 0,
                user_idx: 0, ai_idx: 0,
                bases: [false, false, false]
            }};

            let ball = {{ active: false, x: 440, y: 120, tx: 440, ty: 240, time: 0, size: 2, currentSpeed: 0 }};
            let pointer = {{ x: 440, y: 240 }};
            let isActionDone = false;
            let currentPitchName = "";
            let trail = [];

            cv.addEventListener('mousemove', (e) => {{
                const r = cv.getBoundingClientRect();
                pointer.x = (e.clientX - r.left) * (cv.width / r.width);
                pointer.y = (e.clientY - r.top) * (cv.height / r.height);
            }});

            cv.addEventListener('mousedown', () => {{
                if (ball.active) {{
                    if (match.isTop && !isActionDone) {{
                        isActionDone = true;
                        evaluateSwing();
                    }}
                    return;
                }}

                if (match.isTop) {{
                    // AI 투수가 던짐 (플레이어 타격 기회)
                    let pIndex = Math.floor(Math.random() * AI_PITCHES.length);
                    currentPitchName = AI_PITCHES[pIndex];
                    ball.currentSpeed = AI_BASE_SPEED + Math.floor(Math.random() * 5) - 2;
                    ball.tx = 370 + Math.random() * 140;
                    ball.ty = 170 + Math.random() * 140;
                    initBallReady();
                }} else {{
                    // 플레이어 투수가 조준한 커서 위치로 피칭 배달
                    currentPitchName = "{user_select_pitch}";
                    ball.currentSpeed = USER_BASE_SPEED + Math.floor((100 - {user_style})*0.05);
                    ball.tx = pointer.x;
                    ball.ty = pointer.y;
                    initBallReady();
                }}
            }});

            function initBallReady() {{
                ball.x = 440; ball.y = 120;
                ball.time = 0; ball.size = 2;
                trail = []; isActionDone = false;
                ball.active = true;
            }}

            // 플레이어 스윙 타이밍 정밀 판정기
            function evaluateSwing() {{
                const batter = USER_ROSTER[match.user_idx];
                let t = ball.time;
                
                if (t >= 0.83 && t <= 0.95) {{
                    let dice = Math.random() + (batter.power - 70) * 0.01;
                    if (dice > 1.05) {{
                        triggerHit(4, "💥 대형 홈런!! 타자 " + batter.name + "가 중앙 담장을 완전히 넘기는 초대형 홈런을 터트립니다!");
                    }} else if (dice > 0.45) {{
                        triggerHit(1, "⚾ 안타!! 빠른 타구가 야수 정면을 피해 깨끗한 안타로 연결됩니다.");
                    }} else {{
                        triggerHit(2, "🔥 좌중간 뚫었습니다! 주자 질주, 2루타 완성!");
                    }}
                }} else {{
                    match.s++;
                    document.getElementById('game-ticker').innerHTML = "<span style='color:#f59e0b;'>헛스윙!!</span> 배트가 허공을 크게 가릅니다.";
                    updateCounts();
                }}
            }}

            // AI 타격 연산 자동화 루틴
            function evaluateAIAtBat() {{
                const batter = AI_ROSTER[match.ai_idx];
                const inZone = (ball.tx >= 360 && ball.tx <= 520 && ball.ty >= 160 && ball.ty <= 320);
                
                let swingProb = inZone ? 0.68 : 0.22;
                if (Math.random() < swingProb) {{
                    if (Math.random() > 0.38) {{
                        let dice = Math.random();
                        if (dice > 0.88) triggerHit(4, "🚨 AI 홈런 발생!! " + batter.name + "에게 뼈아픈 역전 장타를 허용합니다.");
                        else triggerHit(1, "🏃 안타 허용: 주자 1,2루 위기로 이어집니다.");
                    }} else {{
                        match.s++;
                        document.getElementById('game-ticker').innerText = "🎯 유인구 성공! 배트가 끌려 나오며 스트라이크를 축적합니다.";
                        updateCounts();
                    }}
                }} else {{
                    if (inZone) {{
                        match.s++;
                        document.getElementById('game-ticker').innerText = "👌 스트라이크 콜! 완벽한 경계선 제구였습니다.";
                    }} else {{
                        match.b++;
                        document.getElementById('game-ticker').innerText = "✋ 볼 판정: 까다로운 궤적이었으나 타자가 참아냅니다.";
                    }}
                    updateCounts();
                }}
            }}

            // 야구 베이스 진루 엔진
            function triggerHit(basesCount, msg) {{
                document.getElementById('game-ticker').innerHTML = "<span style='color:#10b981; font-weight:900;'> " + msg + "</span>";
                if (match.isTop) match.hitsAway++; else match.hitsHome++;
                
                let runsScored = 0;
                if (basesCount === 4) {{
                    runsScored = 1 + match.bases.filter(b => b).length;
                    match.bases = [false, false, false];
                }} else {{
                    for (let h = 0; h < basesCount; h++) {{
                        if (match.bases[2]) {{ runsScored++; match.bases[2] = false; }}
                        if (match.bases[1]) {{ match.bases[2] = true; match.bases[1] = false; }}
                        if (match.bases[0]) {{ match.bases[1] = true; match.bases[0] = false; }}
                        if (h === 0) match.bases[0] = true;
                    }}
                }}

                if (match.isTop) match.scoreAway += runsScored; else match.scoreHome += runsScored;
                match.b = 0; match.s = 0;
                updateCounts();
            }}

            // 쓰리아웃 및 공수 스위칭 제어
            function updateCounts() {{
                if (match.s >= 3) {{ match.o++; match.s = 0; match.b = 0; document.getElementById('game-ticker').innerText += " 🎯 K 삼진 아웃!!"; }}
                if (match.b >= 4) {{ triggerHit(1, "🚶 사사구 밀어내기 볼넷 출루!"); }}
                
                if (match.o >= 3) {{
                    match.o = 0; match.s = 0; match.b = 0;
                    match.bases = [false, false, false];
                    
                    if (match.isTop) {{
                        match.isTop = false; 
                        match.user_idx = (match.user_idx + 1) % USER_ROSTER.length;
                        document.getElementById('game-ticker').innerHTML = "🔄 <b>공수교대!</b> 플레이어가 수비(투수)로 전환합니다. 스트라이크 존을 조준하세요!";
                    }} else {{
                        match.isTop = true;
                        match.ai_idx = (match.ai_idx + 1) % AI_ROSTER.length;
                        match.inning++;
                        document.getElementById('game-ticker').innerHTML = "🔄 <b>공수교대! " + match.inning + "회초 공격 시작</b> 타격 준비 완료!";
                    }}
                }}

                document.getElementById('sb-r-away').innerText = match.scoreAway;
                document.getElementById('sb-r-home').innerText = match.scoreHome;
                document.getElementById('sb-h-away').innerText = match.hitsAway;
                document.getElementById('sb-h-home').innerText = match.hitsHome;
                document.getElementById('sb-inning').innerText = match.inning + "회 " + (match.isTop ? "초" : "말");
                document.getElementById('sb-turn-badge').innerText = match.isTop ? "공격 모드 (타자)" : "수비 모드 (투수)";
                
                document.getElementById('b-dots').innerText = "●".repeat(match.b) + "○".repeat(2-match.b);
                document.getElementById('s-dots').innerText = "●".repeat(match.s) + "○".repeat(2-match.s);
                document.getElementById('o-dots').innerText = "●".repeat(match.o) + "○".repeat(2-match.o);
                
                drawDiamond();
            }}

            function drawDiamond() {{
                dCx.clearRect(0,0,70,70);
                const pts = [{{x:50, y:35}}, {{x:35, y:20}}, {{x:20, y:35}}];
                dCx.strokeStyle = "#334155"; dCx.lineWidth = 2;
                dCx.style = "margin:auto;";
                dCx.beginPath(); dCx.moveTo(35, 5); dCx.lineTo(65, 35); dCx.lineTo(35, 65); dCx.lineTo(5, 35); dCx.closePath(); dCx.stroke();
                
                for(let i=0; i<3; i++) {{
                    dCx.fillStyle = match.bases[i] ? "#38bdf8" : "#1e293b";
                    dCx.fillRect(pts[i].x-5, pts[i].y-5, 10, 10);
                    dCx.strokeStyle = "#475569"; dCx.strokeRect(pts[i].x-5, pts[i].y-5, 10, 10);
                }}
            }}

            function drawScene() {{
                cx.clearRect(0, 0, 880, 420);
                
                cx.fillStyle = "#1e293b"; cx.beginPath();
                cx.moveTo(360, 420); cx.lineTo(520, 420); cx.lineTo(470, 120); cx.lineTo(410, 120);
                cx.closePath(); cx.fill();

                cx.strokeStyle = "rgba(255, 255, 255, 0.25)"; cx.lineWidth = 2;
                cx.strokeRect(360, 160, 160, 160);

                if (ball.active) {{
                    let speedStep = 0.026 + (ball.currentSpeed / 100) * 0.015;
                    ball.time += speedStep;

                    let lx = 440 + (ball.tx - 440) * ball.time;
                    let ly = 120 + (ball.ty - 120) * ball.time;
                    ball.size = 2 + (Math.pow(ball.time, 3.5) * 30);

                    let curveOffsetX = 0;
                    if(currentPitchName.includes("슬라이더") || currentPitchName.includes("스위퍼")) {{
                        curveOffsetX = Math.sin(ball.time * Math.PI) * 45;
                    }} else if(currentPitchName.includes("커브")) {{
                        curveOffsetX = Math.sin(ball.time * Math.PI) * 20;
                        ly += Math.sin(ball.time * Math.PI) * 25;
                    }}

                    ball.x = lx + curveOffsetX;
                    ball.y = ly;
                    trail.push({{ x: ball.x, y: ball.y }});

                    cx.beginPath(); cx.strokeStyle = "rgba(56, 189, 248, 0.4)"; cx.lineWidth = 3;
                    for (let i = 0; i < trail.length; i++) {{
                        if (i === 0) cx.moveTo(trail[i].x, trail[i].y); else cx.lineTo(trail[i].x, trail[i].y);
                    }}
                    cx.stroke();

                    cx.fillStyle = "#ffffff"; cx.strokeStyle = "#000000"; cx.lineWidth = 2;
                    cx.beginPath(); cx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); cx.fill(); cx.stroke();

                    if (ball.time >= 1.0) {{
                        ball.active = false;
                        if (!match.isTop) {{
                            evaluateAIAtBat();
                        }} else {{
                            if (!isActionDone) {{
                                const inZone = (ball.tx >= 360 && ball.tx <= 520 && ball.ty >= 160 && ball.ty <= 320);
                                if (inZone) {{ match.s++; document.getElementById('game-ticker').innerText = "⚠️ 지켜봤으나 스트라이크 존 판정!"; }}
                                else {{ match.b++; document.getElementById('game-ticker').innerText = "👀 잘 골라냈습니다, 볼넷 빌드업 볼 판정."; }}
                                updateCounts();
                            }}
                        }}
                    }}
                }}

                if (!match.isTop && !ball.active) {{
                    cx.strokeStyle = "#f43f5e"; cx.lineWidth = 2;
                    cx.beginPath();
                    cx.arc(pointer.x, pointer.y, 18, 0, Math.PI*2);
                    cx.moveTo(pointer.x-25, pointer.y); cx.lineTo(pointer.x+25, pointer.y);
                    cx.moveTo(pointer.x, pointer.y-25); cx.lineTo(pointer.x, pointer.y+25);
                    cx.stroke();
                }}

                cx.fillStyle = "#94a3b8"; cx.font = "bold 13px sans-serif";
                if (match.isTop) {{
                    cx.fillText("현재 타석(플레이어): " + USER_ROSTER[match.user_idx].name + " [파워: " + USER_ROSTER[match.user_idx].power + "]", 20, 395);
                    cx.fillText("상대 투수: {st.session_state.ai_pitcher} (" + ball.currentSpeed + " mph 예측)", 20, 411);
                }} else {{
                    cx.fillText("현재 타석(AI): " + AI_ROSTER[match.ai_idx].name + " [파워: " + AI_ROSTER[match.ai_idx].power + "]", 20, 395);
                    cx.fillText("마우스 에임으로 수비 피칭 제구 타겟팅 가동 중", 20, 411);
                }}

                requestAnimationFrame(drawScene);
            }}

            drawDiamond();
            drawScene();
        </script>
        """
        st.components.v1.html(game_canvas_html, height=620)

    st.markdown("---")
    if st.button("🔄 게임 완전히 리셋하고 매치업 로비로 돌아가기"):
        st.session_state.game_active = False
        st.rerun()

if __name__ == "__main__":
    main()
