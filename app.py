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
    # 2. 하이엔드 데이터베이스: 구단별 투수 구종 스펙 & 9인 타선 능력치
    # =================================================================
    mlb_roster_db = {
        "LA Dodgers (로스앤젤레스 다저스)": {
            "pitchers": {
                "오타니 쇼헤이": {"pitches": ["포심 직구", "스위퍼", "스플리터"], "speed": 101, "control": 84, "spin": 2650},
                "야마모토 요시노부": {"pitches": ["포심 직구", "명품 커브", "스플리터", "커터"], "speed": 97, "control": 93, "spin": 2810},
                "타일러 글래스노우": {"pitches": ["포심 직구", "파워 커브", "슬라이더"], "speed": 99, "control": 82, "spin": 2930}
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
                "게릿 콜": {"pitches": ["포심 직구", "슬라이더", "너클 커브", "체인지업"], "speed": 99, "control": 91, "spin": 2550},
                "마커스 스트로먼": {"pitches": ["싱커/투심", "슬라이더", "커터"], "speed": 93, "control": 88, "spin": 2420},
                "카를로스 로돈": {"pitches": ["포심 직구", "슬라이더", "체인지업"], "speed": 96, "control": 80, "spin": 2380}
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
        "Atlanta Braves (애틀랜타 브레이브스)": {
            "pitchers": {
                "스펜서 스트라이더": {"pitches": ["포심 직구", "슬라이더", "체인지업"], "speed": 102, "control": 86, "spin": 2980},
                "크리스 세일": {"pitches": ["슬라이더", "포심 직구", "체인지업"], "speed": 95, "control": 90, "spin": 2600},
                "맥스 프리드": {"pitches": ["명품 커브", "포심 직구", "싱커/투심"], "speed": 94, "control": 94, "spin": 2200}
            },
            "lineup": [
                {"name": "로날드 아쿠냐 Jr.", "contact": 92, "power": 95, "number": "13"},
                {"name": "아지 알비스", "contact": 84, "power": 80, "number": "1"},
                {"name": "오스틴 라일리", "contact": 86, "power": 91, "number": "27"},
                {"name": "멧 올슨", "contact": 81, "power": 96, "number": "28"},
                {"name": "마르셀 오즈나", "contact": 83, "power": 93, "number": "20"},
                {"name": "마이클 해리스 II", "contact": 85, "power": 74, "number": "23"},
                {"name": "션 머피", "contact": 79, "power": 81, "number": "12"},
                {"name": "올란도 아르시아", "contact": 75, "power": 67, "number": "11"},
                {"name": "재러드 켈닉", "contact": 76, "power": 70, "number": "24"}
            ]
        },
        "SD Padres (샌디에이고 파드리스)": {
            "pitchers": {
                "딜런 시즈": {"pitches": ["슬라이더", "포심 직구", "너클 커브"], "speed": 99, "control": 81, "spin": 2890},
                "유 다르빗슈": {"pitches": ["포심 직구", "슬라이더", "커터", "명품 커브", "스플리터"], "speed": 95, "control": 89, "spin": 2700},
                "마이클 킹": {"pitches": ["싱커/투심", "체인지업", "슬라이더"], "speed": 94, "control": 87, "spin": 2510}
            },
            "lineup": [
                {"name": "루이스 아라에즈", "contact": 99, "power": 45, "number": "4"},
                {"name": "페르난도 타티스 Jr.", "contact": 87, "power": 92, "number": "23"},
                {"name": "주릭슨 프로파", "contact": 84, "power": 78, "number": "10"},
                {"name": "매니 마차도", "contact": 85, "power": 89, "number": "13"},
                {"name": "제이크 크로넨워스", "contact": 81, "power": 73, "number": "9"},
                {"name": "잰더 보가츠", "contact": 83, "power": 71, "number": "2"},
                {"name": "잭슨 메릴", "contact": 88, "power": 80, "number": "3"},
                {"name": "김하성", "contact": 80, "power": 68, "number": "7"},
                {"name": "카일 히가시오카", "contact": 72, "power": 74, "number": "20"}
            ]
        }
    }

    # =================================================================
    # 3. 게임 내부 상태 세션 브릿지
    # =================================================================
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # =================================================================
    # 4. [초기 진입 로비 화면] 아무것도 조작 불가능한 설정 락(Lock)
    # =================================================================
    if not st.session_state.game_started:
        st.markdown("""
            <div style="background: #ffffff; padding: 50px; border-radius: 24px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.04); border: 2px solid #e2e8f0; max-width: 850px; margin: 40px auto;">
                <div style="background: #ef4444; color: white; font-family: 'Arial Black', sans-serif; font-size: 11px; font-weight: 900; display: inline-block; padding: 3px 12px; border-radius: 4px; margin-bottom: 12px; letter-spacing: 2px;">EA RETRO CORE</div>
                <h1 style="color: #0f172a; margin: 0; font-family: 'Impact', sans-serif; font-size: 52px; letter-spacing: -0.5px;">MVP BASEBALL: <span style="color:#2563eb;">LINEUP PRO</span></h1>
                <p style="color: #64748b; margin-top: 8px; font-weight: 500; font-size: 16px;">상대할 구단과 맞춤형 선발 투수를 선택해 경기장에 진입하세요.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            away_team_sel = st.selectbox("⚾ 공격 팀 (AWAY TEAM) 선택", list(mlb_roster_db.keys()), index=1)
            st.markdown("<div class='stat-box'><b>📋 공격팀 실시간 엔트리</b><br>" + 
                        "<br>".join([f"• {i+1}번: {p['name']} (장타 {p['power']} / 정교 {p['contact']})" for i, p in enumerate(mlb_roster_db[away_team_sel]['lineup'][:4])]) + "<br>...이하 9번타자까지 대기 완료</div>", unsafe_allow_html=True)
            
        with col2:
            home_team_sel = st.selectbox("🏠 수비 팀 (HOME TEAM) 선택", list(mlb_roster_db.keys()), index=0)
            pitcher_sel = st.selectbox("👤 등판할 수비팀 에이스 투수 선택", list(mlb_roster_db[home_team_sel]['pitchers'].keys()))
            p_stat = mlb_roster_db[home_team_sel]['pitchers'][pitcher_sel]
            st.markdown(f"""
                <div class='stat-box' style='border-left: 5px solid #2563eb;'>
                    <b>📊 {pitcher_sel} 선수 고유 데이터</b><br>
                    • 포심 패스트볼 최고 구속: {p_stat['speed']} mph<br>
                    • 커맨드 제구력 평점: {p_stat['control']} / 100<br>
                    • 보유 구질: {', '.join(p_stat['pitches'])}
                </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        if st.button("🏟️ STADIUM ENTER (플레이 볼!)", use_container_width=True):
            st.session_state.away_title = away_team_sel.split(" (")[0]
            st.session_state.home_title = home_team_sel.split(" (")[0]
            st.session_state.active_pitcher = pitcher_sel
            st.session_state.pitcher_spec = p_stat
            st.session_state.away_lineup = mlb_roster_db[away_team_sel]['lineup']
            st.session_state.game_started = True
            st.rerun()
        st.stop()

    # =================================================================
    # 5. [메인 대전 필드] 락 해제 후 투구 컨트롤러 마운팅 구역
    # =================================================================
    st.markdown(f"### 🏟️ LIVE: {st.session_state.away_title} [공격] vs {st.session_state.home_title} [수비]")

    # 선택된 투수의 구종 리스트를 동적으로 가져와 무브먼트 튜닝 계산
    available_pitches = st.session_state.pitcher_spec['pitches']
    base_speed = st.session_state.pitcher_spec['speed']
    base_control = st.session_state.pitcher_spec['control']

    st.markdown("---")
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 2, 2])
    
    with ctrl_col1:
        selected_pitch = st.radio("🔮 던질 구종 선택 (투수 고유 아스날)", available_pitches, horizontal=False)
        
    with ctrl_col2:
        # 선택된 세부 구종에 따른 물리적 속도 편차 자동 트리거링
        if "직구" in selected_pitch or "싱커" in selected_pitch:
            live_speed = st.slider("🔥 전력 투구 구속 제어 (mph)", base_speed-4, base_speed, base_speed)
            h_break, v_break = ("싱커" in selected_pitch and (-3.5, 3.0) or (0.0, -1.5))
        elif "슬라이더" in selected_pitch or "스위퍼" in selected_pitch:
            live_speed = st.slider("🔮 브레이킹 볼 속도 제어 (mph)", base_speed-10, base_speed-6, base_speed-8)
            h_break, v_break = ("스위퍼" in selected_pitch and (7.5, 0.5) or (4.0, 1.5))
        elif "커브" in selected_pitch:
            live_speed = st.slider("🟢 종방향 낙차 속도 제어 (mph)", base_speed-22, base_speed-16, base_speed-19)
            h_break, v_break = (2.0, 8.0)
        else: # 스플리터 / 체인지업 계열오프스피드 피치
            live_speed = st.slider("💤 오프스피드 속도 제어 (mph)", base_speed-14, base_speed-10, base_speed-12)
            h_break, v_break = (-1.5, 5.5)

    with ctrl_col3:
        live_control = st.slider("🎯 핀포인트 제구 집중력", 1, 100, base_control)
        st.markdown(f"""
            <div style="background:#f1f5f9; padding:12px; border-radius:10px; font-size:13px; color:#334155;">
                <b>[투구 물리학 팩터 인디케이터]</b><br>
                • 현재 마운드: {st.session_state.active_pitcher}<br>
                • 공의 좌우 변화궤적: {h_break}인치 | 상하 낙차 변화궤적: {v_break}인치
            </div>
        """, unsafe_allow_html=True)

    # =================================================================
    # 6. 진짜 포수 마스크 시점 (Catcher's Mask View) 코어 그래픽스 파이프라인
    # =================================================================
    # 타자의 능력치 데이터셋을 JSON 데이터 스트림으로 JS 코어 엔진에 다이렉트 주입
    lineup_json = json.dumps(st.session_state.away_lineup, ensure_ascii=False)

    core_canvas_html = f"""
    <div style="background: #ffffff; padding: 20px; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.03); max-width: 960px; margin: 0 auto;">
        
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
            <div style="color:#64748b; font-size:11px; font-weight:bold; margin-bottom:3px;">🎙️ EA REAL-TIME BROADCAST</div>
            <div id="broadcast-ticker">수비팀 투수 {st.session_state.active_pitcher} 선수가 세트포지션에 들어갑니다. 우측 K-ZONE 사각형 내부를 타겟팅하십시오.</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvasCore');
        const ctx = canvas.getContext('2d');

        // 파이썬 주입 구조체 바인딩
        const P_NAME = "{st.session_state.active_pitcher}";
        const P_TYPE = "{selected_pitch}";
        const P_SPEED = {live_speed};
        const P_CONTROL = {live_control};
        const P_H_BREAK = {h_break};
        const P_V_BREAK = {v_break};
        const ATTACK_LINEUP = {lineup_json};

        // 타순 시뮬레이션 제어 변수 연산 오케스트레이션
        let core = {{
            awayScore: 0, homeScore: 0, b: 0, s: 0, o: 0,
            batterIdx: 0, // 0번 타자(1번타자)부터 루프 기동
            bases: [false, false, false]
        }};

        let pointer = {{ x: 0, y: 0 }};
        // 포수 시점: 공이 저 멀리 상단(240, 130)에서 내 얼굴(tx, ty) 방향으로 기하급수적으로 확대 돌격
        let ball = {{ active: false, x: 240, y: 130, tx: 0, ty: 0, time: 0, size: 2.0 }};
        let history = [];

        canvas.addEventListener('mousemove', (e) => {{
            const bound = canvas.getBoundingClientRect();
            pointer.x = (e.clientX - bound.left) * (canvas.width / bound.width);
            pointer.y = (e.clientY - bound.top) * (canvas.height / bound.height);
        }});

        canvas.addEventListener('mousedown', () => {{
            if (ball.active) return;
            // 우측의 가시성 고대비 방송용 K-ZONE 내부 영역 클릭 판정 가드레일
            if (pointer.x > 530 && pointer.x < 870 && pointer.y > 50 && pointer.y < 380) {{
                let rngError = (100 - P_CONTROL) * 0.45;
                
                ball.tx = pointer.x + (Math.random() - 0.5) * rngError;
                ball.ty = pointer.y + (Math.random() - 0.5) * rngError;
                ball.x = 240; ball.y = 130;
                ball.time = 0; ball.size = 2.0;
                ball.active = true;
            }}
        }});

        function writeTicker(txt, isEvent=false) {{
            const div = document.getElementById('broadcast-ticker');
            let colorMarker = isEvent ? "#ef4444" : "#38bdf8";
            div.innerHTML = `<span style="color:${{colorMarker}}; font-weight:bold;">[LIVE]</span> ${{txt}}`;
        }}

        // [핵심 매커니즘] 투수 구질 + 현재 타자의 개별 스탯(Contact/Power) 연동 판정 엔진
        function resolveAIPlateAppearance() {{
            const activeBatter = ATTACK_LINEUP[core.batterIdx];
            const insideStrike = (ball.tx >= 610 && ball.tx <= 790 && ball.ty >= 140 && ball.ty <= 320);
            
            // 타자의 성향 확률 보정: 컨택 능력이 높을수록 헛스윙 확률 급감
            let swingProbability = insideStrike ? 0.65 : 0.22;
            const didSwing = Math.random() < swingProbability;

            if (didSwing) {{
                // 컨택트 스탯 반영 배트 터치 연산 (스펙이 90 이상이면 맞출 확률 비약적 상승)
                let contactWeight = (activeBatter.contact - 70) * 0.006;
                let missRate = 0.45 - contactWeight;
                const didMakeContact = Math.random() > missRate;

                if (didMakeContact) {{
                    // 장타력 스탯 반영 안타/홈런 퀄리티 판정 분기점
                    let powerWeight = (activeBatter.power - 70) * 0.008;
                    const hitRoll = Math.random() + powerWeight;

                    if (hitRoll > 1.05) {{ // 초대형 홈런 달성 조건식
                        let runs = core.bases.filter(b=>b).length + 1;
                        core.awayScore += runs;
                        core.bases = [false, false, false];
                        core.s = 0; core.b = 0;
                        writeTicker(`💥 대형 홈런!! ${{activeBatter.name}} 선수가 ${{P_NAME}}의 ${{P_SPEED}}mph ${{P_TYPE}}를 받아쳐 완벽한 아치를 그립니다!`, true);
                    }} else if (hitRoll > 0.45) {{ // 일반 안타 처리 안야 진출 루프
                        let scoreIn = core.bases[2] ? 1 : 0;
                        core.bases[2] = core.bases[1]; core.bases[1] = core.bases[0]; core.bases[0] = true;
                        core.awayScore += scoreIn;
                        core.s = 0; core.b = 0;
                        writeTicker(`[안타] ${{activeBatter.name}} 깨끗한 안타! 주자들 한 베이스씩 진루하며 찬스를 이어갑니다.`);
                    }} else {{ // 아웃 처리 야수 정면 타구
                        core.o++; core.s = 0; core.b = 0;
                        writeTicker(`[아웃] 정면 타구! 내야수 정면으로 가며 범타로 아웃카운트가 채워집니다.`);
                    }}
                }} else {{
                    core.s++;
                    writeTicker(`[헛스윙] ${{activeBatter.name}} 배트 돌았습니다! ${{P_NAME}}의 볼끝 무브먼트가 대단합니다.`);
                }}
            }} else {{
                if (insideStrike) {{
                    core.s++;
                    writeTicker(`[스트라이크] 루킹 스트라이크! 존 구석을 정밀하게 통과하는 공에 타자 배트 얼어붙습니다.`);
                }} else {{
                    core.b++;
                    writeTicker(`[볼] 잘 골라냈습니다. 미트가 크게 움직이는 완전한 유인구입니다.`);
                }}
            }}

            // 이닝 및 타석 종료 플래그 체킹 바운더리
            let batterChanged = false;
            if (core.s >= 3) {{
                core.o++; core.s = 0; core.b = 0; batterChanged = true;
                writeTicker(`[삼진 아웃] 💥 결정구 삼진! ${{activeBatter.name}} 선수를 3구 삼진으로 돌려세우는 ${{P_NAME}}!`, true);
            }}
            if (core.b >= 4) {{
                core.bases[0] = true; core.s = 0; core.b = 0; batterChanged = true;
                writeTicker(`[볼넷] ${{activeBatter.name}} 정교한 선구안으로 베이스를 채워나갑니다. 포볼 출루.`);
            }}
            if (core.s === 0 && core.b === 0) batterChanged = true; // 안타나 타구 아웃 발생 시 타자 교체

            if (batterChanged) {{
                core.batterIdx = (core.batterIdx + 1) % 9; // 다음 타순으로 바인딩 스위칭
            }}

            if (core.o >= 3) {{
                core.o = 0; core.s = 0; core.b = 0; core.bases = [false,false,false];
                writeTicker(`[🔄 이닝 공수 교대] 3아웃 체인지! 공수 교대되어 덕아웃으로 야수들이 질주합니다.`, true);
            }}

            // HUD UI 데이터 동기화 리플래시
            document.getElementById('txt-away-score').innerText = core.awayScore;
            document.getElementById('txt-home-score').innerText = core.homeScore;
            document.getElementById('txt-bso').innerText = `B${{ "●".repeat(core.b) }} S${{ "●".repeat(core.s) }} O${{ "●".repeat(core.o) }}`;
            
            history.push({{ x: ball.tx, y: ball.ty, inside: insideStrike }});
            if (history.length > 7) history.shift();
        }}

        function renderPipeline() {{
            ctx.fillStyle = "#ffffff"; ctx.fillRect(0,0,920,430);

            // --- [구역 1] 좌측 구역: 리얼 3D 원근법 포수 카메라 뷰 드로잉 ---
            ctx.fillStyle = "#15803d"; // 필드 잔디 텍스처링
            ctx.beginPath(); ctx.moveTo(240, 370); ctx.lineTo(440, 110); ctx.lineTo(40, 110); ctx.closePath(); ctx.fill();

            ctx.fillStyle = "#b45309"; // 투수 마운드 가공
            ctx.beginPath(); ctx.ellipse(240, 150, 26, 7, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#ffffff"; ctx.fillRect(233, 149, 14, 2); // 하이라이트 투판 마킹

            // 원근 레이아웃 다이아몬드 주자 진출 상황 맵 드로잉
            const drawDiamondBase = (bx, by, isOccupied) => {{
                ctx.fillStyle = isOccupied ? "#ef4444" : "#f1f5f9";
                ctx.strokeStyle = isOccupied ? "#f87171" : "#94a3b8";
                ctx.lineWidth = 1.5;
                ctx.save(); ctx.translate(bx, by); ctx.rotate(45 * Math.PI / 180);
                ctx.fillRect(-6, -6, 12, 12); ctx.strokeRect(-6, -6, 12, 12); ctx.restore();
            }};
            drawDiamondBase(310, 230, core.bases[0]); // 1루
            drawDiamondBase(240, 140, core.bases[1]); // 2루
            drawDiamondBase(170, 230, core.bases[2]); // 3루

            // 포수 바로 앞 홈플레이트 정밀 오각형 배치 (가장 가까운 거리감)
            ctx.fillStyle = "#cbd5e1";
            ctx.beginPath(); ctx.moveTo(240, 340); ctx.lineTo(252, 350); ctx.lineTo(252, 358); ctx.lineTo(228, 358); ctx.lineTo(228, 350);
            ctx.closePath(); ctx.fill();

            // 저 멀리서 세트포지션 대기 중인 투수 캐릭터 (축소 렌더링)
            ctx.fillStyle = "#1e293b"; ctx.beginPath(); ctx.arc(240, 138, 4, 0, Math.PI*2); ctx.fill();
            ctx.fillRect(238, 142, 4, 7);

            // 실시간 타석에 서 있는 현역 타자 전광판 텍스트 미러링
            const currentBatter = ATTACK_LINEUP[core.batterIdx];
            ctx.fillStyle = "#0f172a"; ctx.font = "bold 12px sans-serif";
            ctx.fillText(`타자: [${{currentBatter.number}}] ${{currentBatter.name}}`, 50, 350);
            ctx.fillStyle = "#64748b"; ctx.font = "11px sans-serif";
            ctx.fillText(`정교: ${{currentBatter.contact}} / 장타: ${{currentBatter.power}}`, 50, 368);

            // 배팅 스탠스 실루엣 드로잉 위젯
            ctx.fillStyle = "#2563eb"; ctx.beginPath(); ctx.arc(195, 330, 8, 0, Math.PI*2); ctx.fill();
            ctx.strokeStyle = "#78350f"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(195, 332); ctx.lineTo(215, 305); ctx.stroke();

            // 중앙 파티션 격벽 분리 라인 스케치
            ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1.5;
            ctx.beginPath(); ctx.moveTo(470, 10); ctx.lineTo(470, 420); ctx.stroke();

            // --- [구역 2] 우측 구역: 디지털 방송 전용 고해상도 K-ZONE 트랙킹 보드 ---
            ctx.fillStyle = "rgba(37, 99, 235, 0.02)"; ctx.fillRect(610, 140, 180, 180);
            ctx.strokeStyle = "#2563eb"; ctx.lineWidth = 3.5; ctx.strokeRect(610, 140, 180, 180); // 보더 라인 스트라이크
            
            // 9분할 존 가이드라인 슬라이싱 처리
            ctx.strokeStyle = "rgba(37, 99, 235, 0.15)"; ctx.lineWidth = 1.5;
            for(let i=1; i<3; i++) {{
                ctx.beginPath(); ctx.moveTo(610 + (i * 60), 140); ctx.lineTo(610 + (i * 60), 320); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(610, 140 + (i * 60)); ctx.lineTo(790, 140 + (i * 60)); ctx.stroke();
            }}
            ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 1; ctx.strokeRect(540, 60, 320, 310); // 아웃 존 라운더리

            // 실시간 주사 마우스 타겟 가늠쇠 동기화 피드백
            if (!ball.active && pointer.x > 530 && pointer.x < 870) {{
                ctx.strokeStyle = "#ea580c"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(pointer.x, pointer.y, 13, 0, Math.PI*2); ctx.stroke();
                ctx.fillStyle = "#ea580c"; ctx.beginPath(); ctx.arc(pointer.x, pointer.y, 2, 0, Math.PI*2); ctx.fill();
            }}

            // 투구 누적 히트맵 점적 차트 가시화 트랙킹
            history.forEach(h => {{
                ctx.fillStyle = h.inside ? "#22c55e" : "#ef4444";
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.arc(h.x, h.y, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            }});

            // --- [구역 3] 실시간 포수 시점 다이내믹 피치 3D 물리 연산 비행 렌더링 ---
            if (ball.active) {{
                ball.time += 0.052; // 피칭 구속 가속 진행률 변위 프레임 스케일링
                
                // 마운드(240, 138)에서 클릭된 스트라이크 궤적 종착지 타겟팅 보간
                let lx = 240 + (ball.tx - 240) * ball.time;
                let ly = 138 + (ball.ty - 138) * ball.time;
                
                // [포수시점 핵심 물리학] 내 얼굴 앞으로 날아올수록 공 크기가 포물선 형태로 급격히 팽창
                ball.size = 2.0 + (Math.pow(ball.time, 2.5) * 11.0);

                // 구종 변수별 파라미터 적용 휘어짐 이펙트 궤적 튜닝 연산
                let tFactor = Math.pow(ball.time, 2);
                ball.x = lx + (P_H_BREAK * tFactor * 1.5);
                ball.y = ly + (P_V_BREAK * tFactor * 1.5);

                ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#475569"; ctx.lineWidth = 1.5;
                ctx.save();
                ctx.shadowColor = "rgba(0,0,0,0.2)"; ctx.shadowBlur = 4; ctx.shadowOffsetY = 3;
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
                ctx.restore();

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

    # 설정 변경 리셋 트릭
    if st.button("🔄 RETURN TO CONFIG (메인 화면으로 돌아가 팀/투수 다시 고르기)"):
        st.session_state.game_started = False
        st.rerun()

if __name__ == "__main__":
    main()
