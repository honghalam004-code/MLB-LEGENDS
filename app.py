import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB 30 TEAMS PERFECT STRATEGY ENGINE v4", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #05070c; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
        .stSelectbox > div > div { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #22c55e !important; }
        .stButton > button {
            background: linear-gradient(135deg, #22c55e 0%, #15803d 100%) !important;
            color: white !important; font-weight: bold !important; border: none !important; padding: 14px; border-radius: 8px; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # ⚾ MLB 30개 전 구단 실존 원투펀치 데이터셋
    mlb_30_teams = {
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {"포심 패스트볼": {"speed": 0.046, "bx": 0.0, "by": -0.2}, "마스터 스위퍼": {"speed": 0.032, "bx": -6.5, "by": 0.5}},
                "타일러 글래스노우": {"하이 패스트볼": {"speed": 0.047, "bx": 0.2, "by": -0.6}, "파워 커브": {"speed": 0.031, "bx": 0.5, "by": 5.5}}
            }
        },
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스": {"포심 강속구": {"speed": 0.048, "bx": 0.0, "by": -0.5}, "고속 스플린커": {"speed": 0.042, "bx": 1.5, "by": 3.5}},
                "미치 켈러": {"싱커": {"speed": 0.040, "bx": 3.0, "by": 2.0}, "컷 패스트볼": {"speed": 0.043, "bx": -1.5, "by": 0.5}}
            }
        },
        "NY Yankees": {
            "pitchers": {
                "게릿 콜": {"라이징 패스트볼": {"speed": 0.045, "bx": 0.0, "by": -0.7}, "너클 커브": {"speed": 0.030, "bx": 0.8, "by": 5.2}},
                "카를로스 로돈": {"파워 슬라이더": {"speed": 0.036, "bx": -3.5, "by": 1.5}, "포심 패스트볼": {"speed": 0.044, "bx": 0.0, "by": -0.4}}
            }
        },
        "Atlanta Braves": {
            "pitchers": {
                "스펜서 스트라이더": {"괴물 포심": {"speed": 0.049, "bx": 0.0, "by": -0.8}, "악마 슬라이더": {"speed": 0.038, "bx": -3.5, "by": 1.5}},
                "크리스 세일": {"전성기 슬라이더": {"speed": 0.034, "bx": -5.8, "by": 1.0}, "싱커": {"speed": 0.041, "bx": 3.8, "by": 2.2}}
            }
        },
        "SD Padres": {
            "pitchers": {
                "딜런 시즈": {"파워 슬라이더": {"speed": 0.037, "bx": -4.0, "by": 2.0}, "포심 패스트볼": {"speed": 0.045, "bx": 0.0, "by": -0.3}},
                "다르빗슈 유": {"마구 슬러브": {"speed": 0.031, "bx": -5.0, "by": 4.0}, "스플리터": {"speed": 0.039, "bx": 0.8, "by": 3.8}}
            }
        },
        "SF Giants": {
            "pitchers": {
                "로건 웹": {"명품 체인지업": {"speed": 0.033, "bx": 3.5, "by": 4.0}, "프론트도어 싱커": {"speed": 0.040, "bx": 4.2, "by": 1.8}},
                "로비 레이": {"K-슬라이더": {"speed": 0.035, "bx": -3.8, "by": 2.2}, "포심": {"speed": 0.043, "bx": 0.0, "by": -0.4}}
            }
        },
        "NY Mets": {
            "pitchers": {
                "센가 고다이": {"고스트 포크": {"speed": 0.036, "bx": 0.5, "by": 5.8}, "컷 패스트볼": {"speed": 0.043, "bx": -1.8, "by": 0.4}},
                "루이스 세베리노": {"파워 싱커": {"speed": 0.042, "bx": 3.2, "by": 2.0}, "슬라이더": {"speed": 0.035, "bx": -3.0, "by": 1.2}}
            }
        },
        "PHI Phillies": {
            "pitchers": {
                "잭 휠러": {"고속 싱커": {"speed": 0.046, "bx": 3.5, "by": 1.5}, "스위퍼": {"speed": 0.034, "bx": -5.5, "by": 0.8}},
                "애런 놀라": {"명품 너클커브": {"speed": 0.029, "bx": 1.2, "by": 5.6}, "체인지업": {"speed": 0.033, "bx": 2.5, "by": 3.2}}
            }
        },
        "TEX Rangers": {
            "pitchers": {
                "제이콥 디그롬": {"전성기 포심": {"speed": 0.050, "bx": 0.0, "by": -0.9}, "고속 슬라이더": {"speed": 0.042, "bx": -3.0, "by": 0.8}},
                "네이선 이볼디": {"스플리터": {"speed": 0.040, "bx": 0.5, "by": 4.2}, "커터": {"speed": 0.044, "bx": -1.5, "by": 0.6}}
            }
        },
        "HOU Astros": {
            "pitchers": {
                "프람버 발데스": {"폭포수 싱커": {"speed": 0.041, "bx": 4.2, "by": 3.0}, "커브볼": {"speed": 0.029, "bx": 0.4, "by": 5.4}},
                "크리스티안 하비에르": {"라이징 패스트볼": {"speed": 0.043, "bx": -0.2, "by": -0.6}, "슬라이더": {"speed": 0.034, "bx": -3.2, "by": 1.6}}
            }
        },
        "SEA Mariners": {
            "pitchers": {
                "루이스 카스티요": {"위력적 체인지업": {"speed": 0.035, "bx": 3.8, "by": 3.8}, "싱커": {"speed": 0.045, "bx": 3.5, "by": 1.2}},
                "조지 커비": {"송곳 제구 포심": {"speed": 0.045, "bx": 0.0, "by": -0.4}, "슬라이더": {"speed": 0.036, "bx": -3.0, "by": 1.0}}
            }
        },
        "BAL Orioles": {
            "pitchers": {
                "코빈 번스": {"악마 커터": {"speed": 0.044, "bx": -3.2, "by": 0.5}, "파워 커브": {"speed": 0.031, "bx": 0.8, "by": 5.0}},
                "카일 브래디시": {"고속 스위퍼": {"speed": 0.034, "bx": -6.0, "by": 0.6}, "싱커": {"speed": 0.042, "bx": 3.0, "by": 1.8}}
            }
        },
        "TOR Blue Jays": {
            "pitchers": {
                "케빈 가우스먼": {"종떨어지는 스플리터": {"speed": 0.038, "bx": 0.4, "by": 5.5}, "포심 패스트볼": {"speed": 0.044, "bx": 0.0, "by": -0.3}},
                "호세 베리오스": {"파워 슬러브": {"speed": 0.032, "bx": -4.2, "by": 3.8}, "싱커": {"speed": 0.042, "bx": 3.2, "by": 2.0}}
            }
        }
    }

    remaining_teams = {
        "CHC Cubs": ("저스틴 스틸", "슬라이더", "제임슨 타이온", "커터"),
        "STL Cardinals": ("소니 그레이", "스위퍼", "마일스 마이콜라스", "싱커"),
        "MIL Brewers": ("프레디 페랄타", "페스트볼", "브랜든 우드러프", "체인지업"),
        "CIN Reds": ("헌터 Greene", "강속구", "닉 로돌로", "커브"),
        "MIA Marlins": ("샌디 알칸타라", "체인지업", "헤수스 루자르도", "슬라이더"),
        "WSH Nationals": ("조시아 그레이", "슬라이더", "맥켄지 고어", "포심"),
        "TB Rays": ("셰인 맥클라나한", "체인지업", "잭 래텔", "커브"),
        "BOS Red Sox": ("루카스 지올리토", "체인지업", "브라얀 벨로", "싱커"),
        "CLE Guardians": ("태너 바이비", "슬라이더", "트리스탄 맥켄지", "커브"),
        "MIN Twins": ("파블로 로페즈", "체인지업", "조 라이언", "스위퍼"),
        "DET Tigers": ("타릭 스쿠발", "강속구", "마에다 켄타", "스플리터"),
        "KC Royals": ("콜 라간스", "체인지업", "세스 루고", "커브"),
        "CWS White Sox": ("가렛 크로셰", "포심", "크리스 플렉센", "체인지업"),
        "ARI Diamondbacks": ("잭 갤런", "너클커브", "메릴 켈리", "체인지업"),
        "COL Rockies": ("카일 프리랜드", "슬라이더", "오스틴 곰버", "체인지업"),
        "LAA Angels": ("패트릭 산도발", "체인지업", "타일러 안더슨", "커터"),
        "OAK Athletics": ("JP 시어스", "슬라이더", "미치 스펜스", "커터")
    }

    for t_name, data in remaining_teams.items():
        mlb_30_teams[t_name] = {
            "pitchers": {
                data[0]: {f"고증 {data[1]}": {"speed": 0.035, "bx": -3.5, "by": 2.0}, "하이 패스트볼": {"speed": 0.044, "bx": 0.0, "by": -0.4}},
                data[2]: {f"주무기 {data[3]}": {"speed": 0.040, "bx": 3.2, "by": 1.8}, "포심": {"speed": 0.043, "bx": 0.0, "by": -0.3}}
            }
        }

    sorted_teams = sorted(list(mlb_30_teams.keys()))

    if not st.session_state.game_active:
        st.markdown("<h2 style='text-align:center; color:#22c55e; font-weight:800; margin-top:20px;'>🏟️ MLB 30 TEAMS PERFECT STRATEGY ENGINE v4</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_team = st.selectbox("투수 구단 선택", sorted_teams, index=sorted_teams.index("LA Dodgers"))
            sel_pitcher = st.selectbox("선발 투수 선택 (실존 원투펀치)", list(mlb_30_teams[u_team]["pitchers"].keys()))
        with c2:
            a_team = st.selectbox("타자 구단 선택", sorted_teams, index=sorted_teams.index("Pittsburgh Pirates"))
            
        if st.button("🏟️ 고증 프로필 그라운드 오픈"):
            st.session_state.p_team = u_team
            st.session_state.a_team = a_team
            st.session_state.pitcher_name = sel_pitcher
            st.session_state.p_data = mlb_30_teams[u_team]["pitchers"][sel_pitcher]
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_canvas, col_panel = st.columns([3.9, 1.1])

    with col_panel:
        st.markdown("### 📊 MATCH DASHBOARD")
        st.success(f"**투수:** {st.session_state.pitcher_name}\n\n**팀:** {st.session_state.p_team}")
        st.warning(f"**공격팀:** {st.session_state.a_team}")
        st.markdown("---")
        if st.button("🚪 구단 재선택"):
            st.session_state.game_active = False
            st.rerun()

    with col_canvas:
        pitch_names = list(st.session_state.p_data.keys())
        pitch_buttons = ""
        for idx, p_name in enumerate(pitch_names):
            active_style = "background:#22c55e; border:2px solid #ffffff;" if idx == 0 else "background:#1e293b; border:1px solid #22c55e;"
            pitch_buttons += f'<button id="pbtn-{idx}" onclick="selectPitchType(\'{p_name}\', {idx})" style="{active_style} color:white; padding:12px; border-radius:6px; cursor:pointer; width:100%; margin-bottom:8px; font-weight:bold;">{p_name}</button>'

        html_src = f"""
        <div style="max-width:1100px; margin:0 auto;">
            <div style="background:#1e293b; color:white; padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin-bottom:10px; font-weight:bold; border:1px solid #334155;">
                <div style="color:#67e8f9;">🏟️ {st.session_state.p_team} VS {st.session_state.a_team}</div>
                <div id="score-board" style="color:#fbbf24;">B: 0 | S: 0 | O: 0</div>
            </div>

            <div style="display:flex; gap:15px;">
                <canvas id="ballCanvas" width="760" height="540" style="background:#14532d; border:4px solid #334155; border-radius:8px; cursor:crosshair;"></canvas>
                
                <div style="width:240px; background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; height:fit-content; display:flex; flex-direction:column; gap:10px;">
                    <span style="color:#22c55e; font-size:12px; font-weight:bold;">1️⃣ 1단계: 구종 고르기</span>
                    <div>{pitch_buttons}</div>
                    
                    <span style="color:#94a3b8; font-size:11px; color:#e2e8f0; font-weight:bold; background:#0f172a; padding:6px; border-radius:4px; text-align:center;">💡 그라운드 클릭 시 피칭 스타트!</span>
                    
                    <span style="color:#94a3b8; font-size:12px; font-weight:bold; margin-top:5px;">📋 작전 지시 벤치</span>
                    <button id="bunt-toggle" onclick="toggleBunt()" style="background:#475569; color:white; border:1px solid #64748b; padding:10px; border-radius:6px; cursor:pointer; font-weight:bold; text-align:center;">🎯 번트 모션: OFF</button>
                    <button id="steal-btn" onclick="triggerSteal()" style="background:#b45309; color:white; border:none; padding:10px; border-radius:6px; cursor:not-allowed; font-weight:bold; opacity:0.4;" disabled>🏃 기습 도루 감행</button>
                    
                    <div style="background:#0f172a; padding:10px; border-radius:6px; font-size:13px; font-weight:bold; text-align:center; color:#38bdf8;" id="base-viewer">주자 없음</div>
                </div>
            </div>

            <div style="background:#0f172a; border-left:6px solid #22c55e; padding:12px; border-radius:6px; margin-top:12px;">
                <div style="font-size:12px; color:#22c55e; font-weight:800; margin-bottom:4px;">🎙️ REAL MLB 중계석 (타구 궤적 및 야수 유기적 동시 이동 고증 버전)</div>
                <div id="relay-container" style="color:#f1f5f9; font-size:14px; font-family:monospace; max-height:100px; overflow-y:auto; display:flex; flex-direction:column-reverse; gap:4px;">
                    <div style="color: #a1a1aa;">[엔진] 타구 속도/높이(그림자 연산)와 전체 수비대의 백업 수비 기동 로직이 가동 중입니다.</div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('ballCanvas');
            const ctx = canvas.getContext('2d');

            let count = {{ b: 0, s: 0, o: 0 }};
            const pitches = {json.dumps(st.session_state.p_data, ensure_ascii=False)};
            const totalPitchCount = {len(pitch_names)};
            
            let selectedPitchName = "{pitch_names[0]}";

            // 각 야수 피규어들의 초기 고유 세팅
            let players = [
                {{ id: "투수", num: "1", x: 380, y: 180, sx: 380, sy: 180, tx: 380, ty: 180, speedFactor: 0.08 }},
                {{ id: "포수", num: "2", x: 380, y: 495, sx: 380, sy: 495, tx: 380, ty: 495, speedFactor: 0.05 }},
                {{ id: "1루수", num: "3", x: 600, y: 300, sx: 600, sy: 300, tx: 600, ty: 300, speedFactor: 0.10 }},
                {{ id: "2루수", num: "4", x: 490, y: 220, sx: 490, sy: 220, tx: 490, ty: 220, speedFactor: 0.12 }},
                {{ id: "3루수", num: "5", x: 160, y: 300, sx: 160, sy: 300, tx: 160, ty: 300, speedFactor: 0.10 }},
                {{ id: "유격수", num: "6", x: 270, y: 220, sx: 270, sy: 220, tx: 270, ty: 220, speedFactor: 0.13 }},
                {{ id: "좌익수", num: "7", x: 140, y: 110, sx: 140, sy: 110, tx: 140, ty: 110, speedFactor: 0.14 }},
                {{ id: "중견수", num: "8", x: 380, y: 80, sx: 380, sy: 80, tx: 380, ty: 80, speedFactor: 0.15 }},
                {{ id: "우익수", num: "9", x: 620, y: 110, sx: 620, sy: 110, tx: 620, ty: 110, speedFactor: 0.14 }}
            ];

            let runner = {{ active: false, x: 600, y: 300, status: "stay" }}; 
            let targetPos = {{ x: 380, y: 400 }};
            let isBuntMode = false;
            let stealTriggered = false;

            let ballActive = false;
            let ballX = 380, ballY = 180, ballZ = 0.0;
            let ballTx = 380, ballTy = 400;
            let ballSpeed = 0.04, ballBx = 0, ballBy = 0;

            // 💥 타구 궤적(포물선 높이 및 그림자) 고증 변수
            let hitActive = false;
            let hitX = 380, hitY = 400;
            let hitDestX = 380, hitDestY = 150;
            let hitProgress = 0.0;
            let hitSpeed = 0.02;
            let maxHitHeight = 60; // 뜬공의 최대 높이 정점 스케일

            let batterSwinging = false, batterFrame = 0;

            function addLog(msg) {{
                const container = document.getElementById('relay-container');
                const div = document.createElement('div');
                div.innerHTML = msg;
                container.insertBefore(div, container.firstChild);
            }}

            function selectPitchType(name, targetIdx) {{
                if (ballActive || hitActive) return;
                selectedPitchName = name;
                for (let i = 0; i < totalPitchCount; i++) {{
                    const btn = document.getElementById('pbtn-' + i);
                    if (btn) {{
                        if (i === targetIdx) {{
                            btn.style.background = "#22c55e";
                            btn.style.border = "2px solid #ffffff";
                        }} else {{
                            btn.style.background = "#1e293b";
                            btn.style.border = "1px solid #22c55e";
                        }}
                    }}
                }}
            }}

            function toggleBunt() {{
                if (ballActive || hitActive) return;
                isBuntMode = !isBuntMode;
                const btn = document.getElementById('bunt-toggle');
                if (isBuntMode) {{
                    btn.innerText = "🎯 번트 모션: ON";
                    btn.style.background = "#2563eb";
                }} else {{
                    btn.innerText = "🎯 번트 모션: OFF";
                    btn.style.background = "#475569";
                }}
            }}

            function triggerSteal() {{
                if (!runner.active || ballActive || hitActive) return;
                stealTriggered = true;
                addLog("<span style='color:#fbbf24;'>🏃 [작전 실행] 1루 주자가 2루를 향해 리드오프 스타트를 끊었습니다!</span>");
            }}

            function updateBaseUI() {{
                const viewer = document.getElementById('base-viewer');
                const stealBtn = document.getElementById('steal-btn');
                
                if (runner.active && runner.status === "stay") {{
                    viewer.innerText = "주자 1루";
                    stealBtn.removeAttribute('disabled');
                    stealBtn.style.cursor = "pointer";
                    stealBtn.style.opacity = "1";
                }} else if (runner.active && runner.status === "second") {{
                    viewer.innerText = "주자 2루";
                    stealBtn.setAttribute('disabled', 'true');
                    stealBtn.style.cursor = "not-allowed";
                    stealBtn.style.opacity = "0.4";
                }} else {{
                    viewer.innerText = "주자 없음";
                    stealBtn.setAttribute('disabled', 'true');
                    stealBtn.style.cursor = "not-allowed";
                    stealBtn.style.opacity = "0.4";
                }}
            }}

            // 2단계: 그라운드 조준 피칭 개시
            canvas.addEventListener('mousedown', (e) => {{
                if (ballActive || hitActive) return;
                
                let r = canvas.getBoundingClientRect();
                targetPos.x = (e.clientX - r.left) * (760 / r.width);
                targetPos.y = (e.clientY - r.top) * (540 / r.height);
                
                let p = pitches[selectedPitchName];
                ballX = 380; ballY = 180; ballZ = 0.0;
                ballTx = targetPos.x; ballTy = targetPos.y;
                ballSpeed = p.speed; ballBx = p.bx; ballBy = p.by;
                
                ballActive = true;
                hitActive = false;
                batterSwinging = false;
                batterFrame = 0;

                if (stealTriggered) runner.status = "running";

                addLog("⚾ 피칭 가동: [" + selectedPitchName + "] 조준점 투구!");
                players.forEach(pl => {{ pl.tx = pl.sx; pl.ty = pl.sy; }});
            }});

            function judgeZone() {{
                ballActive = false;
                let isStrike = (ballX >= 290 && ballX <= 470 && ballY >= 290 && ballY <= 430);
                batterSwinging = true;

                if (isBuntMode) {{
                    isBuntMode = false;
                    document.getElementById('bunt-toggle').innerText = "🎯 번트 모션: OFF";
                    document.getElementById('bunt-toggle').style.background = "#475569";

                    if (Math.random() < (isStrike ? 0.85 : 0.40)) {{
                        hitActive = true;
                        hitProgress = 0.0;
                        hitX = ballX; hitY = ballY;
                        hitDestX = ballX + (Math.random() - 0.5) * 80;
                        hitDestY = ballY - (40 + Math.random() * 50); // 투수-내야진 사이 짧게 구르는 번트
                        hitSpeed = 0.03;
                        maxHitHeight = 5; // 번트는 고도가 거의 없음

                        addLog("<span style='color:#38bdf8;'>🎯 [기습 번트 내야 로직] 배트에 툭 맞아 투수 앞으로 힘없이 굴러갑니다!</span>");
                        
                        // 💥 전체 수비수 유기적 타구 예측 대형 이동 개시
                        players.forEach(pl => {{
                            if (pl.id === "투수" || pl.id === "1루수" || pl.id === "3루수") {{
                                pl.tx = hitDestX; pl.ty = hitDestY; // 직접 포구 기동
                            } else {{
                                pl.tx = pl.sx + (hitDestX - pl.sx) * 0.2; pl.ty = pl.sy + (hitDestY - pl.sy) * 0.2; // 백업 커버
                            }}
                        }});
                        return;
                    }} else {{
                        addLog("🎯 번트 파울!");
                        count.s++;
                    }}
                }} else {{
                    if (Math.random() < (isStrike ? 0.60 : 0.15)) {{
                        hitActive = true;
                        hitProgress = 0.0;
                        hitX = ballX; hitY = ballY;
                        
                        // 대각선 좌/우/중앙 외야 전역 낙하지점 고증 수학적 분산
                        hitDestX = 100 + Math.random() * 560;
                        hitDestY = 50 + Math.random() * 180;
                        hitSpeed = 0.015 + Math.random() * 0.015;
                        maxHitHeight = 35 + Math.random() * 55; // 팝플라이 및 장타 고도 연산셋

                        addLog("<span style='color:#f87171;'>💥 타격 폭발!! 타구가 큰 포물선을 그리며 외야 관중석 방향으로 날아갑니다!</span>");

                        // 💥 전체 수비수 유기적 동시 대형 백업 이동
                        players.forEach(pl => {{
                            if (pl.id !== "포수") {{
                                // 타구 낙하지점을 향해 모든 수비수가 각자의 고유 속도로 기동 및 백업 포메이션 빌드
                                let distToDest = Math.hypot(hitDestX - pl.sx, hitDestY - pl.sy);
                                if (distToDest < 260) {{
                                    pl.tx = hitDestX; pl.ty = hitDestY; // 주 타겟 수비수 대시
                                }} else {{
                                    // 나머지 수비수들은 송구 길목 및 베이스 커버를 위한 유기적 방향 이동
                                    pl.tx = pl.sx + (hitDestX - pl.sx) * 0.35;
                                    pl.ty = pl.sy + (hitDestY - pl.sy) * 0.35;
                                }}
                            }}
                        }});
                        return;
                    }} else {{
                        if (isStrike) {{ count.s++; addLog("스트라이크 존 통과!"); }}
                        else {{ count.b++; addLog("볼 판정!"); }}
                    }}
                }}

                // 도루 러닝 판정
                if (runner.status === "running") {{
                    stealTriggered = false;
                    if (runner.y <= 245) {{
                        runner.status = "second";
                        runner.x = 490; runner.y = 220;
                        addLog("<span style='color:#22c55e; font-weight:bold;'>🏃 [도루 세이프] 주자 완벽한 도루 성공!</span>");
                    }} else {{
                        runner.active = false; runner.status = "stay";
                        runner.x = 600; runner.y = 300;
                        count.o++;
                        addLog("<span style='color:#ef4444; font-weight:bold;'>❌ [도루 저지] 포수의 2루 송구 아웃!</span>");
                    }}
                }}

                if (count.s >= 3) {{ count.o++; count.s = 0; count.b = 0; addLog("❌ 삼진 아웃!"); }}
                else if (count.b >= 4) {{ count.s = 0; count.b = 0; runner.active = true; runner.status = "stay"; addLog("🏃 볼넷 출루!"); }}
                if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; runner.active = false; runner.status = "stay"; addLog("🔄 쓰리아웃 공수 교대!"); }}
                
                document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                updateBaseUI();
            }}

            function drawRealisticPlayer(pl) {{
                ctx.save();
                ctx.fillStyle = "#1e3a8a"; 
                ctx.fillRect(pl.x - 12, pl.y - 1, 24, 9);
                ctx.fillStyle = "#3b82f6"; 
                ctx.fillRect(pl.x - 5, pl.y - 8, 10, 7);
                ctx.fillStyle = "#1d4ed8"; 
                ctx.fillRect(pl.x - 6, pl.y - 8, 3, 2);
                ctx.fillStyle = "#b45309"; 
                ctx.fillRect(pl.x + 6, pl.y + 1, 5, 5);
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 8px monospace";
                ctx.fillText(pl.num, pl.x - 3, pl.y + 6);
                ctx.fillStyle = "#e2e8f0"; ctx.font = "10px sans-serif";
                ctx.fillText(pl.id, pl.x - 15, pl.y - 12);
                ctx.restore();
            }}

            function loop() {{
                ctx.clearRect(0, 0, 760, 540);

                ctx.fillStyle = "#15803d"; ctx.fillRect(0, 0, 760, 540);
                ctx.fillStyle = "#9a3412"; ctx.beginPath(); ctx.moveTo(40, 540); ctx.lineTo(330, 180); ctx.lineTo(430, 180); ctx.lineTo(720, 540); ctx.fill();

                ctx.strokeStyle = "rgba(255,255,255,0.25)"; ctx.lineWidth = 2; ctx.strokeRect(290, 290, 180, 140);
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(380, 460); ctx.lineTo(405, 475); ctx.lineTo(405, 495); ctx.lineTo(355, 495); ctx.lineTo(355, 475); ctx.fill();

                // 타자 드로우 및 모션 연산
                ctx.save(); ctx.translate(230, 360);
                ctx.fillStyle = "#cbd5e1"; ctx.fillRect(-4, -26, 8, 7);
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, -19); ctx.lineTo(0, 12); ctx.stroke();
                
                if (batterSwinging) {{
                    let ang = (batterFrame / 8) * Math.PI * 0.85; ctx.rotate(ang); batterFrame++;
                    if (batterFrame > 8) batterSwinging = false;
                }} else if (isBuntMode) {{
                    ctx.rotate(Math.PI * 0.35); 
                }} else {{
                    ctx.rotate(-Math.PI * 0.15);
                }}
                ctx.strokeStyle = "#d97706"; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(42, -12); ctx.stroke();
                ctx.restore();

                // 주자 도루 궤적 연산
                if (runner.active) {{
                    if (runner.status === "running") {{
                        let dx = 490 - runner.x, dy = 220 - runner.y;
                        let dist = Math.hypot(dx, dy);
                        if (dist > 2) {{
                            runner.x += (dx / dist) * 3.3;
                            runner.y += (dy / dist) * 2.4;
                        }}
                    }}
                    ctx.fillStyle = "#dc2626"; ctx.fillRect(runner.x - 7, runner.y - 7, 14, 11);
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 8px Arial"; ctx.fillText("RUN", runner.x-7, runner.y-10);
                }}

                // 수비수 이동 처리 루프
                players.forEach(pl => {{
                    // 각 야수의 speedFactor 가중치치를 곱해 기동 속도 고증 차별화
                    pl.x += (pl.tx - pl.x) * pl.speedFactor; 
                    pl.y += (pl.ty - pl.y) * pl.speedFactor;
                    drawRealisticPlayer(pl);
                }});

                if (!ballActive && !hitActive) {{
                    ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 2; ctx.strokeRect(targetPos.x - 6, targetPos.y - 6, 12, 12);
                }}

                // 1. 투구 물리 변화구 연산
                if (ballActive) {{
                    ballZ += ballSpeed;
                    if (ballZ > 1.0) ballZ = 1.0;
                    
                    let mx = Math.sin(ballZ * Math.PI) * ballBx * 4.2;
                    let my = Math.pow(ballZ, 2) * ballBy * 3.8;

                    ballX = 380 + (ballTx - 380) * ballZ + mx;
                    ballY = 180 + (ballTy - 180) * ballZ + my;

                    ctx.save(); ctx.translate(ballX, ballY);
                    let bSize = Math.max(4.0, 4.0 + ballZ * 14);
                    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(0, 0, bSize, 0, Math.PI*2); ctx.fill();
                    ctx.restore();

                    if (ballZ >= 1.0) {{
                        judgeZone();
                    }}
                }}

                // 2. 💥 친 공의 공중 포물선 궤적 및 그림자 + 야수 다이나믹 포구 연산
                if (hitActive) {{
                    hitProgress += hitSpeed;
                    if (hitProgress > 1.0) hitProgress = 1.0;

                    // 낙하지점(hitDest)을 향해 뻗어가는 실시간 투영 좌표
                    hitX = ballTx + (hitDestX - ballTx) * hitProgress;
                    hitY = ballTy + (hitDestY - ballTy) * hitProgress;

                    // 포물선 최고점 연산 수식 ($sin$ 주기)
                    let currentHeight = Math.sin(hitProgress * Math.PI) * maxHitHeight;

                    // 1) 지면 그림자 먼저 드로우
                    ctx.fillStyle = "rgba(0, 0, 0, 0.35)";
                    ctx.beginPath();
                    ctx.arc(hitX, hitY, 5, 0, Math.PI * 2);
                    ctx.fill();

                    // 2) 실제 떠 있는 공 드로우 (높이에 따라 원형 크기가 동적으로 스케일링됨)
                    ctx.save();
                    ctx.translate(hitX, hitY - currentHeight);
                    let currentBallSize = 5 + (currentHeight * 0.2); // 고도 비례 스케일 증가
                    ctx.fillStyle = "#ffffff";
                    ctx.beginPath();
                    ctx.arc(0, 0, currentBallSize, 0, Math.PI * 2);
                    ctx.fill();
                    // 실밥 라인 추가
                    ctx.strokeStyle = "#ef4444";
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.arc(-currentBallSize*0.1, 0, currentBallSize * 0.7, -Math.PI*0.2, Math.PI*0.2);
                    ctx.stroke();
                    ctx.restore();

                    // 3) 낙하 시 수비수 도달 여부 계산 판정
                    if (hitProgress >= 1.0) {{
                        hitActive = false;
                        
                        // 전원 복귀 지시
                        players.forEach(p => {{ p.tx = p.sx; p.ty = p.sy; }});
                        
                        // 낙하지점 기준 가장 가까이 온 수비수 서치
                        let caught = false;
                        players.forEach(pl => {{
                            if (pl.id !== "포수" && pl.id !== "투수") {{
                                if (Math.hypot(pl.x - hitDestX, pl.y - hitDestY) < 32) {{
                                    caught = true;
                                }}
                            }}
                        }});

                        count.s = 0; count.b = 0;
                        if (caught) {{
                            count.o++;
                            addLog("🧤 <span style='color:#38bdf8; font-weight:bold;'>[수비 성공] 수비수 피구어 부대가 낙하지점에 신속 기동하여 플라이 아웃 처리했습니다!</span>");
                        }} else {{
                            if (!runner.active) {{
                                runner.active = true; runner.status = "stay"; runner.x = 600; runner.y = 300;
                                addLog("📢 <span style='color:#22c55e; font-weight:bold;'>안타!! 야수진이 공을 쫓아갔으나 간발의 차로 낙하를 허용했습니다!</span>");
                            }} else {{
                                runner.active = false; runner.status = "stay";
                                addLog("🎉 <span style='color:#fbbf24; font-weight:bold;'>홈인!! 외야를 완전히 갈라버린 깊숙한 장타로 득점에 성공합니다!</span>");
                            }}
                        }}

                        if (count.o >= 3) {{ count.o = 0; count.s = 0; count.b = 0; runner.active = false; runner.status = "stay"; addLog("🔄 쓰리아웃 공수 교대!"); }}
                        document.getElementById('score-board').innerText = "B: " + count.b + " | S: " + count.s + " | O: " + count.o;
                        updateBaseUI();
                    }}
                }}

                requestAnimationFrame(loop);
            }}
            loop();
        </script>
        """
        st.components.v1.html(html_src, height=700)

if __name__ == "__main__":
    main()
