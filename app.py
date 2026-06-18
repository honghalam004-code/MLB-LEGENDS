import streamlit as st
import json

def main():
    # =================================================================
    # 1. 다크 모드 기반 방송 송출용 최고급 스타일 가이드
    # =================================================================
    st.set_page_config(page_title="MLB GAMEDAY PRO ENGINE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b0f19; color: #f8fafc; font-family: 'SF Pro Display', -apple-system, sans-serif; }
        .stSelectbox, .stSlider, .stRadio { background: #1e293b !important; color: white !important; border-radius: 12px; border: 1px solid #334155 !important; }
        div[data-baseweb="select"] > div { background-color: #1e293b !important; color: white !important; }
        label { color: #94a3b8 !important; font-weight: 600 !important; }
        h1, h2, h3 { color: #ffffff !important; font-weight: 900 !important; letter-spacing: -1px; }
        .stButton>button {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            color: white !important; font-weight: 800 !important; padding: 14px 28px !important; border-radius: 12px !important;
            border: 1px solid #3b82f6 !important; box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
        }
        .stat-box { background: #131c2e; padding: 16px; border-radius: 14px; border: 1px solid #1e293b; margin-bottom: 12px; }
        </style>
    """, unsafe_allow_html=True)

    # =================================================================
    # 2. 8대 빅마켓 구단 확장 데이터베이스 (9인 풀 라인업)
    # =================================================================
    mlb_roster_db = {
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": ["포심 직구", "스위퍼", "스플리터"], "speed": 101, "control": 82},
                "야마모토 요시노부": {"pitches": ["포심 직구", "명품 커브", "스플리터"], "speed": 97, "control": 93},
                "타일러 글래스노우": {"pitches": ["포심 직구", "파워 슬라이더", "커브"], "speed": 99, "control": 84}
            },
            "lineup": [
                {"name": "무키 베츠", "contact": 94, "power": 78, "number": "50"},
                {"name": "프레디 프리먼", "contact": 95, "power": 83, "number": "5"},
                {"name": "오타니 쇼헤이", "contact": 91, "power": 99, "number": "17"},
                {"name": "테오스카 에르난데스", "contact": 78, "power": 89, "number": "37"},
                {"name": "윌 스미스", "contact": 84, "power": 81, "number": "16"},
                {"name": "맥스 먼시", "contact": 73, "power": 88, "number": "13"},
                {"name": "토미 에드먼", "contact": 82, "power": 66, "number": "25"},
                {"name": "개빈 럭스", "contact": 80, "power": 61, "number": "9"},
                {"name": "앤디 파헤스", "contact": 76, "power": 74, "number": "84"}
            ]
        },
        "NY Yankees (뉴욕 양키스)": {
            "pitchers": {
                "게릿 콜": {"pitches": ["포심 직구", "너클 커브", "파워 슬라이더"], "speed": 99, "control": 92},
                "마커스 스트로먼": {"pitches": ["투심 싱커", "슬라이더", "커터"], "speed": 93, "control": 88},
                "카를로스 로돈": {"pitches": ["포심 직구", "슬라이더", "체인지업"], "speed": 96, "control": 80}
            },
            "lineup": [
                {"name": "글레이버 토레스", "contact": 81, "power": 75, "number": "25"},
                {"name": "후안 소토", "contact": 93, "power": 94, "number": "22"},
                {"name": "애런 저지", "contact": 89, "power": 100, "number": "99"},
                {"name": "재즈 치좀 Jr.", "contact": 79, "power": 82, "number": "13"},
                {"name": "지안카를로 스탠튼", "contact": 71, "power": 96, "number": "27"},
                {"name": "앤서니 볼피", "contact": 78, "power": 68, "number": "11"},
                {"name": "오스틴 웰스", "contact": 77, "power": 72, "number": "28"},
                {"name": "앤서니 리조", "contact": 79, "power": 76, "number": "48"},
                {"name": "알렉스 버두고", "contact": 82, "power": 65, "number": "24"}
            ]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitchers": {
                "딜런 시즈": {"pitches": ["파워 슬라이더", "포심 직구", "너클 커브"], "speed": 99, "control": 81},
                "유 다르빗슈": {"pitches": ["포심 직구", "슬라이더", "스플리터", "커터"], "speed": 95, "control": 89},
                "마이클 킹": {"pitches": ["투심 싱커", "체인지업", "슬라이더"], "speed": 94, "control": 87}
            },
            "lineup": [
                {"name": "루이스 아라에즈", "contact": 99, "power": 45, "number": "4"},
                {"name": "페르난도 타티스 Jr.", "contact": 87, "power": 92, "number": "23"},
                {"name": "주릭슨 프로파", "contact": 84, "power": 78, "number": "10"},
                {"name": "매니 마차도", "contact": 85, "power": 89, "number": "13"},
                {"name": "잭슨 메릴", "contact": 88, "power": 80, "number": "3"},
                {"name": "잰더 보가츠", "contact": 83, "power": 71, "number": "2"},
                {"name": "김하성", "contact": 80, "power": 68, "number": "7"},
                {"name": "카일 히가시오카", "contact": 72, "power": 74, "number": "20"},
                {"name": "타일러 웨이드", "contact": 74, "power": 52, "number": "11"}
            ]
        },
        "Atlanta Braves (애틀랜타 브레이브스)": {
            "pitchers": {
                "스펜서 스트라이더": {"pitches": ["포심 직구", "슬라이더", "체인지업"], "speed": 102, "control": 85},
                "크리스 세일": {"pitches": ["슬라이더", "포심 직구", "체인지업"], "speed": 95, "control": 91}
            },
            "lineup": [
                {"name": "로날드 아쿠냐 Jr.", "contact": 92, "power": 95, "number": "13"},
                {"name": "아지 알비스", "contact": 84, "power": 80, "number": "1"},
                {"name": "오스틴 라일리", "contact": 86, "power": 91, "number": "27"},
                {"name": "맷 올슨", "contact": 81, "power": 96, "number": "28"},
                {"name": "마르셀 오즈나", "contact": 83, "power": 93, "number": "20"},
                {"name": "마이클 해ريس II", "contact": 85, "power": 74, "number": "23"},
                {"name": "션 머피", "contact": 79, "power": 81, "number": "12"},
                {"name": "올란도 아르시아", "contact": 75, "power": 67, "number": "11"},
                {"name": "재러드 켈닉", "contact": 76, "power": 70, "number": "24"}
            ]
        },
        "NY Mets (뉴욕 메츠)": {
            "pitchers": {
                "센가 코다이": {"pitches": ["포심 직구", "고스트 포크", "커터"], "speed": 98, "control": 81},
                "루이스 세베리노": {"pitches": ["포심 직구", "슬라이더", "체인지업"], "speed": 97, "control": 84}
            },
            "lineup": [
                {"name": "프란시스코 린도어", "contact": 88, "power": 86, "number": "12"},
                {"name": "브랜든 니모", "contact": 84, "power": 76, "number": "9"},
                {"name": "피트 알론소", "contact": 77, "power": 97, "number": "20"},
                {"name": "제이디 마르티네즈", "contact": 80, "power": 84, "number": "28"},
                {"name": "제프 맥닐", "contact": 82, "power": 58, "number": "1"},
                {"name": "프란시스코 알바레즈", "contact": 74, "power": 80, "number": "4"},
                {"name": "해리슨 베이더", "contact": 76, "power": 66, "number": "44"},
                {"name": "마크 비엔토스", "contact": 79, "power": 83, "number": "27"},
                {"name": "타이론 테일러", "contact": 75, "power": 68, "number": "15"}
            ]
        },
        "Philadelphia Phillies (필라델피아 필리스)": {
            "pitchers": {
                "잭 휠러": {"pitches": ["포심 직구", "싱커/투심", "스위퍼", "스플리터"], "speed": 99, "control": 94},
                "애런 놀라": {"pitches": ["너클 커브", "싱커/투심", "체인지업"], "speed": 94, "control": 91}
            },
            "lineup": [
                {"name": "카일 슈와버", "contact": 72, "power": 98, "number": "12"},
                {"name": "트레이 터너", "contact": 90, "power": 76, "number": "7"},
                {"name": "브라이스 하퍼", "contact": 89, "power": 95, "number": "3"},
                {"name": "알렉 봄", "contact": 86, "power": 80, "number": "28"},
                {"name": "닉 카스텔야노스", "contact": 79, "power": 82, "number": "8"},
                {"name": "브라이슨 스콧", "contact": 82, "power": 64, "number": "5"},
                {"name": "J.T. 리얼무토", "contact": 81, "power": 75, "number": "10"},
                {"name": "브랜든 마쉬", "contact": 76, "power": 72, "number": "16"},
                {"name": "요한 로하스", "contact": 73, "power": 48, "number": "9"}
            ]
        },
        "Houston Astros (휴스턴 애스트로스)": {
            "pitchers": {
                "프램버 발데스": {"pitches": ["투심 싱커", "명품 커브", "체인지업"], "speed": 96, "control": 86},
                "저스틴 벌랜더": {"pitches": ["포심 직구", "슬라이더", "파워 커브"], "speed": 94, "control": 90}
            },
            "lineup": [
                {"name": "호세 알투베", "contact": 91, "power": 74, "number": "27"},
                {"name": "카일 터커", "contact": 89, "power": 91, "number": "30"},
                {"name": "요단 알바레즈", "contact": 93, "power": 98, "number": "44"},
                {"name": "알렉스 브레그먼", "contact": 85, "power": 79, "number": "2"},
                {"name": "제레미 페냐", "contact": 81, "power": 65, "number": "3"},
                {"name": "야이너 디아즈", "contact": 84, "power": 77, "number": "38"},
                {"name": "존 싱글턴", "contact": 72, "power": 71, "number": "28"},
                {"name": "제이크 마이어스", "contact": 75, "power": 66, "number": "0"},
                {"name": "마우리시오 두본", "contact": 79, "power": 54, "number": "14"}
            ]
        },
        "Seattle Mariners (시애틀 매리너스)": {
            "pitchers": {
                "루이스 카스티요": {"pitches": ["포심 직구", "싱커/투심", "슬라이더"], "speed": 98, "control": 89},
                "조지 커비": {"pitches": ["포심 직구", "슬라이더", "스플리터"], "speed": 97, "control": 97}
            },
            "lineup": [
                {"name": "J.P. 크로포드", "contact": 80, "power": 64, "number": "3"},
                {"name": "훌리오 로드리게스", "contact": 85, "power": 90, "number": "44"},
                {"name": "칼 라일리", "contact": 74, "power": 88, "number": "29"},
                {"name": "랜디 아로자레나", "contact": 78, "power": 81, "number": "56"},
                {"name": "루크 레일리", "contact": 75, "power": 79, "number": "20"},
                {"name": "조시 로하스", "contact": 77, "power": 58, "number": "16"},
                {"name": "딜런 무어", "contact": 73, "power": 69, "number": "25"},
                {"name": "빅터 로블레스", "contact": 81, "power": 55, "number": "10"},
                {"name": "레오 에르난데스", "contact": 71, "power": 62, "number": "2"}
            ]
        }
    }

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # =================================================================
    # 3. [초기 진입 로비 화면] 중계방송 타이틀 락 스크린
    # =================================================================
    if not st.session_state.game_started:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 45px; border-radius: 24px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid #334155; max-width: 900px; margin: 40px auto;">
                <div style="background: #2563eb; color: white; font-family: -apple-system, sans-serif; font-size: 11px; font-weight: 800; display: inline-block; padding: 4px 14px; border-radius: 30px; margin-bottom: 16px; letter-spacing: 1.5px;">ESPN LIVE BROADCAST SYSTEM</div>
                <h1 style="color: #ffffff; margin: 0; font-size: 42px; font-weight:900;">MLB GAMEDAY: <span style="color:#3b82f6;">REAL PITCH</span></h1>
                <p style="color: #94a3b8; margin-top: 10px; font-size: 15px;">8대 빅마켓 구단 풀 라인업 탑재 완료. 실제 포수 각도에서 완벽한 궤적의 핀포인트 제구를 경험하세요.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            away_team_sel = st.selectbox("⚾ AWAY (공격 팀 구단)", list(mlb_roster_db.keys()), index=1)
            st.markdown("<div class='stat-box'><b>📋 1번~9번 타순 라인업 대기 상태</b><br>" + 
                        "<br>".join([f"• {i+1}번: {p['name']} (파워 {p['power']} / 컨택트 {p['contact']})" for i, p in enumerate(mlb_roster_db[away_team_sel]['lineup'][:4])]) + "<br>...이하 하위타선 자동 매운맛 배치 완료</div>", unsafe_allow_html=True)
            
        with col2:
            home_team_sel = st.selectbox("🏠 HOME (수비 팀 구단)", list(mlb_roster_db.keys()), index=0)
            pitcher_sel = st.selectbox("👤 에이스 선발 투수 등판", list(mlb_roster_db[home_team_sel]['pitchers'].keys()))
            p_stat = mlb_roster_db[home_team_sel]['pitchers'][pitcher_sel]
            st.markdown(f"""
                <div class='stat-box' style='border-left: 4px solid #3b82f6;'>
                    <b>📊 {pitcher_sel} 스펙 시트</b><br>
                    • 포심 패스트볼 최고 구속: {p_stat['speed']} mph<br>
                    • 제구 신뢰도 평점: {p_stat['control']} / 100<br>
                    • 구종 레파토리: {', '.join(p_stat['pitches'])}
                </div>
            """, unsafe_allow_html=True)
            
        if st.button("🏟️ BROADCAST START (경기장 중계 연결)", use_container_width=True):
            st.session_state.away_title = away_team_sel.split(" (")[0]
            st.session_state.home_title = home_team_sel.split(" (")[0]
            st.session_state.active_pitcher = pitcher_sel
            st.session_state.pitcher_spec = p_stat
            st.session_state.away_lineup = mlb_roster_db[away_team_sel]['lineup']
            st.session_state.game_started = True
            st.rerun()
        st.stop()

    # =================================================================
    # 4. [메인 대전 마운드] 컨트롤 패널 브릿지
    # =================================================================
    st.markdown(f"### 📡 ESPN LIVE: {st.session_state.away_title} [공격] vs {st.session_state.home_title} [수비]")

    available_pitches = st.session_state.pitcher_spec['pitches']
    base_speed = st.session_state.pitcher_spec['speed']
    base_control = st.session_state.pitcher_spec['control']

    st.markdown("---")
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 2, 2])
    
    with ctrl_col1:
        selected_pitch = st.radio("🔮 볼 배합 선택", available_pitches, horizontal=False)
        
    with ctrl_col2:
        if "직구" in selected_pitch or "싱커" in selected_pitch:
            live_speed = st.slider("🔥 구속 게이지 (mph)", base_speed-5, base_speed, base_speed)
            h_break, v_break = ("싱커" in selected_pitch and (-4.0, 3.5) or (0.0, -2.0))
        elif "슬라이더" in selected_pitch or "스위퍼" in selected_pitch:
            live_speed = st.slider("🔮 횡무브먼트 릴리즈 속도 (mph)", base_speed-11, base_speed-6, base_speed-8)
            h_break, v_break = ("스위퍼" in selected_pitch and (8.5, 0.5) or (5.0, 2.0))
        elif "커브" in selected_pitch:
            live_speed = st.slider("🟢 종무브먼트 낙차 속도 (mph)", base_speed-22, base_speed-15, base_speed-18)
            h_break, v_break = (2.5, 9.0)
        else: # 포크 / 스플리터 / 체인지업
            live_speed = st.slider("💤 오프스피드 종속 제어 (mph)", base_speed-14, base_speed-9, base_speed-11)
            h_break, v_break = (-1.0, 6.5)

    with ctrl_col3:
        live_control = st.slider("🎯 커맨드 핀포인트 집중도", 1, 100, base_control)
        st.markdown(f"""
            <div style="background:#1e293b; padding:12px; border-radius:10px; font-size:13px; color:#94a3b8; border: 1px solid #334155;">
                • <b>제구 집중도가 낮을 때</b> 조준 실패 시 사구 중심부로 몰리는 <b>'실투 아우라'</b>가 연동됩니다.<br>
                • 변화구 궤적에는 릴리즈 포인트마다 <b>물리 스핀 무작위 노이즈</b> 필터가 가동됩니다.
            </div>
        """, unsafe_allow_html=True)

    # =================================================================
    # 5. 리얼 중계방송 그래픽 엔진 통합 캔버스 파이프라인
    # =================================================================
    lineup_json = json.dumps(st.session_state.away_lineup, ensure_ascii=False)

    core_canvas_html = f"""
    <div style="background: #0f172a; padding: 20px; border-radius: 20px; border: 1px solid #1e293b; box-shadow: 0 15px 40px rgba(0,0,0,0.6); max-width: 960px; margin: 0 auto;">
        
        <div style="background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; padding: 10px 24px; margin-bottom: 15px; font-family: monospace; color:#fff;">
            <div>
                <span style="font-weight: 900; letter-spacing:1px; color:#94a3b8;">AWAY</span>
                <span style="font-weight: 900; font-size:18px; color:#fff; margin-left:6px;">{st.session_state.away_title[:3].upper()}</span>
                <span id="txt-away-score" style="background:#ef4444; padding:2px 10px; border-radius:4px; margin-left:10px; font-weight:900;">0</span>
            </div>
            <div style="text-align: center;">
                <span style="color:#3b82f6; font-weight:bold; font-size:12px; letter-spacing:1px; border:1px solid #3b82f6; padding:2px 10px; border-radius:4px;">LIVE GAMEDAY TRACKER</span>
                <div id="txt-bso" style="font-size:14px; font-weight:900; color:#cbd5e1; margin-top:4px;">B○○ S○○ O○○</div>
            </div>
            <div style="text-align: right;">
                <span id="txt-home-score" style="background:#2563eb; padding:2px 10px; border-radius:4px; margin-right:10px; font-weight:900;">0</span>
                <span style="font-weight: 900; font-size:18px; color:#fff;">{st.session_state.home_title[:3].upper()}</span>
                <span style="font-weight: 900; letter-spacing:1px; color:#94a3b8; margin-left:6px;">HOME</span>
            </div>
        </div>

        <canvas id="canvasCore" width="920" height="430" style="background: #090d16; border: 1px solid #334155; border-radius: 10px; display: block; margin: 0 auto; cursor: crosshair;"></canvas>
        
        <div style="background:#131c30; color:#e2e8f0; padding:15px; border-radius:10px; font-size:14px; margin-top:15px; line-height:1.6; border-left:4px solid #3b82f6; font-family: sans-serif;">
            <div style="color:#64748b; font-size:11px; font-weight:bold; letter-spacing:1px; margin-bottom:4px;">🎙️ GAME ANALYST REAL-TIME COMMENTARY</div>
            <div id="broadcast-ticker">야간 조명이 켜진 스타디움입니다. 우측 네온 스트라이크 존 내부의 가상의 포수 미트 타겟을 겨냥 후 마우스를 클릭해 릴리즈 하십시오.</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvasCore');
        const ctx = canvas.getContext('2d');

        const P_NAME = "{st.session_state.active_pitcher}";
        const P_TYPE = "{selected_pitch}";
        const P_SPEED = {live_speed};
        const P_CONTROL = {live_control};
        const P_H_BREAK = {h_break};
        const P_V_BREAK = {v_break};
        const ATTACK_LINEUP = {lineup_json};

        let core = {{
            awayScore: 0, homeScore: 0, b: 0, s: 0, o: 0,
            batterIdx: 0,
            bases: [false, false, false]
        }};

        let pointer = {{ x: 0, y: 0 }};
        let ball = {{ active: false, x: 240, y: 140, tx: 0, ty: 0, time: 0, size: 2.0 }};
        
        // 투구 궤적 잔상 어레이 시스템 (모션 블러 극대화)
        let ballTrail = [];
        let isMistakePitch = false;
        let randomNoiseX = 0;
        let randomNoiseY = 0;
        let history = [];

        // 타구 폭발 효과 레이아웃
        let hitEffect = {{ active: false, x: 0, y: 0, timer: 0, type: "" }};

        canvas.addEventListener('mousemove', (e) => {{
            const bound = canvas.getBoundingClientRect();
            pointer.x = (e.clientX - bound.left) * (canvas.width / bound.width);
            pointer.y = (e.clientY - bound.top) * (canvas.height / bound.height);
        }});

        canvas.addEventListener('mousedown', () => {{
            if (ball.active) return;
            if (pointer.x > 530 && pointer.x < 870 && pointer.y > 50 && pointer.y < 380) {{
                
                // 제구 확률 및 실투 매커니즘 바인딩
                let mistakeChance = (100 - P_CONTROL) * 0.38; 
                isMistakePitch = Math.random() * 100 < mistakeChance;

                if (isMistakePitch) {{
                    // 정가운데 폭탄 실투 강제 고정
                    ball.tx = 700 + (Math.random() - 0.5) * 20;
                    ball.ty = 230 + (Math.random() - 0.5) * 20;
                }} else {{
                    let rngError = (100 - P_CONTROL) * 0.38;
                    ball.tx = pointer.x + (Math.random() - 0.5) * rngError;
                    ball.ty = pointer.y + (Math.random() - 0.5) * rngError;
                }}

                // 변화구 변동 카오스 노이즈 계수 생성
                randomNoiseX = (Math.random() - 0.5) * 3.5;
                randomNoiseY = (Math.random() - 0.5) * 3.5;

                ball.x = 240; ball.y = 140;
                ball.time = 0; ball.size = 2.0;
                ballTrail = [];
                ball.active = true;
                hitEffect.active = false;
            }}
        }});

        function writeTicker(txt, isCritical=false) {{
            const div = document.getElementById('broadcast-ticker');
            let color = isCritical ? "#ef4444" : "#60a5fa";
            div.innerHTML = `<span style="color:${{color}}; font-weight:bold;">[ANALYSIS]</span> ${{txt}}`;
        }}

        function resolveAIPlateAppearance() {{
            const activeBatter = ATTACK_LINEUP[core.batterIdx];
            const insideStrike = (ball.tx >= 610 && ball.tx <= 790 && ball.ty >= 140 && ball.ty <= 320);
            
            let swingProbability = insideStrike ? 0.70 : 0.22;
            if (isMistakePitch) swingProbability = 0.95;

            const didSwing = Math.random() < swingProbability;

            if (didSwing) {{
                let missRate = 0.40 - (activeBatter.contact - 70) * 0.006;
                if (isMistakePitch) missRate = 0.02;

                const didMakeContact = Math.random() > missRate;

                if (didMakeContact) {{
                    let powerWeight = (activeBatter.power - 70) * 0.009;
                    if (isMistakePitch) powerWeight += 0.45; 

                    const hitRoll = Math.random() + powerWeight;

                    // 이펙트 트리거 바인딩
                    hitEffect.active = true;
                    hitEffect.x = ball.x; hitEffect.y = ball.y;
                    hitEffect.timer = 25;

                    if (hitRoll > 1.05) {{
                        hitEffect.type = "HOMERUN";
                        let runs = core.bases.filter(b=>b).length + 1;
                        core.awayScore += runs;
                        core.bases = [false, false, false];
                        core.s = 0; core.b = 0;
                        writeTicker(`💥 [TRACKER] 배트 정중앙 크러시! ${{activeBatter.name}} 선수가 고유 파워(${{activeBatter.power}})를 실어 완벽한 아치를 쏘아 올립니다!`, true);
                    }} else if (hitRoll > 0.40) {{
                        hitEffect.type = "HIT";
                        let scoreIn = core.bases[2] ? 1 : 0;
                        core.bases[2] = core.bases[1]; core.bases[1] = core.bases[0]; core.bases[0] = true;
                        core.awayScore += scoreIn;
                        core.s = 0; core.b = 0;
                        writeTicker(`[HIT] 안타! 외야 우중간을 가르는 날카로운 라인드라이브 타구 패스입니다.`);
                    }} else {{
                        hitEffect.type = "OUT";
                        core.o++; core.s = 0; core.b = 0;
                        writeTicker(`[OUT] 배트 밑동에 맞아 힘없이 뜬 공, 내야수 팝플라이 아웃아웃 처리됩니다.`);
                    }}
                }} else {{
                    core.s++;
                    writeTicker(`[STRIKE] ${{activeBatter.name}} 격렬한 헛스윙! ${{P_NAME}} 선수의 변칙 무브먼트에 타이밍을 완전히 빼앗겼습니다.`);
                }}
            }} else {{
                if (insideStrike) {{
                    core.s++;
                    writeTicker(`[STRIKE] 루킹 스트라이크. 완벽하게 존 하단을 통과하는 보더라인 피칭.`);
                }} else {{
                    core.b++;
                    writeTicker(`[BALL] 정밀하게 골라냅니다. 타자의 시선이 흐트러지지 않았습니다.`);
                }}
            }}

            let next = false;
            if (core.s >= 3) {{ core.o++; core.s = 0; core.b = 0; next = true; writeTicker(`[삼진 아웃] 💥 K-ZONE 모서리를 찌르는 결정구 삼진! 마운드 지배합니다.`, true); }}
            if (core.b >= 4) {{ core.bases[0] = true; core.s = 0; core.b = 0; next = true; writeTicker(`[볼넷 허용] 베이스 출루 허용, 다음 타자와의 전면 승부 유도.`); }}
            if (core.s === 0 && core.b === 0) next = true;

            if (next) core.batterIdx = (core.batterIdx + 1) % 9;
            if (core.o >= 3) {{ core.o = 0; core.s = 0; core.b = 0; core.bases = [false,false,false]; writeTicker(`[🔄 INNING CHANGE] 3아웃 공수교대 공수 로테이션 가동.`, true); }}

            document.getElementById('txt-away-score').innerText = core.awayScore;
            document.getElementById('txt-home-score').innerText = core.homeScore;
            document.getElementById('txt-bso').innerText = `B${{ "●".repeat(core.b) }} S${{ "●".repeat(core.s) }} O${{ "●".repeat(core.o) }}`;
            
            history.push({{ x: ball.tx, y: ball.ty, inside: insideStrike, mistake: isMistakePitch }});
            if (history.length > 10) history.shift();
        }}

        function renderPipeline() {{
            // 캔버스 잔상 제거 및 딥 다크 스페이스 백그라운드 매핑
            ctx.fillStyle = "#090d16"; ctx.fillRect(0,0,920,430);

            // 1. [그래픽 고도화] 야간 경기장 원근 스탠드 렌더링
            let groundGrad = ctx.createLinearGradient(240, 110, 240, 390);
            groundGrad.addColorStop(0, "#064e3b"); groundGrad.addColorStop(1, "#022c22");
            ctx.fillStyle = groundGrad;
            ctx.beginPath(); ctx.moveTo(240, 390); ctx.lineTo(460, 110); ctx.lineTo(20, 110); ctx.closePath(); ctx.fill();

            // 리얼 마운드 텍스처링
            ctx.fillStyle = "#78350f"; ctx.beginPath(); ctx.ellipse(240, 150, 28, 8, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#e2e8f0"; ctx.fillRect(232, 149, 16, 2);

            // 루상 다이아몬드 미니 트래커 렌더링
            const drawProBase = (bx, by, isAct) => {{
                ctx.fillStyle = isAct ? "#3b82f6" : "#334155";
                ctx.strokeStyle = isAct ? "#60a5fa" : "#475569";
                ctx.lineWidth = 2;
                ctx.save(); ctx.translate(bx, by); ctx.rotate(45 * Math.PI / 180);
                ctx.fillRect(-7, -7, 14, 14); ctx.strokeRect(-7, -7, 14, 14); ctx.restore();
            }};
            drawProBase(320, 240, core.bases[0]);
            drawProBase(240, 145, core.bases[1]);
            drawProBase(160, 240, core.bases[2]);

            // 정밀 오각형 3D 원근 홈플레이트
            ctx.fillStyle = "#f8fafc"; ctx.shadowColor = "rgba(0,0,0,0.5)"; ctx.shadowBlur = 6;
            ctx.beginPath(); ctx.moveTo(240, 355); ctx.lineTo(256, 367); ctx.lineTo(256, 377); ctx.lineTo(224, 377); ctx.lineTo(224, 367); ctx.fill();
            ctx.shadowBlur = 0;

            // 정밀 축소 투수 피규어 실루엣
            ctx.fillStyle = "#f1f5f9"; ctx.beginPath(); ctx.arc(240, 136, 5, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#94a3b8"; ctx.fillRect(237, 141, 6, 9);

            // 좌측 타자 텍스트 매트릭스 보드
            const activeB = ATTACK_LINEUP[core.batterIdx];
            ctx.fillStyle = "#ffffff"; ctx.font = "bold 13px sans-serif";
            ctx.fillText(`${{core.batterIdx+1}}번 타자: [NO.${{activeB.number}}] ${{activeB.name}}`, 30, 345);
            ctx.fillStyle = "#64748b"; ctx.font = "12px sans-serif";
            ctx.fillText(`CONTACT: ${{activeB.contact}} | POWER: ${{activeB.power}}`, 30, 365);

            // 성인 연령대 느낌의 세련된 다크 솔리드 타자 실루엣
            ctx.fillStyle = "rgba(30, 41, 59, 0.9)"; ctx.beginPath(); ctx.arc(190, 330, 10, 0, Math.PI*2); ctx.fill();
            ctx.fillRect(185, 340, 12, 30);
            ctx.strokeStyle = "#b45309"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(190, 335); ctx.lineTo(215, 305); ctx.stroke();

            // 중앙 방송 경계벽 분할 처리
            ctx.strokeStyle = "#1e293b"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(480, 10); ctx.lineTo(480, 420); ctx.stroke();

            // 2. [우측 메인 피드] 고해상도 하이테크 K-ZONE 설계
            ctx.fillStyle = "rgba(15, 23, 42, 0.6)"; ctx.fillRect(540, 40, 340, 350); // 백그라운드 차폐 플레이트
            
            // 반투명 보더 네온 스트라이크 존
            ctx.fillStyle = "rgba(59, 130, 246, 0.04)"; ctx.fillRect(610, 140, 180, 180);
            ctx.strokeStyle = "#3b82f6"; ctx.lineWidth = 3.5; ctx.strokeRect(610, 140, 180, 180);
            
            // 스트라이크 9분할 인덱스 스케치
            ctx.strokeStyle = "rgba(59, 130, 246, 0.15)"; ctx.lineWidth = 1;
            for(let i=1; i<3; i++) {{
                ctx.beginPath(); ctx.moveTo(610 + (i * 60), 140); ctx.lineTo(610 + (i * 60), 320); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(610, 140 + (i * 60)); ctx.lineTo(790, 140 + (i * 60)); ctx.stroke();
            }}
            // 아웃존 경계 바운더리 점선 처리
            ctx.strokeStyle = "#334155"; ctx.setLineDash([4, 4]); ctx.strokeRect(550, 60, 300, 310); ctx.setLineDash([]);

            // 마우스 크로스헤어 포수 미트 서클 동기화
            if (!ball.active && pointer.x > 530 && pointer.x < 870) {{
                ctx.strokeStyle = "rgba(234, 88, 12, 0.8)"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(pointer.x, pointer.y, 14, 0, Math.PI*2); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(pointer.x - 20, pointer.y); ctx.lineTo(pointer.x + 20, pointer.y);
                ctx.moveTo(pointer.x, pointer.y - 20); ctx.lineTo(pointer.x, pointer.y + 20); ctx.stroke();
            }}

            // 피칭 히트맵 히스토리 인디케이터 투사
            history.forEach(h => {{
                ctx.fillStyle = h.mistake ? "#f59e0b" : (h.inside ? "#10b981" : "#ef4444");
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(h.x, h.y, 8, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            }});

            // 3. [리얼 물리학 기반] 다이내믹 피치 3D 비행 연산 기믹
            if (ball.active) {{
                ball.time += 0.052; // 프레임 속도 동기화
                
                let lx = 240 + (ball.tx - 240) * ball.time;
                let ly = 138 + (ball.ty - 138) * ball.time;
                
                ball.size = 2.0 + (Math.pow(ball.time, 2.8) * 12.5); // 포수 전면 도달 시 볼 크기 역대급 팽창

                let tFactor = Math.pow(ball.time, 2);
                ball.x = lx + ((P_H_BREAK + randomNoiseX) * tFactor * 1.6);
                ball.y = ly + ((P_V_BREAK + randomNoiseY) * tFactor * 1.6);

                // 현재 좌표를 잔상 스택에 바인딩
                ballTrail.push({{ x: ball.x, y: ball.y, size: ball.size }});
                if (ballTrail.length > 5) ballTrail.shift();

                // 모션 블러 잔상 이펙트 가시화 드로잉
                ballTrail.forEach((t, idx) => {{
                    ctx.fillStyle = `rgba(255, 255, 255, ${{0.15 * (idx + 1)}})`;
                    ctx.beginPath(); ctx.arc(t.x, t.y, t.size * 0.9, 0, Math.PI * 2); ctx.fill();
                }});

                // 만약 실투일 경우 타오르는 고열의 경고 아우라 이펙트 마운팅
                if (isMistakePitch) {{
                    ctx.shadowColor = "#ef4444"; ctx.shadowBlur = 15;
                    ctx.fillStyle = "#ef4444"; ctx.font = "black 14px sans-serif";
                    ctx.fillText("⚠️ HANGING PITCH (실투 몰림!)", ball.x - 50, ball.y - 25);
                }}

                // 실물 질감의 화이트 베이스볼 드로잉
                ctx.fillStyle = "#f8fafc"; ctx.strokeStyle = "#334155"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
                ctx.shadowBlur = 0;

                if (ball.time >= 1.0) {{
                    ball.active = false;
                    resolveAIPlateAppearance();
                }}
            }}

            // 타격 폭발 히트 이펙트 파이프라인
            if (hitEffect.active && hitEffect.timer > 0) {{
                hitEffect.timer--;
                ctx.fillStyle = hitEffect.type === "HOMERUN" ? "rgba(234, 179, 8, 0.4)" : "rgba(255, 255, 255, 0.4)";
                ctx.beginPath(); ctx.arc(hitEffect.x, hitEffect.y, (25 - hitEffect.timer) * 3, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 20px sans-serif";
                ctx.fillText(hitEffect.type, hitEffect.x - 40, hitEffect.y - 10);
            }}

            requestAnimationFrame(renderPipeline);
        }}
        renderPipeline();
    </script>
    """

    st.components.v1.html(core_canvas_html, height=630)

    if st.button("🔄 EXIT CURRENT MATCH (다른 구단 및 라이벌 매치 구성하기)"):
        st.session_state.game_started = False
        st.rerun()

if __name__ == "__main__":
    main()
