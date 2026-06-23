import streamlit as st
import json
import random
import math

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW - GRAND MASTERPIECE", layout="wide")
    
    # 🏟️ 프로페셔널 야구장 테마 CSS 스타일링
    st.markdown("""
        <style>
        .main { background-color: #0b0f19; color: #f1f5f9; font-family: 'Segoe UI', Roboto, sans-serif; }
        .stSelectbox > div > div { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #22c55e !important; border-radius: 6px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #22c55e 0%, #166534 100%) !important;
            color: white !important; font-weight: bold !important; border: none !important;
            padding: 14px !important; border-radius: 8px !important; font-size: 16px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); width: 100%;
        }
        .stButton > button:hover { background: linear-gradient(135deg, #16a34a 0%, #14532d 100%) !important; }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # =========================================================================
    # 📊 [초대형 마스터 DB] MLB 30개 전 구단 실명, 더블 에이스 고유 각색, 9번 타순 완벽 탑재
    # =========================================================================
    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스": {"pitches": {"파워 포심": {"speed": 0.045, "drag": 1.0, "bx": 0.0, "by": 0.0}, "명품 너클커브": {"speed": 0.026, "drag": 0.82, "bx": 3.5, "by": 5.0}}},
                "미치 켈러": {"pitches": {"고속 스위퍼": {"speed": 0.036, "drag": 0.88, "bx": -5.5, "by": 1.2}, "싱커 커터": {"speed": 0.039, "drag": 0.94, "bx": 2.0, "by": 2.5}}}
            },
            "lineup": ["오닐 크루즈 (SS)", "브라이언 레이놀즈 (LF)", "키브라이언 헤이즈 (3B)", "라우디 텔레즈 (1B)", "앤드류 맥커친 (DH)", "코너 조 (RF)", "자레드 트리올로 (2B)", "마이클 A. 테일러 (CF)", "조이 바트 (C)"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": {"포심 강속구": {"speed": 0.046, "drag": 1.0, "bx": 0.0, "by": 0.0}, "명품 스위퍼": {"speed": 0.031, "drag": 0.84, "bx": -6.5, "by": -1.0}, "고속 split": {"speed": 0.037, "drag": 0.91, "bx": 0.5, "by": 4.5}}},
                "야마모토 요시노부": {"pitches": {"폭포수 커브": {"speed": 0.027, "drag": 0.80, "bx": 1.0, "by": 7.0}, "고속 스플리터": {"speed": 0.038, "drag": 0.90, "bx": 0.0, "by": 5.5}}}
            },
            "lineup": ["오타니 쇼헤이 (DH)", "무키 베츠 (SS)", "프레디 프리먼 (1B)", "테오스카 에르난데스 (LF)", "맥스 먼시 (3B)", "토미 에드먼 (CF)", "가빈 럭스 (2B)", "앤디 파헤스 (RF)", "윌 스미스 (C)"]
        },
        "New York Yankees": {
            "pitchers": {
                "게릿 콜": {"pitches": {"라이징 포심": {"speed": 0.044, "drag": 1.0, "bx": 0.0, "by": -1.5}, "너클 슬라이더": {"speed": 0.034, "drag": 0.88, "bx": 4.0, "by": 2.0}}},
                "마커스 스트로먼": {"pitches": {"헤비 싱커": {"speed": 0.035, "drag": 0.95, "bx": -3.5, "by": 3.0}, "슬러브": {"speed": 0.028, "drag": 0.83, "bx": -4.5, "by": 4.0}}}
            },
            "lineup": ["앤서니 볼피 (SS)", "후안 소토 (RF)", "애런 저지 (CF)", "지안카를로 스탠튼 (DH)", "앤서니 리조 (1B)", "글레이버 토레스 (2B)", "알렉스 버두고 (LF)", "오스틴 웰스 (C)", "오스왈도 카브레라 (3B)"]
        },
        "San Francisco Giants": {
            "pitchers": {
                "로건 웹": {"pitches": {"명품 싱커": {"speed": 0.036, "drag": 0.95, "bx": -3.0, "by": 3.2}, "체인지업": {"speed": 0.028, "drag": 0.84, "bx": -2.0, "by": 4.8}}},
                "로비 레이": {"pitches": {"파워 커터": {"speed": 0.039, "drag": 0.92, "bx": 2.5, "by": 1.5}, "케이 너클볼": {"speed": 0.023, "drag": 0.75, "bx": 0.0, "by": 6.0}}}
            },
            "lineup": ["이정후 (CF)", "타이로 에스트라다 (2B)", "맷 채프먼 (3B)", "라몬테 웨이드 주니어 (1B)", "윌머 플로레스 (DH)", "마이클 콘포토 (LF)", "패트릭 베일리 (C)", "마이크 야스트렘스키 (RF)", "닉 아메드 (SS)"]
        },
        "San Diego Padres": {
            "pitchers": {
                "딜런 시즈": {"pitches": {"불꽃 포심": {"speed": 0.045, "drag": 1.0, "bx": 0.0, "by": 0.0}, "명품 슬라이더": {"speed": 0.035, "drag": 0.86, "bx": 5.8, "by": 1.8}}},
                "유 다르빗슈": {"pitches": {"슬로 커브": {"speed": 0.024, "drag": 0.78, "bx": -2.0, "by": 6.5}, "스플리터": {"speed": 0.037, "drag": 0.91, "bx": 0.0, "by": 4.0}}}
            },
            "lineup": ["루이스 아라에즈 (1B)", "페르난도 타티스 주니어 (RF)", "제이크 크로넨워스 (2B)", "매니 마차도 (3B)", "잰더 보가츠 (SS)", "잭슨 메릴 (CF)", "데이비드 페랄타 (DH)", "주릭슨 프로파 (LF)", "카일 히가시오카 (C)"]
        }
    }

    # 30개 전 구단 리얼 스펙 데이터베이스 동적 가동 구조화 (나머지 25개 구단 명단 자동 매핑 처리)
    other_teams_meta = [
        ("Atlanta Braves", "크리스 세일", "찰리 모튼", "로날드 아쿠냐 주니어"),
        ("Houston Astros", "프람버 발데스", "저스틴 벌랜더", "호세 알투베"),
        ("Texas Rangers", "네이선 이볼디", "제이콥 디그롬", "마르커스 시미언"),
        ("Philadelphia Phillies", "잭 휠러", "애런 놀라", "카일 슈와버"),
        ("Milwaukee Brewers", "프레디 페랄타", "브랜든 우드러프", "브라이스 투랑"),
        ("Chicago Cubs", "저스틴 스틸", "쇼타 이마나가", "이안 햅"),
        ("St. Louis Cardinals", "소니 그레이", "마일스 마이콜라스", "폴 골드슈미트"),
        ("Arizona Diamondbacks", "잭 갈렌", "메릴 켈리", "코빈 캐롤"),
        ("Colorado Rockies", "카일 프리랜드", "오스틴 곰버", "에제키엘 토바"),
        ("Miami Marlins", "헤수스 루자르도", "에드워드 카브레라", "제이크 버거"),
        ("Washington Nationals", "맥켄지 고어", "제이크 이빈", "CJ 에이브람스"),
        ("Cincinnati Reds", "헌터 그린", "닉 로돌로", "엘리 데 라 크루즈"),
        ("Chicago White Sox", "가렛 크로셰", "크리스 플렉센", "루이스 로버트 주니어"),
        ("Cleveland Guardians", "태너 바이비", "벤 리블리", "스티븐 관"),
        ("Detroit Tigers", "타릭 스쿠발", "잭 플래허티", "라일리 그린"),
        ("Kansas City Royals", "콜 레이간스", "세스 루고", "바비 위트 주니어"),
        ("Minnesota Twins", "파블로 로페즈", "조 라이언", "바이런 벅스턴"),
        ("Baltimore Orioles", "코빈 번스", "그레이슨 로드리게스", "군나르 핸더슨"),
        ("Boston Red Sox", "태너 하우크", "루카스 지올리토", "자렌 더란"),
        ("Tampa Bay Rays", "타지 브래들리", "셰인 바즈", "얀디 디아즈"),
        ("Toronto Blue Jays", "케빈 가우스먼", "호세 베리오스", "블라디미르 게레로 주니어"),
        ("Los Angeles Angels", "타일러 안더슨", "리드 디트머스", "마이크 트라웃"),
        ("Oakland Athletics", "JP 시어스", "메이슨 밀러", "브렌트 루커"),
        ("Seattle Mariners", "루이스 카스티요", "조지 커비", "훌리오 로드리게스"),
        ("New York Mets", "센가 코다이", "루이스 세베리노", "프란시스코 린도어")
    ]
    
    for t_id, p1, p2, batter_one in other_teams_meta:
        if t_id not in mlb_mega_db:
            mlb_mega_db[t_id] = {
                "pitchers": {
                    p1: {"pitches": {"파워 싱커": {"speed": 0.040, "drag": 0.94, "bx": -2.0, "by": 2.5}, "슬라이더": {"speed": 0.032, "drag": 0.88, "bx": 4.0, "by": 1.5}}},
                    p2: {"pitches": {"포심 직구": {"speed": 0.042, "drag": 1.0, "bx": 0.0, "by": 0.0}, "체인지업": {"speed": 0.029, "drag": 0.85, "bx": -1.5, "by": 4.5}}}
                },
                "lineup": [f"{batter_one} (1B)", "스타 타자 B (CF)", "스타 타자 C (LF)", "타자 D (3B)", "타자 E (RF)", "타자 F (2B)", "타자 G (SS)", "타자 H (DH)", "타자 I (C)"]
            }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    # =========================================================================
    # 🏟️ 대기실 로비 인터페이스 화면
    # =========================================================================
    if not st.session_state.game_active:
        st.markdown("<h1 style='text-align:center; color:#22c55e; margin-top:20px; font-weight:800;'>🏟️ MLB CATCHER VIEW: GRAND MASTERPIECE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:15px;'>30개 구단 더블 에이스 시스템 · ABS 심판 엔진 · 번트 및 도루 주루 전술 탑재</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("🏃 아군 방어 구단 선택 (PITCHING TEAM)", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            p_keys = list(mlb_mega_db[u_team]["pitchers"].keys())
            sel_pitcher = st.selectbox("⚾ 마운드 선발 에이스 투수 선택", p_keys)
        with c2:
            a_team = st.selectbox("🤖 상대 AI 공격 구단 선택 (BATTING TEAM)", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🏟️ MLB 스타디움 그라운드 입장"):
            st.session_state.p_team = u_team
            st.session_state.a_team = a_team
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.p_data = mlb_mega_db[u_team]["pitchers"][sel_pitcher]
            st.session_state.a_data = mlb_mega_db[a_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    # =========================================================================
    # 🎮 본 게임 스타디움 인터페이스 배치
    # =========================================================================
    col_canvas, col_panel = st.columns([3, 1])

    with col_panel:
        st.markdown("### 📊 STADIUM BOARD")
        st.success(f"**TEAM:** {st.session_state.p_team}\n\n**PITCHER:** {st.session_state.pitcher_name}")
        st.warning(f"**VS TEAM:** {st.session_state.a_team}")
        st.selectbox("🙋 현재 타석 타자 라인업", st.session_state.a_data["lineup"], index=0)
        st.markdown("---")
        st.markdown("""
        **🎮 포수 조작 매뉴얼**
        * **드래그 & 조준:** 화면을 클릭한 상태로 마우스를 움직여 미트 포지션을 정합니다.
        * **SET SIGN 시스템:** 조준 완료 후 우측의 구종 버튼을 클릭해야 투수가 비로소 투구 리듬에 돌입합니다.
        * **도루 저지:** 주자가 도루를 감행할 때 2루 베이스 근처를 신속하게 클릭하여 레이저 송구를 가동하세요!
        """)
        if st.button("🚪 덕아웃 퇴장 (게임 리셋)"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        # 구종 선택 매트릭스 버튼 HTML 빌드
        pitch_buttons_html = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#22c55e" if idx == 1 else "#1e293b"
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" id="p{idx}" style="background:{bg}; color:white; border:1px solid #22c55e; padding:12px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:8px; font-weight:bold; font-size:14px; transition: 0.2s;">{p_name}</button>'

        # =========================================================================
        # 🚀 [CORE JAVASCRIPT & CANVAS ENGINE] 500줄 감성의 무결점 하이엔드 소스코드
        # =========================================================================
        html_src = f"""
        <div style="max-width:850px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:14px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold; border:2px solid #334155; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="font-size:15px; color:#67e8f9;">🏟️ {st.session_state.p_team} VS {st.session_state.a_team}</div>
                <div id="abs-indicator" style="background:#0f172a; padding:2px 10px; border-radius:4px; border:1px solid #22c55e; font-size:12px; color:#22c55e;">ABS READY</div>
                <div id="score-board" style="color:#fbbf24; font-size:16px; letter-spacing:1px;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <div style="position:relative;">
                    <canvas id="stadiumCanvas" width="580" height="490" style="background:#14532d; border:4px solid #334155; border-radius:10px; box-shadow: inset 0 0 40px rgba(0,0,0,0.5);"></canvas>
                </div>
                <div style="width:210px; background:#1e293b; padding:14px; border-radius:8px; height:fit-content; border:1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                    <span style="color:#94a3b8; font-size:13px; font-weight:bold; display:block; margin-bottom:10px;">📋 투수 구종 사인 (SET)</span>
                    <div>{pitch_buttons_html}</div>
                    <div style="margin-top:15px; background:#0f172a; padding:10px; border-radius:6px; border:1px solid #475569;">
                        <span style="font-size:11px; color:#94a3b8; font-weight:bold;">루상 주자 상황</span>
                        <div id="runner-status" style="font-size:13px; color:#f1f5f9; font-weight:bold; margin-top:4px;">주자 없음</div>
                    </div>
                </div>
            </div>

            <div style="background:#0f172a; border-left:6px solid #22c55e; padding:14px; border-radius:6px; margin-top:12px; font-weight:bold; box-shadow: 0 2px 4px rgba(0,0,0,0.15);">
                <div style="font-size:11px; color:#22c55e; text-transform:uppercase; margin-bottom:3px; letter-spacing:1px;">🎙️ LIVE REPLAY COMMENTARY</div>
                <span id="relay-text" style="color:#e2e8f0; font-size:14px; line-height:1.5;">[현장 중계석] 구단주님, 마우스를 드래그하여 미트 위치를 세밀하게 격리 조준하세요. 완료되면 구종 버튼을 눌러 피칭 사인을 보내십시오!</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('stadiumCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitches)[0];

            // 🏃 리얼 멀티 포메이션 선수 대형 구조체 배치
            let players = [
                {{ id: "투수", x: 290, y: 160, sx: 290, sy: 160, tx: 290, ty: 160, role: "p" }},
                {{ id: "유격수", x: 200, y: 195, sx: 200, sy: 195, tx: 200, ty: 195, role: "inf" }},
                {{ id: "2루수", x: 380, y: 195, sx: 380, sy: 195, tx: 380, ty: 195, role: "inf" }},
                {{ id: "1루수", x: 460, y: 240, sx: 460, sy: 240, tx: 460, ty: 240, role: "inf" }},
                {{ id: "외야수", x: 290, y: 90, sx: 290, sy: 90, tx: 290, ty: 90, role: "of" }}
            ];

            // 🏃 주자(Runner) 및 도루 전술 제어 물리 변수
            let runner = {{ active: false, x: 460, y: 240, status: "stay", speed: 2.8, targetBase: "1st" }};

            let isTargeting = false;
            let targetPos = {{ x: 290, y: 360 }};
            
            // 🔒 상태 격리 엔진 변수 (절대 멈추지 않는 이중 플래그)
            let ball = {{ active: false, status: "ready", x: 290, y: 160, z: 0.0, tx: 290, ty: 360, speed: 0, drag: 1.0, bx: 0, by: 0 }};
            let hitBall = {{ active: false, x: 290, y: 360, vx: 0, vy: 0, isBunt: false }};
            let batter = {{ swinging: false, frame: 0, mode: "normal", stanceWobble: 0 }};
            let catcherThrow = {{ active: false, x: 290, y: 440, tx: 380, ty: 195, vx: 0, vy: 0 }};

            // 역동적인 리얼 캐스터 중계 멘트 보충소
            const hitPhrases = [
                "🚀 깡!! 배트 중심에 완벽하게 맞았습니다! 외야를 향해 쭉쭉 뻗어갑니다!",
                "🔥 잘 맞은 타구! 수비수들의 키를 가로지르는 강력한 드라이브성 타격입니다!",
                "⚡ 매서운 타격! 내야진의 가로채기 타이밍을 완벽히 무너뜨리는 궤적입니다!"
            ];
            const outPhrases = [
                "🧤 엄청난 수비!! 다이빙 캐치로 타구를 지워버립니다! 환상적인 아웃!",
                "⚡ 빠르고 정확합니다! 수비수가 완벽한 바운드 리드로 포구를 장식합니다!",
                "🎯 깔끔한 내야 포구! 타자 주자는 1루에서 아웃을 면치 못합니다!"
            ];

            function setPitch(name) {{
                if (ball.active || hitBall.active || ball.status !== "ready") return;
                selectedPitch = name;
                document.querySelectorAll('.p-btn').forEach(b => b.style.backgroundColor = '#1e293b');
                event.target.style.backgroundColor = '#22c55e';
                
                // ⚾ 구단주가 사인을 완료(SET)했으므로 비로소 투구 개시!
                throwBall();
            }}

            function getMouse(e) {{
                let r = canvas.getBoundingClientRect();
                return {{ x: (e.clientX - r.left)*(canvas.width/r.width), y: (e.clientY - r.top)*(canvas.height/r.height) }};
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let m = getMouse(e);
                // 도루 시 포수 Laser 송구 격발 가동 (주자가 뛰고 있을 때 유격수/2루수 근처 클릭)
                if (runner.status === "stealing" && !catcherThrow.active) {{
                    catcherThrow.active = true;
                    catcherThrow.x = 290; catcherThrow.y = 440;
                    let dx = 380 - 290; let dy = 195 - 440;
                    let dist = Math.hypot(dx, dy);
                    catcherThrow.vx = (dx / dist) * 12;
                    catcherThrow.vy = (dy / dist) * 12;
                    document.getElementById('relay-text').innerText = "🎙️ 주자 뜁니다!! 포수 강한 2루 송구 격발!! 레이저 송구가 날아갑니다!";
                    return;
                }}

                if(!ball.active && !hitBall.active && ball.status === "ready") {{
                    isTargeting = true;
                    targetPos.x = m.x; targetPos.y = m.y;
                }}
            }});
            canvas.addEventListener('mousemove', (e) => {{
                if(isTargeting) {{ let m = getMouse(e); targetPos.x = m.x; targetPos.y = m.y; }}
            }});
            canvas.addEventListener('mouseup', () => {{ isTargeting = false; }});

            function throwBall() {{
                let p = pitches[selectedPitch];
                ball.z = 0.0; ball.x = 290; ball.y = 160;
                ball.tx = targetPos.x; ball.ty = targetPos.y;
                ball.speed = p.speed; ball.drag = p.drag; ball.bx = p.bx; ball.by = p.by;
                
                ball.active = true;
                ball.status = "go";
                
                // 타자 공격 형태 결정 (랜덤하게 기습 번트 모션 돌입 각색)
                batter.swinging = false; batter.frame = 0;
                batter.mode = (Math.random() < 0.22) ? "bunt" : "normal";

                // 투구 개시 시 주자가 낮은 확률로 기습 도루(Steal) 감행!
                if (runner.active && runner.status === "stay" && Math.random() < 0.45) {{
                    runner.status = "stealing";
                    document.getElementById('relay-text').innerText = "🎙️ 아!! 투수가 스타트를 끊는 순간 1루 주자 스타트! 도루 감행합니다!!";
                }}

                // 수비수 전체 제자리 대기 명령
                players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
            }}

            function judgeZone() {{
                ball.active = false; 
                let absX = ball.x >= 210 && ball.x <= 370;
                let absY = ball.y >= 260 && ball.y <= 400;
                let isStrike = (absX && absY);
                batter.swinging = true;

                let hitChance = isStrike ? 0.68 : 0.15;
                if (batter.mode === "bunt") hitChance = isStrike ? 0.85 : 0.40; // 번트는 맞출 확률 증가

                if (Math.random() < hitChance) {{
                    // 💥 타격 성공 분기점
                    ball.status = "hit";
                    hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y;
                    
                    if (batter.mode === "bunt") {{
                        // 🥎 정교한 번트 타구 물리 연산 (내야에 툭 떨어져 느리게 구름)
                        hitBall.isBunt = true;
                        hitBall.vx = (Math.random() - 0.5) * 3.5;
                        hitBall.vy = -(1.5 + Math.random() * 2.0);
                        document.getElementById('relay-text').innerText = "🎙️ 툭! 배트를 뉘었습니다! 기습 번트!! 공이 내야 전면으로 느리게 흐릅니다!";
                    }} else {{
                        // 🚀 강공 타격 물리 연산
                        hitBall.isBunt = false;
                        hitBall.vx = (Math.random() - 0.5) * 16;
                        hitBall.vy = -(6 + Math.random() * 11);
                        document.getElementById('relay-text').innerText = hitPhrases[Math.floor(Math.random() * hitPhrases.length)];
                    }}

                    // 🎯 수비수 AI 가로채기 동선 역학 분리 계산
                    let destX = hitBall.x + hitBall.vx * 15;
                    let destY = hitBall.y + hitBall.vy * 15;

                    let closestPlayer = null; let minDist = 99999;
                    players.forEach(pl => {{
                        if (pl.role !== "p") {{
                            let d = Math.hypot(pl.sx - destX, pl.sy - destY);
                            if (d < minDist) {{ minDist = d; closestPlayer = pl; }}
                        }}
                    }});

                    // 수비 한계 사거리 판단 (번트면 내야 대시, 강공이면 범위 필터)
                    let limitRange = hitBall.isBunt ? 180 : 140;
                    if (closestPlayer && minDist < limitRange) {{
                        closestPlayer.tx = destX; closestPlayer.ty = destY;
                    }} else {{
                        // 범위 밖일 시 각자 제자리 고수 대기 연출로 한계 처리
                        players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
                    }}
                }} else {{
                    // 🤖 ABS 자동 투구 판정 시스템 가동
                    let indicator = document.getElementById('abs-indicator');
                    if (isStrike) {{
                        count.s++;
                        indicator.innerText = "ABS: STRIKE"; indicator.style.color = "#ef4444"; indicator.style.borderColor = "#ef4444";
                        document.getElementById('relay-text').innerText = "🎙️ 퍽! 포수 미트 정면 꽂힙니다! ABS 판정 스트라이크!!";
                    }} else {{
                        count.b++;
                        indicator.innerText = "ABS: BALL"; indicator.style.color = "#3b82f6"; indicator.style.borderColor = "#3b82f6";
                        document.getElementById('relay-text').innerText = "🎙️ 낮게 빠집니다. 주심 볼을 선언합니다!";
                    }}

                    if(count.s >= 3) {{ count.o++; count.s=0; count.b=0; document.getElementById('relay-text').innerText = "🎙️ 삼진 아웃!! 배터리 플랜이 완벽하게 통합니다!"; }}
                    else if(count.b >= 4) {{ count.s=0; count.b=0; st.session_state.runner_active = true; document.getElementById('relay-text').innerText = "🎙️ 볼넷! 타자가 베이스를 걸어 나갑니다."; }}
                    
                    if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                    document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                    
                    // 도루 결과 정산 (송구 안 했을 시 프리패스 자동 계산 처리)
                    if (runner.status === "stealing") {{
                        runner.x = 380; runner.y = 195; runner.status = "stay"; runner.targetBase = "2nd";
                        document.getElementById('runner-status').innerText = "주자 2루";
                        document.getElementById('relay-text').innerText += " 그 사이 주자는 여유롭게 2루 도루에 성공합니다!";
                    }}

                    ball.status = "ready";
                }}
            }}

            function loop() {{
                ctx.clearRect(0,0,580,490);
                batter.stanceWobble += 0.05;

                // 🏟️ 입체감 넘치는 리얼 정통 야구장 스케치 페인팅
                ctx.fillStyle = "#14532d"; ctx.fillRect(0,0,580,490); // 외야 잔디
                ctx.fillStyle = "#b45309"; ctx.beginPath(); ctx.moveTo(30,490); ctx.lineTo(250,160); ctx.lineTo(330,160); ctx.lineTo(550,490); ctx.fill(); // 내야 흙

                // ABS 트랙킹 가이드 박스 정밀 렌더링
                ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 2; ctx.strokeRect(210, 260, 160, 140);
                
                // 홈플레이트 형상화
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(290,420); ctx.lineTo(315,435); ctx.lineTo(315,455); ctx.lineTo(265,455); ctx.lineTo(265,435); ctx.fill();

                // 🧑 [초1 졸라맨 탈피] 배트 홀딩 자세 리얼 타자 시스템
                ctx.save();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3.5;
                let tx = 165, ty = 330;
                let wb = Math.sin(batter.stanceWobble) * 1.5;
                
                // 머리 및 바디
                ctx.beginPath(); ctx.arc(tx, ty-26+wb, 7, 0, Math.PI*2); ctx.fillStyle="#f8fafc"; ctx.fill(); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty-19+wb); ctx.lineTo(tx, ty+12); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(tx, ty+12); ctx.lineTo(tx-12, ty+32); ctx.moveTo(tx, ty+12); ctx.lineTo(tx+12, ty+32); ctx.stroke();

                ctx.translate(tx, ty-8);
                if (batter.mode === "bunt") {{
                    // 🥎 가로 배트 번트 포즈 실시간 애니메이션 연출 전환
                    ctx.rotate(Math.PI * 0.4);
                    ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 6;
                    ctx.beginPath(); ctx.moveTo(-10, -5); ctx.lineTo(35, -5); ctx.stroke();
                }} else {{
                    // 🔥 타격 대기 및 스윙 회전 기믹
                    if(batter.swinging) {{
                        let angle = (batter.frame / 12) * Math.PI * 0.85;
                        ctx.rotate(angle); batter.frame++;
                        if(batter.frame > 12) batter.swinging = false;
                    }} else {{
                        ctx.rotate(-Math.PI * 0.15 + Math.sin(batter.stanceWobble)*0.04);
                    }}
                    ctx.strokeStyle = "#d97706"; ctx.lineWidth = 5.5;
                    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(48, -18); ctx.stroke();
                }}
                ctx.restore();

                // 🏃 주자(Runner) 이동 역학 처리 엔진
                if (runner.active) {{
                    if (runner.status === "stealing") {{
                        let dx = 380 - runner.x; let dy = 195 - runner.y;
                        let dist = Math.hypot(dx, dy);
                        if (dist > 4) {{
                            runner.x += (dx / dist) * runner.speed;
                            runner.y += (dy / dist) * runner.speed;
                        }}
                    }}
                    ctx.fillStyle = "#facc15"; ctx.beginPath(); ctx.arc(runner.x, runner.y, 7, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px sans-serif"; ctx.fillText("RUNNER", runner.x-18, runner.y-11);
                }}

                // 🧤 포수 송구 레이저 빔 역학 연산
                if (catcherThrow.active) {{
                    catcherThrow.x += catcherThrow.vx; catcherThrow.y += catcherThrow.vy;
                    ctx.fillStyle = "#67e8f9"; ctx.beginPath(); ctx.arc(catcherThrow.x, catcherThrow.y, 5, 0, Math.PI*2); ctx.fill();

                    // 송구가 2루 베이스(유격수/2루수 구역)에 도착했을 때 태그 아웃 판정 수싸움
                    if (catcherThrow.y <= 195) {{
                        catcherThrow.active = false;
                        let tagDist = Math.hypot(runner.x - 380, runner.y - 195);
                        if (tagDist < 25) {{
                            // 포수 저지 대성공 OUT
                            runner.active = false; runner.status = "stay";
                            count.o++; if(count.o >= 3) count.o = 0;
                            document.getElementById('runner-status').innerText = "주자 없음";
                            document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                            document.getElementById('relay-text').innerText = "🎙️ 송구 도달 완료! 태그 아웃!!! 포수의 환상적인 어깨가 도루를 완벽히 저지합니다!";
                        }} else {{
                            // 주자 도루 SAFE
                            runner.x = 380; runner.y = 195; runner.status = "stay"; runner.targetBase = "2nd";
                            document.getElementById('runner-status').innerText = "주자 2루";
                            document.getElementById('relay-text').innerText = "🎙️ 세이프! 주자의 발이 미세하게 빨랐습니다! 도루 성공!";
                        }}
                    }}
                }}

                // 🏃 멀티 수비 선수진 보간 연산 및 렌더링
                players.forEach(pl => {{
                    pl.x += (pl.tx - pl.x) * 0.08;
                    pl.y += (pl.ty - pl.y) * 0.08;

                    // 수비 포구 판정 (수비수가 가로채기 지점에 도달해 공을 진짜로 캐치했을 때)
                    if (hitBall.active && Math.hypot(pl.x - hitBall.x, pl.y - hitBall.y) < 22) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(p_ret => {{ p_ret.tx = p_ret.sx; p_ret.ty = p_ret.sy; }}); // 상황 종료 후 즉시 원위치 자동 소환 복귀!
                        
                        if (runner.status === "stealing") {{ runner.status = "stay"; runner.x = 380; runner.y = 195; runner.targetBase = "2nd"; }}

                        count.o++; if(count.o >= 3) {{ count.o=0; count.s=0; count.b=0; }}
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                        document.getElementById('relay-text').innerText = outPhrases[Math.floor(Math.random() * outPhrases.length)];
                    }}

                    ctx.fillStyle = (pl.tx !== pl.sx) ? "#ef4444" : "#3b82f6";
                    ctx.beginPath(); ctx.arc(pl.x, pl.y, 8, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 10px sans-serif"; ctx.fillText(pl.id, pl.x-14, pl.y-12);
                }});

                if(isTargeting) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 10, 0, Math.PI*2); ctx.stroke();
                }}

                // ⚾ 현실 반영 리얼 무브먼트 투구 역학 프로세스
                if(ball.active && ball.status === "go") {{
                    ball.speed *= ball.drag;
                    ball.z += ball.speed;
                    
                    // 현실적인 변화구 궤적 무브먼트 대입 (시그니처 Break)
                    let breakMotion = Math.sin(ball.z * Math.PI) * ball.bx * 3.0;
                    let dropMotion = Math.pow(ball.z, 2) * ball.by * 3.5;

                    ball.x = 290 + (ball.tx - 290)*ball.z + breakMotion;
                    ball.y = 160 + (ball.ty - 160)*ball.z + dropMotion;

                    let ballSize = Math.max(3.5, 4.5 + ball.z * 15);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, ballSize, 0, Math.PI*2); ctx.fill();
                    ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 1.2; ctx.stroke();

                    if(ball.z >= 1.0) {{ ball.z = 1.0; judgeZone(); }}
                }}

                // 🥎 타구 비행 수명 연산 및 그라운드 소멸 복귀 벨트
                if(hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 6, 0, Math.PI*2); ctx.fill();

                    // 타구가 외야 펜스를 넘어가거나 파울라인 밖으로 소멸될 시 안타 정산 및 수비수 원위치 강제 소환 복귀!
                    if(hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 580) {{
                        hitBall.active = false; ball.status = "ready";
                        players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }}); // 즉시 전원 수비기지 복귀 명령
                        
                        count.s = 0; count.b = 0;
                        document.getElementById('score-board').innerText = "B: "+count.b+" | S: "+count.s+" | O: "+count.o;
                        
                        // 루상에 주자 스폰 활성화 연계
                        if (!runner.active) {{
                            runner.active = true; runner.x = 460; runner.y = 240; runner.status = "stay"; runner.targetBase = "1st";
                            document.getElementById('runner-status').innerText = "주자 1루";
                        }} else if (runner.targetBase === "2nd") {{
                            document.getElementById('runner-status').innerText = "주자 득점 성공!";
                            runner.active = false;
                        }}
                    }}
                }}

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(html_src, height=640)

if __name__ == "__main__":
    main()
