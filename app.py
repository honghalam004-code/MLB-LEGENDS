import streamlit as st
import json
import random

def main():
    # -----------------------------------------------------------------
    # 1. 고대비 시인성 극대화 화이트 테마 가이드 스타일
    # -----------------------------------------------------------------
    st.set_page_config(page_title="MLB PERFECT REAL TRACKER", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; color: #0f172a; font-family: -apple-system, sans-serif; }
        .stSelectbox, .stRadio, .stTabs { background: #ffffff !important; color: #0f172a !important; border-radius: 8px; border: 2px solid #cbd5e1 !important; }
        label { color: #1e293b !important; font-weight: 800 !important; font-size: 15px !important; }
        .stButton>button {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
            color: white !important; font-weight: 900 !important; padding: 14px 28px !important; 
            border-radius: 10px !important; border: 1px solid #0f172a !important; font-size: 16px !important;
            width: 100%; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        }
        .mode-box { background: #ffffff; padding: 20px; border-radius: 12px; border: 2px solid #e2e8f0; margin-bottom: 15px; }
        </style>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # 2. 현실 고증 MLB 30개 구단 전체 데이터베이스
    # -----------------------------------------------------------------
    mlb_30_teams = {
        "NY Yankees (뉴욕 양키스)": {
            "pitcher": "게릿 콜", "speed": 99, "control": 92, "pitches": ["포심 직구", "너클 커브", "슬라이더"],
            "lineup": [{"name": "후안 소토", "contact": 93, "power": 94}, {"name": "애런 저지", "contact": 89, "power": 100}, {"name": "지안카를로 스탠튼", "contact": 72, "power": 95}]
        },
        "Baltimore Orioles (볼티모어 오리올스)": {
            "pitcher": "코빈 번스", "speed": 98, "control": 90, "pitches": ["커터", "커브", "체인지업"],
            "lineup": [{"name": "건너 허더슨", "contact": 88, "power": 89}, {"name": "애들리 러치맨", "contact": 85, "power": 78}, {"name": "앤서니 산탄데르", "contact": 79, "power": 91}]
        },
        "Boston Red Sox (보스턴 레드삭스)": {
            "pitcher": "루카스 지올리토", "speed": 94, "control": 83, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "라파엘 데버스", "contact": 89, "power": 92}, {"name": "재런 두란", "contact": 86, "power": 71}, {"name": "타일러 오닐", "contact": 76, "power": 87}]
        },
        "Tampa Bay Rays (탬파베이 레이스)": {
            "pitcher": "셰인 바즈", "speed": 97, "control": 85, "pitches": ["포심 직구", "슬라이더", "커브"],
            "lineup": [{"name": "얀디 디아즈", "contact": 90, "power": 68}, {"name": "브랜든 로우", "contact": 78, "power": 81}, {"name": "크리스토퍼 모렐", "contact": 71, "power": 83}]
        },
        "Toronto Blue Jays (토론토 블루제이스)": {
            "pitcher": "케빈 가우스먼", "speed": 96, "control": 89, "pitches": ["포심 직구", "스플리터", "슬라이더"],
            "lineup": [{"name": "블라디미르 게레로 Jr.", "contact": 94, "power": 91}, {"name": "보 비셋", "contact": 81, "power": 65}, {"name": "조지 스프링어", "contact": 77, "power": 74}]
        },
        "Cleveland Guardians (클리블랜드 가디언스)": {
            "pitcher": "태너 바이비", "speed": 95, "control": 87, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "스티븐 관", "contact": 95, "power": 52}, {"name": "호세 라미레즈", "contact": 88, "power": 93}, {"name": "조시 네일러", "contact": 82, "power": 86}]
        },
        "Kansas City Royals (캔자스시티 로열스)": {
            "pitcher": "콜 레이간스", "speed": 98, "control": 86, "pitches": ["포심 직구", "체인지업", "슬라이더"],
            "lineup": [{"name": "바비 위트 Jr.", "contact": 94, "power": 92}, {"name": "살바도르 페레즈", "contact": 80, "power": 84}, {"name": "비니 파스콴티노", "contact": 83, "power": 76}]
        },
        "Detroit Tigers (디트로이트 타이거스)": {
            "pitcher": "타릭 스쿠발", "speed": 99, "control": 94, "pitches": ["포심 직구", "체인지업", "싱커"],
            "lineup": [{"name": "라일리 그린", "contact": 85, "power": 82}, {"name": "콜트 키스", "contact": 78, "power": 64}, {"name": "케리 카펜터", "contact": 81, "power": 80}]
        },
        "Minnesota Twins (미네소타 트윈스)": {
            "pitcher": "파블로 로페즈", "speed": 96, "control": 89, "pitches": ["포심 직구", "체인지업", "스위퍼"],
            "lineup": [{"name": "바이런 벅스턴", "contact": 79, "power": 87}, {"name": "로이스 루이스", "contact": 86, "power": 90}, {"name": "카를로스 코레아", "contact": 84, "power": 75}]
        },
        "Chicago White Sox (시카고 화이트삭스)": {
            "pitcher": "가렛 크로셰", "speed": 100, "control": 88, "pitches": ["포심 직구", "커터", "슬라이더"],
            "lineup": [{"name": "루이스 로베르트 Jr.", "contact": 75, "power": 83}, {"name": "앤드류 본", "contact": 77, "power": 71}, {"name": "개빈 시트", "contact": 73, "power": 65}]
        },
        "Houston Astros (휴스턴 애스트로스)": {
            "pitcher": "프램버 발데스", "speed": 96, "control": 86, "pitches": ["싱커", "커브", "체인지업"],
            "lineup": [{"name": "호세 알투베", "contact": 91, "power": 75}, {"name": "요단 알바레즈", "contact": 93, "power": 98}, {"name": "카일 터커", "contact": 89, "power": 91}]
        },
        "Seattle Mariners (시애틀 매리너스)": {
            "pitcher": "루이스 카스티요", "speed": 97, "control": 88, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "훌리오 로드리게스", "contact": 84, "power": 86}, {"name": "랜디 아로자레나", "contact": 78, "power": 80}, {"name": "칼 라일리", "contact": 72, "power": 87}]
        },
        "Texas Rangers (텍사스 레인저스)": {
            "pitcher": "제이콥 디그롬", "speed": 101, "control": 95, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "코리 시거", "contact": 90, "power": 91}, {"name": "마커스 시미언", "contact": 81, "power": 78}, {"name": "아돌리스 가르시아", "contact": 74, "power": 85}]
        },
        "LA Angels (로스앤젤레스 에인절스)": {
            "pitcher": "타일러 앤더슨", "speed": 91, "control": 87, "pitches": ["체인지업", "커터", "싱커"],
            "lineup": [{"name": "마이크 트라웃", "contact": 85, "power": 94}, {"name": "로건 오호피", "contact": 78, "power": 77}, {"name": "테일러 워드", "contact": 80, "power": 81}]
        },
        "Oakland Athletics (오클랜드 애슬레틱스)": {
            "pitcher": "JP 시어스", "speed": 93, "control": 82, "pitches": ["포심 직구", "스위퍼", "체인지업"],
            "lineup": [{"name": "브렌트 루커", "contact": 83, "power": 94}, {"name": "로렌스 버틀러", "contact": 80, "power": 82}, {"name": "셰이 랭겔리어스", "contact": 72, "power": 85}]
        },
        "Philadelphia Phillies (필라델피아 필리스)": {
            "pitcher": "잭 휠러", "speed": 99, "control": 94, "pitches": ["포심 직구", "싱커", "스위퍼"],
            "lineup": [{"name": "트레이 터너", "contact": 90, "power": 76}, {"name": "브라이스 하퍼", "contact": 89, "power": 95}, {"name": "카일 슈와버", "contact": 72, "power": 98}]
        },
        "Atlanta Braves (애틀랜타 브레이브스)": {
            "pitcher": "크리스 세일", "speed": 96, "control": 91, "pitches": ["슬라이더", "포심 직구", "체인지업"],
            "lineup": [{"name": "로날드 아쿠냐 Jr.", "contact": 91, "power": 94}, {"name": "오스틴 라일리", "contact": 85, "power": 89}, {"name": "마르셀 오즈나", "contact": 84, "power": 93}]
        },
        "NY Mets (뉴욕 메츠)": {
            "pitcher": "센가 코다이", "speed": 98, "control": 82, "pitches": ["포심 직구", "포크볼", "컷패스트볼"],
            "lineup": [{"name": "프란시스코 린도어", "contact": 87, "power": 88}, {"name": "피트 알론소", "contact": 76, "power": 96}, {"name": "브랜든 니모", "contact": 83, "power": 74}]
        },
        "Washington Nationals (워싱턴 내셔널스)": {
            "pitcher": "맥켄지 고어", "speed": 96, "control": 81, "pitches": ["포심 직구", "슬라이더", "커브"],
            "lineup": [{"name": "CJ 에이브람스", "contact": 80, "power": 73}, {"name": "제임스 우드", "contact": 82, "power": 81}, {"name": "딜런 크루즈", "contact": 77, "power": 70}]
        },
        "Miami Marlins (마이애미 말린스)": {
            "pitcher": "샌디 알칸타라", "speed": 99, "control": 91, "pitches": ["싱커", "체인지업", "슬라이더"],
            "lineup": [{"name": "제이크 버거", "contact": 76, "power": 85}, {"name": "헤수스 산체스", "contact": 78, "power": 78}, {"name": "자비에 에드워즈", "contact": 81, "power": 52}]
        },
        "Milwaukee Brewers (밀워키 브루어스)": {
            "pitcher": "프레디 페랄타", "speed": 96, "control": 84, "pitches": ["포심 직구", "슬라이더", "체인지업"],
            "lineup": [{"name": "윌리 아다메스", "contact": 79, "power": 88}, {"name": "윌리엄 콘트레라스", "contact": 87, "power": 81}, {"name": "잭슨 چو리오", "contact": 83, "power": 79}]
        },
        "St. Louis Cardinals (세인트루이스 카디널스)": {
            "pitcher": "소니 그레이", "speed": 94, "control": 89, "pitches": ["스위퍼", "커브", "포심 직구"],
            "lineup": [{"name": "놀란 아레나도", "contact": 82, "power": 76}, {"name": "폴 골드슈미트", "contact": 80, "power": 79}, {"name": "윌슨 콘트레라스", "contact": 84, "power": 82}]
        },
        "Chicago Cubs (시카고 컵스)": {
            "pitcher": "이마나가 쇼타", "speed": 93, "control": 93, "pitches": ["포심 직구", "스플리터", "커브"],
            "lineup": [{"name": "코디 벨린저", "contact": 83, "power": 78}, {"name": "스즈키 세이야", "contact": 86, "power": 83}, {"name": "이안 햅", "contact": 80, "power": 80}]
        },
        "Cincinnati Reds (신시내티 레즈)": {
            "pitcher": "헌터 그린", "speed": 101, "control": 85, "pitches": ["포심 직구", "슬라이더"],
            "lineup": [{"name": "엘리 데 라 크루즈", "contact": 81, "power": 89}, {"name": "스펜서 스티어", "contact": 80, "power": 78}, {"name": "조나단 인디아", "contact": 83, "power": 66}]
        },
        "Pittsburgh Pirates (피츠버그 파이리츠)": {
            "pitcher": "폴 스킨스", "speed": 102, "control": 92, "pitches": ["싱커", "슬라이더", "스플리터"],
            "lineup": [{"name": "브라이언 레이놀즈", "contact": 86, "power": 82}, {"name": "오닐 크루즈", "contact": 78, "power": 86}, {"name": "키브라이언 헤이즈", "contact": 79, "power": 62}]
        },
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitcher": "오타니 쇼헤이", "speed": 101, "control": 82, "pitches": ["포심 직구", "스위퍼", "스플리터"],
            "lineup": [{"name": "무키 베츠", "contact": 93, "power": 79}, {"name": "프레디 프리먼", "contact": 94, "power": 84}, {"name": "오타니 쇼헤이", "contact": 91, "power": 99}]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitcher": "딜런 시즈", "speed": 99, "control": 83, "pitches": ["슬라이더", "포심 직구", "너클 커브"],
            "lineup": [{"name": "루이스 아라에즈", "contact": 99, "power": 45}, {"name": "페르난도 타티스 Jr.", "contact": 88, "power": 92}, {"name": "매니 마차도", "contact": 85, "power": 88}]
        },
        "Arizona Diamondbacks (애리조나 다이아몬드백스)": {
            "pitcher": "잭 갤런", "speed": 95, "control": 90, "pitches": ["포심 직구", "너클 커브", "체인지업"],
            "lineup": [{"name": "코빈 캐롤", "contact": 82, "power": 70}, {"name": "케텔 마르테", "contact": 90, "power": 90}, {"name": "크리스찬 워커", "contact": 81, "power": 87}]
        },
        "SF Giants (샌프란시스코 자이언츠)": {
            "pitcher": "로건 웹", "speed": 94, "control": 93, "pitches": ["체인지업", "싱커", "슬라이더"],
            "lineup": [{"name": "이정후", "contact": 88, "power": 55}, {"name": "맷 채프먼", "contact": 80, "power": 84}, {"name": "헬리오트 라모스", "contact": 82, "power": 79}]
        },
        "Colorado Rockies (콜로라도 로키스)": {
            "pitcher": "카일 프리랜드", "speed": 91, "control": 84, "pitches": ["슬라이더", "체인지업", "싱커"],
            "lineup": [{"name": "에제키엘 토바", "contact": 83, "power": 74}, {"name": "브렌턴 도일", "contact": 79, "power": 78}, {"name": "라이언 맥맨", "contact": 77, "power": 76}]
        }
    }

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # -----------------------------------------------------------------
    # 3. 경기 매치업 선택 대기실
    # -----------------------------------------------------------------
    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #ffffff; padding: 30px; border-radius: 15px; text-align: center; border: 3px solid #0f172a; max-width: 900px; margin: 30px auto;">
                <h1 style="color: #0f172a; margin: 0; font-size: 34px; font-weight: 900; letter-spacing:-1px;">⚾ MLB PERFECT REAL TRACKER V3</h1>
                <p style="color: #475569; font-weight: 600; margin-top: 5px;">직구 궤적 수정 완료 • 하단 대형 해설창 탑재 • 30개 전구단 오리지널 엔진</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            team_away = st.selectbox("🎯 AWAY 공격 팀 선택", list(mlb_30_teams.keys()), index=25)
        with c2:
            team_home = st.selectbox("🏠 HOME 수비 팀 선택", list(mlb_30_teams.keys()), index=0)
            
        p_data = mlb_30_teams[team_home]
        
        if st.button("🏟️ 야구장 입장 (포수 시점 활성화)"):
            st.session_state.away_name = team_away.split(" (")[0]
            st.session_state.home_name = team_home.split(" (")[0]
            st.session_state.pitcher_name = p_data['pitcher']
            st.session_state.base_speed = p_data['speed']
            st.session_state.base_control = p_data['control']
            st.session_state.pitch_list = p_data['pitches']
            st.session_state.away_roster = mlb_30_teams[team_away]['lineup']
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    st.markdown(f"### 📡 MATCHUP: {st.session_state.away_name} vs {st.session_state.home_name}")
    tab_p, tab_h = st.tabs(["🎯 투수/포수 1인칭 미트 모드", "💥 플레이어 타격 챌린지 모드"])

    # -----------------------------------------------------------------
    # [TAB 1] 직구 궤적 교정 + 대형 해설창 포수 시점 모드
    # -----------------------------------------------------------------
    with tab_p:
        col_set1, col_set2 = st.columns([1, 2])
        with col_set1:
            sel_pitch_1 = st.radio("🔮 구종 메인 셀렉트", st.session_state.pitch_list, key="p_pitch")
        with col_set2:
            balance_p = st.slider("⚖️ 피칭 스타일 다이내믹 시소 스위치", 0, 100, 50, key="p_balance")

        p_max = st.session_state.base_speed + 5
        p_min = st.session_state.base_speed - 15
        live_speed_p = int(p_max - (balance_p / 100.0) * (p_max - p_min))
        live_control_p = int(5 + (balance_p / 100.0) * 91)

        st.markdown(f"📊 **투구 스펙:** 구속 **{live_speed_p} mph** | 제구력 수치 **{live_control_p} / 100**")

        # 무브먼트 계수 설정
        if "직구" in sel_pitch_1 or "싱커" in sel_pitch_1 or "커터" in sel_pitch_1:
            hb, vb = (0.0, -1.0)
        elif "스위퍼" in sel_pitch_1 or "슬라이더" in sel_pitch_1:
            hb, vb = (17.0, 2.0)
        elif "커브" in sel_pitch_1 or "너클 커브" in sel_pitch_1:
            hb, vb = (4.0, 18.0)
        else:
            hb, vb = (-2.0, 11.0)

        lineup_json_p = json.dumps(st.session_state.away_roster, ensure_ascii=False)

        canvas_html_p = f"""
        <div style="background: #ffffff; padding: 5px; border-radius: 12px; border: 2px solid #0f172a; max-width: 920px; margin: 0 auto;">
            <div style="background: #0f172a; color: #ffffff; padding: 10px 15px; border-radius: 6px; display: flex; justify-content: space-between; font-weight: bold; font-family: monospace; font-size:15px; margin-bottom:8px;">
                <div>[타석] {st.session_state.away_name.upper()} <span id="p-score-away" style="color:#f43f5e; font-weight:900;">0</span></div>
                <div id="p-bso-text" style="color:#fbbf24; font-size:16px; letter-spacing:1px;">B○○ S○○ O○○</div>
                <div>[수비] {st.session_state.home_name.upper()} <span id="p-score-home" style="color:#3b82f6; font-weight:900;">0</span></div>
            </div>

            <canvas id="canvasPitchMode" width="900" height="480" style="background: #f8fafc; border: 2px solid #0f172a; display: block; margin: 0 auto; cursor: none;"></canvas>
            
            <div style="background: #0f172a; color: #ffffff; padding: 22px; border-radius: 8px; font-size: 20px; font-weight: 800; margin-top: 10px; border-left: 8px solid #3b82f6; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); text-align: left; line-height: 1.5;">
                <span id="p-ticker" style="color: #f8fafc;">⚾ [준비 완료] 마우스를 움직여 포수 미트를 조준하고 클릭하여 공을 받으세요!</span>
            </div>
        </div>

        <script>
            const cv = document.getElementById('canvasPitchMode');
            const cx = cv.getContext('2d');

            const SPEED = {live_speed_p};
            const CONTROL = {live_control_p};
            const HB = {hb};
            const VB = {vb};
            const PITCH_NAME = "{sel_pitch_1}";
            const ROSTER = {lineup_json_p};

            let state = {{ away: 0, home: 0, b: 0, s: 0, o: 0, idx: 0 }};
            let pointer = {{ x: 450, y: 260 }};
            let ball = {{ active: false, x: 450, y: 150, tx: 450, ty: 260, time: 0, size: 2 }};
            
            let trajectory = [];
            let isMisfire = false;
            let noiseX = 0, noiseY = 0;
            let marks = [];

            cv.addEventListener('mousemove', (e) => {{
                const r = cv.getBoundingClientRect();
                pointer.x = (e.clientX - r.left) * (cv.width / r.width);
                pointer.y = (e.clientY - r.top) * (cv.height / r.height);
            }});

            cv.addEventListener('mousedown', () => {{
                if (ball.active) return;

                let risk = (100 - CONTROL) * 0.52;
                isMisfire = Math.random() * 100 < risk;

                if (isMisfire) {{
                    ball.tx = 450 + (Math.random() - 0.5) * 120;
                    ball.ty = 240 + (Math.random() - 0.5) * 120;
                }} else {{
                    let o_range = (100 - CONTROL) * 0.35;
                    ball.tx = pointer.x + (Math.random() - 0.5) * o_range;
                    ball.ty = pointer.y + (Math.random() - 0.5) * o_range;
                }}

                noiseX = (Math.random() - 0.5) * 5.0;
                noiseY = (Math.random() - 0.5) * 5.0;

                ball.x = 450; ball.y = 150;
                ball.time = 0; ball.size = 2;
                trajectory = [];
                ball.active = true;
            }});

            function setTicker(m) {{
                document.getElementById('p-ticker').innerHTML = m;
            }}

            function evaluateAtBat() {{
                const b_stat = ROSTER[state.idx];
                const strikeZone = (ball.tx >= 330 && ball.tx <= 570 && ball.ty >= 130 && ball.ty <= 370);
                
                let swingChance = strikeZone ? 0.72 : 0.25;
                if (isMisfire) swingChance = 0.90;

                if (Math.random() < swingChance) {{
                    let contactMiss = 0.34 - (b_stat.contact - 70) * 0.006;
                    if (isMisfire) contactMiss = 0.01;

                    if (Math.random() > contactMiss) {{
                        let pw_coef = (b_stat.power - 70) * 0.009;
                        if (isMisfire) pw_coef += 0.50;
                        const dice = Math.random() + pw_coef;

                        if (dice > 1.15) {{
                            state.away += 1; state.s = 0; state.b = 0;
                            setTicker(`<span style="color:#f43f5e; font-weight:900;">💥 대형 홈런 상황!</span> 타자 ${b_stat.name}가 실투를 완벽한 타이밍에 걷어올려 담장을 넘겼습니다!`);
                        }} else if (dice > 0.45) {{
                            state.s = 0; state.b = 0;
                            setTicker(`<span style="color:#22c55e; font-weight:900;">⚾ 안타 발생:</span> 구종의 회전을 뚫어내고 깨끗한 우전 안타를 생산합니다.`);
                        }} else {{
                            state.o++; state.s = 0; state.b = 0;
                            setTicker(`<span style="color:#e2e8f0;">내야 아웃:</span> 볼끝 회전에 빗맞으며 평범한 플라이 구질로 물러납니다.`);
                        }}
                    }} else {{
                        state.s++; setTicker(`<span style="color:#fbbf24; font-weight:900;">🔥 헛스윙!!</span> 미트 속으로 파고드는 ${PITCH_NAME}의 위력에 방망이가 헛돌았습니다.`);
                    }}
                }} else {{
                    if (strikeZone) {{ state.s++; setTicker(`<span style="color:#3b82f6; font-weight:900;">⚾ 스트라이크!</span> 보더라인 경계면을 자르며 정교하게 꽂힙니다.`); }}
                    else {{ state.b++; setTicker(`<span style="color:#a8a29e;">볼 판정:</span> 타자가 배트를 멈추며 예리하게 참아냈습니다.`); }}
                }}

                if (state.s >= 3) {{ state.o++; state.s = 0; state.b = 0; setTicker(`<span style="color:#ef4444; font-weight:900;">🎯 삼진 아웃!!</span> 완벽하게 꺾이는 결정구로 타자를 제압했습니다.`); }}
                if (state.b >= 4) {{ state.s = 0; state.b = 0; setTicker(`<span style="color:#fbbf24;">볼넷 출루:</span> 제구가 흔들리며 주자를 내보냅니다.`); }}
                if (state.o >= 3) {{ state.o = 0; state.s = 0; state.b = 0; state.idx = (state.idx + 1) % ROSTER.length; setTicker(`🔄 쓰리아웃 공수교대 완료. 다음 이닝으로 전환합니다.`); }}

                document.getElementById('p-score-away').innerText = state.away;
                document.getElementById('p-score-home').innerText = state.home;
                document.getElementById('p-bso-text').innerText = `B${{ "●".repeat(state.b) }} S${{ "●".repeat(state.s) }} O${{ "●".repeat(state.o) }}`;

                marks.push({{ x: ball.tx, y: ball.ty, sz: strikeZone, mis: isMisfire }});
                if (marks.length > 8) marks.shift();
            }}

            function loop() {{
                cx.clearRect(0, 0, 900, 480);
                
                // 고대비 화이트 테마 배경
                cx.fillStyle = "#f1f5f9"; cx.fillRect(0,0,900,480);

                // 원근 홈플레이트 드로잉
                cx.fillStyle = "#e2e8f0";
                cx.beginPath();
                cx.moveTo(380, 420); cx.lineTo(520, 420);
                cx.lineTo(550, 460); cx.lineTo(450, 480); cx.lineTo(350, 460);
                cx.closePath(); cx.fill();

                // 중앙 스트라이크 존 박스
                cx.fillStyle = "#ffffff"; cx.fillRect(330, 130, 240, 240);
                cx.strokeStyle = "#475569"; cx.lineWidth = 3; cx.strokeRect(330, 130, 240, 240);

                // 격자선
                cx.strokeStyle = "#cbd5e1"; cx.lineWidth = 1;
                for(let i=1; i<3; i++) {{
                    cx.beginPath(); cx.moveTo(330 + (i*80), 130); cx.lineTo(330 + (i*80), 370); cx.stroke();
                    cx.beginPath(); cx.moveTo(330, 130 + (i*80)); cx.lineTo(570, 130 + (i*80)); cx.stroke();
                }}

                // 투수 마운드
                cx.fillStyle = "#94a3b8"; cx.fillRect(440, 146, 20, 5);

                // 투구 마킹 고정 렌더
                marks.forEach(m => {{
                    cx.fillStyle = m.mis ? "#fbbf24" : (m.sz ? "#10b981" : "#ef4444");
                    cx.beginPath(); cx.arc(m.x, m.y, 7, 0, Math.PI*2); cx.fill();
                    cx.strokeStyle = "#ffffff"; cx.lineWidth = 1.5; cx.stroke();
                }});

                if (ball.active) {{
                    let frameStep = 0.032 + (SPEED / 100) * 0.018;
                    ball.time += frameStep;

                    // [고증 완료] 직구 계열일 경우 뱀처럼 휘어지는 트위스트 연산을 무조건 0으로 차단!!
                    let isFastball = PITCH_NAME.includes("직구") || PITCH_NAME.includes("싱커") || PITCH_NAME.includes("커터");
                    let twistX = isFastball ? 0 : Math.sin(ball.time * Math.PI) * 65.0;
                    let twistY = isFastball ? 0 : -Math.sin(ball.time * Math.PI) * 40.0;

                    let lx = 450 + (ball.tx - 450) * ball.time;
                    let ly = 150 + (ball.ty - 150) * ball.time;

                    ball.size = 2.0 + (Math.pow(ball.time, 4.0) * 36.0);
                    let b_factor = Math.pow(ball.time, 2.4);
                    
                    ball.x = lx + twistX + ((HB + (isFastball ? 0 : noiseX)) * b_factor * 2.5);
                    ball.y = ly + twistY + ((VB + (isFastball ? 0 : noiseY)) * b_factor * 2.5);

                    trajectory.push({{ x: ball.x, y: ball.y }});

                    // 굵고 선명한 궤적 드로잉
                    cx.beginPath();
                    cx.strokeStyle = isMisfire ? "#f43f5e" : "#0f172a";
                    cx.lineWidth = 6;
                    for (let i = 0; i < trajectory.length; i++) {{
                        if (i === 0) cx.moveTo(trajectory[i].x, trajectory[i].y);
                        else cx.lineTo(trajectory[i].x, trajectory[i].y);
                    }}
                    cx.stroke();

                    // 야구공
                    cx.fillStyle = "#ffffff"; cx.strokeStyle = "#0f172a"; cx.lineWidth = 3;
                    cx.beginPath(); cx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); cx.fill(); cx.stroke();

                    if (ball.time >= 1.0) {{
                        ball.active = false;
                        evaluateAtBat();
                    }}
                }}

                // 포수 미트 마커
                if (!ball.active) {{
                    cx.fillStyle = "rgba(146, 64, 14, 0.9)";
                    cx.strokeStyle = "#451a03"; cx.lineWidth = 2;
                    cx.beginPath(); cx.arc(pointer.x, pointer.y, 25, 0, Math.PI*2); cx.fill(); cx.stroke();
                    
                    cx.strokeStyle = "#ffffff"; cx.lineWidth = 2;
                    cx.beginPath(); cx.moveTo(pointer.x-10, pointer.y); cx.lineTo(pointer.x+10, pointer.y);
                    cx.moveTo(pointer.x, pointer.y-10); cx.lineTo(pointer.x, pointer.y+10); cx.stroke();
                }}

                cx.fillStyle = "#0f172a"; cx.font = "bold 14px sans-serif";
                cx.fillText(`타자: ${{ROSTER[state.idx].name}} (파워 ${{ROSTER[state.idx].power}})`, 20, 445);
                cx.fillStyle = "#64748b";
                cx.fillText(`투수 원근 릴리즈 시스템 V3`, 20, 465);

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(canvas_html_p, height=620)

    # -----------------------------------------------------------------
    # [TAB 2] 플레이어 전용 타격 챌린지 모드 (직구 교정 버전)
    # -----------------------------------------------------------------
    with tab_h:
        col_set3, col_set4 = st.columns([1, 2])
        with col_set3:
            sel_pitch_2 = st.radio("🔮 AI 투수 투구 구종 지정", st.session_state.pitch_list, key="h_pitch")
        with col_set4:
            balance_h = st.slider("⚖️ AI 투수 구속 제구 조절 벨트", 0, 100, 50, key="h_balance")

        live_speed_h = int(p_max - (balance_h / 100.0) * (p_max - p_min))
        live_control_h = int(5 + (balance_h / 100.0) * 91)

        st.markdown(f"📊 **상대 AI 투수 세팅:** 구속 **{live_speed_h} mph** | 제구력 수치 **{live_control_h} / 100**")

        if "직구" in sel_pitch_2 or "싱커" in sel_pitch_2 or "커터" in sel_pitch_2:
            thb, tvb = (0.0, -1.0)
        elif "스위퍼" in sel_pitch_2 or "슬라이더" in sel_pitch_2:
            thb, tvb = (16.0, 2.0)
        elif "커브" in sel_pitch_2 or "너클 커브" in sel_pitch_2:
            thb, tvb = (4.0, 17.0)
        else:
            thb, tvb = (-1.0, 11.0)

        canvas_html_h = f"""
        <div style="background: #ffffff; padding: 5px; border-radius: 12px; border: 2px solid #0f172a; max-width: 920px; margin: 0 auto;">
            <div style="background: #1e293b; color: #ffffff; padding: 10px 15px; border-radius: 6px; display: flex; justify-content: space-between; font-weight: bold; font-family: monospace; font-size:14px; margin-bottom:8px;">
                <div>[플레이어 안타 개수] <span id="h-score-player" style="color:#10b981; font-weight:900;">0</span></div>
                <div id="h-count-text" style="color:#fbbf24; font-size:15px;">S: 0 | O: 0</div>
                <div>AI SPEED: {live_speed_h} mph</div>
            </div>

            <canvas id="canvasBatterMode" width="900" height="480" style="background: #f8fafc; border: 2px solid #0f172a; display: block; margin: 0 auto;"></canvas>
            
            <div style="background: #1e293b; color: #ffffff; padding: 22px; border-radius: 8px; font-size: 20px; font-weight: 800; margin-top: 10px; border-left: 8px solid #10b981; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); text-align: left; line-height: 1.5;">
                <span id="h-ticker" style="color: #fbbf24;">🎯 [타격 대기] 화면을 클릭하여 투구를 유도한 후, 공이 가장 커지는 임팩트 타이밍에 맞춰 한 번 더 대형 스윙 클릭을 가하세요!</span>
            </div>
        </div>

        <script>
            const cv2 = document.getElementById('canvasBatterMode');
            const cx2 = cv2.getContext('2d');

            const H_SPEED = {live_speed_h};
            const H_CONTROL = {live_control_h};
            const H_HB = {thb};
            const H_VB = {tvb};
            const H_PITCH = "{sel_pitch_2}";

            let b_state = {{ hit: 0, s: 0, o: 0 }};
            let h_ball = {{ active: false, x: 450, y: 150, tx: 450, ty: 250, time: 0, size: 2 }};
            let h_trail = [];
            let h_noiseX = 0, h_noiseY = 0;
            let targetX = 450, targetY = 250;
            let isSwung = false;

            cv2.addEventListener('mousedown', () => {{
                if (!h_ball.active) {{
                    let range = (100 - H_CONTROL) * 0.45;
                    targetX = 450 + (Math.random() - 0.5) * range;
                    targetY = 240 + (Math.random() - 0.5) * range;
                    h_noiseX = (Math.random() - 0.5) * 6.0;
                    h_noiseY = (Math.random() - 0.5) * 6.0;

                    h_ball.x = 450; h_ball.y = 150; h_ball.time = 0; h_ball.size = 2;
                    h_trail = []; isSwung = false;
                    h_ball.active = true;
                    document.getElementById('h-ticker').innerHTML = "<span style='color:#ffffff;'>⚾ 투구 시작! 공이 직선 또는 회전 궤적으로 질주합니다! 집중하세요!</span>";
                }} else {{
                    if (isSwung) return;
                    isSwung = true;

                    let t_diff = h_ball.time;
                    if (t_diff >= 0.83 && t_diff <= 0.96) {{
                        b_state.hit++; b_state.s = 0;
                        document.getElementById('h-ticker').innerHTML = `💥 <span style="color:#10b981; font-weight:bold;">JUST HIT!! 정타 작렬!</span> 배트 중심에 정확히 맞으며 야구장 외야를 가르는 안타를 터트렸습니다!`;
                    }} else if (t_diff < 0.83) {{
                        b_state.s++;
                        document.getElementById('h-ticker').innerHTML = "<span style='color:#ef4444;'>❌ 얼리 스윙:</span> 성급했습니다! 공이 홈플레이트에 채 도달하기 전에 배트가 먼저 돌았습니다.";
                    }} else {{
                        b_state.s++;
                        document.getElementById('h-ticker').innerHTML = "<span style='color:#ef4444;'>❌ 레이트 스윙:</span> 타이밍이 완전히 늦었습니다! 강속구 볼끝에 타이밍을 빼앗겼습니다.";
                    }}
                    checkInningStatus();
                }}
            }});

            function checkInningStatus() {{
                if (b_state.s >= 3) {{ b_state.o++; b_state.s = 0; }}
                if (b_state.o >= 3) {{ b_state.hit = 0; b_state.s = 0; b_state.o = 0; }}
                document.getElementById('h-score-player').innerText = b_state.hit;
                document.getElementById('h-count-text').innerText = `S: ${{b_state.s}} | O: ${{b_state.o}}`;
            }}

            function loopBatter() {{
                cx2.clearRect(0, 0, 900, 480);
                cx2.fillStyle = "#f8fafc"; cx2.fillRect(0,0,900,480);

                // 원근 홈플레이트
                cx2.fillStyle = "#e2e8f0";
                cx2.beginPath();
                cx2.moveTo(380, 420); cx2.lineTo(520, 420);
                cx2.lineTo(550, 460); cx2.lineTo(450, 480); cx2.lineTo(350, 460);
                cx2.closePath(); cx2.fill();

                // 스트라이크 존 박스
                cx2.fillStyle = "#ffffff"; cx2.fillRect(340, 140, 220, 220);
                cx2.strokeStyle = "#1e293b"; cx2.lineWidth = 3; cx2.strokeRect(340, 140, 220, 220);

                // 마운드
                cx2.fillStyle = "#94a3b8"; cx2.fillRect(442, 148, 16, 4);

                if (h_ball.active) {{
                    let frameStep = 0.030 + (H_SPEED / 100) * 0.015;
                    h_ball.time += frameStep;

                    let isFastball = H_PITCH.includes("직구") || H_PITCH.includes("싱커") || H_PITCH.includes("커터");
                    let arcX = isFastball ? 0 : Math.sin(h_ball.time * Math.PI) * 60.0;
                    let arcY = isFastball ? 0 : -Math.sin(h_ball.time * Math.PI) * 35.0;

                    let lx = 450 + (targetX - 450) * h_ball.time;
                    let ly = 150 + (targetY - 150) * h_ball.time;

                    h_ball.size = 2.0 + (Math.pow(h_ball.time, 4.0) * 44.0);
                    let bf = Math.pow(h_ball.time, 2.4);
                    
                    h_ball.x = lx + arcX + ((H_HB + (isFastball ? 0 : h_noiseX)) * bf * 2.4);
                    h_ball.y = ly + arcY + ((H_VB + (isFastball ? 0 : h_noiseY)) * bf * 2.4);

                    h_trail.push({{ x: h_ball.x, y: h_ball.y }});

                    cx2.beginPath(); cx2.strokeStyle = "#64748b"; cx2.lineWidth = 4;
                    for(let i=0; i<h_trail.length; i++) {{
                        if (i===0) cx2.moveTo(h_trail[i].x, h_trail[i].y);
                        else cx2.lineTo(h_trail[i].x, h_trail[i].y);
                    }}
                    cx2.stroke();

                    cx2.fillStyle = "#ffffff"; cx2.strokeStyle = "#0f172a"; cx2.lineWidth = 3;
                    cx2.beginPath(); cx2.arc(h_ball.x, h_ball.y, h_ball.size, 0, Math.PI*2); cx2.fill(); cx2.stroke();

                    if (h_ball.time >= 1.0) {{
                        h_ball.active = false;
                        if (!isSwung) {{
                            b_state.s++;
                            document.getElementById('h-ticker').innerHTML = "<span style='color:#fbbf24;'>⚠️ 루킹 스트라이크:</span> 미트 안으로 정직하게 빨려 들어가는 공을 그저 지켜보았습니다.";
                            checkInningStatus();
                        }}
                    }}
                }} else {{
                    cx2.fillStyle = "#0f172a"; cx2.font = "bold 15px sans-serif";
                    cx2.fillText("👆 화면 아무 곳이나 클릭하면 AI 투수가 투구를 시작합니다!", 260, 250);
                }}

                requestAnimationFrame(loopBatter);
            }}
            loopBatter();
        </script>
        """
        st.components.v1.html(canvas_html_h, height=620)

    st.markdown("---")
    if st.button("🔄 전구단 선택 로비 화면으로 리셋"):
        st.session_state.game_active = False
        st.rerun()

if __name__ == "__main__":
    main()
