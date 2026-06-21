import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB PRO ULTIMATE - FIX EDITION", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox > div > div { background-color: #1c2541 !important; color: #ffffff !important; border: 2px solid #3a86ff !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #3a86ff 0%, #023e8a 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 16px !important;
            border-radius: 8px !important; border: none !important; padding: 12px 20px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    mlb_data = {
        # AL East
        "New York Yankees": {"pitcher": {"name": "게릿 콜", "p1": "포심 직구", "p2": "너클 커브"}, "lineup": ["글레이버 토레스", "후안 소토", "애런 저지", "지안카를로 스탠튼", "재즈 치좀 Jr.", "앤서니 볼피", "알렉스 버두고", "오스틴 웰스", "앤서니 리조"]},
        "Baltimore Orioles": {"pitcher": {"name": "코빈 번스", "p1": "커터", "p2": "폭포수 커브"}, "lineup": ["거너 헨더슨", "애들리 러치맨", "앤서니 산탄데르", "라이언 마운트캐슬", "세드릭 멀린스", "조던 웨스트버그", "오스틴 헤이스", "콜튼 카우저", "라몬 우리아스"]},
        "Boston Red Sox": {"pitcher": {"name": "태너 하우크", "p1": "싱커", "p2": "스위퍼"}, "lineup": ["자렌 듀란", "윌리엄 아브레유", "라파엘 데버스", "타일러 오닐", "요시다 마사타카", "코너 웡", "트리스턴 카사스", "세단 라파엘라", "데이비드 해밀턴"]},
        "Tampa Bay Rays": {"pitcher": {"name": "셰인 맥클라나한", "p1": "광속구", "p2": "체인지업"}, "lineup": ["얀디 디아즈", "브랜든 로우", "란디 아로사레나", "아이작 파레디스", "조쉬 로우", "호세 시리", "르네 핀토", "테일러 월스", "리치 팔라시오스"]},
        "Toronto Blue Jays": {"pitcher": {"name": "케빈 가우스먼", "p1": "포심 직구", "p2": "스플리터"}, "lineup": ["조지 스프링어", "블라디미르 게레로 Jr.", "보 비셋", "저스틴 터너", "돌튼 바شو", "알레한드로 커크", "케빈 키어마이어", "어니 클레멘트", "아이재아 카이너-팔레파"]},
        # AL Central
        "Cleveland Guardians": {"pitcher": {"name": "태너 바이비", "p1": "포심 직구", "p2": "고속 슬라이더"}, "lineup": ["스티븐 콴", "안드레스 히메네스", "호세 라미레즈", "조쉬 네일러", "데이비드 프라이", "윌 브레넌", "보 네일러", "브라이언 로키오", "타일러 프리먼"]},
        "Kansas City Royals": {"pitcher": {"name": "콜 레이건스", "p1": "광속구", "p2": "체인지업"}, "lineup": ["마이켈 가르시아", "바비 위트 Jr.", "비니 파스콴티노", "살바도르 페레즈", "헌터 렌프로", "넬슨 벨라스케스", "MJ 멜렌데즈", "카일 이스벨", "가렛 햄슨"]},
        "Detroit Tigers": {"pitcher": {"name": "타릭 스쿠발", "p1": "광속구", "p2": "체인지업"}, "lineup": ["라일리 그린", "맷 비어링", "스펜서 토켈슨", "케리 카펜터", "지오 어셸라", "하비에르 바에즈", "콜트 키스", "제이크 로저스", "파커 메도우스"]},
        "Minnesota Twins": {"pitcher": {"name": "파블로 로페즈", "p1": "포심 직구", "p2": "스위퍼"}, "lineup": ["에두아르도 줄리엔", "카를로스 코레아", "로이스 루이스", "맥스 케플러", "바이런 벅스턴", "카를로스 산타나", "라이언 제퍼스", "윌리 카스트로", "마누엘 마고"]},
        "Chicago White Sox": {"pitcher": {"name": "개럿 크로셰", "p1": "광속구", "p2": "고속 슬라이더"}, "lineup": ["앤드류 베닌텐디", "요안 몬카다", "루이스 로버트 Jr.", "일로이 히메네스", "앤드류 본", "코리 줄스", "폴 데용", "마틴 말도나도", "니키 로페즈"]},
        # AL West
        "Houston Astros": {"pitcher": {"name": "프램버 발데스", "p1": "싱커", "p2": "폭포수 커브"}, "lineup": ["호세 알투베", "카일 터커", "요르단 알바레즈", "알렉스 브레그먼", "제레미 페냐", "야이너 디아즈", "마우리시오 두본", "제이크 마이어스", "호세 아브레유"]},
        "Texas Rangers": {"pitcher": {"name": "네이선 이볼디", "p1": "포심 직구", "p2": "스플리터"}, "lineup": ["마커스 세미엔", "코리 시거", "에반 카터", "아돌리스 가르시아", "조쉬 영", "나다니엘 로우", "조나 하임", "에제키엘 두란", "레오디 타베라스"]},
        "Seattle Mariners": {"pitcher": {"name": "루이스 카스티요", "p1": "포심 직구", "p2": "체인지업"}, "lineup": ["J.P. 크로포드", "훌리오 로드리게스", "칼 롤리", "미치 가버", "미치 해니거", "루크 레일리", "타이 프랑스", "딜런 무어", "조쉬 로하스"]},
        "Los Angeles Angels": {"pitcher": {"name": "호세 소리아노", "p1": "싱커", "p2": "너클 커브"}, "lineup": ["놀란 샤누엘", "마이크 트라웃", "테일러 워드", "미겔 사노", "로건 오하피", "앤서니 렌던", "잭 네토", "조 아델", "루이스 렝히포"]},
        "Oakland Athletics": {"pitcher": {"name": "메이슨 밀러", "p1": "광속구", "p2": "고속 슬라이더"}, "lineup": ["에스테우리 루이즈", "잭 겔로프", "브렌트 루커", "J.D. 데이비스", "세스 브라운", "타일러 소더스트롬", "셰이 랭글리어스", "아브라함 토로", "닉 앨런"]},
        # NL East
        "Atlanta Braves": {"pitcher": {"name": "맥스 프리드", "p1": "포심 직구", "p2": "폭포수 커브"}, "lineup": ["로날드 아쿠냐 Jr.", "아지 알비스", "오스틴 라일리", "맷 올슨", "마르셀 오수나", "마이클 해리스 2세", "션 머피", "자레드 켈닉", "올랜도 아르시아"]},
        "Philadelphia Phillies": {"pitcher": {"name": "잭 휠러", "p1": "포심 직구", "p2": "스위퍼"}, "lineup": ["카일 슈와버", "트레이 터너", "브라이스 하퍼", "J.T. 리얼무토", "알렉 봄", "닉 카스테야노스", "브라이슨 스탓", "에드문도 소사", "요한 로하스"]},
        "New York Mets": {"pitcher": {"name": "센가 코다이", "p1": "포심 직구", "p2": "유령 포크볼"}, "lineup": ["프란시스코 린도어", "피트 알론소", "브랜든 니모", "J.D. 마르티네즈", "제프 맥닐", "스탈링 마르테", "프란시스코 알바레즈", "브렛 베이티", "해리슨 베이더"]},
        "Washington Nationals": {"pitcher": {"name": "매켄지 고어", "p1": "포심 직구", "p2": "폭포수 커브"}, "lineup": ["CJ 에이브람스", "레인 토마스", "제시 윙커", "조이 갤로", "루이스 가르시아", "키버트 루이즈", "일데마로 바르가스", "제이콥 영", "빅터 로블레스"]},
        "Miami Marlins": {"pitcher": {"name": "헤수스 루자르도", "p1": "광속구", "p2": "체인지업"}, "lineup": ["제이콥 아미야", "브라이언 데 라 크루즈", "조쉬 벨", "재즈 치whom Jr.", "헤수스 산체스", "오토 로페즈", "닉 고든", "비달 브루얀", "알리 산체스"]},
        # NL Central
        "Milwaukee Brewers": {"pitcher": {"name": "프레디 페랄타", "p1": "포심 직구", "p2": "고속 슬라이더"}, "lineup": ["잭 트랙", "윌리엄 콘트레라스", "크리스티안 옐리치", "윌리 아다메스", "리스 호스킨스", "브라이스 투랑", "게리 산체스", "잭슨 추리오", "살 프렐릭"]},
        "Chicago Cubs": {"pitcher": {"name": "저스틴 이마나가", "p1": "포심 직구", "p2": "스플리터"}, "lineup": ["이안 햅", "스즈키 세이야", "코디 벨린저", "크리스토퍼 모렐", "댄스비 스완슨", "마이클 부시", "니코 호너", "미겔 아마야", "피트 크로우-암스트롱"]},
        "St. Louis Cardinals": {"pitcher": {"name": "소니 그레이", "p1": "싱커", "p2": "스위퍼"}, "lineup": ["브렌던 도노반", "폴 골드슈미트", "윌슨 콘트레라스", "놀란 아레나도", "알렉 버럴슨", "라스 누트바", "놀란 고먼", "아이반 에레라", "메이신 윈"]},
        "Cincinnati Reds": {"pitcher": {"name": "헌터 그린", "p1": "광속구", "p2": "고속 슬라이더"}, "lineup": ["조나단 인디아", "엘리 데 라 크루즈", "스펜서 스티어", "제이머 칸델라리오", "타일러 스티븐슨", "루크 메일리", "스튜어트 페어차일드", "닉 마티니", "윌 벤슨"]},
        "Pittsburgh Pirates": {"pitcher": {"name": "폴 스킨스", "p1": "광속구", "p2": "스플링커"}, "lineup": ["앤드류 매커친", "브라이언 레이놀즈", "오닐 크루즈", "조이 바트", "로우디 텔레즈", "키브라이언 헤이스", "카이너-팔레파", "데 라 크루즈", "자레드 트리올로"]},
        # NL West
        "Los Angeles Dodgers": {"pitcher": {"name": "야마모토 요시노부", "p1": "포심 직구", "p2": "스플리터"}, "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "T. 에르난데스", "맥스 먼시", "윌 스미스", "가빈 럭스", "토미 에드먼", "미겔 로하스"]},
        "San Diego Padres": {"pitcher": {"name": "딜런 시즈", "p1": "포심 직구", "p2": "고속 슬라이더"}, "lineup": ["루이스 아라에즈", "페르난도 타티스 Jr.", "주릭슨 프로파", "매니 마차도", "잭슨 메릴", "김하성", "잰더 보가츠", "제이크 크로넨워스", "카일 히가시오카"]},
        "San Francisco Giants": {"pitcher": {"name": "로건 웹", "p1": "싱커", "p2": "체인지업"}, "lineup": ["이정후", "맷 채프먼", "마이클 콘포토", "호르헤 솔레어", "타이로 에스트라다", "패트릭 베일리", "마이크 야스트렘스키", "라몬테 웨이드 Jr.", "닉 아메드"]},
        "Arizona Diamondbacks": {"pitcher": {"name": "잭 갤런", "p1": "포심 직구", "p2": "너클 커브"}, "lineup": ["코빈 캐롤", "케텔 마르테", "루어데스 구리엘 Jr.", "크리스찬 워커", "작 피더슨", "에우헤니오 수아레즈", "가브리엘 모레노", "알렉 토마스", "제랄도 페르도모"]},
        "Colorado Rockies": {"pitcher": {"name": "라이언 펠트너", "p1": "포심 직구", "p2": "고속 슬라이더"}, "lineup": ["찰리 블랙몬", "에제키엘 토바", "라이언 맥맨", "엘리아스 디아즈", "놀란 존스", "브렌던 로저스", "제이콥 스탈링스", "샘 힐리어드", "브렌턴 도일"]}
    }
    
    mlb_teams = sorted(list(mlb_data.keys()))

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 900;">⚾ MLB PRO ULTIMATE - TEMPO FIXED</h1>
                <p style="color: #ffb703; margin-top: 10px; font-size: 18px; font-weight: bold;">[초고속 버그 패치] 투구 속도 정상화 및 번트/추가진루 밸런스 완전 수정</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            user_team = st.selectbox("🏃 내 구단 선택", mlb_teams, index=mlb_teams.index("San Diego Padres"))
        with c_right:
            ai_team = st.selectbox("🤖 라이벌 AI 구단", mlb_teams, index=mlb_teams.index("Los Angeles Dodgers"))
            
        if st.button("🏟️ 경기 시작"):
            st.session_state.p_team = user_team
            st.session_state.a_team = ai_team
            st.session_state.p_data = mlb_data[user_team]
            st.session_state.a_data = mlb_data[ai_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_game_screen, col_tactics_panel = st.columns([3.2, 1])

    p_data = st.session_state.p_data
    a_data = st.session_state.a_data

    js_p_lineup = json.dumps(p_data['lineup'], ensure_ascii=False)
    js_a_lineup = json.dumps(a_data['lineup'], ensure_ascii=False)

    with col_tactics_panel:
        st.markdown("### 📊 라인업")
        st.info(f"**⚾ 내 투수:** {p_data['pitcher']['name']}\n\n**1:** {p_data['lineup'][0]}\n**2:** {p_data['lineup'][1]}")
        st.error(f"**🤖 AI 투수:** {a_data['pitcher']['name']}\n\n**1:** {a_data['lineup'][0]}\n**2:** {a_data['lineup'][1]}")
        if st.button("🚪 로비로 돌아가기"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.p_team
        team_a = st.session_state.a_team
        my_pitch1 = p_data['pitcher']['p1']
        my_pitch2 = p_data['pitcher']['p2']

        html_part = f"""
        <div id="game-container" style="background: #0b1329; padding: 15px; border-radius: 14px; border: 2px solid #1c2541; max-width: 760px; margin: 0 auto;">
            
            <div style="background: #020c1b; border: 2px solid #3a86ff; border-radius: 8px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; color: white;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span id="current-turn-badge" style="background: #3a86ff; padding: 4px 8px; border-radius: 4px; font-weight: bold;">1회초 공격</span>
                    <span style="color: #4cc9f0; font-weight: 800;">{team_p}</span> 
                    <span id="score-p" style="font-size: 24px; font-weight: 900; color: #4cc9f0;">0</span> 
                    <span style="color: #64748b;">:</span> 
                    <span id="score-opp" style="font-size: 24px; font-weight: 900; color: #f72585;">0</span> 
                    <span style="color: #f72585; font-weight: 800;">{team_a}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 16px;">B: 0 | S: 0 | O: 0</span>
                </div>
            </div>

            <div style="text-align: center; margin-bottom: 10px;">
                <span style="background: #ffb703; color: #020c1b; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 18px;">
                    현재 타자: <span id="current-batter-name">{p_data['lineup'][0]}</span>
                </span>
            </div>

            <canvas id="baseballField" width="720" height="440" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px; cursor: crosshair;"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px;">
                    <span style="color: white; margin-right: 10px;">마운드: <b>{p_data['pitcher']['name']}</b></span>
                    <button onclick="setPitch('{my_pitch1}')" id="btn-fast" style="background: #d90429; color: white; border: 2px solid #ffffff; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">{my_pitch1} (선택됨)</button>
                    <button onclick="setPitch('{my_pitch2}')" id="btn-change" style="background: #1c2541; color: #a1a1aa; border: 1px solid #4b5563; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer;">{my_pitch2}</button>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">📐 기습 번트 대기</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 15px;">🏃 즉시 도루</button>
                    <button onclick="tryAdvanceBase()" id="btn-advance" style="display: none; background: #e63946; color: white; border: 2px solid #ffffff; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; animation: blinker 1s linear infinite;">🚨 주자 추가 진루 감행!</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-weight: bold; margin-top: 8px; border-left: 6px solid #3a86ff;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 메이저리그 베이스볼 개막합니다! 공을 끝까지 지켜보세요!</span>
            </div>
            <style> @keyframes blinker {{ 50% {{ opacity: 0.5; }} }} </style>
        </div>
        """

        js_part = f"""
        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 }};
            let bases = [false, false, false]; 

            const pLineup = {js_p_lineup};
            const aLineup = {js_a_lineup};
            const aiPitcherName = "{a_data['pitcher']['name']}";
            const aiPitch1 = "{a_data['pitcher']['p1']}";
            const aiPitch2 = "{a_data['pitcher']['p2']}";

            let pBatterIndex = 0; let aBatterIndex = 0;

            // 🕰️ 템포 조정을 위해 구속 대폭 하향 패치 (기존의 1/3 속도로 제어 가능하게 변경)
            const pitchDict = {{
                "포심 직구": {{ speed: 0.007, breakX: 0, breakY: 0 }},
                "광속구": {{ speed: 0.009, breakX: 0, breakY: 0 }}, 
                "고속 슬라이더": {{ speed: 0.006, breakX: 50, breakY: 10 }},
                "스플링커": {{ speed: 0.006, breakX: -20, breakY: 40 }}, 
                "너클 커브": {{ speed: 0.004, breakX: -15, breakY: 60 }}, 
                "폭포수 커브": {{ speed: 0.004, breakX: -15, breakY: 55 }},
                "싱커": {{ speed: 0.006, breakX: -35, breakY: 20 }},
                "스위퍼": {{ speed: 0.005, breakX: 70, breakY: 0 }},
                "체인지업": {{ speed: 0.005, breakX: -15, breakY: 25 }},
                "스플리터": {{ speed: 0.006, breakX: 0, breakY: 45 }},
                "유령 포크볼": {{ speed: 0.005, breakX: 5, breakY: 50 }},
                "커터": {{ speed: 0.006, breakX: 20, breakY: 5 }}
            }};

            let myPitch1 = document.getElementById('btn-fast').innerText.replace(" (선택됨)", "");
            let myPitch2 = document.getElementById('btn-change').innerText;

            let ball = {{ active: false, isHit: false, isBunt: false, x: 360, y: 220, z: 0, tx: 360, ty: 320, size: 2, name: myPitch1 }};
            let selectedPitch = myPitch1;
            
            // 🚨 투구 간 딜레이 대폭 증가 (연속 투구 방지)
            let aiPitchTimer = 120; 
            let isSwung = false; let swingFrame = 0; let buntFrame = 0;
            let isBuntStance = false;

            let fielders = [
                {{ pos: "1B", x: 490, y: 240 }}, {{ pos: "2B", x: 410, y: 170 }}, {{ pos: "SS", x: 310, y: 170 }},
                {{ pos: "3B", x: 230, y: 240 }}, {{ pos: "LF", x: 170, y: 110 }}, {{ pos: "CF", x: 360, y: 90 }}, {{ pos: "RF", x: 550, y: 110 }}
            ];

            function addScore(points) {{
                if (currentMode === "batter") game.pScore += points; else game.oppScore += points;
                document.getElementById('score-p').innerText = game.pScore; document.getElementById('score-opp').innerText = game.oppScore;
            }}

            function nextBatter() {{
                if (currentMode === "batter") {{
                    pBatterIndex = (pBatterIndex + 1) % 9;
                    document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                }} else {{
                    aBatterIndex = (aBatterIndex + 1) % 9;
                    document.getElementById('current-batter-name').innerText = aLineup[aBatterIndex];
                }}
            }}

            function advanceRunners(hitType) {{
                if (hitType === "walk") {{
                    if (bases[0] && bases[1] && bases[2]) {{ addScore(1); }}
                    else if (bases[0] && bases[1]) {{ bases[2] = true; }} else if (bases[0]) {{ bases[1] = true; }}
                    bases[0] = true;
                }} else if (hitType === "single") {{
                    if (bases[2]) {{ addScore(1); bases[2] = false; }} 
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }} 
                    if (bases[0]) {{ bases[1] = true; bases[0] = false; }} 
                    bases[0] = true; 
                }} else if (hitType === "homerun") {{
                    let runs = 1; if (bases[0]) runs++; if (bases[1]) runs++; if (bases[2]) runs++;
                    addScore(runs); bases = [false, false, false]; 
                }}
            }}

            function tryAdvanceBase() {{
                if (game.o >= 3) return;
                document.getElementById('btn-advance').style.display = 'none';
                
                let safe = Math.random() > 0.5; 
                if (safe) {{
                    advanceRunners("single"); 
                    document.getElementById('commentary').innerHTML = `🏃 <b>주자 추가 진루 대성공!!</b> 완벽한 슬라이딩으로 세이프 판정을 받아냅니다!`;
                }} else {{
                    game.o++;
                    if (bases[2]) bases[2] = false;
                    else if (bases[1]) bases[1] = false;
                    else if (bases[0]) bases[0] = false;
                    
                    document.getElementById('commentary').innerHTML = `☠️ <b>태그 아웃!!</b> 무리하게 베이스를 노리다가 저격당했습니다!`;
                    updateInningStatus();
                }}
            }}

            // 📐 번트 메커니즘 전면 리워크
            function triggerBunt() {{
                if (!ball.active || ball.isHit) {{
                    isBuntStance = !isBuntStance;
                    document.getElementById('commentary').innerHTML = isBuntStance ? "📐 <b>번트 자세 장착!</b> 공이 들어올 때 정확히 맞추세요." : "🎙️ 번트 자세를 취소하고 타격형태로 돌아갑니다.";
                    return;
                }}
                if (isBuntStance || !isBuntStance) {{
                    isBuntStance = true;
                    buntFrame = 15;
                    evalBunt();
                }}
            }}

            function evalBunt() {{
                if (ball.active && ball.z >= 0.75 && ball.z <= 0.95) {{
                    ball.isHit = true; ball.isBunt = true;
                    let safe = Math.random() > 0.4;
                    if (safe) {{
                        advanceRunners("single");
                        document.getElementById('commentary').innerHTML = `📐 <b>스퀴즈 번트 성공!</b> 수비진이 당황한 사이 주자 전원 진루!`;
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = `🎙️ 번트가 투수 정면으로 가며 아웃 판정을 받습니다.`;
                    }}
                    nextBatter(); updateInningStatus();
                }} else {{
                    game.s++; ball.active = false;
                    document.getElementById('commentary').innerHTML = `🎙️ 번트 헛방! 타이밍이 맞지 않았습니다.`;
                    updateInningStatus();
                }}
                isBuntStance = false;
            }}

            // 🏃 도루 찬스 보정
            function triggerSteal() {{
                if (!bases[0] && !bases[1]) {{
                    document.getElementById('commentary').innerHTML = "❌ <b>도루 실패:</b> 현재 베이스에 나간 주자가 없습니다!";
                    return;
                }}
                let safe = Math.random() > 0.45;
                if (safe) {{
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }}
                    else if (bases[0]) {{ bases[1] = true; bases[0] = false; }}
                    document.getElementById('commentary').innerHTML = "🏃 <b>도루 성공!</b> 포수의 송구보다 주자의 발이 더 빨랐습니다!";
                }} else {{
                    game.o++;
                    if (bases[1]) bases[1] = false;
                    else if (bases[0]) bases[0] = false;
                    document.getElementById('commentary').innerHTML = "☠️ <b>도루 저지 아웃!</b> 포수의 송구 칼배달!";
                    updateInningStatus();
                }}
            }}

            function setPitch(type) {{
                selectedPitch = type;
                let bf = document.getElementById('btn-fast'); let bc = document.getElementById('btn-change');
                if(type === myPitch1) {{
                    bf.style.background = '#d90429'; bf.style.color = 'white'; bf.style.border = '2px solid white'; bf.innerText = myPitch1 + " (선택됨)";
                    bc.style.background = '#1c2541'; bc.style.color = '#a1a1aa'; bc.style.border = '1px solid #4b5563'; bc.innerText = myPitch2;
                }} else {{
                    bc.style.background = '#f77f00'; bc.style.color = 'white'; bc.style.border = '2px solid white'; bc.innerText = myPitch2 + " (선택됨)";
                    bf.style.background = '#1c2541'; bf.style.color = '#a1a1aa'; bf.style.border = '1px solid #4b5563'; bf.innerText = myPitch1;
                }}
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect(); let mx = e.clientX - rect.left; let my = e.clientY - rect.top;
                
                document.getElementById('btn-advance').style.display = 'none';

                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch; ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; isSwung = false;
                    }}
                }} else {{
                    if (isBuntStance) {{
                        evalBunt();
                        return;
                    }}
                    if (ball.active && !ball.isHit && !isSwung) {{ 
                        isSwung = true; swingFrame = 10; 
                        evalBatterSwing(mx, my);
                    }}
                }}
            }});

            function evalBatterSwing(mx, my) {{
                let hitDist = Math.hypot(mx - ball.x, my - ball.y);
                let timingScore = Math.abs(ball.z - 0.85); 

                if (ball.z >= 0.65 && ball.z <= 1.05) {{
                    if (hitDist <= 35 && timingScore <= 0.08) {{
                        evaluateHitTrajectory("homerun", false);
                    }} 
                    else if (hitDist <= 65 && timingScore <= 0.18) {{
                        evaluateHitTrajectory("good", false);
                    }} 
                    else if (hitDist <= 95) {{
                        evaluateHitTrajectory("poor", false);
                    }} 
                    else {{
                        game.s++; ball.active = false; 
                        document.getElementById('commentary').innerHTML = `🎙️ 헛스윙! 공 근처에 맞추지 못했습니다.`; 
                        updateInningStatus();
                    }}
                }} else {{ 
                    game.s++; ball.active = false; 
                    document.getElementById('commentary').innerHTML = `🎙️ 타이밍 미스 가차없이 헛스윙!`; 
                    updateInningStatus(); 
                }}
            }}

            function evalAiBatter() {{
                if (ball.active && !ball.isHit && !isSwung && ball.z >= 0.75 && ball.z <= 0.90) {{
                    let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                    let willSwing = insideZone ? (Math.random() > 0.4) : (Math.random() > 0.75);

                    if (willSwing) {{
                        isSwung = true; swingFrame = 10;
                        let whiffChance = insideZone ? 0.35 : 0.80; 
                        
                        if (Math.random() < whiffChance) {{
                            document.getElementById('commentary').innerHTML = `🎙️ AI <b>헛스윙 삼진 유도!</b> 멋진 구질이었습니다.`;
                            game.s++; ball.active = false; updateInningStatus();
                        }} else {{
                            let roll = Math.random();
                            if (roll > 0.88) evaluateHitTrajectory("homerun", true);
                            else if (roll > 0.45) evaluateHitTrajectory("good", true);
                            else evaluateHitTrajectory("poor", true);
                        }}
                    }}
                }}
            }}

            function evaluateHitTrajectory(hitQuality, isAiHitter) {{
                ball.isHit = true; ball.isBunt = false;
                let batterName = isAiHitter ? aLineup[aBatterIndex] : pLineup[pBatterIndex];

                if (hitQuality === "homerun") {{
                    ball.tx = 360 + (Math.random() * 200 - 100); ball.ty = -100; 
                    advanceRunners("homerun");
                    document.getElementById('commentary').innerHTML = `🔥 <b>그랜드슬램급 대형 홈런!!!</b> ${{batterName}} 선수의 방망이가 춤을 춥니다!`;
                    nextBatter(); updateInningStatus();
                }} else if (hitQuality === "good") {{
                    ball.tx = 360 + (Math.random() * 300 - 150); ball.ty = 50 + Math.random() * 100; 
                    advanceRunners("single");
                    
                    if (!isAiHitter) {{
                        document.getElementById('commentary').innerHTML = `🎙️ 안타 확정! ${{batterName}} 출루합니다!<br><span style="color:#ffb703; font-size:14px;">👉 [추가 진루 감행] 버튼으로 한 베이스 더 노려보세요!</span>`;
                        document.getElementById('btn-advance').style.display = 'inline-block';
                    }} else {{
                        document.getElementById('commentary').innerHTML = `🎙️ AI 안타 허용! 영리한 타격을 펼칩니다.`;
                    }}
                    nextBatter(); updateInningStatus();
                }} else {{
                    ball.tx = 360 + (Math.random() * 100 - 50); ball.ty = 200; game.o++; 
                    document.getElementById('commentary').innerHTML = `🎙️ 인필드 플라이성 땅볼 아웃입니다! 수비 안정적입니다.`;
                    nextBatter(); updateInningStatus();
                }}
            }}

            function updateInningStatus() {{
                if (game.s >= 3) {{ 
                    game.o++; game.s = 0; game.b = 0; 
                    document.getElementById('commentary').innerHTML = `🎙️ 삼진 아웃!! 공수 교대 카운트가 올라갑니다.`; 
                    nextBatter();
                }}
                if (game.b >= 4) {{ 
                    game.s = 0; game.b = 0; 
                    document.getElementById('commentary').innerHTML = `🎙️ 포어 볼(Walk)! 주자 만루를 향해 밀어냅니다.`; 
                    advanceRunners("walk"); nextBatter();
                }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; bases = [false, false, false]; 
                    document.getElementById('btn-advance').style.display = 'none'; 
                    ball.active = false;
                    
                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비"; document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block'; document.getElementById('batter-controls').style.display = 'none';
                        document.getElementById('current-batter-name').innerText = aLineup[aBatterIndex];
                        document.getElementById('commentary').innerHTML = "🚨 <b>공수교대!</b> 유인구를 던져 타자를 요리하세요!";
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격"; document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none'; document.getElementById('batter-controls').style.display = 'block';
                        document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                        document.getElementById('commentary').innerHTML = `🚨 <b>공수교대!</b> 원하는 포지션에 마우스를 대고 준비하세요.`;
                    }}
                    aiPitchTimer = 150; 
                }}
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 720, 440);
                ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 440);
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.moveTo(0, 440); ctx.lineTo(720, 440); ctx.lineTo(550, 190); ctx.lineTo(170, 190); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#2a9d8f"; ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(480, 260); ctx.lineTo(360, 140); ctx.lineTo(240, 260); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.arc(360, 220, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.fillRect(350, 218, 20, 4);
                ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(370, 370); ctx.lineTo(350, 370); ctx.closePath(); ctx.fill(); 
                ctx.fillRect(475, 255, 12, 12); ctx.fillRect(354, 134, 12, 12); ctx.fillRect(235, 255, 12, 12); 

                ctx.fillStyle = "#ffb703"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 2;
                if (bases[0]) {{ ctx.beginPath(); ctx.arc(481, 261, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }}
                if (bases[1]) {{ ctx.beginPath(); ctx.arc(360, 140, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }}
                if (bases[2]) {{ ctx.beginPath(); ctx.arc(241, 261, 8, 0, Math.PI*2); ctx.fill(); ctx.stroke(); }}

                ctx.fillStyle = "#d90429"; ctx.fillRect(352, 200, 16, 20); 
                fielders.forEach(f => {{
                    ctx.fillStyle = "#023e8a"; ctx.fillRect(f.x - 8, f.y - 10, 16, 12);
                    ctx.fillStyle = "rgba(255,255,255,0.8)"; ctx.font = "11px Arial"; ctx.fillText(f.pos, f.x - 7, f.y + 14);
                }});

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5; ctx.strokeRect(310, 260, 100, 90);
                
                // 🕰️ AI 투수 투구 간 휴식 딜레이 제어
                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        ball.name = Math.random() > 0.5 ? aiPitch1 : aiPitch2;
                        ball.tx = 310 + Math.random() * 100; ball.ty = 260 + Math.random() * 90;
                        ball.x = 360; ball.y = 220; ball.z = 0; ball.size = 2;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; isSwung = false;
                        document.getElementById('commentary').innerHTML = `🤖 투수 <b>${{aiPitcherName}}</b>(이)가 <b>${{ball.name}}</b> 신중하게 투구했습니다!`;
                    }}
                }}

                if (ball.active) {{
                    let pData = pitchDict[ball.name] || pitchDict["포심 직구"];
                    let currentSpeed = ball.isHit ? -0.02 : pData.speed;
                    ball.z += currentSpeed; 
                    
                    if (!ball.isHit) {{
                        let break_factor = Math.pow(ball.z, 2.5); 
                        let base_x = 360 + (ball.tx - 360) * ball.z;
                        let base_y = 220 + (ball.ty - 220) * ball.z;
                        ball.x = base_x + (pData.breakX * break_factor);
                        ball.y = base_y + (pData.breakY * break_factor);
                    }} else {{
                        ball.x = 360 + (ball.tx - 360) * ball.z; ball.y = 220 + (ball.ty - 220) * ball.z;
                    }}
                    
                    if (ball.isHit) {{ ball.size = ball.isBunt ? 4 : Math.max(1, 2.5 + (ball.z * 10)); }} 
                    else {{ ball.size = 2.5 + (Math.pow(ball.z, 3.2) * 20); }}

                    if (!ball.isHit && ball.z > 0.75) {{
                        ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#e63946"; ctx.lineWidth = 3;
                    }} else {{
                        ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    }}
                    
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher" && !ball.isHit) evalAiBatter();

                    if (!ball.isHit && ball.z >= 1.0) {{
                        ball.active = false;
                        let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                        if (insideZone) {{ 
                            game.s++; 
                            document.getElementById('commentary').innerHTML = "🎙️ 스트라이크!";
                        }} else {{ 
                            game.b++;
                            document.getElementById('commentary').innerHTML = "🎙️ 볼!";
                        }}
                        updateInningStatus();
                        aiPitchTimer = 120;
                    }} else if (ball.isHit && (ball.z <= -0.5 || ball.z >= 1.5)) {{ 
                        ball.active = false; aiPitchTimer = 120;
                    }}
                }}

                if (buntFrame > 0) {{
                    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(330, 340); ctx.lineTo(390, 340); ctx.stroke(); buntFrame--;
                }} else if (isBuntStance) {{
                    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 5;
                    ctx.beginPath(); ctx.moveTo(330, 340); ctx.lineTo(390, 340); ctx.stroke();
                }} else if (swingFrame > 0) {{
                    ctx.save(); let angleRatio = (swingFrame / 10) * Math.PI;
                    ctx.translate(400, 350); ctx.rotate(-angleRatio + Math.PI / 3);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 8;
                    ctx.beginPath(); moveTo(0, 0); ctx.lineTo(-80, -20); ctx.stroke(); ctx.restore(); swingFrame--;
                }} else {{
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(395, 340); ctx.lineTo(430, 270); ctx.stroke();
                }}

                requestAnimationFrame(drawScene);
            }}

            drawScene();
        </script>
        """

        full_html = html_part + js_part
        st.components.v1.html(full_html, height=800)

if __name__ == "__main__":
    main()
