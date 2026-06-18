import streamlit as st

def main():
    # 1. 고화질 스타일링을 위한 기본 설정
    st.set_page_config(page_title="MLB PRO: Ultra HD Simulator", layout="wide")
    
    # 사이드바 제거 및 전체 배경/폰트 커스텀 CSS
    st.markdown("""
        <style>
        .main { background-color: #05070a; color: white; }
        .stSelectbox, .stTextInput, .stSlider { color: white !important; }
        .pitch-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # 상단 럭셔리 헤더
    st.markdown("""
        <div style="background: linear-gradient(90deg, #001529 0%, #003366 50%, #001529 100%); padding: 15px; border-radius: 10px; text-align: center; border-bottom: 3px solid #00e676; margin-bottom: 20px;">
            <h1 style="color: #ffffff; margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 5px; font-size: 40px; text-shadow: 2px 2px 10px rgba(0,230,118,0.5);">MLB PRO <span style="color:#00e676;">SIMULATOR</span></h1>
        </div>
    """, unsafe_allow_html=True)

    # --- [2. MLB 팀 데이터] ---
    mlb_teams = [
        "애리조나 다이아몬드백스", "애틀랜타 브레이브스", "볼티모어 오리올스", "보스턴 레드삭스", 
        "시카고 컵스", "시카고 화이트삭스", "신시내티 레즈", "클리블랜드 가디언스", 
        "콜로라도 로키스", "디트로이트 타이거스", "휴스턴 애스트로스", "캔자스시티 로열스", 
        "로스앤젤레스 에인절스", "로스앤젤레스 다저스", "마이애미 말린스", "밀워키 브루어스", 
        "미네소타 트윈스", "뉴욕 메츠", "뉴욕 양키스", "오클랜드 애슬레틱스", 
        "필라델피아 필리스", "피츠버그 파이어리츠", "샌디에이고 파드리스", "샌프란시스코 자이언츠", 
        "시애틀 매리너스", "세인트루이스 카디널스", "탬파베이 레이스", "텍사스 레인저스", 
        "토론토 블루제이스", "워싱턴 내셔널스"
    ]

    # --- STEP 1: 상단 매치업 선택 ---
    t_col1, t_col2, t_col3 = st.columns([1, 1, 1])
    with t_col1:
        away_team = st.selectbox("⚾ 원정 팀 (AWAY)", mlb_teams, index=18)
    with t_col2:
        home_team = st.selectbox("🏠 홈 팀 (HOME)", mlb_teams, index=13)
    with t_col3:
        pitcher_name = st.text_input("👤 투수 이름", "에이스 투수")

    st.markdown("---")

    # --- STEP 2: 하단 컨트롤 섹션 (선행 정의) ---
    # 그래픽 아래에 두기 위해 변수만 먼저 설정합니다.
    st.markdown("### 🛠️ PITCHER COMMAND CENTER")
    c_col1, c_col2 = st.columns([1, 2])
    with c_col1:
        selected_pitch = st.radio("🔮 구종 장착", ["포심 직구", "슬라이더", "커브"], horizontal=True)
    with c_col2:
        if selected_pitch == "포심 직구":
            p_speed, p_control = st.slider("최고 구속", 85, 105, 98), st.slider("제구력", 1, 100, 90)
        elif selected_pitch == "슬라이더":
            p_speed, p_control = st.slider("구속", 75, 95, 88), st.slider("제구력", 1, 100, 80)
        else:
            p_speed, p_control = st.slider("구속", 65, 88, 78), st.slider("제구력", 1, 100, 75)

    # --- STEP 3: 고화질 메인 시뮬레이션 엔진 ---
    raw_game_html = """
    <div style="background-color: #0a0a0a; padding: 25px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); border: 1px solid #1a1a1a;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-family: sans-serif; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px; border-left: 5px solid #00e676;">
            <div style="flex: 1;">
                <div style="font-size: 10px; color: #aaa; text-transform: uppercase;">Away Team</div>
                <div style="font-size: 18px; font-weight: 900; color: #fff;">__AWAY_TEAM__ <span id="sb-away" style="color:#00e676; margin-left:10px;">0</span></div>
            </div>
            <div style="flex: 0 0 150px; text-align: center;">
                <div id="sb-inning" style="background: #00e676; color: #000; font-size: 14px; font-weight: 800; padding: 5px 15px; border-radius: 20px; display: inline-block;">1회 초</div>
                <div style="display: flex; justify-content: center; gap: 8px; margin-top: 8px;">
                    <div id="b-dots" style="display:flex; gap:3px;"></div>
                    <div id="s-dots" style="display:flex; gap:3px;"></div>
                    <div id="o-dots" style="display:flex; gap:3px;"></div>
                </div>
            </div>
            <div style="flex: 1; text-align: right;">
                <div style="font-size: 10px; color: #aaa; text-transform: uppercase;">Home Team</div>
                <div style="font-size: 18px; font-weight: 900; color: #fff;"><span id="sb-home" style="color:#00e676; margin-right:10px;">0</span> __HOME_TEAM__</div>
            </div>
        </div>

        <canvas id="proCanvas" width="900" height="450" style="border-radius: 10px; cursor: crosshair; background: #000;"></canvas>
        
        <div id="live-ticker" style="margin-top: 15px; background: #000; border: 1px solid #1a1a1a; color: #00e676; font-family: monospace; padding: 12px; height: 60px; overflow-y: auto; font-size: 14px; border-radius: 8px;">
            [INITIALIZING] MLB PRO 데이터 스트리밍 완료... 준비되셨으면 존을 클릭하세요.
        </div>
    </div>

    <script>
        const canvas = document.getElementById('proCanvas');
        const ctx = canvas.getContext('2d');

        const pitchConfig = {
            name: "__PITCHER_NAME__",
            type: "__PITCH_TYPE__",
            speed: __PITCH_SPEED__,
            control: __PITCH_CONTROL__
        };

        let state = {
            away: 0, home: 0, inning: 1, isTop: true,
            b: 0, s: 0, o: 0,
            bases: [false, false, false],
            batter: "AARON JUDGE"
        };

        let mouse = { x: 0, y: 0 };
        let pitch = { active: False, x: 250, y: 250, tx: 0, ty: 0, progress: 0 };
        let history = [];

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
        });

        canvas.addEventListener('mousedown', () => {
            if (pitch.active) return;
            if (mouse.x > 500 && mouse.x < 850 && mouse.y > 50 && mouse.y < 400) {
                let err = (100 - pitchConfig.control) * 0.45;
                pitch.tx = mouse.x + (Math.random() - 0.5) * err;
                pitch.ty = mouse.y + (Math.random() - 0.5) * err;
                pitch.x = 250; pitch.y = 250; pitch.active = true;
            }
        });

        function log(m) {
            const t = document.getElementById('live-ticker');
            t.innerHTML = `<span style="color:#fff;">>></span> ${m}<br>` + t.innerHTML;
        }

        function drawUI() {
            document.getElementById('sb-away').innerText = state.away;
            document.getElementById('sb-home').innerText = state.home;
            document.getElementById('sb-inning').innerText = `${state.inning}회 ${state.isTop ? '초' : '말'}`;
            
            const dot = (c, color) => `<div style="width:10px; height:10px; border-radius:50%; background:${color};"></div>`.repeat(c) + `<div style="width:10px; height:10px; border-radius:50%; background:#222;"></div>`.repeat(3-c);
            document.getElementById('b-dots').innerHTML = dot(state.b, '#22c55e');
            document.getElementById('s-dots').innerHTML = dot(state.s, '#eab308');
            document.getElementById('o-dots').innerHTML = dot(state.o, '#ef4444');
        }

        function resolve() {
            const isStrike = (pitch.tx > 600 && pitch.tx < 780 && pitch.ty > 140 && pitch.ty < 340);
            const speed = pitchConfig.speed + Math.floor(Math.random() * 4) - 2;
            const swing = Math.random() < (isStrike ? 0.6 : 0.25);

            if (swing) {
                if (Math.random() < 0.4) {
                    const hit = Math.random();
                    if (hit < 0.1) {
                        let r = state.bases.filter(b=>b).length + 1;
                        if(state.isTop) state.away += r; else state.home += r;
                        state.bases = [false, false, false];
                        log(`<span style="color:#ff4d4d; font-weight:bold;">HOME RUN!</span> ${state.batter}가 담장을 부숩니다! (${speed} mph)`);
                    } else if (hit < 0.45) {
                        let run = state.bases[2] ? 1 : 0;
                        state.bases = [2,1,0].forEach(i => state.bases[i] = (i==0 ? true : state.bases[i-1]));
                        if(state.isTop) state.away += run; else state.home += run;
                        log(`HIT! 날카로운 타구가 필드를 가릅니다! (${speed} mph)`);
                    } else { state.o++; log(`OUT! 유격수 정면 타구입니다.`); }
                    state.s = 0; state.b = 0;
                } else { state.s++; log(`SWING & MISS! 방망이가 헛돕니다! (${speed} mph)`); }
            } else {
                if (isStrike) { state.s++; log(`STRIKE! 꼼짝 못하는 스트라이크! (${speed} mph)`); }
                else { state.b++; log(`BALL! 타자가 침착하게 참아냅니다.`); }
            }

            if(state.s >= 3) { state.o++; state.s = 0; state.b = 0; log(`STRIKE OUT! 투수의 결정구가 박혔습니다!`); }
            if(state.b >= 4) { state.bases[0] = true; state.s = 0; state.b = 0; log(`WALK! 1루 출루를 허용합니다.`); }
            if(state.o >= 3) { state.o = 0; state.s = 0; state.b = 0; state.bases = [false,false,false]; state.isTop = !state.isTop; if(state.isTop) state.inning++; log(`CHANGE! 이닝이 종료되었습니다.`); }
            
            history.push({x: pitch.tx, y: pitch.ty, s: isStrike});
            if(history.length > 5) history.shift();
            drawUI();
        }

        function render() {
            ctx.clearRect(0,0,900,450);

            // --- 고해상도 스타디움 뷰 (좌측) ---
            const grad = ctx.createRadialGradient(250,225,50,250,225,250);
            grad.addColorStop(0, '#1a3300'); grad.addColorStop(1, '#0d1a00');
            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.ellipse(250, 225, 200, 150, 0, 0, Math.PI*2); ctx.fill();
            
            // 베이스 라인 및 조명 효과
            ctx.strokeStyle = "rgba(255,255,255,0.1)";
            ctx.lineWidth = 2;
            ctx.strokeRect(50, 50, 400, 350);

            function drawBase(x,y,occ) {
                ctx.fillStyle = occ ? "#00e676" : "#222";
                ctx.save(); ctx.translate(x,y); ctx.rotate(45*Math.PI/180);
                ctx.fillRect(-8,-8,16,16); ctx.restore();
            }
            drawBase(350, 225, state.bases[0]); drawBase(250, 125, state.bases[1]); drawBase(150, 225, state.bases[2]);

            // 타자 & 투수 (고급 실루엣)
            ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(250,225,6,0,Math.PI*2); ctx.fill(); // 투수
            ctx.fillStyle = "#00e676"; ctx.beginPath(); ctx.arc(250,335,8,0,Math.PI*2); ctx.fill(); // 타자 머리
            ctx.strokeStyle = "#fb923c"; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(250,335); ctx.lineTo(230,310); ctx.stroke(); // 배트

            // --- 닥터K 스트라이크 존 (우측) ---
            ctx.fillStyle = "rgba(0, 230, 118, 0.05)";
            ctx.fillRect(600, 140, 180, 200);
            ctx.strokeStyle = "#00e676"; ctx.lineWidth = 3;
            ctx.strokeRect(600, 140, 180, 200);
            
            // 격자무늬 (HD 레이더 느낌)
            ctx.strokeStyle = "rgba(255,255,255,0.1)";
            ctx.lineWidth = 1;
            for(let i=1; i<3; i++) {
                ctx.beginPath(); ctx.moveTo(600+(i*60), 140); ctx.lineTo(600+(i*60), 340); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(600, 140+(i*66)); ctx.lineTo(780, 140+(i*66)); ctx.stroke();
            }

            // 에임 크로스헤어
            if (mouse.x > 500 && !pitch.active) {
                ctx.strokeStyle = "#00e676"; ctx.setLineDash([5, 5]);
                ctx.beginPath(); ctx.moveTo(mouse.x, 0); ctx.lineTo(mouse.x, 450); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(500, mouse.y); ctx.lineTo(900, mouse.y); ctx.stroke();
                ctx.setLineDash([]);
                ctx.beginPath(); ctx.arc(mouse.x, mouse.y, 15, 0, Math.PI*2); ctx.stroke();
            }

            // 잔상 기록
            history.forEach(h => {
                ctx.fillStyle = h.s ? "#00e676" : "#ff4d4d";
                ctx.beginPath(); ctx.arc(h.x, h.y, 6, 0, Math.PI*2); ctx.fill();
            });

            // 투구 물리 엔진
            if (pitch.active) {
                pitch.x += (pitch.tx - pitch.x) * 0.14;
                pitch.y += (pitch.ty - pitch.y) * 0.14;
                
                // 변화구 무브먼트
                if(pitchConfig.type == "슬라이더") pitch.x += 1.5;
                if(pitchConfig.type == "커브") pitch.y += 2.0;

                ctx.fillStyle = "#fff"; ctx.shadowBlur = 15; ctx.shadowColor = "#fff";
                ctx.beginPath(); ctx.arc(pitch.x, pitch.y, 8, 0, Math.PI*2); ctx.fill();
                ctx.shadowBlur = 0;

                if (Math.abs(pitch.x - pitch.tx) < 2) {
                    pitch.active = false;
                    resolve();
                }
            }

            requestAnimationFrame(render);
        }
        drawUI(); render();
    </script>
    """

    # 4. 데이터 주입 및 HTML 출력
    final_html = raw_game_html.replace("__AWAY_TEAM__", away_team).replace("__HOME_TEAM__", home_team).replace("__PITCHER_NAME__", pitcher_name).replace("__PITCH_TYPE__", selected_pitch).replace("__PITCH_SPEED__", str(p_speed)).replace("__PITCH_CONTROL__", str(p_control))

    st.components.v1.html(final_html, height=700)

if __name__ == "__main__":
    main()
