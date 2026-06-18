import streamlit as st
import json

def main():
    # =================================================================
    # 1. 묵직한 중계화면 스타일 가이드
    # =================================================================
    st.set_page_config(page_title="MLB PRO: HIGH-DYNAMIC TRAJECTORY", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #070a12; color: #f1f5f9; font-family: 'Segoe UI', Roboto, sans-serif; }
        .stSelectbox, .stRadio { background: #111827 !important; color: white !important; border-radius: 12px; border: 1px solid #374151 !important; }
        div[data-baseweb="select"] > div { background-color: #111827 !important; color: white !important; }
        .stSlider { background: transparent !important; }
        label { color: #9ca3af !important; font-weight: 700 !important; font-size: 14px !important; }
        h1, h2, h3 { color: #ffffff !important; font-weight: 900 !important; letter-spacing: -1px; }
        .stButton>button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important; font-weight: 900 !important; padding: 16px 32px !important; border-radius: 12px !important;
            border: 1px solid #3b82f6 !important; box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4);
            font-size: 16px !important;
        }
        .stat-box { background: #0f172a; padding: 16px; border-radius: 14px; border: 1px solid #1e293b; margin-bottom: 12px; }
        </style>
    """, unsafe_allow_html=True)

    # =================================================================
    # 2. MLB 8대 빅마켓 구단 연동 데이터베이스
    # =================================================================
    mlb_roster_db = {
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": ["포심 직구", "스위퍼", "스플리터"], "speed": 101, "control": 82},
                "야마모토 요시노부": {"pitches": ["포심 직구", "명품 커브", "스플리터"], "speed": 97, "control": 93}
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
                "게릿 콜": {"pitches": ["포심 직구", "너클 커브", "파워 슬라이더"], "speed": 99, "control": 92}
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
                "유 다르빗슈": {"pitches": ["포심 직구", "슬라이더", "스플리터"], "speed": 95, "control": 89}
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
                "스펜서 스트라이더": {"pitches": ["포심 직구", "슬라이더"], "speed": 102, "control": 85}
            },
            "lineup": [
                {"name": "로날드 아쿠냐 Jr.", "contact": 92, "power": 95, "number": "13"},
                {"name": "아지 알비스", "contact": 84, "power": 80, "number": "1"},
                {"name": "오스틴 라일리", "contact": 86, "power": 91, "number": "27"},
                {"name": "맷 올슨", "contact": 81, "power": 96, "number": "28"},
                {"name": "마르셀 오즈나", "contact": 83, "power": 93, "number": "20"},
                {"name": "마이클 해리스 II", "contact": 85, "power": 74, "number": "23"},
                {"name": "션 머피", "contact": 79, "power": 81, "number": "12"},
                {"name": "올란도 아르시아", "contact": 75, "power": 67, "number": "11"},
                {"name": "재러드 켈닉", "contact": 76, "power": 70, "number": "24"}
            ]
        },
        "NY Mets (뉴욕 메츠)": {
            "pitchers": { "센가 코다이": {"pitches": ["포심 직구", "고스트 포크"], "speed": 98, "control": 81} },
            "lineup": [ {"name": "프란시스코 린도어", "contact": 88, "power": 86, "number": "12"}, {"name": "브랜든 니모", "contact": 84, "power": 76, "number": "9"}, {"name": "피트 알론소", "contact": 77, "power": 97, "number": "20"}, {"name": "제이디 마르티네즈", "contact": 80, "power": 84, "number": "28"}, {"name": "제프 맥닐", "contact": 82, "power": 58, "number": "1"}, {"name": "프란시스코 알바레즈", "contact": 74, "power": 80, "number": "4"}, {"name": "해리슨 베이더", "contact": 76, "power": 66, "number": "44"}, {"name": "마크 비엔토스", "contact": 79, "power": 83, "number": "27"}, {"name": "타이론 테일러", "contact": 75, "power": 68, "number": "15"} ]
        },
        "Philadelphia Phillies (필라델피아 필리스)": {
            "pitchers": { "잭 휠러": {"pitches": ["포심 직구", "스위퍼"], "speed": 99, "control": 94} },
            "lineup": [ {"name": "카일 슈와버", "contact": 72, "power": 98, "number": "12"}, {"name": "트레이 터너", "contact": 90, "power": 76, "number": "7"}, {"name": "브라이스 하퍼", "contact": 89, "power": 95, "number": "3"}, {"name": "알렉 봄", "contact": 86, "power": 80, "number": "28"}, {"name": "닉 카스텔야노스", "contact": 79, "power": 82, "number": "8"}, {"name": "브라이슨 스콧", "contact": 82, "power": 64, "number": "5"}, {"name": "J.T. 리얼무토", "contact": 81, "power": 75, "number": "10"}, {"name": "브랜든 마쉬", "contact": 76, "power": 72, "number": "16"}, {"name": "요한 로하스", "contact": 73, "power": 48, "number": "9"} ]
        },
        "Houston Astros (휴스턴 애스트로스)": {
            "pitchers": { "프램버 발데스": {"pitches": ["투심 싱커", "명품 커브"], "speed": 96, "control": 86} },
            "lineup": [ {"name": "호세 알투베", "contact": 91, "power": 74, "number": "27"}, {"name": "카일 터커", "contact": 89, "power": 91, "number": "30"}, {"name": "요단 알바레즈", "contact": 93, "power": 98, "number": "44"}, {"name": "알렉스 브레그먼", "contact": 85, "power": 79, "number": "2"}, {"name": "제레미 페냐", "contact": 81, "power": 65, "number": "3"}, {"name": "야이너 디아즈", "contact": 84, "power": 77, "number": "38"}, {"name": "존 싱글턴", "contact": 72, "power": 71, "number": "28"}, {"name": "제이크 마이어스", "contact": 75, "power": 66, "number": "0"}, {"name": "마URI시오 두본", "contact": 79, "power": 54, "number": "14"} ]
        },
        "Seattle Mariners (시애틀 매리너스)": {
            "pitchers": { "조지 커비": {"pitches": ["포심 직구", "스플리터"], "speed": 97, "control": 97} },
            "lineup": [ {"name": "J.P. 크로포드", "contact": 80, "power": 64, "number": "3"}, {"name": "훌리오 로드리게스", "contact": 85, "power": 90, "number": "44"}, {"name": "칼 라일리", "contact": 74, "power": 88, "number": "29"}, {"name": "랜디 아로자레나", "contact": 78, "power": 81, "number": "56"}, {"name": "루크 레일리", "contact": 75, "power": 79, "number": "20"}, {"name": "조시 로하스", "contact": 77, "power": 58, "number": "16"}, {"name": "딜런 무어", "contact": 73, "power": 69, "number": "25"}, {"name": "빅터 로블레스", "contact": 81, "power": 55, "number": "10"}, {"name": "레오 에르난데스", "contact": 71, "power": 62, "number": "2"} ]
        }
    }

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # =================================================================
    # 3. 로비 화면
    # =================================================================
    if not st.session_state.game_started:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #111827 0%, #1f2937 100%); padding: 40px; border-radius: 20px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5); border: 1px solid #374151; max-width: 880px; margin: 40px auto;">
                <div style="background: #eab308; color: #111827; font-size: 11px; font-weight: 800; display: inline-block; padding: 3px 12px; border-radius: 4px; margin-bottom: 12px; letter-spacing: 1px;">MLB GAMEDAY HD V2</div>
                <h1 style="color: #ffffff; margin: 0; font-size: 38px;">PRO BALLISTIC: <span style="color:#3b82f6;">시소 스탯 & 3D 포물선</span></h1>
                <p style="color: #9ca3af; margin-top: 8px;">구속을 높이면 제구가 무너지고, 제구를 높이면 구속이 감소합니다. 휘어 감기는 입체 궤적을 확인하세요.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            away_team_sel = st.selectbox("⚾ AWAY (공격 팀)", list(mlb_roster_db.keys()), index=1)
            st.markdown("<div class='stat-box'><b>📋 1번~9번 타선 연동 스펙</b><br>" + "<br>".join([f"• {i+1}번: {p['name']} (파워 {p['power']})" for i, p in enumerate(mlb_roster_db[away_team_sel]['lineup'][:3])]) + "</div>", unsafe_allow_html=True)
            
        with col2:
            home_team_sel = st.selectbox("🏠 HOME (수비 팀)", list(mlb_roster_db.keys()), index=0)
            pitcher_sel = st.selectbox("👤 등판 선발 투수", list(mlb_roster_db[home_team_sel]['pitchers'].keys()))
            p_stat = mlb_roster_db[home_team_sel]['pitchers'][pitcher_sel]
            st.markdown(f"<div class='stat-box'><b>📊 에이스 베이스 라인</b><br>• 기본 구속: {p_stat['speed']} mph<br>• 기본 제구: {p_stat['control']}</div>", unsafe_allow_html=True)
            
        if st.button("🏟️ LIVE MATCH ENTER", use_container_width=True):
            st.session_state.away_title = away_team_sel.split(" (")[0]
            st.session_state.home_title = home_team_sel.split(" (")[0]
            st.session_state.active_pitcher = pitcher_sel
            st.session_state.pitcher_spec = p_stat
            st.session_state.away_lineup = mlb_roster_db[away_team_sel]['lineup']
            st.session_state.game_started = True
            st.rerun()
        st.stop()

    # =================================================================
    # 4. [시소 시스템 구현] 구속 vs 제구 상호 억제 다이내믹 밸런서
    # =================================================================
    st.markdown(f"### 📡 LIVE TRACKING: {st.session_state.away_title} vs {st.session_state.home_title}")
    st.markdown("---")

    selected_pitch = st.radio("🔮 결정구 선택", st.session_state.pitcher_spec['pitches'], horizontal=True)

    # 핵심: 구속-제구 트레이드 오프 슬라이더 (하나를 올리면 하나가 떨어짐)
    st.markdown("#### ⚖️ 피칭 스타일 밸런서 (구속 vs 제구 시소 시스템)")
    balance_ratio = st.slider("◀ 구속 극대화 (전력 투구) | 정밀 제구 (보더라인 커맨드) ▶", 0, 100, 50, help="왼쪽으로 갈수록 구속 폭등+제구 폭망, 오른쪽으로 갈수록 구속 감소+칼제구")

    # 시소 로직에 의한 실시간 스탯 재계산
    max_capable_speed = st.session_state.pitcher_spec['speed'] + 3
    min_capable_speed = st.session_state.pitcher_spec['speed'] - 15

    # 비율에 맞춰 구속과 제구가 서로를 깎아내림
    live_speed = int(max_capable_speed - (balance_ratio / 100.0) * (max_capable_speed - min_capable_speed))
    live_control = int(5 + (balance_ratio / 100.0) * 92)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"<div style='background:#1e1b4b; padding:10px; border-radius:8px; text-align:center;'>🔥 실시간 출력 구속: <b style='font-size:20px; color:#60a5fa;'>{live_speed} mph</b></div>", unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"<div style='background:#062f25; padding:10px; border-radius:8px; text-align:center;'>🎯 실시간 제구 집중력: <b style='font-size:20px; color:#34d399;'>{live_control} / 100</b></div>", unsafe_allow_html=True)

    # 구종별 회전 무브먼트 값 세팅
    if "직구" in selected_pitch or "싱커" in selected_pitch:
        h_break, v_break = ("싱커" in selected_pitch and (-5.0, 4.0) or (0.0, -3.0))
    elif "슬라이더" in selected_pitch or "스위퍼" in selected_pitch:
        h_break, v_break = ("스위퍼" in selected_pitch and (12.0, 1.0) or (7.0, 3.5))
    elif "커브" in selected_pitch:
        h_break, v_break = (3.5, 12.0)
    else: # 포크 / 스플리터
        h_break, v_break = (-1.5, 9.5)

    # =================================================================
    # 5. [사진 싱크로 100%] 3D 입체 휘어짐 포물선 그래픽 엔진 캔버스
    # =================================================================
    lineup_json = json.dumps(st.session_state.away_lineup, ensure_ascii=False)

    core_canvas_html = f"""
    <div style="background: #090d16; padding: 15px; border-radius: 16px; border: 1px solid #1f2937; max-width: 960px; margin: 0 auto;">
        
        <div style="background: #111827; border: 1px solid #2d3748; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; margin-bottom: 12px; font-family: monospace; color:#fff;">
            <div>
                <span style="font-weight: 900; color:#9ca3af;">{st.session_state.away_title[:3].upper()}</span>
                <span id="txt-away-score" style="background:#ef4444; padding:1px 8px; border-radius:3px; margin-left:6px; font-weight:900;">0</span>
            </div>
            <div>
                <div id="txt-bso" style="font-size:13px; font-weight:900; color:#e5e7eb; letter-spacing:1px;">B○○ S○○ O○○</div>
            </div>
            <div>
                <span id="txt-home-score" style="background:#2563eb; padding:1px 8px; border-radius:3px; margin-right:6px; font-weight:900;">0</span>
                <span style="font-weight: 900; color:#9ca3af;">{st.session_state.home_title[:3].upper()}</span>
            </div>
        </div>

        <canvas id="canvasCore" width="920" height="420" style="background: #040711; border: 1px solid #374151; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
        
        <div style="background:#0f172a; color:#9ca3af; padding:12px; border-radius:8px; font-size:13px; margin-top:12px; border-left:4px solid #ef4444; font-family:sans-serif;">
            <div id="broadcast-ticker"><b>[ESPN 라이브 궤적 분석]</b> 우측 K-ZONE을 클릭하세요. 마운드에서부터 홈플레이트까지 거대한 3D 아치 포물선 궤적이 그어집니다.</div>
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

        let core = {{ awayScore: 0, homeScore: 0, b: 0, s: 0, o: 0, batterIdx: 0, bases: [false, false, false] }};
        let pointer = {{ x: 0, y: 0 }};
        let ball = {{ active: false, x: 240, y: 150, tx: 0, ty: 0, time: 0, size: 2 }};
        
        // 정밀 잔상 추적 어레이 (사진 속 파란색 실시간 입체 궤적선 동기화 전용)
        let ballTrail = [];
        let isMistakePitch = false;
        let randomNoiseX = 0, randomNoiseY = 0;
        let history = [];

        canvas.addEventListener('mousemove', (e) => {{
            const bound = canvas.getBoundingClientRect();
            pointer.x = (e.clientX - bound.left) * (canvas.width / bound.width);
            pointer.y = (e.clientY - bound.top) * (canvas.height / bound.height);
        }});

        canvas.addEventListener('mousedown', () => {{
            if (ball.active) return;
            if (pointer.x > 530 && pointer.x < 870 && pointer.y > 40 && pointer.y < 380) {{
                
                // 제구 수치 역산으로 실투 및 오차 계산
                let mistakeChance = (100 - P_CONTROL) * 0.45;
                isMistakePitch = Math.random() * 100 < mistakeChance;

                if (isMistakePitch) {{
                    ball.tx = 700 + (Math.random() - 0.5) * 15;
                    ball.ty = 220 + (Math.random() - 0.5) * 15;
                }} else {{
                    let rngError = (100 - P_CONTROL) * 0.45;
                    ball.tx = pointer.x + (Math.random() - 0.5) * rngError;
                    ball.ty = pointer.y + (Math.random() - 0.5) * rngError;
                }}

                // 사진처럼 다이내믹한 요동을 치게 만드는 변화구 강력 카오스 노이즈
                randomNoiseX = (Math.random() - 0.5) * 6.0;
                randomNoiseY = (Math.random() - 0.5) * 6.0;

                ball.x = 240; ball.y = 150;
                ball.time = 0; ball.size = 2;
                ballTrail = [];
                ball.active = true;
            }}
        }});

        function writeTicker(txt) {{
            document.getElementById('broadcast-ticker').innerHTML = `<b>[LIVE ANALYST]</b> ${{txt}}`;
        }}

        function resolveAIPlateAppearance() {{
            const activeBatter = ATTACK_LINEUP[core.batterIdx];
            const insideStrike = (ball.tx >= 610 && ball.tx <= 790 && ball.ty >= 130 && ball.ty <= 310);
            
            let swingProb = insideStrike ? 0.72 : 0.20;
            if (isMistakePitch) swingProb = 0.95;

            if (Math.random() < swingProb) {{
                let missRate = 0.38 - (activeBatter.contact - 70) * 0.005;
                if (isMistakePitch) missRate = 0.01;

                if (Math.random() > missRate) {{
                    let powerWeight = (activeBatter.power - 70) * 0.008;
                    if (isMistakePitch) powerWeight += 0.50; 
                    const roll = Math.random() + powerWeight;

                    if (roll > 1.05) {{
                        let runs = core.bases.filter(b=>b).length + 1; core.awayScore += runs;
                        core.bases = [false, false, false]; core.s = 0; core.b = 0;
                        writeTicker(`💥 <span style="color:#ef4444; font-weight:bold;">장외 홈런 폭발!</span> ${{activeBatter.name}}이 몰린 공을 제대로 받아쳐 스탠드 상단을 부숩니다! (${{P_SPEED}} mph)`);
                    }} else if (roll > 0.40) {{
                        let scoreIn = core.bases[2] ? 1 : 0;
                        core.bases[2] = core.bases[1]; core.bases[1] = core.bases[0]; core.bases[0] = true;
                        core.awayScore += scoreIn; core.s = 0; core.b = 0;
                        writeTicker(`[안타] 배트 중심에 저스트 미트, 주자들 진루에 성공합니다.`);
                    }} else {{
                        core.o++; core.s = 0; core.b = 0; writeTicker(`[범타 아웃] 고수위 변화구의 회전력에 밀려 내야 플라이 아웃.`);
                    }}
                }} else {{
                    core.s++; writeTicker(`[헛스윙] 무시무시한 볼끝 횡무브먼트에 허공을 가르는 스윙.`);
                }}
            }} else {{
                if (insideStrike) {{ core.s++; writeTicker(`[스트라이크] 존 모서리를 찌르는 완벽한 밸런싱 로케이션.`); }}
                else {{ core.b++; writeTicker(`[볼] 바깥쪽으로 예리하게 빠져나가는 유인구.`); }}
            }}

            if (core.s >= 3) {{ core.o++; core.s = 0; core.b = 0; writeTicker(`[삼진!!] 완벽한 속임수 완급조절로 이닝 스토퍼 가동.`); }}
            if (core.b >= 4) {{ core.bases[0] = true; core.s = 0; core.b = 0; writeTicker(`[볼넷 출루] 베이스를 채웁니다.`); }}
            if (core.s === 0 && core.b === 0) core.batterIdx = (core.batterIdx + 1) % 9;
            if (core.o >= 3) {{ core.o = 0; core.s = 0; core.b = 0; core.bases = [false,false,false]; writeTicker(`[🔄 공수교대] 쓰리아웃 잔루 정산 완료.`); }}

            document.getElementById('txt-away-score').innerText = core.awayScore;
            document.getElementById('txt-home-score').innerText = core.homeScore;
            document.getElementById('txt-bso').innerText = `B${{ "●".repeat(core.b) }} S${{ "●".repeat(core.s) }} O${{ "●".repeat(core.o) }}`;
            
            history.push({{ x: ball.tx, y: ball.ty, inside: insideStrike, mistake: isMistakePitch }});
            if (history.length > 8) history.shift();
        }}

        function renderPipeline() {{
            ctx.fillStyle = "#040711"; ctx.fillRect(0,0,920,420);

            // 1. 야간 구장 스탠드 원근 모델링
            ctx.fillStyle = "#064e3b"; ctx.beginPath(); ctx.moveTo(240, 380); ctx.lineTo(440, 120); ctx.lineTo(40, 120); ctx.closePath(); ctx.fill();
            ctx.fillStyle = "#541c15"; ctx.beginPath(); ctx.ellipse(240, 150, 24, 7, 0, 0, Math.PI*2); ctx.fill();

            // 미니 주자 상황판
            const dBase = (bx, by, act) => {{
                ctx.fillStyle = act ? "#3b82f6" : "#1e293b"; ctx.save(); ctx.translate(bx, by); ctx.rotate(45*Math.PI/180); ctx.fillRect(-6,-6,12,12); ctx.restore();
            }};
            dBase(300, 230, core.bases[0]); dBase(240, 145, core.bases[1]); dBase(180, 230, core.bases[2]);

            // 리얼 포수 뒤 시점 홈플레이트
            ctx.fillStyle = "#f8fafc"; ctx.beginPath(); ctx.moveTo(240, 350); ctx.lineTo(254, 362); ctx.lineTo(254, 372); ctx.lineTo(226, 372); ctx.lineTo(226, 362); ctx.fill();

            // 센터 디바이더 월
            ctx.strokeStyle = "#111827"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(470, 0); ctx.lineTo(470, 420); ctx.stroke();

            // 2. 우측 3D 하이테크 네온 스트라이크 존 리빌딩
            ctx.fillStyle = "rgba(17, 24, 39, 0.8)"; ctx.fillRect(550, 40, 320, 340);
            ctx.strokeStyle = "rgba(59, 130, 246, 0.4)"; ctx.lineWidth = 1; ctx.strokeRect(550, 40, 320, 340);
            
            // 핵심 메인 스트라이크 존 네온 박스
            ctx.fillStyle = "rgba(59, 130, 246, 0.05)"; ctx.fillRect(610, 130, 180, 180);
            ctx.strokeStyle = "#3b82f6"; ctx.lineWidth = 3; ctx.strokeRect(610, 130, 180, 180);

            // 포수 조준 크로스헤어 미트 타겟팅
            if (!ball.active && pointer.x > 530 && pointer.x < 870) {{
                ctx.strokeStyle = "#ea580c"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(pointer.x, pointer.y, 14, 0, Math.PI*2); ctx.stroke();
            }}

            // 기존 히트맵 마킹
            history.forEach(h => {{
                ctx.fillStyle = h.mistake ? "#fbbf24" : (h.inside ? "#10b981" : "#ef4444");
                ctx.beginPath(); ctx.arc(h.x, h.y, 7, 0, Math.PI*2); ctx.fill();
            }});

            // 3. [스크린샷 100% 동기화] 거대한 3D 아치 포물선 물리 비행 구현 엔진
            if (ball.active) {{
                ball.time += 0.042; // 구속 변환 스케일러 반영

                // 단순 직선이 아니라 사진처럼 위/옆으로 크게 한바퀴 포물선을 그리며 다가오게 만드는 아크 보정 함수
                // 시간축(time)이 흐름에 따라 사인 곡선 형태의 거대한 휘어짐 궤도를 생성합니다.
                let arcX = Math.sin(ball.time * Math.PI) * 45.0; // 옆으로 거대하게 휘어짐
                let arcY = -Math.sin(ball.time * Math.PI) * 25.0; // 위로 볼록하게 포물선 비행

                // 종속 베이스라인 원근 선형 보간
                let lx = 240 + (ball.tx - 240) * ball.time;
                let ly = 150 + (ball.ty - 150) * ball.time;

                // 포수 미트 도달 시 극대화되는 3D 원근 렌즈 보정
                ball.size = 2.0 + (Math.pow(ball.time, 3.2) * 16.5);

                // 최종 변환 좌표에 물리 브레이킹 팩터와 포물선 아크 세팅 결합
                let breakFactor = Math.pow(ball.time, 2.5);
                ball.x = lx + arcX + ((P_H_BREAK + randomNoiseX) * breakFactor * 2.2);
                ball.y = ly + arcY + ((P_V_BREAK + randomNoiseY) * breakFactor * 2.2);

                // 사진 속 가메데이 궤적 전용 잔상 스택 적재
                ballTrail.push({{ x: ball.x, y: ball.y, size: ball.size }});

                // [사진 효과 완벽 재현] 지나온 모든 발자취를 파란색 연결 네온 트랙으로 화면에 실시간 잔영 유지 드로잉
                ctx.beginPath();
                ctx.strokeStyle = isMistakePitch ? "rgba(239, 68, 68, 0.4)" : "rgba(96, 165, 250, 0.5)";
                ctx.lineWidth = 4;
                for (let i = 0; i < ballTrail.length; i++) {{
                    if (i === 0) ctx.moveTo(ballTrail[i].x, ballTrail[i].y);
                    else ctx.lineTo(ballTrail[i].x, ballTrail[i].y);
                }}
                ctx.stroke();

                // 개별 볼 도트 선명도 그라데이션
                ballTrail.forEach((t, index) => {{
                    ctx.fillStyle = isMistakePitch ? `rgba(239, 68, 68, ${{0.08 * index}})` : `rgba(59, 130, 246, ${{0.08 * index}})`;
                    ctx.beginPath(); ctx.arc(t.x, t.y, t.size * 0.8, 0, Math.PI * 2); ctx.fill();
                }});

                if (isMistakePitch) {{
                    ctx.fillStyle = "#ef4444"; ctx.font = "bold 13px sans-serif";
                    ctx.fillText("⚠️ 실투 (한가운데)", ball.x - 40, ball.y - 20);
                }}

                // 리얼 야구공 드로잉
                ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#1e293b"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

                if (ball.time >= 1.0) {{
                    ball.active = false;
                    resolveAIPlateAppearance();
                }}
            }}

            requestAnimationFrame(renderPipeline);
        }}
        renderPipeline();
    </script>
    """

    st.components.v1.html(core_canvas_html, height=600)

    if st.button("🔄 타순 변경 및 구단 재설정 (로비로 가기)"):
        st.session_state.game_started = False
        st.rerun()

if __name__ == "__main__":
    main()
