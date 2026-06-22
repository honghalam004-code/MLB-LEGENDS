import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB CATCHER VIEW - PERFECT ENGINE", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .stSelectbox > div > div { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #16a34a !important; border-radius: 6px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
            color: #ffffff !important; font-weight: bold !important;
            border-radius: 8px !important; border: none !important; padding: 12px 24px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # =========================================================================
    # 📊 [스펙 보존] 30개 전 구단 오리지널 마스터 데이터베이스
    # =========================================================================
    mlb_mega_db = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스 (선발)": {"pitches": {"파워 포심": {"speed": 0.042, "drag": 1.0, "break": 0.0}, "명품 너클커브": {"speed": 0.025, "drag": 0.83, "break": 4.5}}},
                "데이비드 베드나 (마무리)": {"pitches": {"하이 패스트볼": {"speed": 0.039, "drag": 1.0, "break": 0.0}}}
            },
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "키브라이언 헤이즈", "라우디 텔레즈", "앤드류 맥커친", "코너 조", "자레드 트리올로", "마이클 A. 테일러", "조이 바트"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이 (선발)": {"pitches": {"파워 포심": {"speed": 0.041, "drag": 1.0, "break": 0.0}, "명품 스위퍼": {"speed": 0.029, "drag": 0.85, "break": -4.8}, "고속 split": {"speed": 0.034, "drag": 0.91, "break": 0.3}}},
                "에반 필립스 (마무리)": {"pitches": {"슬라이더": {"speed": 0.032, "drag": 0.89, "break": 3.0}}}
            },
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "테오스카 에르난데스", "맥스 먼시", "토미 에드먼", "가빈 럭스", "앤디 파헤스", "윌 스미스"]
        },
        "New York Yankees": {
            "pitchers": {
                "게릿 콜 (선발)": {"pitches": {"강속구 포심": {"speed": 0.040, "drag": 1.0, "break": 0.0}, "고속 슬라이더": {"speed": 0.033, "drag": 0.90, "break": 2.5}}},
                "루크 위버 (마무리)": {"pitches": {"커터": {"speed": 0.035, "drag": 0.94, "break": 1.0}}}
            },
            "lineup": ["앤서니 볼피", "후안 소토", "애런 저지", "지안카를로 스탠튼", "앤서니 리조", "글레이버 토레스", "알렉스 버두고", "오스틴 웰스", "오스왈도 카브레라"]
        },
        "San Francisco Giants": {
            "pitchers": {
                "로건 웹 (선발)": {"pitches": {"명품 싱커": {"speed": 0.035, "drag": 0.94, "break": -2.5}, "체인지업": {"speed": 0.027, "drag": 0.83, "break": -1.8}}},
                "캠밀로 도발 (마무리)": {"pitches": {"102마일 싱커": {"speed": 0.042, "drag": 0.96, "break": -1.5}}}
            },
            "lineup": ["이정후", "타이로 에스트라다", "맷 채프먼", "라몬테 웨이드 주니어", "윌머 플로레스", "마이클 콘포토", "패트릭 베일리", "마이크 야스트렘스키", "닉 아메드"]
        }
    }

    # 나머지 구단 리스트 자동 가동 처리 (호환성 보장)
    other_teams = [
        ("San Diego Padres", "딜런 시즈 (선발)", "루이스 아라에즈", "로베르트 수아레즈 (마무리)"),
        ("Atlanta Braves", "크리스 세일 (선발)", "로날드 아쿠냐 주니어", "라이셀 이글레시아스 (마무리)"),
        ("Houston Astros", "프람버 발데스 (선발)", "호세 알투베", "조시 헤이더 (마무리)"),
        ("Texas Rangers", "네이선 이볼디 (선발)", "마르커스 시미언", "커비 예이츠 (마무리)"),
        ("Philadelphia Phillies", "잭 휠러 (선발)", "카일 슈와버", "제프 호프만 (마무리)"),
        ("Milwaukee Brewers", "프레디 페랄타 (선발)", "브라이스 투랑", "데빈 윌리엄스 (마무리)"),
        ("Chicago Cubs", "저스틴 스틸 (선발)", "이안 햅", "포터 호지 (마무리)"),
        ("St. Louis Cardinals", "소니 그레이 (선발)", "마신 위니", "라이안 헬슬리 (마무리)"),
        ("Arizona Diamondbacks", "잭 갈렌 (선발)", "코빈 캐롤", "폴 시월드 (마무리)"),
        ("Colorado Rockies", "카일 프리랜드 (선발)", "찰리 몬스터", "타일러 킨리 (마무리)"),
        ("Miami Marlins", "샌디 알칸타라 (선발)", "재즈 치좀", "캘빈 포셰이 (마무리)"),
        ("Washington Nationals", "맥켄지 고어 (선발)", "CJ 에이브람스", "카일 피네건 (마무리)"),
        ("Cincinnati Reds", "헌터 그린 (선발)", "엘리 데 라 크루즈", "알렉시스 디아즈 (마무리)"),
        ("Chicago White Sox", "가렛 크로셰 (선발)", "토미 팸", "존 브레비아 (마무리)"),
        ("Cleveland Guardians", "태너 바이비 (선발)", "스티븐 관", "엠마누엘 클라세 (마무리)"),
        ("Detroit Tigers", "타릭 스쿠발 (선발)", "라일리 그린", "제이슨 폴리 (마무리)"),
        ("Kansas City Royals", "콜 레이간스 (선발)", "마이켈 가르시아", "제임스 맥아더 (마무리)"),
        ("Minnesota Twins", "파블로 로페즈 (선발)", "윌리 카스트로", "요안 두란 (마무리)"),
        ("Baltimore Orioles", "코빈 번스 (선발)", "군나르 핸더슨", "크레이그 킴브렐 (마무리)"),
        ("Boston Red Sox", "태너 하우크 (선발)", "자렌 더란", "켄리 젠슨 (마무리)"),
        ("Tampa Bay Rays", "타지 브래들리 (선발)", "얀디 디아즈", "피트 페어뱅크스 (마무리)"),
        ("Toronto Blue Jays", "케빈 가우스먼 (선발)", "조지 스프링어", "채드 그린 (마무리)"),
        ("Los Angeles Angels", "타일러 안더슨 (선발)", "놀란 샤누엘", "벤 조이스 (마무리)"),
        ("Oakland Athletics", "JP 시어스 (선발)", "아브라함 토로", "메이슨 밀러 (마무리)"),
        ("Seattle Mariners", "루이스 카스티요 (선발)", "J.P. 크로포드", "안드레스 무뇨즈 (마무리)"),
        ("New York Mets", "센가 코다이 (선발)", "프란시스코 린도어", "에드윈 디아즈 (마무리)")
    ]
    for t_name, p_main, b_first, p_close in other_teams:
        if t_name not in mlb_mega_db:
            mlb_mega_db[t_name] = {
                "pitchers": {
                    p_main: {"pitches": {"포심 강속구": {"speed": 0.040, "drag": 1.0, "break": 0.0}, "체인지업": {"speed": 0.028, "drag": 0.85, "break": -1.5}}},
                    p_close: {"pitches": {"클로저 패스트볼": {"speed": 0.042, "drag": 1.0, "break": 0.0}}}
                },
                "lineup": [b_first, "타자 B", "타자 C", "타자 D", "타자 E", "타자 F", "타자 G", "타자 H", "타자 I"]
            }

    sorted_teams = sorted(list(mlb_mega_db.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#16a34a; margin-top:20px;'>🏟️ 정통 포수시점 야구 게임 (수비범위 제한 고정판)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8;'>30개 구단 시스템 적용 완료 · 유격수 무한 추적 현상 해결</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("🏃 내 투수 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            p_keys = list(mlb_mega_db[u_team]["pitchers"].keys())
            sel_pitcher = st.selectbox("⚾ 투수 선택", p_keys)
        with c2:
            a_team = st.selectbox("🤖 상대 AI 타자 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            
        if st.button("🏟️ 야구 경기 개시"):
            st.session_state.p_team = u_team
            st.session_state.a_team = a_team
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.p_data = mlb_mega_db[u_team]["pitchers"][sel_pitcher]
            st.session_state.a_data = mlb_mega_db[a_team]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_canvas, col_panel = st.columns([3, 1])

    with col_panel:
        st.markdown("### 🎮 MATRIX 경기 패널")
        st.success(f"투수: {st.session_state.pitcher_name}")
        st.selectbox("🙋 타석 타자", st.session_state.a_data["lineup"])
        st.markdown("---")
        if st.button("🚪 메인 화면으로"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_buttons_html = ""
        for idx, p_name in enumerate(st.session_state.p_data['pitches'].keys(), 1):
            bg = "#16a34a" if idx == 1 else "#1e293b"
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" class="p-btn" id="p{idx}" style="background:{bg}; color:white; border:1px solid #16a34a; padding:11px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:7px; font-weight:bold; font-size:13px;">{p_name}</button>'

        html_part = f"""
        <div style="max-width:820px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold;">
                <div>⚾ {st.session_state.pitcher_name} (포수 시점 구동)</div>
                <div id="count-board" style="color:#f59e0b; font-size:16px;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="catcherCanvas" width="560" height="480" style="background:#166534; border:3px solid #334155; border-radius:8px;"></canvas>
                <div style="width:190px; background:#1e293b; padding:12px; border-radius:8px; height:fit-content; border:1px solid #334155;">
                    <span style="color:#94a3b8; font-size:12px; font-weight:bold;">구종 매트릭스</span>
                    <div style="margin-top:8px;">{pitch_buttons_html}</div>
                </div>
            </div>

            <div style="background:#1e293b; border-left:5px solid #16a34a; padding:12px; border-radius:6px; margin-top:10px; font-weight:bold; color:#e2e8f0; font-size:13px;">
                <span id="commentary">🎙️ [현장 전스] 마우스를 조절하고 드래그 릴리즈하여 투구하세요. 유격수는 자기 수비 구역 안에서만 추적합니다.</span>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('catcherCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitchesData = {json.dumps(st.session_state.p_data['pitches'], ensure_ascii=False)};
            let selectedPitch = Object.keys(pitchesData)[0];

            // 🏃 핵심: 유격수의 고유 원래 위치(sx, sy)와 타겟 위치 분리
            let fielder = {{ id: "유격수", x: 220, y: 195, sx: 220, sy: 195, tx: 220, ty: 195 }};

            let isDragging = false;
            let targetPos = {{ x: 280, y: 350 }};

            let ball = {{ active: false, status: "ready", x: 280, y: 150, z: 0.0, tx: 280, ty: 350, speed: 0, drag: 1.0, breakX: 0 }};
            let hitBall = {{ active: false, x: 280, y: 350, vx: 0, vy: 0 }};
            let batter = {{ swinging: false, frame: 0, waitWobble: 0 }};

            function setPitch(pName) {{
                selectedPitch = pName;
                document.querySelectorAll('.p-btn').forEach(b => b.style.backgroundColor = '#1e293b');
                event.target.style.backgroundColor = '#16a34a';
            }}

            function getMousePos(e) {{
                let r = canvas.getBoundingClientRect();
                return {{
                    x: (e.clientX - r.left) * (canvas.width / r.width),
                    y: (e.clientY - r.top) * (canvas.height / r.height)
                }};
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if (!ball.active && !hitBall.active && ball.status === "ready") {{
                    isDragging = true;
                    let m = getMousePos(e); targetPos.x = m.x; targetPos.y = m.y;
                }}
            }});
            canvas.addEventListener('mousemove', (e) => {{
                if (isDragging) {{ let m = getMousePos(e); targetPos.x = m.x; targetPos.y = m.y; }}
            }});
            canvas.addEventListener('mouseup', () => {{
                if (isDragging) {{ isDragging = false; firePitch(); }}
            }});

            function firePitch() {{
                let p = pitchesData[selectedPitch];
                ball.z = 0.0;
                ball.x = 280; ball.y = 150;
                ball.tx = targetPos.x; ball.ty = targetPos.y;
                ball.speed = p.speed;
                ball.drag = p.drag;
                ball.breakX = p.break;

                ball.active = true;
                ball.status = "flying";
                batter.swinging = false; batter.frame = 0;

                // 투구 즉시 수비수 제자리 강제 홀딩 정렬
                fielder.tx = fielder.sx; fielder.ty = fielder.sy;
            }}

            function evaluateZone() {{
                let inside = (ball.x >= 200 && ball.x <= 360 && ball.y >= 250 && ball.y <= 390);
                batter.swinging = true;

                if (Math.random() < (inside ? 0.62 : 0.16)) {{
                    ball.active = false;
                    ball.status = "hit";
                    hitBall.active = true;
                    hitBall.x = ball.x; hitBall.y = ball.y;
                    hitBall.vx = (Math.random() - 0.5) * 14;
                    hitBall.vy = -(5 + Math.random() * 9);

                    let destX = hitBall.x + hitBall.vx * 15;
                    let destY = hitBall.y + hitBall.vy * 15;

                    // 🎯 수비수 AI 한계 사거리 계산 (유격수 기지점 기준 130픽셀 내만 추적)
                    let dist = Math.hypot(fielder.sx - destX, fielder.sy - destY);
                    if (dist < 130) {{
                        fielder.tx = destX; fielder.ty = destY;
                        document.getElementById('commentary').innerText = "🎙️ 깡! 유격수 수비 범위 내 타구! 포구를 향해 이동합니다!";
                    }} else {{
                        // 수비 범위 아웃 시 제자리에 서있거나 아주 미세하게만 몸을 틂 (공을 끝까지 쫓아가지 않음)
                        fielder.tx = fielder.sx + (destX - fielder.sx) * 0.25;
                        fielder.ty = fielder.sy + (destY - fielder.sy) * 0.25;
                        document.getElementById('commentary').innerText = "🎙️ 아! 안타입니다! 유격수의 사거리를 완전히 벗어난 타구입니다!";
                    }}
                }} else {{
                    if (inside) {{ count.s++; }} else {{ count.b++; }}
                    if (count.s >= 3) {{ count.o++; count.s = 0; count.b = 0; }}
                    else if (count.b >= 4) {{ count.s = 0; count.b = 0; }}
                    if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; }}

                    document.getElementById('count-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                    
                    // 정지 버그 제거를 위한 루프 제어 완벽 초기화
                    ball.active = false;
                    ball.status = "ready";
                }}
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 560, 480);
                batter.waitWobble += 0.07;

                // 정통 야구 그라운드 시각화 (녹색 잔디 + 인필드 흙)
                ctx.fillStyle = "#15803d"; ctx.fillRect(0, 0, 560, 480);
                ctx.fillStyle = "#b45309"; ctx.beginPath(); ctx.moveTo(40, 480); ctx.lineTo(240, 150); ctx.lineTo(320, 150); ctx.lineTo(520, 480); ctx.fill();

                // 스트라이크존 아웃라인 가이드
                ctx.strokeStyle = "rgba(255,255,255,0.4)"; ctx.lineWidth = 2; ctx.strokeRect(200, 250, 160, 140);

                // 🧑 정통 라인형 타자 렌더링 복구
                ctx.save();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3;
                let bx = 160, by = 320;
                let headWobble = Math.sin(batter.waitWobble) * 1.2;
                
                ctx.beginPath(); ctx.arc(bx, by - 25 + headWobble, 6, 0, Math.PI * 2); ctx.fillStyle = "#ffffff"; ctx.fill(); // 머리
                ctx.beginPath(); ctx.moveTo(bx, by - 19 + headWobble); ctx.lineTo(bx, by + 10); ctx.stroke(); // 척추
                ctx.beginPath(); ctx.moveTo(bx, by + 10); ctx.lineTo(bx - 9, by + 28); ctx.moveTo(bx, by + 10); ctx.lineTo(bx + 9, by + 28); ctx.stroke(); // 하체

                // 타자 배트 스윙 회전 기믹
                ctx.translate(bx, by - 10);
                if (batter.swinging) {{
                    let swingAngle = (batter.frame / 12) * Math.PI * 0.75;
                    ctx.rotate(swingAngle); batter.frame++;
                    if (batter.frame > 12) batter.swinging = false;
                }}
                ctx.strokeStyle = "#f59e0b"; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(45, -14); ctx.stroke();
                ctx.restore();

                // 🏃 유격수 보간 제어 및 렌더링
                fielder.x += (fielder.tx - fielder.x) * 0.07;
                fielder.y += (fielder.ty - fielder.y) * 0.07;
                ctx.fillStyle = "#3b82f6"; ctx.beginPath(); ctx.arc(fielder.x, fielder.y, 8, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 10px sans-serif"; ctx.fillText(fielder.id, fielder.x - 14, fielder.y - 12);

                if (isDragging) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(targetPos.x, targetPos.y, 9, 0, Math.PI * 2); ctx.stroke();
                }}

                // 투구 실시간 이동 메커니즘
                if (ball.active && ball.status === "flying") {{
                    ball.speed *= ball.drag;
                    ball.z += ball.speed;
                    let bk = Math.sin(ball.z * Math.PI) * ball.breakX * 21;
                    ball.x = 280 + (ball.tx - 280) * ball.z + bk;
                    ball.y = 150 + (ball.ty - 150) * ball.z;

                    let size = Math.max(3, 4 + ball.z * 15);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(ball.x, ball.y, size, 0, Math.PI * 2); ctx.fill();
                    ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 1; ctx.stroke();

                    if (ball.z >= 1.0) {{ ball.z = 1.0; evaluateZone(); }}
                }}

                // 타구 연산 및 수비수 귀환 연동
                if (hitBall.active) {{
                    hitBall.x += hitBall.vx; hitBall.y += hitBall.vy;
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(hitBall.x, hitBall.y, 6, 0, Math.PI * 2); ctx.fill();

                    if (hitBall.y < 0 || hitBall.x < 0 || hitBall.x > 560) {{
                        hitBall.active = false; ball.active = false; ball.status = "ready";
                        
                        // 타구 소멸 시 유격수 원래 위치 좌표로 귀환 명령 수립
                        fielder.tx = fielder.sx; fielder.ty = fielder.sy;
                    }}
                }}

                requestAnimationFrame(drawScene);
            }}
            drawScene();
        </script>
        """
        st.components.v1.html(html_part, height=630)

if __name__ == "__main__":
    main()
