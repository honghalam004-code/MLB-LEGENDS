import streamlit as st
import random
import time

def main():
    # ==========================================
    # 1. APPLICATION SETUP & THEME CONFIGURATION
    # ==========================================
    st.set_page_config(page_title="MVP BASEBALL: ULTIMATE 700", layout="wide", initial_sidebar_state="collapsed")
    
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; color: #0f172a; font-family: 'Inter', -apple-system, sans-serif; }
        .stSelectbox, .stSlider, .stRadio, .stNumberInput { background: #ffffff !important; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        h1, h2, h3 { color: #1e293b !important; font-weight: 900 !important; }
        .stButton>button { background: linear-gradient(to right, #1d4ed8, #2563eb) !important; color: white !important; font-weight: 800 !important; padding: 16px !important; border-radius: 12px !important; transition: all 0.2s; }
        .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3); }
        .data-card { background: white; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
        </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 2. MASSIVE DATABASE: MLB 30 TEAMS & PITCHERS
    # ==========================================
    mlb_database = {
        "AL EAST": {
            "NY Yankees (뉴욕 양키스)": ["게릿 콜 (G. Cole)", "마커스 스트로먼 (M. Stroman)", "카를로스 로돈 (C. Rodon)", "클레이 홈즈 (C. Holmes)"],
            "Baltimore Orioles (볼티모어 오리올스)": ["코빈 번스 (C. Burnes)", "그레이슨 로드리게스 (G. Rodriguez)", "카일 브래디쉬 (K. Bradish)"],
            "Boston Red Sox (보스턴 레드삭스)": ["루카스 지올리토 (L. Giolito)", "브라얀 벨로 (B. Bello)", "켄리 잰슨 (K. Jansen)"],
            "Tampa Bay Rays (탬파베이 레이스)": ["잭 에플린 (Z. Eflin)", "에런 시발리 (A. Civale)", "피트 페어뱅크스 (P. Fairbanks)"],
            "Toronto Blue Jays (토론토 블루제이스)": ["케빈 가우스먼 (K. Gausman)", "크리스 배싯 (C. Bassitt)", "호세 베리오스 (J. Berrios)"]
        },
        "AL CENTRAL": {
            "Cleveland Guardians (클리블랜드)": ["셰인 비버 (S. Bieber)", "태너 바이비 (T. Bibee)", "에마누엘 클라세 (E. Clase)"],
            "Minnesota Twins (미네소타 트윈스)": ["파블로 로페즈 (P. Lopez)", "조 라이언 (J. Ryan)", "요안 두란 (J. Duran)"],
            "Detroit Tigers (디트로이트 타이거스)": ["타릭 스쿠발 (T. Skubal)", "잭 플래허티 (J. Flaherty)", "마에다 겐타 (K. Maeda)"],
            "KC Royals (캔자스시티 로열스)": ["콜 레이건스 (C. Ragans)", "세스 루고 (S. Lugo)", "마이클 와카 (M. Wacha)"],
            "Chicago White Sox (시카고 화이트삭스)": ["딜런 시즈 (D. Cease)", "마이클 코펙 (M. Kopech)", "개럿 크로셰 (G. Crochet)"]
        },
        "AL WEST": {
            "Houston Astros (휴스턴 애스트로스)": ["저스틴 벌랜더 (J. Verlander)", "프램버 발데스 (F. Valdez)", "조시 헤이더 (J. Hader)"],
            "Texas Rangers (텍사스 레인저스)": ["네이선 이볼디 (N. Eovaldi)", "맥스 슈어저 (M. Scherzer)", "제이콥 디그롬 (J. deGrom)"],
            "Seattle Mariners (시애틀 매리너스)": ["루이스 카스티요 (L. Castillo)", "조지 커비 (G. Kirby)", "안드레스 무뇨스 (A. Munoz)"],
            "LA Angels (로스앤젤레스 에인절스)": ["패트릭 산도발 (P. Sandoval)", "타일러 앤더슨 (T. Anderson)", "카를로스 에스테베스 (C. Estevez)"],
            "Oakland Athletics (오클랜드 애슬레틱스)": ["폴 블랙번 (P. Blackburn)", "JP 시어스 (J. Sears)", "메이슨 밀러 (M. Miller)"]
        },
        "NL EAST": {
            "Atlanta Braves (애틀랜타 브레이브스)": ["스펜서 스트라이더 (S. Strider)", "맥스 프리드 (M. Fried)", "크리스 세일 (C. Sale)"],
            "Philadelphia Phillies (필라델피아)": ["잭 휠러 (Z. Wheeler)", "애런 놀라 (A. Nola)", "호세 알바라도 (J. Alvarado)"],
            "Miami Marlins (마이애미 말린스)": ["헤수스 루자르도 (J. Luzardo)", "에우리 페레즈 (E. Perez)", "태너 스캇 (T. Scott)"],
            "NY Mets (뉴욕 메츠)": ["센가 코다이 (K. Senga)", "루이스 세베리노 (L. Severino)", "에드윈 디아즈 (E. Diaz)"],
            "Washington Nationals (워싱턴)": ["조시아 그레이 (J. Gray)", "맥켄지 고어 (M. Gore)", "카일 피니건 (K. Finnegan)"]
        },
        "NL CENTRAL": {
            "Milwaukee Brewers (밀워키 브루어스)": ["프레디 페랄타 (F. Peralta)", "웨이드 마일리 (W. Miley)", "데빈 윌리엄스 (D. Williams)"],
            "Chicago Cubs (시카고 컵스)": ["저스틴 스틸 (J. Steele)", "이마나가 쇼타 (S. Imanaga)", "카일 헨드릭스 (K. Hendricks)"],
            "Cincinnati Reds (신시내티 레즈)": ["헌터 그린 (H. Greene)", "그레이엄 애시크래프트 (G. Ashcraft)", "알렉시스 디아즈 (A. Diaz)"],
            "Pittsburgh Pirates (피츠버그 파이어리츠)": ["미치 켈러 (M. Keller)", "폴 스킨스 (P. Skenes)", "데이비드 베드너 (D. Bednar)"],
            "STL Cardinals (세인트루이스 카디널스)": ["소니 그레이 (S. Gray)", "마일스 마이콜라스 (M. Mikolas)", "라이언 헬슬리 (R. Helsley)"]
        },
        "NL WEST": {
            "LA Dodgers (로스앤젤레스 다저스)": ["오타니 쇼헤이 (S. Ohtani)", "야마모토 요시노부 (Y. Yamamoto)", "클레이튼 커쇼 (C. Kershaw)", "타일러 글래스노우 (T. Glasnow)"],
            "AZ Diamondbacks (애리조나)": ["잭 갤런 (Z. Gallen)", "메릴 켈리 (M. Kelly)", "에두아르도 로드리게스 (E. Rodriguez)"],
            "SD Padres (샌디에이고 파드리스)": ["유 다르빗슈 (Y. Darvish)", "조 머스그로브 (J. Musgrove)", "마이클 킹 (M. King)"],
            "SF Giants (샌프란시스코 자이언츠)": ["로건 웹 (L. Webb)", "블레이크 스넬 (B. Snell)", "카밀로 도발 (C. Doval)"],
            "Colorado Rockies (콜로라도 로키스)": ["카일 프리랜드 (K. Freeland)", "저스틴 로렌스 (J. Lawrence)", "라이언 펠트너 (R. Feltner)"]
        }
    }

    # ==========================================
    # 3. SESSION STATE MANAGEMENT
    # ==========================================
    if 'game_active' not in st.session_state: st.session_state.game_active = False
    if 'weather_wind' not in st.session_state: st.session_state.weather_wind = 0
    if 'stadium_type' not in st.session_state: st.session_state.stadium_type = "Open Air"

    # ==========================================
    # 4. GAME LOBBY: PRE-GAME CONFIGURATION
    # ==========================================
    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: white; padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #e2e8f0; max-width: 1000px; margin: 20px auto; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                <span style="background: #ef4444; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 14px;">ULTIMATE PRO ENGINE 2026</span>
                <h1 style="font-size: 50px; font-weight: 900; margin: 10px 0; color: #0f172a;">MVP BASEBALL: <span style="color: #2563eb;">CATCHER'S VIEW</span></h1>
                <p style="color: #64748b; font-size: 18px;">메이저리그 30개 구단 전체 로스터와 환경 변수를 설정하고 게임을 시작하세요.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # --- Away Team Selection ---
        st.markdown("### ✈️ AWAY TEAM (원정 팀 설정)")
        a_col1, a_col2, a_col3 = st.columns(3)
        with a_col1: a_div = st.selectbox("원정팀 지구 선택", list(mlb_database.keys()), key="ad")
        with a_col2: a_team = st.selectbox("원정팀 선택", list(mlb_database[a_div].keys()), key="at")
        with a_col3: a_pitcher = st.selectbox("원정 선발 투수", mlb_database[a_div][a_team], key="ap")

        # --- Home Team Selection ---
        st.markdown("### 🏠 HOME TEAM (홈 팀 설정)")
        h_col1, h_col2, h_col3 = st.columns(3)
        with h_col1: h_div = st.selectbox("홈팀 지구 선택", list(mlb_database.keys()), index=5, key="hd")
        with h_col2: h_team = st.selectbox("홈팀 선택", list(mlb_database[h_div].keys()), index=0, key="ht")
        with h_col3: h_pitcher = st.selectbox("홈 선발 투수 (현재 마운드)", mlb_database[h_div][h_team], key="hp")

        # --- Environment Settings ---
        st.markdown("### 🌤️ STADIUM & WEATHER (구장 및 날씨 환경)")
        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1: stadium_env = st.selectbox("구장 환경", ["개방형 구장 (Open Air)", "돔 구장 (Dome Stadium)"])
        with e_col2: weather = st.selectbox("날씨", ["맑음 (Clear)", "흐림 (Cloudy)", "비 (Rain - 공이 미끄러움)"])
        with e_col3: wind = st.slider("풍속 (mph - 타구 및 변화구 궤적 영향)", -15, 15, 0, help="음수는 역풍/좌측, 양수는 순풍/우측")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏟️ STADIUM ENTER (경기장 입장하여 플레이 볼!)", use_container_width=True):
            st.session_state.away_team = a_team.split(" (")[0]
            st.session_state.home_team = h_team.split(" (")[0]
            st.session_state.pitcher_name = h_pitcher
            st.session_state.stadium_env = stadium_env
            st.session_state.weather = weather
            st.session_state.wind = wind
            st.session_state.game_active = True
            st.rerun()
        st.stop() # LOBBY GUARDRAIL

    # ==========================================
    # 5. LIVE GAME UI: HEADER & SCOREBOARD
    # ==========================================
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #1e293b, #0f172a); border-radius: 15px; padding: 20px; color: white; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div>
                <h3 style="margin:0; color:#cbd5e1; font-size:16px; font-weight:normal;">LIVE MATCHUP</h3>
                <h1 style="margin:0; font-size:32px; color:white;">{st.session_state.away_team} vs {st.session_state.home_team}</h1>
            </div>
            <div style="text-align:right;">
                <span style="background: #3b82f6; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px;">MOUND: {st.session_state.pitcher_name}</span>
                <br>
                <span style="color:#94a3b8; font-size:12px;">{st.session_state.stadium_env} | WIND: {st.session_state.wind} mph</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 6. PITCH COMMAND CENTER (LOWER CONTROLS)
    # ==========================================
    st.markdown("### ⚙️ PITCHING ARSENAL (구종 및 투구 매커니즘 정밀 제어)")
    
    # 9가지 구종 선택
    pitch_types = [
        "포심 패스트볼 (Four-Seam)", "투심/싱커 (Sinker)", "커터 (Cutter)", 
        "슬라이더 (Slider)", "스위퍼 (Sweeper)", "파워 커브 (Curveball)", 
        "슬러브 (Slurve)", "체인지업 (Changeup)", "스플리터 (Splitter)"
    ]
    
    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    with c1:
        sel_pitch = st.selectbox("⚾ 구종 (Pitch Type)", pitch_types)
    with c2:
        # 구종별 기본 구속 세팅
        default_speed = 95
        if "싱커" in sel_pitch or "커터" in sel_pitch: default_speed = 92
        if "슬라이더" in sel_pitch or "스플리터" in sel_pitch: default_speed = 87
        if "체인지업" in sel_pitch: default_speed = 84
        if "커브" in sel_pitch or "스위퍼" in sel_pitch: default_speed = 80
        p_speed = st.slider("속도 (Velocity - mph)", 70, 105, default_speed)
    with c3:
        p_control = st.slider("제구력 (Command - 1~100)", 1, 100, 85)
    with c4:
        p_spin = st.slider("회전수 (Spin Rate - RPM)", 1500, 3300, 2400, step=50)

    # Calculate Break values dynamically in Python before passing to JS
    # h_break: Horizontal movement, v_break: Vertical movement
    h_break = 0.0
    v_break = 0.0
    
    if "포심" in sel_pitch: v_break = -1.5 # 라이징 무브먼트 환상
    if "싱커" in sel_pitch: h_break = -2.5; v_break = 3.5
    if "커터" in sel_pitch: h_break = 1.5; v_break = 0.5
    if "슬라이더" in sel_pitch: h_break = 4.5; v_break = 1.5
    if "스위퍼" in sel_pitch: h_break = 8.5; v_break = 0.5 # 횡 무브먼트 극대화
    if "커브" in sel_pitch: h_break = 2.0; v_break = 7.5 # 폭포수 낙차
    if "슬러브" in sel_pitch: h_break = 5.0; v_break = 4.5
    if "체인지업" in sel_pitch: h_break = -2.0; v_break = 4.0
    if "스플리터" in sel_pitch: h_break = 0.0; v_break = 6.5 # 홈플레이트 앞 급락

    # ==========================================
    # 7. ULTIMATE JAVASCRIPT GAME ENGINE (HTML/CANVAS)
    # ==========================================
    engine_html = f"""
    <div style="background: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #cbd5e1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); max-width: 1000px; margin: 0 auto; position: relative;">
        
        <div style="position: absolute; top: 40px; left: 40px; background: rgba(15, 23, 42, 0.85); color: white; padding: 15px 25px; border-radius: 12px; font-family: 'Arial Black', sans-serif; border: 2px solid rgba(255,255,255,0.2); z-index: 100; backdrop-filter: blur(4px);">
            <div style="display: flex; justify-content: space-between; width: 220px; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 5px;">
                <span style="color:#94a3b8; font-size:12px;">AWAY</span>
                <span style="font-size: 20px;">{st.session_state.away_team[:3].upper()}</span>
                <span id="score-away" style="font-size: 24px; color:#38bdf8;">0</span>
            </div>
            <div style="display: flex; justify-content: space-between; width: 220px; margin-bottom: 12px;">
                <span style="color:#94a3b8; font-size:12px;">HOME</span>
                <span style="font-size: 20px;">{st.session_state.home_team[:3].upper()}</span>
                <span id="score-home" style="font-size: 24px; color:#38bdf8;">0</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 14px; color: #cbd5e1; background: #000; padding: 5px 10px; border-radius: 6px;">
                <span id="inning-text">TOP 1ST</span>
                <span>
                    <span style="color:#22c55e" id="lamp-b">○○○</span> 
                    <span style="color:#eab308" id="lamp-s">○○</span> 
                    <span style="color:#ef4444" id="lamp-o">○○</span>
                </span>
            </div>
        </div>

        <canvas id="ultraCanvas" width="950" height="500" style="background: #f1f5f9; border-radius: 12px; border: 1px solid #94a3b8; display: block; margin: 0 auto; cursor: crosshair;"></canvas>
        
        <div style="margin-top: 15px; background: #0f172a; padding: 15px; border-radius: 10px; border-left: 5px solid #2563eb;">
            <div style="color: #64748b; font-size: 12px; font-weight: bold; margin-bottom: 4px;">🎙️ LIVE PLAY-BY-PLAY COMMENTARY</div>
            <div id="commentary-box" style="color: #f8fafc; font-family: sans-serif; font-size: 15px; height: 60px; overflow-y: auto; line-height: 1.5;">
                경기가 시작되었습니다. 타석에 첫 타자가 들어섭니다. 우측의 투명한 K-ZONE을 클릭하여 투구 위치를 결정하십시오.
            </div>
        </div>

        <div id="radar-gun" style="position: absolute; bottom: 120px; left: 40px; background: rgba(0, 0, 0, 0.8); border: 3px solid #ef4444; border-radius: 10px; padding: 10px 20px; color: #ef4444; font-family: 'Courier New', monospace; font-size: 32px; font-weight: bold; text-shadow: 0 0 10px #ef4444; display: none;">
            99 MPH
        </div>
    </div>

    <script>
        const canvas = document.getElementById('ultraCanvas');
        const ctx = canvas.getContext('2d');

        // Python -> JS Inject Data
        const P_NAME = "{st.session_state.pitcher_name}";
        const P_TYPE = "{sel_pitch.split(' (')[0]}";
        const P_SPEED = {p_speed};
        const P_CONTROL = {p_control};
        const P_H_BREAK = {h_break};
        const P_V_BREAK = {v_break};
        const ENV_WIND = {st.session_state.wind};
        const WEATHER = "{st.session_state.weather}";

        // Game State Engine
        let db = {{ 
            away: 0, home: 0, inning: 1, isTop: true, 
            b: 0, s: 0, o: 0, bases: [false, false, false],
            pitchCount: 0, strikesThrown: 0
        }};

        // Advanced Catcher's View Physics System
        // Origin (Pitcher's Release Point): (250, 150) -> Far background, center-top
        // Destination (Catcher's Mitt): (ball.tx, ball.ty) -> Near foreground, center-bottom
        let ball = {{ active: false, x: 250, y: 150, tx: 0, ty: 0, z: 0, size: 2.0 }};
        let aim = {{ x: 0, y: 0 }};
        let pitchTrail = []; // Array of {{x, y, isStrike}}

        // Commentary Database (Massive Arrays for Variety)
        const comments = {{
            strikeout: [
                "루킹 삼진! 타자 얼어붙습니다!",
                "헛스윙 삼진! 배트가 허공을 가릅니다!",
                `기가 막힌 구위입니다. ${P_NAME}의 삼진 쇼!`,
                "타이밍을 완전히 빼앗았습니다. 스트라이크 아웃!"
            ],
            walk: [
                "포볼입니다. 타자가 걸어나갑니다.",
                "제구가 흔들리며 볼넷을 허용합니다.",
                "풀카운트 승부 끝에 결국 1루를 내줍니다."
            ],
            homerun: [
                "좌측 담장! 좌측 담장!! 넘어갔습니다! 홈런!!",
                "까마득하게 날아갑니다. 의심할 여지 없는 대형 홈런!",
                "배트 중심에 정확히 맞았습니다. 굿바이 베이스볼!"
            ],
            hit: [
                "깔끔한 안타! 1루에 출루합니다.",
                "빈 곳을 찌르는 적시타! 주자 움직입니다.",
                "잘 맞은 타구, 중견수 앞 안타입니다."
            ],
            out_ground: [
                "내야 땅볼입니다. 유격수 잡아서 1루에... 아웃!",
                "투수 앞 땅볼, 침착하게 처리합니다.",
                "힘없는 타구, 2루수가 걷어냅니다."
            ],
            out_fly: [
                "높이 뜬 공, 외야수가 콜을 외치고 잡아냅니다.",
                "우익수 쪽 뜬공, 워닝 트랙 앞에서 잡힙니다.",
                "평범한 플라이 아웃입니다."
            ],
            strike_look: [
                "보더라인을 완벽하게 걸치는 스트라이크!",
                "타자 지켜만 봅니다. 원 스트라이크.",
                "예리하게 파고듭니다."
            ],
            strike_swing: [
                "크게 헛스윙합니다!",
                "볼끝이 살아서 들어오네요. 헛스윙!",
                "타자 타이밍이 전혀 맞지 않습니다."
            ],
            ball: [
                "아슬아슬하게 존을 벗어났습니다.",
                "유인구에 속지 않네요. 볼.",
                "바깥쪽 깊숙한 공, 볼입니다."
            ]
        }};

        function pickRandom(arr) {{ return arr[Math.floor(Math.random() * arr.length)]; }}

        function log(msg, color="#ffffff") {{
            const box = document.getElementById('commentary-box');
            box.innerHTML = `<span style="color:${color}; font-weight:bold;">[현장]</span> ${msg}<br>` + box.innerHTML;
        }}

        function updateScoreboard() {{
            document.getElementById('score-away').innerText = db.away;
            document.getElementById('score-home').innerText = db.home;
            document.getElementById('inning-text').innerText = `${db.isTop ? 'TOP' : 'BOT'} ${db.inning}`;
            
            const lamp = (count, max) => '●'.repeat(count) + '○'.repeat(max - count);
            document.getElementById('lamp-b').innerText = lamp(db.b, 3);
            document.getElementById('lamp-s').innerText = lamp(db.s, 2);
            document.getElementById('lamp-o').innerText = lamp(db.o, 3);
        }}

        // Mouse Tracking
        canvas.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            aim.x = (e.clientX - rect.left) * (canvas.width / rect.width);
            aim.y = (e.clientY - rect.top) * (canvas.height / rect.height);
        }});

        // Trigger Pitch
        canvas.addEventListener('mousedown', () => {{
            if (ball.active) return;
            // Target zone validation (Right side of canvas)
            if (aim.x > 530 && aim.x < 870 && aim.y > 60 && aim.y < 440) {{
                
                // 1. Calculate Command Error Margin (Reverse engineered from 1-100 control)
                let errorRadius = (100 - P_CONTROL) * 0.6;
                // Weather condition effect: Rain decreases control by adding more error
                if (WEATHER === "비 (Rain - 공이 미끄러움)") errorRadius *= 1.3;

                let finalTx = aim.x + (Math.random() - 0.5) * errorRadius;
                let finalTy = aim.y + (Math.random() - 0.5) * errorRadius;

                // 2. Wind Physics Effect
                finalTx += (ENV_WIND * 1.2);

                ball.tx = finalTx;
                ball.ty = finalTy;
                
                // 3. Reset Physics State
                ball.x = 250; 
                ball.y = 150; 
                ball.z = 0; // z is progress from 0.0 to 1.0
                ball.size = 2.0;
                ball.active = true;
                
                document.getElementById('radar-gun').style.display = 'none';
            }}
        }});

        // Advanced AI Resolution Engine
        function resolvePitch() {{
            db.pitchCount++;
            
            // Strike Zone Definition (Scaled to right side canvas UI)
            // Center is roughly x:700, y:250. Zone is 180x200
            const inZone = (ball.tx >= 610 && ball.tx <= 790 && ball.ty >= 150 && ball.ty <= 350);
            
            // Radar Gun Display
            const displaySpeed = P_SPEED + Math.floor(Math.random() * 3) - 1;
            const radar = document.getElementById('radar-gun');
            radar.innerText = `${displaySpeed} MPH`;
            radar.style.display = 'block';

            // Batter Math
            let speedAdvantage = (displaySpeed - 88) * 0.01;
            let breakAdvantage = (Math.abs(P_H_BREAK) + Math.abs(P_V_BREAK)) * 0.02;
            let batterSwingProb = inZone ? 0.65 : 0.20;
            
            if (db.s === 2) batterSwingProb += 0.2; // Protect plate with 2 strikes
            if (db.b === 3) batterSwingProb -= 0.2; // Take pitch on 3 balls

            const isSwing = Math.random() < batterSwingProb;

            if (isSwing) {{
                // Contact Math
                let contactProb = 0.75 - speedAdvantage - breakAdvantage;
                if (!inZone) contactProb -= 0.3; // Harder to hit balls out of zone

                const isContact = Math.random() < contactProb;

                if (isContact) {{
                    const hitQuality = Math.random();
                    if (hitQuality < 0.05 + (inZone ? 0.05 : 0)) {{
                        // HOME RUN
                        let runs = db.bases.filter(b => b).length + 1;
                        if (db.isTop) db.away += runs; else db.home += runs;
                        db.bases = [false, false, false];
                        db.s = 0; db.b = 0;
                        log(`[${P_TYPE} - ${displaySpeed}mph] ` + pickRandom(comments.homerun), "#ef4444");
                    }} 
                    else if (hitQuality < 0.35) {{
                        // BASE HIT
                        let runs = db.bases[2] ? 1 : 0;
                        db.bases[2] = db.bases[1]; db.bases[1] = db.bases[0]; db.bases[0] = true;
                        if (db.isTop) db.away += runs; else db.home += runs;
                        db.s = 0; db.b = 0;
                        log(`[${P_TYPE} - ${displaySpeed}mph] ` + pickRandom(comments.hit), "#eab308");
                    }} 
                    else {{
                        // OUT
                        db.o++;
                        db.s = 0; db.b = 0;
                        let outMsg = Math.random() > 0.5 ? pickRandom(comments.out_ground) : pickRandom(comments.out_fly);
                        log(`[${P_TYPE} - ${displaySpeed}mph] ` + outMsg, "#94a3b8");
                    }}
                }} else {{
                    // SWING AND MISS
                    db.s++;
                    log(`[${P_TYPE} - ${displaySpeed}mph] ` + pickRandom(comments.strike_swing), "#22c55e");
                }}
            }} else {{
                // TAKE PITCH
                if (inZone) {{
                    db.s++;
                    log(`[${P_TYPE} - ${displaySpeed}mph] ` + pickRandom(comments.strike_look), "#22c55e");
                }} else {{
                    db.b++;
                    log(`[${P_TYPE} - ${displaySpeed}mph] ` + pickRandom(comments.ball), "#3b82f6");
                }}
            }}

            // State Checks
            if (db.s >= 3) {{
                db.o++; db.s = 0; db.b = 0;
                log(pickRandom(comments.strikeout), "#ef4444");
            }}
            if (db.b >= 4) {{
                db.bases[0] = true; db.s = 0; db.b = 0;
                log(pickRandom(comments.walk), "#eab308");
            }}
            if (db.o >= 3) {{
                db.o = 0; db.s = 0; db.b = 0; db.bases = [false,false,false];
                db.isTop = !db.isTop;
                if (db.isTop) db.inning++;
                log("공수 교대! 이닝이 종료되었습니다.", "#ffffff");
            }}

            updateScoreboard();
            pitchTrail.push({{ x: ball.tx, y: ball.ty, strike: inZone }});
            if(pitchTrail.length > 9) pitchTrail.shift();
        }}

        // ==========================================
        // 8. HIGH-FIDELITY RENDER LOOP (60 FPS)
        // ==========================================
        function drawStadium() {{
            // Sky & Environment (Reacts to weather)
            let skyColor1 = "#38bdf8"; let skyColor2 = "#bae6fd";
            if (WEATHER.includes("흐림")) {{ skyColor1 = "#64748b"; skyColor2 = "#94a3b8"; }}
            if (WEATHER.includes("비")) {{ skyColor1 = "#475569"; skyColor2 = "#64748b"; }}
            
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 200);
            skyGrad.addColorStop(0, skyColor1); skyGrad.addColorStop(1, skyColor2);
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, 500, 200);

            // Outfield Grass (Perspective)
            ctx.fillStyle = "#166534";
            ctx.beginPath(); ctx.moveTo(250, 400); ctx.lineTo(480, 100); ctx.lineTo(20, 100); ctx.fill();
            
            // Grass Patterns (Mowed lines)
            ctx.fillStyle = "rgba(255,255,255,0.03)";
            ctx.beginPath(); ctx.moveTo(250, 400); ctx.lineTo(350, 100); ctx.lineTo(280, 100); ctx.fill();
            ctx.beginPath(); ctx.moveTo(250, 400); ctx.lineTo(150, 100); ctx.lineTo(220, 100); ctx.fill();

            // Infield Dirt
            ctx.fillStyle = "#b45309";
            ctx.beginPath(); ctx.ellipse(250, 150, 35, 12, 0, 0, Math.PI*2); ctx.fill(); // Mound
            ctx.fillStyle = "#ffffff"; ctx.fillRect(240, 148, 20, 3); // Rubber

            // Bases (Perspective Math)
            const drawBase = (x, y, active) => {{
                ctx.fillStyle = active ? "#ef4444" : "#e2e8f0";
                ctx.strokeStyle = active ? "#f87171" : "#94a3b8";
                ctx.lineWidth = 1;
                ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI/4);
                ctx.fillRect(-6, -6, 12, 12); ctx.strokeRect(-6, -6, 12, 12); ctx.restore();
            }};
            drawBase(340, 250, db.bases[0]); // 1B
            drawBase(250, 150, db.bases[1]); // 2B (On Mound in this 2D projection)
            drawBase(160, 250, db.bases[2]); // 3B

            // Home Plate (Large, close up)
            ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(250, 370); ctx.lineTo(265, 385); ctx.lineTo(265, 395); ctx.lineTo(235, 395); ctx.lineTo(235, 385); ctx.closePath();
            ctx.fill(); ctx.stroke();

            // The Pitcher (Entity in distance)
            ctx.fillStyle = "#0f172a";
            ctx.beginPath(); ctx.arc(250, 135, 5, 0, Math.PI*2); ctx.fill(); // Head
            ctx.fillRect(246, 140, 8, 12); // Body
            
            // Divider
            ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(500, 10); ctx.lineTo(500, 490); ctx.stroke();
        }}

        function drawKZone() {{
            // White clean backdrop for broadcast UI
            ctx.fillStyle = "#ffffff"; ctx.fillRect(501, 0, 449, 500);

            // Main Strike Zone Box
            const zx = 610, zy = 150, zw = 180, zh = 200;
            ctx.fillStyle = "rgba(37, 99, 235, 0.05)"; ctx.fillRect(zx, zy, zw, zh);
            ctx.strokeStyle = "#2563eb"; ctx.lineWidth = 3; ctx.strokeRect(zx, zy, zw, zh);
            
            // 9-Grid Lines
            ctx.strokeStyle = "rgba(37, 99, 235, 0.2)"; ctx.lineWidth = 1;
            for(let i=1; i<3; i++) {{
                ctx.beginPath(); ctx.moveTo(zx + (i*zw/3), zy); ctx.lineTo(zx + (i*zw/3), zy+zh); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(zx, zy + (i*zh/3)); ctx.lineTo(zx+zw, zy + (i*zh/3)); ctx.stroke();
            }}

            // Pitch Heatmap History
            pitchTrail.forEach((p, idx) => {{
                ctx.fillStyle = p.strike ? "#22c55e" : "#ef4444";
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2;
                ctx.globalAlpha = 0.3 + (0.7 * (idx / 9)); // Fade older pitches
                ctx.beginPath(); ctx.arc(p.x, p.y, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke();
                ctx.globalAlpha = 1.0;
            }});

            // Laser Crosshair Aiming Logic
            if (!ball.active && aim.x > 510 && aim.x < 940) {{
                ctx.strokeStyle = "rgba(234, 88, 12, 0.4)"; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
                ctx.beginPath(); ctx.moveTo(aim.x, 20); ctx.lineTo(aim.x, 480); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(520, aim.y); ctx.lineTo(930, aim.y); ctx.stroke();
                ctx.setLineDash([]);
                
                ctx.strokeStyle = "#ea580c"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(aim.x, aim.y, 15, 0, Math.PI*2); ctx.stroke();
                ctx.beginPath(); ctx.arc(aim.x, aim.y, 2, 0, Math.PI*2); ctx.fill();
            }}
        }}

        function drawBallPhysics() {{
            if (!ball.active) return;
            
            // Advance Time (Speed dictates frame delta)
            let frameSpeed = 0.02 + (P_SPEED * 0.0003);
            ball.z += frameSpeed;
            
            if (ball.z > 1.0) ball.z = 1.0;

            // Base Linear Interpolation (Start 250,150 -> End tx,ty)
            let baseX = 250 + (ball.tx - 250) * ball.z;
            let baseY = 150 + (ball.ty - 150) * ball.z;

            // Magnus Effect (Breaking Ball Physics) Applied parabolically
            // Break is most prominent in the latter half of the flight
            let breakFactor = Math.pow(ball.z, 2); 
            let applyH = P_H_BREAK * breakFactor * 1.5;
            let applyV = P_V_BREAK * breakFactor * 1.5;

            ball.x = baseX + applyH;
            ball.y = baseY + applyV;
            
            // Optical Illusion / Perspective (Ball gets massive as it hits the mitt)
            // Starts at size 2.0 (far), ends at size 14.0 (near)
            ball.size = 2.0 + (Math.pow(ball.z, 3) * 12.0);

            // Render Ball Entity
            ctx.fillStyle = "#ffffff";
            ctx.strokeStyle = "#64748b";
            ctx.lineWidth = 1 + ball.z; // Seams get thicker as it approaches
            
            ctx.shadowColor = "rgba(0,0,0,0.3)"; ctx.shadowBlur = 5; ctx.shadowOffsetY = 2; // Shadow depth
            ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.shadowColor = "transparent";

            // Collision / Arrival Resolution
            if (ball.z >= 1.0) {{
                ball.active = false;
                resolvePitch();
            }}
        }}

        // Main 60FPS Game Loop
        function loop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawStadium();
            drawKZone();
            drawBallPhysics();
            
            // Draw Weather Rain overlay
            if (WEATHER.includes("비")) {{
                ctx.fillStyle = "rgba(255,255,255,0.4)";
                for(let i=0; i<30; i++) {{
                    let rx = Math.random() * 500;
                    let ry = Math.random() * 500;
                    ctx.fillRect(rx, ry, 1, 10);
                }}
            }}

            requestAnimationFrame(loop);
        }}

        // Init
        updateScoreboard();
        loop();
    </script>
    """

    st.components.v1.html(engine_html, height=720)

    # ==========================================
    # 9. RESET CONTROLS & FOOTER
    # ==========================================
    st.markdown("---")
    r_col1, r_col2 = st.columns([1, 5])
    with r_col1:
        if st.button("🔄 LOBBY 복귀", use_container_width=True):
            st.session_state.game_active = False
            st.rerun()
    with r_col2:
        st.markdown("<p style='color:#94a3b8; font-size:12px; margin-top:15px;'>© 2026 EA SPORTS MVP BASEBALL PRO SIMULATOR. All rights reserved. Physics engine calculates magnus effect, wind resistance, and 3D perspective projection.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
