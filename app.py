import streamlit as st
import random
import time

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="미니 MLB 시뮬레이터", layout="centered")
st.title("⚾ 초간단 MLB 야구 시뮬레이터 v1.0")
st.write("버튼을 눌러 투수와 타자의 대결을 진행하세요!")

# 2. 게임 상태(Session State) 초기화
# 스트림릿은 버튼을 누르면 코드가 처음부터 다시 실행되므로, 경기 데이터를 저장해두어야 합니다.
if 'inning' not in st.session_state:
    st.session_state.inning = 1
    st.session_state.half = "초"  # 초 또는 말
    st.session_state.outs = 0
    st.session_state.strikes = 0
    st.session_state.balls = 0
    st.session_state.score = {"AWAY": 0, "HOME": 0}
    st.session_state.bases = [False, False, False]  # 1루, 2루, 3루 주자 여부
    st.session_state.log = []  # 경기 중계 기록

# 3. 게임 리셋 함수
def reset_game():
    st.session_state.inning = 1
    st.session_state.half = "초"
    st.session_state.outs = 0
    st.session_state.strikes = 0
    st.session_state.balls = 0
    st.session_state.score = {"AWAY": 0, "HOME": 0}
    st.session_state.bases = [False, False, False]
    st.session_state.log = ["경기가 초기화되었습니다."]

# 4. 투구 결과 계산 로직 (가장 단순한 확률 모델)
def play_pitch():
    # 확률 설정 (추후 이 부분을 선수 스탯 기반으로 디테일하게 업그레이드합니다)
    pitch_result = random.choices(
        ["스트라이크", "볼", "안타", "아웃", "홈런"],
        weights=[30, 30, 15, 20, 5],
        k=1
    )[0]
    
    current_team = "AWAY" if st.session_state.half == "초" else "HOME"
    
    if pitch_result == "스트라이크":
        st.session_state.strikes += 1
        st.session_state.log.insert(0, f"⚾ 스트라이크! (C: {st.session_state.balls}B {st.session_state.strikes}S)")
        if st.session_state.strikes >= 3:
            st.session_state.outs += 1
            st.session_state.strikes = 0
            st.session_state.balls = 0
            st.session_state.log.insert(0, f"❌ 삼진 아웃!! (아웃: {st.session_state.outs})")

    elif pitch_result == "볼":
        st.session_state.balls += 1
        st.session_state.log.insert(0, f"🟢 볼! (C: {st.session_state.balls}B {st.session_state.strikes}S)")
        if st.session_state.balls >= 4:
            st.session_state.strikes = 0
            st.session_state.balls = 0
            # 볼넷 주자 이동 (단순화: 1루 비어있으면 1루로, 꽉 차있으면 밀어내기 등은 다음 버전에 고도화)
            if not st.session_state.bases[0]:
                st.session_state.bases[0] = True
                st.session_state.log.insert(0, f"🚶 볼넷! 타자 주자 1루로 나갑니다.")
            else:
                st.session_state.score[current_team] += 1
                st.session_state.log.insert(0, f"🚶 밀어내기 볼넷! 1점 득점!")

    elif pitch_result == "아웃":
        st.session_state.outs += 1
        st.session_state.strikes = 0
        st.session_state.balls = 0
        st.session_state.log.insert(0, f"⚾ 범타 아웃! (아웃: {st.session_state.outs})")

    elif pitch_result == "안타":
        st.session_state.strikes = 0
        st.session_state.balls = 0
        # 주자 진루 (단순하게 모든 주자 1루씩 이동으로 처리)
        runs = 0
        if st.session_state.bases[2]: runs += 1
        st.session_state.bases[2] = st.session_state.bases[1]
        st.session_state.bases[1] = st.session_state.bases[0]
        st.session_state.bases[0] = True
        
        st.session_state.score[current_team] += runs
        st.session_state.log.insert(0, f"🔥 안타! 주자 진루! (득점: +{runs})")

    elif pitch_result == "홈런":
        st.session_state.strikes = 0
        st.session_state.balls = 0
        # 주자 전원 득점 + 타자 득점
        runners = st.session_state.bases.count(True)
        total_runs = runners + 1
        st.session_state.score[current_team] += total_runs
        st.session_state.bases = [False, False, False]
        st.session_state.log.insert(0, f"🚀 💥 홈런!!!! {total_runs}점 홈런이 터집니다!")

    # 공수 교대 검사 (3아웃)
    if st.session_state.outs >= 3:
        st.session_state.outs = 0
        st.session_state.strikes = 0
        st.session_state.balls = 0
        st.session_state.bases = [False, False, False]
        
        if st.session_state.half == "초":
            st.session_state.half = "말"
            st.session_state.log.insert(0, f"🔄 공수 교대! {st.session_state.inning}이닝 말로 넘어갑니다.")
        else:
            st.session_state.inning += 1
            st.session_state.half = "초"
            st.session_state.log.insert(0, f"🔄 이닝 종료! {st.session_state.inning}이닝 초로 넘어갑니다.")

# 5. UI 화면 배치 (전광판)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="원정 팀 (AWAY)", value=st.session_state.score["AWAY"])
with col2:
    st.metric(label="이닝", value=f"{st.session_state.inning}회 {st.session_state.half}")
with col3:
    st.metric(label="홈 팀 (HOME)", value=st.session_state.score["HOME"])

st.markdown("---")

# 6. UI 화면 배치 (현재 볼카운트 및 주자 상황)
col_game1, col_game2 = st.columns([1, 1])

with col_game1:
    st.subheader("📊 카운트")
    st.write(f"**🔴 OUT:** {'●' * st.session_state.outs}{'○' * (3 - st.session_state.outs)}")
    st.write(f"**🟡 STRIKE:** {'●' * st.session_state.strikes}{'○' * (3 - st.session_state.strikes)}")
    st.write(f"**🟢 BALL:** {'●' * st.session_state.balls}{'○' * (4 - st.session_state.balls)}")

with col_game2:
    st.subheader("🏃 주자 상황")
    b1 = "◆" if st.session_state.bases[0] else "◇"
    b2 = "◆" if st.session_state.bases[1] else "◇"
    b3 = "◆" if st.session_state.bases[2] else "◇"
    st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;{b2}&nbsp;&nbsp;&nbsp;&nbsp; (2루)")
    st.write(f"&nbsp;&nbsp;{b3}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{b1} (3루 / 1루)")

st.markdown("---")

# 7. 조작 버튼
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("⚾ 다음 공 투구", type="primary", use_container_width=True):
        play_pitch()
        st.rerun()

with col_btn2:
    if st.button("🔄 게임 리셋", use_container_width=True):
        reset_game()
        st.rerun()

# 8. 중계 로그 출력
st.subheader("📋 경기 중계")
for line in st.session_state.log[:10]: # 최근 10개 기록만 노출
    st.text(line)
