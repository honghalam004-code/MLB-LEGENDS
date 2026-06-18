import streamlit as st
import json

def main():
    # =================================================================
    # 1. 시네마틱 화이트 테마 및 글로벌 UI 스타일 가이드
    # =================================================================
    st.set_page_config(page_title="MVP BASEBALL: REAL ROSTER ENGINE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; color: #0f172a; font-family: 'Inter', -apple-system, sans-serif; }
        .stSelectbox, .stSlider, .stRadio { background: #ffffff !important; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        h1, h2, h3 { color: #0f172a !important; font-weight: 900 !important; letter-spacing: -0.5px; }
        .stButton>button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important; font-weight: 800 !important; padding: 14px 28px !important; border-radius: 12px !important;
        }
        .stat-box { background: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)

    # =================================================================
    # 2. 하이엔드 데이터베이스: 대폭 확장된 MLB 인기 구단 로스터
    # =================================================================
    mlb_roster_db = {
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": ["포심 직구", "스위퍼", "스플리터"], "speed": 101, "control": 82},
                "야마모토 요시노부": {"pitches": ["포심 직구", "명품 커브", "스플리터"], "speed": 97, "control": 94},
                "타일러 글래스노우": {"pitches": ["포심 직구", "파워 커브", "슬라이더"], "speed": 99, "control": 84}
            },
            "lineup": [
                {"name": "무키 베츠", "contact": 94, "power": 78, "number": "50"},
                {"name": "프레디 프리먼", "contact": 95, "power": 83, "number": "5"},
                {"name": "오타니 쇼헤이", "contact": 91, "power": 99, "number": "17"},
                {"name": "테오스카 에르난데스", "contact": 78, "power": 89, "number": "37"},
                {"name": "윌 스미스", "contact": 84, "power": 81, "number": "16"},
                {"name": "맥스 먼시", "contact": 73, "power": 88, "number": "13"}
            ]
        },
        "NY Yankees (뉴욕 양키스)": {
            "pitchers": {
                "게릿 콜": {"pitches": ["포심 직구", "슬라이더", "너클 커브"], "speed": 99, "control": 92},
                "마커스 스트로먼": {"pitches": ["싱커/투심", "슬라이더", "커터"], "speed": 93, "control": 88},
                "루이스 가일": {"pitches": ["포심 직구", "슬라이더", "체인지업"], "speed": 96, "control": 78}
            },
            "lineup": [
                {"name": "글레이버 토레스", "contact": 81, "power": 75, "number": "25"},
                {"name": "후안 소토", "contact": 93, "power": 94, "number": "22"},
                {"name": "애런 저지", "contact": 89, "power": 100, "number": "99"},
                {"name": "재즈 치좀 Jr.", "contact": 79, "power": 82, "number": "13"},
                {"name": "지안카를로 스탠튼", "contact": 71, "power": 96, "number": "27"},
                {"name": "앤서니 볼피", "contact": 78, "power": 68, "number": "11"}
            ]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitchers": {
                "딜런 시즈": {"pitches": ["슬라이더", "포심 직구", "너클 커브"], "speed": 99, "control": 81},
                "유 다르빗슈": {"pitches": ["포심 직구", "슬라이더", "커터", "명품 커브"], "speed": 95, "control": 89},
                "마이클 킹": {"pitches": ["싱커/투심", "체인지업", "슬라이더"], "speed": 94, "control": 87}
            },
            "lineup": [
                {"name": "루이스 아라에즈", "contact": 99, "power": 45, "number": "4"},
                {"name": "페르난도 타티스 Jr.", "contact": 87, "power": 92, "number": "23"},
                {"name": "주릭슨 프로파", "contact": 84, "power": 78, "number": "10"},
                {"name": "매니 마차도", "contact": 85, "power": 89, "number": "13"},
                {"name": "잭슨 메릴", "contact": 88, "power": 80, "number": "3"},
                {"name": "김하성", "contact": 80, "power": 68, "number": "7"}
            ]
        },
        "NY Mets (뉴욕 메츠)": {
            "pitchers": {
                "센가 코다이": {"pitches": ["포심 직구", "고스트 포크", "커터"], "speed": 98, "control": 80},
                "루이스 세베리노": {"pitches": ["포심 직구", "슬라이더", "체인지업"], "speed": 97, "control": 83}
            },
            "lineup": [
                {"name": "프란시스코 린도어", "contact": 88, "power": 86, "number": "12"},
                {"name": "브랜든 니모", "contact": 84, "power": 76, "number": "9"},
                {"name": "피트 알론소", "contact": 77, "power": 97, "number": "20"},
                {"name": "제이디 마르티네즈", "contact": 80, "power": 84, "number": "28"},
                {"name": "제프 맥닐", "contact": 82, "power": 58, "number": "1"},
                {"name": "프란시스코 알바레즈", "contact": 74, "power": 80, "number": "4"}
            ]
        },
        "Houston Astros (휴스턴 애스트로스)": {
            "pitchers": {
                "프램버 발데스": {"pitches": ["싱커/투심", "명품 커브", "체인지업"], "speed": 95, "control": 87},
                "저스틴 벌랜더": {"pitches": ["포심 직구", "슬라이더", "파워 커브"], "speed": 94, "control": 91}
            },
            "lineup": [
                {"name": "호세 알투베", "contact": 91, "power": 74, "number": "27"},
                {"name": "카일 터커", "contact": 89, "power": 91, "number": "30"},
                {"name": "요단 알바레즈", "contact": 93, "power": 98, "number": "44"},
                {"name": "알렉스 브레그먼", "contact": 85, "power": 79, "number": "2"},
                {"name": "제레미 페냐", "contact": 81, "power": 65, "number": "3"},
                {"name": "야이너 디아즈", "contact": 84, "power": 77, "number": "38"}
            ]
        }
    }

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # =================================================================
    # 3. [초기 진입 로비 화면] 구단 설정 가드레일
    # =================================================================
    if not st.session_state.game_started:
        st.markdown("""
            <div style="background: #ffffff; padding: 40px; border-radius: 24px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.04); border: 2px solid #e2e8f0; max-width: 850px; margin: 40px auto;">
                <div style="background: #ef4444; color: white; font-family: 'Arial Black', sans-serif; font-size: 11px; font-weight: 900; display: inline-block; padding: 3px 12px; border-radius: 4px; margin-bottom: 12px; letter-spacing: 2px;">EA RETRO BASEBALL 2026</div>
                <h1 style="color: #0f172a; margin: 0; font-family: 'Impact', sans-serif; font-size: 48px;">MVP BASEBALL: <span style="color:#2563eb;">DYNAMIC PATH</span></h1>
                <p style="color: #64748b; margin-top: 8px; font-weight: 500;">구단 라인업 연동 완료. 투수의 제구력 스탯이 낮으면 '실투'가 발생합니다.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            away_team_sel = st.selectbox("⚾ 공격 팀 (AWAY TEAM) 선택", list(mlb_roster_db.keys()), index=1)
            st.markdown("<div class='stat-box'><b>📋 공격팀 대기 타선 (스타 플레이어 빌드)</b><br>" + 
                        "<br>".join([f"• {p['name']} (장타력 {p['power']} / 정교함 {p['contact']})" for p in mlb_roster_db[away_team_sel]['lineup'][:3]]) + "<br>...하위 타선 빌드 완료</div>", unsafe_allow_html=True)
            
        with col2:
            home_team_sel = st.selectbox("🏠 수비 팀 (HOME TEAM) 선택", list(mlb_roster_db.keys()), index=0)
            pitcher_sel = st.selectbox("👤 등판할 에이스 투수 선택", list(mlb_roster_db[home_team_sel]['pitchers'].keys()))
            p_stat = mlb_roster_db[home_team_sel]['pitchers'][pitcher_sel]
            st.markdown(f"""
                <div class='stat-box' style='border-left: 5px solid #2563eb;'>
                    <b>📊 {pitcher_sel} 투수 스펙</b><br>
                    • 포심 패스트볼 베이스: {p_stat['speed']} mph<br>
                    • 기본 제구 안정성: {p_stat['control']} / 100<br>
                    • 장착 구종: {', '.join(p_stat['pitches'])}
                </div>
            """, unsafe_allow_html=True)
            
        if st.button(" Stadium Enter (플레이 볼!)", use_container_width=True):
            st.session_state.away_title = away_team_sel.split(" (")[0]
            st.session_state.home_title = home_team_sel.split(" (")[0]
            st.session_state.active_pitcher = pitcher_sel
            st.session_state.pitcher_spec = p_stat
            st.session_state.away_lineup = mlb_roster_db[away_team_sel]['lineup']
            st.session_state.game_started = True
            st.rerun()
        st.stop()

    # =================================================================
    # 4. [메인 배틀 필드] 경기 제어 스위치보드
    # =================================================================
    st.markdown(f"### 🏟️ 라이브 매치: {st.session_state.away_title} [공격] vs {st.session_state.home_title} [수비]")

    available_pitches = st.session_state.pitcher_spec['pitches']
    base_speed = st.session_state.pitcher_spec['speed']
    base_control = st.session_state.pitcher_spec['control']

    st.markdown("---")
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 2, 2])
    
    with ctrl_col1:
        selected_pitch = st.radio("🔮 투구 구종 선택", available_pitches, horizontal=False)
        
    with ctrl_col2:
        if "직구" in selected_pitch or "싱커" in selected_pitch:
            live_speed = st.slider("🔥 투구 구속 설정 (mph)", base_speed-4, base_speed, base_speed)
            h_break, v_break = ("싱커" in selected_pitch and (-3.5, 3.0) or (0.0, -1.5))
        elif "슬라이더" in selected_pitch or "스위퍼" in selected_pitch:
            live_speed = st.slider("🔮 브레이킹 속도 설정 (mph)", base_speed-10, base_speed-6, base_speed-8)
            h_break, v_break = ("스위퍼" in selected_pitch and (8.0, 0.5) or (4.5, 1.5))
        elif "커브" in selected_pitch:
            live_speed = st.slider("🟢 종방향 낙차 구속 (mph)", base_speed-20, base_speed-14, base_speed-17)
            h_break, v_break = (2.0, 8.5)
        else: # 포크, 체인지업
            live_speed = st.slider("💤 오프스피드 구속 (mph)", base_speed-13, base_speed-9, base_speed-11)
            h_break, v_break = (-1.0, 6.0)

    with ctrl_col3:
        live_control = st.slider("🎯 핀포인트 제구 집중도", 1, 100, base_control)
        st.markdown(f"""
            <div style="background:#f1f5f9; padding:12px; border-radius:10px; font-size:13px; color:#334155;">
                <b>[물리 엔진 작동 로그]</b><br>
                • 제구 집중도가 낮을수록 무작위 <b>'실투(Hanging)'</b> 확률 증가!<br>
                • 변화구 선택 시 매 투구마다 궤적에 미세한 <b>랜덤 스핀 노이즈</b>가 추가됩니다.
            </div>
        """, unsafe_allow_html=True)

    # =================================================================
    # 5. 실투 및 카오스 무브먼트 내장 자바스크립트 엔진 매핑
    # =================================================================
    lineup_json = json.dumps(st.session_state.away_lineup, ensure_ascii=False)

    core_canvas_html = f"""
    <div style="background: #ffffff; padding: 20px; border-radius: 20px; border: 1px solid #e2e8f0; max-width: 960px; margin: 0 auto;">
        
        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; margin-bottom: 15px; font-family: sans-serif;">
            <div>
                <span style="font-weight: 800; color: #0f172a; font-size: 16px;">{st.session_state.away_title[:3].upper()}</span>
                <span id="txt-away-score" style="background:#fff; border:1px solid #cbd5e1; padding:2px 10px; border-radius:6px; margin-left:8px; font-weight:900; color:#2563eb;">0</span>
            </div>
            <div style="text-align: center;">
                <div style="background:#0f172a; color:#ffffff; font-size:12px; padding:3px 14px; border-radius:20px; font-weight:bold; display:inline-block;">1회초 (TOP 1ST)</div>
                <div id="txt-bso" style="font-family:monospace; font-size:13px; font-weight:900; color:#475569; margin-top:5px;">B○○ S○○ O○○</div>
            </div>
            <div style="text-align: right;">
                <span id="txt-home-score" style="background:#fff; border:1px solid #cbd5e1; padding:2px 10px; border-radius:6px; margin-right:8px; font-weight:900; color:#2563eb;">0</span>
                <span style="font-weight: 800; color: #0f172a; font-size: 16px;">{st.session_state.home_title[:3].upper()}</span>
            </div>
        </div>

        <canvas id="canvasCore" width="920" height="430" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; display: block; margin: 0 auto; cursor: crosshair;"></canvas>
        
        <div style="background:#0f172a; color:#f8fafc; padding:15px; border-radius:10px; font-size:14px; margin-top:15px; line-height:1.5; border-left:5px solid #2563eb;">
            <div style="color:#64748b; font-size:11px; font-weight:bold; margin-bottom:3px;">🎙️ LIVE GAME PLAY-BY-PLAY</div>
            <div id="broadcast-ticker">포수 마스크 뒤쪽 시점입니다. 우측 스트라이크 존을 클릭하면 멀리 마운드에서 공이 날아옵니다.</div>
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
        let ball = {{ active: false, x: 240, y: 138, tx: 0, ty: 0, time: 0, size: 2.0 }};
        
        // 실투 및 궤적 카오스 변수
        let isMistakePitch = false;
        let randomNoiseX = 0;
        let randomNoiseY = 0;
        let history = [];

        canvas.addEventListener('mousemove', (e) => {{
            const bound = canvas.getBoundingClientRect();
            pointer.x = (e.clientX - bound.left) * (canvas.width / bound.width);
            pointer.y = (e.clientY - bound.top) * (canvas.height / bound.height);
        }});

        canvas.addEventListener('mousedown', () => {{
            if (ball.active) return;
            if (pointer.x > 530 && pointer.x < 870 && pointer.y > 50 && pointer.y < 380) {{
                
                // 1. 제구 스탯 기반 실투(Hanging Pitch) 확률 연산 (제구가 낮을수록 실투 폭등)
                let mistakeChance = (100 - P_CONTROL) * 0.35; 
                isMistakePitch = Math.random() * 100 < mistakeChance;

                if (isMistakePitch) {{
                    // 실투 발생: 강제로 스트라이크 존 한가운데 몰림 좌표 강제 주입!
                    ball.tx = 700 + (Math.random() - 0.5) * 25;
                    ball.ty = 230 + (Math.random() - 0.5) * 25;
                }} else {{
                    // 정상 투구: 유저 조준점에 제구 오차범위 적용
                    let rngError = (100 - P_CONTROL) * 0.4;
                    ball.tx = pointer.x + (Math.random() - 0.5) * rngError;
                    ball.ty = pointer.y + (Math.random() - 0.5) * rngError;
                }}

                // 2. 변화구 궤적 무작위성(카오스 노이즈) 생성 - 던질 때마다 휩쓸림이 다름
                randomNoiseX = (Math.random() - 0.5) * 2.5;
                randomNoiseY = (Math.random() - 0.5) * 2.5;

                ball.x = 240; ball.y = 138;
                ball.time = 0; ball.size = 2.0;
                ball.active = true;
            }}
        }});

        function writeTicker(txt, isAlert=false) {{
            const div = document.getElementById('broadcast-ticker');
            let marker = isAlert ? "#ef4444" : "#38bdf8";
            div.innerHTML = `<span style="color:${{marker}}; font-weight:bold;">[알림]</span> ${{txt}}`;
        }}

        function resolveAIPlateAppearance() {{
            const activeBatter = ATTACK_LINEUP[core.batterIdx];
            const insideStrike = (ball.tx >= 610 && ball.tx <= 790 && ball.ty >= 140 && ball.ty <= 320);
            
            // 타자 스윙 기본 AI 판정
            let swingProbability = insideStrike ? 0.68 : 0.25;
            if (isMistakePitch) swingProbability = 0.90; // 실투는 타자가 귀신같이 알아채고 후려칩니다.

            const didSwing = Math.random() < swingProbability;

            if (didSwing) {{
                let missRate = 0.42 - (activeBatter.contact - 70) * 0.005;
                if (isMistakePitch) missRate = 0.05; // 실투는 거의 무조건 배트에 맞음

                const didMakeContact = Math.random() > missRate;

                if (didMakeContact) {{
                    let powerWeight = (activeBatter.power - 70) * 0.008;
                    if (isMistakePitch) powerWeight += 0.35; // 실투를 때리면 장타/홈런 확률 초폭등!!

                    const hitRoll = Math.random() + powerWeight;

                    if (hitRoll > 1.05) {{
                        let runs = core.bases.filter(b=>b).length + 1;
                        core.awayScore += runs;
                        core.bases = [false, false, false];
                        core.s = 0; core.b = 0;
                        let prefix = isMistakePitch ? "⚠️ [실투 참사] 한가운데 몰린 공을 놓치지 않네요! " : "💥 ";
                        writeTicker(`${{prefix}} ${{activeBatter.name}} 홈런!! 담장 밖 백스크린을 때리는 초대형 타구입니다!`, true);
                    }} else if (hitRoll > 0.42) {{
                        let scoreIn = core.bases[2] ? 1 : 0;
                        core.bases[2] = core.bases[1]; core.bases[1] = core.bases[0]; core.bases[0] = true;
                        core.awayScore += scoreIn;
                        core.s = 0; core.b = 0;
                        writeTicker(`[안타] ${{activeBatter.name}} 배트 중심에 맞춘 안타! 주자 진루합니다.`);
                    }} else {{
                        core.o++; core.s = 0; core.b = 0;
                        writeTicker(`[범타 아웃] 잘 맞았으나 야수 정면 플라이 아웃 처리됩니다.`);
                    }}
                }} else {{
                    core.s++;
                    writeTicker(`[헛스윙] 배트가 허공을 가릅니다. 현혹적인 궤적입니다.`);
                }}
            }} else {{
                if (insideStrike) {{
                    core.s++;
                    writeTicker(`[스트라이크] 존 구석을 찌르는 완벽한 로케이션.`);
                }} else {{
                    core.b++;
                    writeTicker(`[볼] 볼입니다. 존에서 다소 빠집니다.`);
                }}
            }}

            // 상태값 정산 루프
            let nextBatter = false;
            if (core.s >= 3) {{ core.o++; core.s = 0; core.b = 0; nextBatter = true; writeTicker(`[삼진!!] 💥 완벽한 결정구로 ${{activeBatter.name}}를 돌려세웁니다!`, true); }}
            if (core.b >= 4) {{ core.bases[0] = true; core.s = 0; core.b = 0; nextBatter = true; writeTicker(`[볼넷] 볼 카운트 싸움 실패, 출루를 허용합니다.`); }}
            if (core.s === 0 && core.b === 0) nextBatter = true;

            if (nextBatter) core.batterIdx = (core.batterIdx + 1) % core.bases.length; 
            if (core.o >= 3) {{ core.o = 0; core.s = 0; core.b = 0; core.bases = [false,false,false]; writeTicker(`[🔄 이닝 종료] 쓰리아웃 공수 교대됩니다.`, true); }}

            document.getElementById('txt-away-score').innerText = core.awayScore;
            document.getElementById('txt-home-score').innerText = core.homeScore;
            document.getElementById('txt-bso').innerText = `B${{ "●".repeat(core.b) }} S${{ "●".repeat(core.s) }} O${{ "●".repeat(core.o) }}`;
            
            history.push({{ x: ball.tx, y: ball.ty, inside: insideStrike, mistake: isMistakePitch }});
            if (history.length > 8) history.shift();
        }}

        function renderPipeline() {{
            ctx.fillStyle = "#ffffff"; ctx.fillRect(0,0,920,430);

            // 좌측 3D 야구장 그리기
            ctx.fillStyle = "#166534"; ctx.beginPath(); ctx.moveTo(240, 370); ctx.lineTo(440, 110); ctx.lineTo(40, 110); ctx.closePath(); ctx.fill();
            ctx.fillStyle = "#b45309"; ctx.beginPath(); ctx.ellipse(240, 150, 26, 7, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#ffffff"; ctx.fillRect(233, 149, 14, 2);

            // 루상 주자 그리기
            const drawDiamondBase = (bx, by, isOccupied) => {{
                ctx.fillStyle = isOccupied ? "#ef4444" : "#f1f5f9";
                ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 1.5;
                ctx.save(); ctx.translate(bx, by); ctx.rotate(45 * Math.PI / 180);
                ctx.fillRect(-6, -6, 12, 12); ctx.strokeRect(-6, -6, 12, 12); ctx.restore();
            }};
            drawDiamondBase(310, 230, core.bases[0]);
            drawDiamondBase(240, 140, core.bases[1]);
            drawDiamondBase(170, 230, core.bases[2]);

            // 홈플레이트
            ctx.fillStyle = "#cbd5e1"; ctx.beginPath(); ctx.moveTo(240, 340); ctx.lineTo(252, 350); ctx.lineTo(252, 358); ctx.lineTo(228, 358); ctx.lineTo(228, 350); ctx.fill();

            // 저 멀리 투수
            ctx.fillStyle = "#1e293b"; ctx.beginPath(); ctx.arc(240, 138, 4, 0, Math.PI*2); ctx.fill(); ctx.fillRect(238, 142, 4, 7);

            // 타석 타자 정보 스크린
            const currentBatter = ATTACK_LINEUP[core.batterIdx];
            ctx.fillStyle = "#0f172a"; ctx.font = "bold 12px sans-serif";
            ctx.fillText(`타석: [${{currentBatter.number}}] ${{currentBatter.name}}`, 40, 345);
            ctx.fillStyle = "#64748b"; ctx.font = "11px sans-serif";
            ctx.fillText(`컨택트: ${{currentBatter.contact}} | 파워: ${{currentBatter.power}}`, 40, 363);

            // 타자 그래픽 아바타
            ctx.fillStyle = "#2563eb"; ctx.beginPath(); ctx.arc(195, 325, 8, 0, Math.PI*2); ctx.fill();
            ctx.strokeStyle = "#78350f"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(195, 327); ctx.lineTo(215, 300); ctx.stroke();

            // 분할 격벽선
            ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(470, 10); ctx.lineTo(470, 420); ctx.stroke();

            // 우측 K-ZONE 그리기
            ctx.fillStyle = "rgba(37, 99, 235, 0.02)"; ctx.fillRect(610, 140, 180, 180);
            ctx.strokeStyle = "#2563eb"; ctx.lineWidth = 3.5; ctx.strokeRect(610, 140, 180, 180);
            
            ctx.strokeStyle = "rgba(37, 99, 235, 0.12)"; ctx.lineWidth = 1.5;
            for(let i=1; i<3; i++) {{
                ctx.beginPath(); ctx.moveTo(610 + (i * 60), 140); ctx.lineTo(610 + (i * 60), 320); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(610, 140 + (i * 60)); ctx.lineTo(790, 140 + (i * 60)); ctx.stroke();
            }}
            ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 1; ctx.strokeRect(540, 60, 320, 310);

            // 크로스헤어
            if (!ball.active && pointer.x > 530 && pointer.x < 870) {{
                ctx.strokeStyle = "#ea580c"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(pointer.x, pointer.y, 13, 0, Math.PI*2); ctx.stroke();
            }}

            // 피칭 히트맵 표시
            history.forEach(h => {{
                ctx.fillStyle = h.mistake ? "#eab308" : (h.inside ? "#22c55e" : "#ef4444");
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(h.x, h.y, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            }});

            // 실시간 3D 비행 물리학 물리 엔진 연산 구역
            if (ball.active) {{
                ball.time += 0.054;
                
                let lx = 240 + (ball.tx - 240) * ball.time;
                let ly = 138 + (ball.ty - 138) * ball.time;
                
                ball.size = 2.0 + (Math.pow(ball.time, 2.5) * 11.0);

                // 물리학 연산: 고유 브레이킹 수치 + 무작위 스핀 노이즈 팩터 결합
                let tFactor = Math.pow(ball.time, 2);
                ball.x = lx + ((P_H_BREAK + randomNoiseX) * tFactor * 1.5);
                ball.y = ly + ((P_V_BREAK + randomNoiseY) * tFactor * 1.5);

                // 실투일 경우 빨간색 경고 오라 효과 부여
                if (isMistakePitch) {{
                    ctx.shadowColor = "#ef4444"; ctx.shadowBlur = 10;
                    ctx.fillStyle = "#ef4444"; ctx.font = "bold 16px sans-serif";
                    ctx.fillText("⚠️ 실투!", ball.x - 20, ball.y - 20);
                }}

                ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#475569"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
                ctx.shadowBlur = 0; // 섀도우 초기화

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

    st.components.v1.html(core_canvas_html, height=620)

    if st.button("🔄 처음으로 돌아가서 구단/투수 다시 고르기"):
        st.session_state.game_started = False
        st.rerun()

if __name__ == "__main__":
    main()
