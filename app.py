import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB ALL 30 TEAMS - ULTIMATE ACE", layout="wide")
    
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

    # 📊 메이저리그 30개 전 구단 원투펀치 및 오타니 쇼헤이 투수 데이터 완벽 반영
    mlb_all_30_data = {
        # --- NL 서부 (5개) ---
        "LA Dodgers": {
            "pitchers": {
                "야마모토 요시노부": {"fb_speed": 95, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.037, "miss": 0.01}, "폭포수 커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.021, "miss": 0.08}, "스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.032, "miss": 0.15}}},
                "오타니 쇼헤이": {"fb_speed": 100, "pitches": {"파워 포심": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.043, "miss": 0.01}, "명품 스위퍼": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.034, "miss": 0.05}, "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.033, "miss": 0.14}}}
            }, "catcher": "윌 스미스", "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "T. 에르난데스", "맥스 먼시", "가빈 럭스", "토미 에드먼", "미겔 로하스"]
        },
        "San Diego Padres": {
            "pitchers": {
                "딜런 시즈": {"fb_speed": 97, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.039, "miss": 0.01}, "고속 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.04}, "마구 너클볼": {"mastery": 4, "type": "knuckle", "color": "#ffffff", "speed_mod": 0.016, "miss": 0.25}}},
                "다르빗슈 유": {"fb_speed": 95, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.037, "miss": 0.01}, "컷패스트볼": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.035, "miss": 0.02}, "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.031, "miss": 0.12}}}
            }, "catcher": "카일 히가시오카", "lineup": ["루이스 아라에즈", "페르난도 타티스 Jr.", "주릭슨 프로파", "매니 마차도", "잭슨 메릴", "김하성", "잰더 보가츠", "제이크 크로넨워스"]
        },
        "San Francisco Giants": {
            "pitchers": {
                "로건 웹": {"fb_speed": 93, "pitches": {"명품 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.034, "miss": 0.03}, "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.023, "miss": 0.06}}},
                "로비 레이": {"fb_speed": 94, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.035, "miss": 0.01}, "K 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.032, "miss": 0.07}}}
            }, "catcher": "톰 머피", "lineup": ["이정후", "맷 채프먼", "라몬테 웨이드 Jr.", "호르헤 솔레어", "윌머 플로레스", "마이크 야스트렘스키", "타이로 에스트라다", "패트릭 베일리"]
        },
        "Arizona Diamondbacks": {
            "pitchers": {
                "잭 갤런": {"fb_speed": 94, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.035, "miss": 0.01}, "너클 커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.020, "miss": 0.08}}},
                "메릴 켈리": {"fb_speed": 93, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.034, "miss": 0.01}, "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.023, "miss": 0.05}}}
            }, "catcher": "가브리엘 모레노", "lineup": ["코빈 캐롤", "케텔 마르테", "루르데스 구리엘 Jr.", "크리스티안 워커", "족 피더슨", "에우헤니오 수아레즈", "알렉 토마스", "제랄도 페르도모"]
        },
        "Colorado Rockies": {
            "pitchers": {
                "카일 프리랜드": {"fb_speed": 92, "pitches": {"포심 직구": {"mastery": 3, "type": "fast", "color": "#e63946", "speed_mod": 0.033, "miss": 0.01}, "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.031, "miss": 0.05}}},
                "칼 콴트릴": {"fb_speed": 93, "pitches": {"싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.034, "miss": 0.03}, "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.030, "miss": 0.10}}}
            }, "catcher": "제이콥 스탈링스", "lineup": ["찰리 블랙몬", "에제키엘 토바", "라이언 맥마흔", "놀란 존스", "브렌든 로저스", "크리스 브라이언트", "마이클 토글리아", "브렌튼 도일"]
        },

        # --- NL 동부 (5개) ---
        "Philadelphia Phillies": {
            "pitchers": {
                "잭 휠러": {"fb_speed": 96, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.038, "miss": 0.01}, "파워 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.036, "miss": 0.04}}},
                "애런 노라": {"fb_speed": 93, "pitches": {"너클 커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.019, "miss": 0.09}, "체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.023, "miss": 0.05}}}
            }, "catcher": "J.T. 리얼무토", "lineup": ["카일 슈와버", "트레이 터너", "브라이스 하퍼", "알렉 봄", "닉 카스테야노스", "브라이슨 스탓", "에드문도 소사", "요한 로하스"]
        },
        "Atlanta Braves": {
            "pitchers": {
                "맥스 프리드": {"fb_speed": 94, "pitches": {"고속 커터": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.034, "miss": 0.02}, "폭포수 커브": {"mastery": 4, "type": "curve", "color": "#ffb703", "speed_mod": 0.020, "miss": 0.07}}},
                "크리스 세일": {"fb_speed": 95, "pitches": {"지옥 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.032, "miss": 0.06}, "체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.024, "miss": 0.05}}}
            }, "catcher": "션 머피", "lineup": ["로날드 아쿠냐 Jr.", "아지 알비스", "오스틴 라일리", "맷 올슨", "마르셀 오수나", "마이클 해리스 2세", "자레드 켈닉", "올랜도 아르시아"]
        },
        "New York Mets": {
            "pitchers": {
                "센가 코다이": {"fb_speed": 96, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.038, "miss": 0.01}, "유령 포크": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.031, "miss": 0.18}}},
                "루이스 세베리노": {"fb_speed": 95, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.037, "miss": 0.01}, "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.05}}}
            }, "catcher": "프란시스코 알바레즈", "lineup": ["프란시스코 린도어", "브랜든 니모", "피트 알론소", "J.D. 마르티네즈", "제프 맥닐", "스탈링 마르테", "마크 비엔토스", "해리슨 베이더"]
        },
        "Washington Nationals": {
            "pitchers": {
                "맥켄지 고어": {"fb_speed": 95, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.037, "miss": 0.01}, "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.032, "miss": 0.06}}},
                "제이크 이라빈": {"fb_speed": 94, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.035, "miss": 0.01}, "커브": {"mastery": 4, "type": "curve", "color": "#ffb703", "speed_mod": 0.020, "miss": 0.07}}}
            }, "catcher": "키베르트 루이스", "lineup": ["CJ 에이브람스", "레인 토마스", "제시 윈커", "조이 갈로", "에디 로사리오", "루이스 가르시아 Jr.", "제이콥 영", "일데마로 바르가사"]
        },
        "Miami Marlins": {
            "pitchers": {
                "샌디 알칸타라": {"fb_speed": 98, "pitches": {"파워 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.040, "miss": 0.03}, "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.026, "miss": 0.06}}},
                "헤수스 루자르도": {"fb_speed": 96, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.038, "miss": 0.01}, "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.06}}}
            }, "catcher": "닉 포테즈", "lineup": ["재즈 치좀 Jr.", "브라이언 데 라 크루즈", "제이크 버거", "조시 벨", "헤수스 산체스", "팀 앤더슨", "닉 고든", "비달 브루한"]
        },

        # --- 나머지 구단들도 동일 구조로 30개 자동 생성 루프 가능하게 껍데기/스탯 완벽 마이그레이션 ---
        "Chicago Cubs": {"pitchers": {"저스틴 스틸": {"fb_speed": 93, "pitches": {"슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.032, "miss": 0.05}}}, "이마나가 쇼타": {"fb_speed": 92, "pitches": {"라이징 패스트볼": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.035, "miss": 0.01}, "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.030, "miss": 0.12}}}}, "catcher": "미겔 아마야", "lineup": ["니코 호너", "스완슨", "벨린저", "스즈키 세이야", "이안 햅", "모렐", "부시", "타크먼"]},
        "Milwaukee Brewers": {"pitchers": {"프레디 페랄타": {"fb_speed": 95, "pitches": {"포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.037, "miss": 0.01}, "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.05}}}, "브랜든 우드러프": {"fb_speed": 96, "pitches": {"싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.036, "miss": 0.03}}}}, "catcher": "윌리엄 콘트레라스", "lineup": ["츄리오", "콘트레라스", "아다메스", "호스킨스", "옐리치", "투랑", "오티즈", "프릭"]},
        "St. Louis Cardinals": {"pitchers": {"소니 그레이": {"fb_speed": 93, "pitches": {"스위퍼": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.032, "miss": 0.05}}}, "마일스 마이콜라스": {"fb_speed": 93, "pitches": {"싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.033, "miss": 0.02}}}}, "catcher": "윌슨 콘트레라스", "lineup": ["윈", "골드슈미트", "아레나도", "콘트레라스", "도노반", "고먼", "누트바", "버leson"]},
        "Cincinnati Reds": {"pitchers": {"헌터 그린": {"fb_speed": 99, "pitches": {"초고속 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.042, "miss": 0.01}}}, "앤드류 아보트": {"fb_speed": 93, "pitches": {"커브": {"mastery": 4, "type": "curve", "color": "#ffb703", "speed_mod": 0.020, "miss": 0.06}}}}, "catcher": "타일러 스티븐슨", "lineup": ["데 라 크루즈", "인디아", "스티븐슨", "스티어", "캔델라리오", "페랄타", "페어차일드", "벤슨"]},
        "Pittsburgh Pirates": {"pitchers": {"미치 켈러": {"fb_speed": 95, "pitches": {"커터": {"mastery": 4, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.035, "miss": 0.02}}}, "폴 스킨스": {"fb_speed": 100, "pitches": {"100마일 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.043, "miss": 0.01}, "스플린커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.040, "miss": 0.05}}}}, "catcher": "조이 바트", "lineup": ["크루즈", "레이놀즈", "헤이즈", "수윈스키", "조", "텔레즈", "트리올로", "테일러"]},
        
        # --- AL 동부 (5개) ---
        "New York Yankees": {
            "pitchers": {
                "게릿 콜": {"fb_speed": 98, "pitches": {"포심 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.041, "miss": 0.01}, "고속 슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.034, "miss": 0.05}}},
                "카를로스 로돈": {"fb_speed": 96, "pitches": {"파워 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.06}}}
            }, "catcher": "오스틴 웰스", "lineup": ["글레이버 토레스", "후안 소토", "애런 저지", "지안카를로 스탠튼", "재즈 치whom Jr.", "앤서니 볼피", "알렉스 버두고", "앤서니 리조"]
        },
        "Baltimore Orioles": {"pitchers": {"코빈 번스": {"fb_speed": 95, "pitches": {"명품 커터": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.036, "miss": 0.02}}}, "그레이슨 로드리게스": {"fb_speed": 97, "pitches": {"체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.026, "miss": 0.05}}}}, "catcher": "애들리 러치맨", "lineup": ["헨더슨", "러치맨", "마운트캐슬", "산탄데르", "웨스트버그", "카오서", "멀린스", "마테오"]},
        "Boston Red Sox": {"pitchers": {"태너 후크": {"fb_speed": 94, "pitches": {"싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.035, "miss": 0.03}}}, "루카스 지올리토": {"fb_speed": 93, "pitches": {"체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.024, "miss": 0.05}}}}, "catcher": "코너 웡", "lineup": ["듀란", "데버스", "오닐", "카사스", "요시다", "라파엘라", "스토리", "웡"]},
        "Tampa Bay Rays": {"pitchers": {"타지 브래들리": {"fb_speed": 96, "pitches": {"스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.032, "miss": 0.12}}}, "셰인 바즈": {"fb_speed": 96, "pitches": {"슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.05}}}}, "catcher": "벤 러트베트", "lineup": ["디아즈", "로저스", "아로자레나", "로베르토", "파레데스", "로사리오", "시리", "카바예로"]},
        "Toronto Blue Jays": {"pitchers": {"케빈 가우스먼": {"fb_speed": 94, "pitches": {"마구 스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.032, "miss": 0.16}}}, "크리스 배싯": {"fb_speed": 92, "pitches": {"싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.032, "miss": 0.02}}}}, "catcher": "알레한드로 커크", "lineup": ["스프링어", "게레로 Jr.", "비솃", "터너", "바쇼", "키어마이어", "클레멘트", "커크"]},

        # AL 중부 (5개)
        "Cleveland Guardians": {"pitchers": {"태너 바이비": {"fb_speed": 95, "pitches": {"슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.05}}}, "벤 라이블리": {"fb_speed": 92, "pitches": {"싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.032, "miss": 0.02}}}}, "catcher": "보 네일러", "lineup": ["콴", "히메네즈", "라미레즈", "네일러", "프라이", "브레넌", "로치오", "토마스"]},
        "Kansas City Royals": {"pitchers": {"콜 레이간스": {"fb_speed": 96, "pitches": {"체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.025, "miss": 0.06}}}, "세스 루고": {"fb_speed": 93, "pitches": {"커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.020, "miss": 0.08}}}}, "catcher": "살바도르 페레즈", "lineup": ["가르시아", "위트 Jr.", "페레즈", "파스콴티노", "벨라스케스", "멜렌데즈", "프레이저", "이스벨"]},
        "Detroit Tigers": {"pitchers": {"타릭 스쿠발": {"fb_speed": 96, "pitches": {"트리플A 체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.025, "miss": 0.07}}}, "잭 플래허티": {"fb_speed": 94, "pitches": {"슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.032, "miss": 0.05}}}}, "catcher": "제이크 로저스", "lineup": ["메도우스", "그린", "카펜터", "토켈슨", "키스", "바에즈", "어쉴라", "로저스"]},
        "Minnesota Twins": {"pitchers": {"파블로 로페즈": {"fb_speed": 95, "pitches": {"체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.024, "miss": 0.06}}}, "조 라이언": {"fb_speed": 94, "pitches": {"스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.031, "miss": 0.10}}}}, "catcher": "라이언 제퍼스", "lineup": ["벅스턴", "코레아", "루이스", "케플러", "제퍼스", "카스트로", "산타나", "마르곳"]},
        "Chicago White Sox": {"pitchers": {"개릿 크로셰": {"fb_speed": 98, "pitches": {"파워 커터": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.038, "miss": 0.03}}}, "크리스 플렉센": {"fb_speed": 92, "pitches": {"체인지업": {"mastery": 3, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.022, "miss": 0.04}}}}, "catcher": "코리 리", "lineup": ["팜", "본", "로버트 Jr.", "히메네즈", "데종", "리", "로페즈", "멘딕"]},

        # AL 서부 (5개)
        "Houston Astros": {"pitchers": {"프람버 발데스": {"fb_speed": 94, "pitches": {"폭포수 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.035, "miss": 0.04}}}, "저스틴 벌랜더": {"fb_speed": 94, "pitches": {"노련한 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.035, "miss": 0.01}}}}, "catcher": "야이너 디아즈", "lineup": ["알투베", "브레그먼", "알바레즈", "터커", "디아즈", "페냐", "싱글턴", "마이어스"]},
        "Seattle Mariners": {"pitchers": {"루이스 카스티요": {"fb_speed": 96, "pitches": {"체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.025, "miss": 0.05}}}, "조지 커비": {"fb_speed": 96, "pitches": {"칼날 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.038, "miss": 0.00}}}}, "catcher": "칼 롤리", "lineup": ["크로포드", "로드리게스", "롤리", "가버", "폴랑코", "하니거", "로하스", "록클리어"]},
        "Texas Rangers": {"pitchers": {"네이선 이볼디": {"fb_speed": 96, "pitches": {"스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.033, "miss": 0.13}}}, "존 그레이": {"fb_speed": 95, "pitches": {"슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.033, "miss": 0.05}}}}, "catcher": "조나 하임", "lineup": ["세미엔", "시거", "스미스", "가르시아", "랭포드", "하임", "로우", "타베라스"]},
        "Los Angeles Angels": {"pitchers": {"타일러 앤더슨": {"fb_speed": 91, "pitches": {"체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.022, "miss": 0.06}}}, "패트릭 산도발": {"fb_speed": 93, "pitches": {"슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.031, "miss": 0.05}}}}, "catcher": "로건 오호피", "lineup": ["샤누엘", "네토", "워드", "오호피", "필라", "아델", "드루리", "모니악"]},
        "Oakland Athletics": {"pitchers": {"JP 시어스": {"fb_speed": 93, "pitches": {"슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.032, "miss": 0.05}}}, "메이슨 밀러": {"fb_speed": 102, "pitches": {"102마일 광속구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.045, "miss": 0.01}, "슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.035, "miss": 0.06}}}}, "catcher": "셰어 랭겔리어스", "lineup": ["블레데이", "앤더슨", "루커", "랭겔리어스", "소더스트롬", "토로", "슈맨", "해리스"]}
    }
    
    mlb_teams = sorted(list(mlb_all_30_data.keys()))

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 30px; font-weight: 900;">⚾ MLB FULL 30 TEAMS MATRIX</h1>
                <p style="color: #ffb703; margin-top: 10px; font-size: 16px; font-weight: bold;">🔥 아쉬움 제로! 30개 전 구단 완벽 구현 & '투수 오타니 쇼헤이(100mph)' 마운드 전격 대복귀!</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            user_team = st.selectbox("🏃 내 구단 선택 (30개 전체)", mlb_teams, index=0)
            user_p_options = list(mlb_all_30_data[user_team]["pitchers"].keys())
            user_selected_p = st.selectbox("🔥 내 팀 선발 투수 출격", user_p_options)
            
        with c2:
            ai_team = st.selectbox("🤖 상대 AI 구단 선택", mlb_teams, index=1)
            ai_p_options = list(mlb_all_30_data[ai_team]["pitchers"].keys())
            ai_selected_p = st.selectbox("🔥 AI 팀 선발 투수 출격", ai_p_options)
            
        if st.button("🏟️ 30개 구단 매치업 확정 및 경기 시작"):
            st.session_state.p_team = user_team
            st.session_state.a_team = ai_team
            
            st.session_state.p_pitcher_name = user_selected_p
            st.session_state.p_pitcher_data = mlb_all_30_data[user_team]["pitchers"][user_selected_p]
            st.session_state.p_catcher = mlb_all_30_data[user_team]["catcher"]
            st.session_state.p_lineup = mlb_all_30_data[user_team]["lineup"]
            
            st.session_state.a_pitcher_name = ai_selected_p
            st.session_state.a_pitcher_data = mlb_all_30_data[ai_team]["pitchers"][ai_selected_p]
            st.session_state.a_catcher = mlb_all_30_data[ai_team]["catcher"]
            st.session_state.a_lineup = mlb_all_30_data[ai_team]["lineup"]
            
            st.session_state.game_active = True
            st.rerun()
        st.stop()

    col_game_screen, col_tactics_panel = st.columns([3.2, 1])

    p_pitcher_name = st.session_state.p_pitcher_name
    p_pitcher_data = st.session_state.p_pitcher_data
    p_lineup = st.session_state.p_lineup
    
    a_pitcher_name = st.session_state.a_pitcher_name
    a_pitcher_data = st.session_state.a_pitcher_data
    a_lineup = st.session_state.a_lineup

    js_p_lineup = json.dumps(p_lineup, ensure_ascii=False)
    js_a_lineup = json.dumps(a_lineup, ensure_ascii=False)
    js_p_pitches = json.dumps(p_pitcher_data['pitches'], ensure_ascii=False)
    js_a_pitches = json.dumps(a_pitcher_data['pitches'], ensure_ascii=False)

    with col_tactics_panel:
        st.markdown("### 📊 30개 구단 매치업 정보")
        st.info(f"** 내 팀:** {st.session_state.p_team}\n* 🔥 투수: {p_pitcher_name} ({p_pitcher_data['fb_speed']} mph)\n* 🧤 포수: {st.session_state.p_catcher}\n\n**현재 타자:** {p_lineup[0]}")
        st.error(f"**🤖 AI 팀:** {st.session_state.a_team}\n* 🔥 투수: {a_pitcher_name} ({a_pitcher_data['fb_speed']} mph)\n* 🧤 포수: {st.session_state.a_catcher}\n\n**상대 타자:** {a_lineup[0]}")
        if st.button("🚪 다른 팀 고르러 가기"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        team_p = st.session_state.p_team
        team_a = st.session_state.a_team

        pitch_buttons_html = ""
        for idx, (p_name, p_info) in enumerate(p_pitcher_data['pitches'].items(), 1):
            stars = "⭐" * p_info['mastery']
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" id="btn-p{idx}" style="background: {"#d90429" if idx==1 else "#1c2541"}; color: white; border: 1px solid #4b5563; padding: 6px 3px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:11px;">{p_name}<br><span style="color:#ffb703;">{stars}</span></button>'

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
                    현재 타석: <span id="current-batter-name">{p_lineup[0]}</span>
                </span>
            </div>

            <canvas id="baseballField" width="720" height="440" style="background: #1a4d2e; border: 2px solid #3a86ff; display: block; border-radius: 8px; cursor: crosshair;"></canvas>
            
            <div style="margin-top: 10px; text-align: center; background: #1c2541; padding: 12px; border-radius: 8px;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 8px;">
                    <span style="color: white; display: inline-block; margin-bottom: 8px;">🔥 선발 투수 <b>{p_pitcher_name}</b>의 구질 라인업 (최고 구속: {p_pitcher_data['fb_speed']}mph)</span><br>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
                        {pitch_buttons_html}
                    </div>
                </div>
                
                <div id="batter-controls" style="display: block;">
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;">📐 기습 번트 자세</button>
                    <button onclick="triggerSteal()" style="background: #ffb703; color: #020c1b; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 15px;">🏃 즉시 도루</button>
                    <button onclick="tryAdvanceBase()" id="btn-advance" style="display: none; background: #e63946; color: white; border: 2px solid #ffffff; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; animation: blinker 1s linear infinite;">🚨 주자 추가 진루!</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 14px; border-radius: 8px; font-weight: bold; margin-top: 8px; border-left: 6px solid #3a86ff; min-height: 55px;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 캐스터: 메이저리그 30개 전 구단 완벽 구현! LA 다저스의 오타니 쇼헤이를 고르면 100마일 직구와 춤추는 스위퍼를 던질 수 있습니다!</span>
            </div>
        </div>
        """

        # [기존과 동일하게 모든 로직 및 프레임워크 애니메이션 유지]
        js_part = f"""
        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 }};
            let bases = [false, false, false]; 

            const pLineup = {js_p_lineup};
            const aLineup = {js_a_lineup};
            const pPitches = {js_p_pitches};
            const aPitches = {js_a_pitches};
            
            const aiPitcherName = "{a_pitcher_name}";
            const aiCatcherName = "{st.session_state.a_catcher}";
            const myCatcherName = "{st.session_state.p_catcher}";

            let pBatterIndex = 0; let aBatterIndex = 0;
            let selectedPitch = Object.keys(pPitches)[0];

            let ball = {{ active: false, isHit: false, isBunt: false, isPassed: false, x: 360, y: 210, z: 0, startX: 360, startY: 210, tx: 360, ty: 320, size: 2, name: selectedPitch }};
            
            let aiPitchTimer = 55; 
            let isSwung = false; let swingFrame = 0;
            let isBuntStance = false;
            let animTicks = 0;

            let fielders = [
                {{ pos: "1B", x: 490, y: 240, ox: 490, oy: 240 }},
                {{ pos: "2B", x: 410, y: 170, ox: 410, oy: 170 }},
                {{ pos: "SS", x: 310, y: 170, ox: 310, oy: 170 }},
                {{ pos: "3B", x: 230, y: 240, ox: 230, oy: 240 }},
                {{ pos: "LF", x: 170, y: 110, ox: 170, oy: 110 }},
                {{ pos: "CF", x: 360, y: 90,  ox: 360, oy: 90 }},
                {{ pos: "RF", x: 550, y: 110, ox: 550, oy: 110 }}
            ];

            function addScore(points) {{
                if (currentMode === "batter") game.pScore += points; else game.oppScore += points;
                document.getElementById('score-p').innerText = game.pScore; document.getElementById('score-opp').innerText = game.oppScore;
            }}

            function nextBatter() {{
                if (currentMode === "batter") {{
                    pBatterIndex = (pBatterIndex + 1) % 8;
                    document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                }} else {{
                    aBatterIndex = (aBatterIndex + 1) % 8;
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
                }} else if (hitType === "passed_ball") {{
                    if (bases[2]) {{ addScore(1); bases[2] = false; }}
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }}
                    if (bases[0]) {{ bases[1] = true; bases[0] = false; }}
                }}
            }}

            function tryAdvanceBase() {{
                if (game.o >= 3) return;
                document.getElementById('btn-advance').style.display = 'none';
                let safe = Math.random() > 0.48; 
                if (safe) {{
                    advanceRunners("single"); 
                    document.getElementById('commentary').innerHTML = "🎙️ 해설: 엄청난 베이스러닝으로 추가 진루 성공!";
                }} else {{
                    game.o++;
                    if (bases[2]) bases[2] = false; else if (bases[1]) bases[1] = false; else if (bases[0]) bases[0] = false;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 아웃! 상대 외야진의 완벽한 펜스 플레이에 걸렸습니다.";
                    updateInningStatus();
                }}
            }}

            function triggerBunt() {{
                if (!ball.active || ball.isHit || ball.isPassed) return;
                isBuntStance = true; evalBunt();
            }}

            function evalBunt() {{
                if (ball.active && ball.z >= 0.78 && ball.z <= 0.95) {{
                    ball.isHit = true; ball.isBunt = true;
                    if (Math.random() > 0.45) {{
                        advanceRunners("single");
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 절묘한 코스! 번트 안타 세이프!";
                    }} else {{
                        game.o++;
                        document.getElementById('commentary').innerHTML = "🎙️ 해설: 투수가 빠르게 잡아 1루 아웃.";
                    }}
                    nextBatter(); updateInningStatus();
                }} else {{
                    game.s++; ball.active = false;
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 공을 맞추지 못해 스트라이크 선언!";
                    updateInningStatus();
                }}
                isBuntStance = false;
            }}

            function triggerSteal() {{
                if (!bases[0] && !bases[1]) {{
                    document.getElementById('commentary').innerHTML = "🎙️ 중계석: 주자가 활성화되지 않았습니다.";
                    return;
                }}
                if (Math.random() > 0.5) {{
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }}
                    else if (bases[0]) {{ bases[1] = true; bases[0] = false; }}
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 도루 대성공! 타이밍을 완전히 뺏었습니다.";
                }} else {{
                    game.o++;
                    if (bases[1]) bases[1] = false; else if (bases[0]) bases[0] = false;
                    document.getElementById('commentary').innerHTML = "🎙️ 해설: 포수의 칼송구에 태그 아웃!";
                    updateInningStatus();
                }}
            }}

            function setPitch(type) {{
                selectedPitch = type;
                let activeCount = Object.keys(pPitches).length;
                for(let i=1; i<=activeCount; i++) {{
                    let btn = document.getElementById("btn-p" + i);
                    if (btn && btn.innerText.includes(type)) {{
                        btn.style.background = "#d90429"; btn.style.border = "2px solid white";
                    }} else if (btn) {{
                        btn.style.background = "#1c2541"; btn.style.border = "1px solid #4b5563";
                    }}
                }}
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect(); let mx = e.clientX - rect.left; let my = e.clientY - rect.top;
                document.getElementById('btn-advance').style.display = 'none';

                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch; ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 210; ball.z = 0;
                        ball.startX = 360; ball.startY = 210;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; ball.isPassed = false; isSwung = false;
                    }}
                }} else {{
                    if (isBuntStance) {{ evalBunt(); return; }}
                    if (ball.active && !ball.isHit && !ball.isPassed && !isSwung) {{ 
                        isSwung = true; swingFrame = 12; evalBatterSwing(mx, my);
                    }}
                }}
            }});

            function evalBatterSwing(mx, my) {{
                let hitDist = Math.hypot(mx - ball.x, my - ball.y);
                let timingScore = Math.abs(ball.z - 0.85); 

                if (ball.z >= 0.72 && ball.z <= 0.96) {{
                    if (hitDist <= 30 && timingScore <= 0.04) evaluateHitTrajectory("homerun", false);
                    else if (hitDist <= 55 && timingScore <= 0.09) evaluateHitTrajectory("good", false);
                    else if (hitDist <= 85) evaluateHitTrajectory("poor", false);
                    else {{
                        game.s++; ball.active = false; 
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: <b>헛스윙! 공끝이 완전히 살아 나갑니다!</b>"; 
                        updateInningStatus();
                    }}
                }} else {{ 
                    game.s++; ball.active = false; 
                    document.getElementById('commentary').innerHTML = "🎙️ 해설: 완전히 타이밍이 흐트러진 헛스윙!"; 
                    updateInningStatus(); 
                }}
            }}

            function evalAiBatter() {{
                if (ball.active && !ball.isHit && !ball.isPassed && !isSwung && ball.z >= 0.76 && ball.z <= 0.90) {{
                    let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                    let currentPitches = (currentMode === "pitcher") ? pPitches : aPitches;
                    let pData = currentPitches[ball.name] || {{type: "fast", mastery: 3}};
                    
                    let aiMissChance = (pData.type === "knuckle" || pData.type === "splitter" || pData.type === "slider") ? 0.60 : 0.35;
                    aiMissChance += (pData.mastery * 0.04); 

                    let willSwing = insideZone ? (Math.random() > 0.40) : (Math.random() > 0.88);

                    if (willSwing) {{
                        isSwung = true; swingFrame = 12;
                        if (Math.random() < aiMissChance) {{
                            document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 헛스윙 삼진! 강력한 결정구가 통했습니다!";
                            game.s++; ball.active = false; updateInningStatus();
                        }} else {{
                            let roll = Math.random();
                            if (roll > 0.92) evaluateHitTrajectory("homerun", true);
                            else if (roll > 0.48) evaluateHitTrajectory("good", true);
                            else evaluateHitTrajectory("poor", true);
                        }}
                    }}
                }}
            }}

            function evaluateHitTrajectory(hitQuality, isAiHitter) {{
                ball.isHit = true; ball.isBunt = false;

                if (hitQuality === "homerun") {{
                    ball.tx = 360 + (Math.random() * 260 - 130); ball.ty = -160; 
                    advanceRunners("homerun");
                    document.getElementById('commentary').innerHTML = "🎙️ 캐스터: <b>외야 우측!! 완전히 쪼개버렸습니다! 홈런!!</b>";
                    nextBatter(); updateInningStatus();
                }} else if (hitQuality === "good") {{
                    ball.tx = 360 + (Math.random() * 340 - 170); ball.ty = 40 + Math.random() * 110; 
                    advanceRunners("single");
                    if (!isAiHitter) {{
                        document.getElementById('commentary').innerHTML = "🎙️ 해설: 안타! 총알 같은 타구였습니다.";
                        document.getElementById('btn-advance').style.display = 'inline-block';
                    }} else {{
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 정면 돌파가 안타로 이어집니다.";
                    }}
                    nextBatter(); updateInningStatus();
                }} else {{
                    ball.tx = 360 + (Math.random() * 140 - 70); ball.ty = 175; game.o++; 
                    document.getElementById('commentary').innerHTML = "🎙️ 해설: 뜬공 아웃 처리됩니다.";
                    nextBatter(); updateInningStatus();
                }}
            }}

            function updateInningStatus() {{
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 스트라이크 아웃 삼진!"; nextBatter(); }}
                if (game.b >= 4) {{ game.s = 0; game.b = 0; document.getElementById('commentary').innerHTML = "🎙️ 중계석: 무리하지 않고 볼넷으로 출루."; advanceRunners("walk"); nextBatter(); }}
                
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; bases = [false, false, false]; 
                    document.getElementById('btn-advance').style.display = 'none'; ball.active = false;
                    
                    if (currentMode === "batter") {{
                        currentMode = "pitcher";
                        document.getElementById('current-turn-badge').innerText = "1회말 수비"; document.getElementById('current-turn-badge').style.backgroundColor = "#f72585";
                        document.getElementById('pitcher-controls').style.display = 'block'; document.getElementById('batter-controls').style.display = 'none';
                        
                        let aiFirstPitch = Object.keys(aPitches)[0];
                        selectedPitch = aiFirstPitch;
                        document.getElementById('current-batter-name').innerText = aLineup[aBatterIndex];
                    }} else {{
                        currentMode = "batter";
                        document.getElementById('current-turn-badge').innerText = "2회초 공격"; document.getElementById('current-turn-badge').style.backgroundColor = "#3a86ff";
                        document.getElementById('pitcher-controls').style.display = 'none'; document.getElementById('batter-controls').style.display = 'block';
                        
                        selectedPitch = Object.keys(pPitches)[0];
                        setPitch(selectedPitch);
                        document.getElementById('current-batter-name').innerText = pLineup[pBatterIndex];
                    }}
                    aiPitchTimer = 55; 
                }}
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawHuman(x, y, isPitcher, frameTick, label="") {{
                ctx.lineWidth = 3; ctx.strokeStyle = isPitcher ? "#e63946" : "#4cc9f0"; ctx.fillStyle = isPitcher ? "#e63946" : "#4cc9f0";
                let idleOffset = Math.sin(frameTick * 0.08) * 1.8;
                ctx.beginPath(); ctx.arc(x, y - 22 + (isPitcher ? 0 : idleOffset), 6, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.moveTo(x, y - 16 + (isPitcher ? 0 : idleOffset)); ctx.lineTo(x, y); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - 6, y + 14); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 6, y + 14); ctx.stroke();
                if(label) {{ ctx.fillStyle = "#ffffff"; ctx.font = "10px Arial"; ctx.fillText(label, x - 12, y - 30); }}
            }}

            function drawScene() {{
                animTicks++; ctx.clearRect(0, 0, 720, 440); ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 440);
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.moveTo(0, 440); ctx.lineTo(720, 440); ctx.lineTo(550, 190); ctx.lineTo(170, 190); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#2a9d8f"; ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(480, 260); ctx.lineTo(360, 140); ctx.lineTo(240, 260); ctx.closePath(); ctx.fill();
                ctx.fillStyle = "#a66a38"; ctx.beginPath(); ctx.arc(360, 210, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ffffff"; ctx.fillRect(350, 208, 20, 4);
                ctx.beginPath(); ctx.moveTo(360, 380); ctx.lineTo(370, 370); ctx.lineTo(350, 370); ctx.closePath(); ctx.fill(); 
                ctx.fillRect(475, 255, 12, 12); ctx.fillRect(354, 134, 12, 12); ctx.fillRect(235, 255, 12, 12); 

                if (bases[0]) {{ ctx.fillStyle = "#ffb703"; ctx.beginPath(); ctx.arc(481, 261, 8, 0, Math.PI*2); ctx.fill(); }}
                if (bases[1]) {{ ctx.fillStyle = "#ffb703"; ctx.beginPath(); ctx.arc(360, 140, 8, 0, Math.PI*2); ctx.fill(); }}
                if (bases[2]) {{ ctx.fillStyle = "#ffb703"; ctx.beginPath(); ctx.arc(241, 261, 8, 0, Math.PI*2); ctx.fill(); }}

                drawHuman(360, 195, true, animTicks, "P"); drawHuman(285, 355, false, animTicks, "H");
                drawHuman(360, 395, true, animTicks, "C"); 

                fielders.forEach(f => {{
                    if (ball.active && ball.isHit) {{
                        let dx = ball.x - f.x; let dy = ball.y - f.y; let dist = Math.hypot(dx, dy);
                        if(dist > 5) {{ f.x += (dx / dist) * 2.8; f.y += (dy / dist) * 2.8; }} 
                    }} else {{ 
                        let dx = f.ox - f.x; let dy = f.oy - f.y; f.x += dx * 0.06; f.y += dy * 0.06;
                    }}
                    ctx.fillStyle = "#023e8a"; ctx.fillRect(f.x - 8, f.y - 10, 16, 12);
                    ctx.fillStyle = "rgba(255,255,255,0.8)"; ctx.font = "11px Arial"; ctx.fillText(f.pos, f.x - 7, f.y + 14);
                }});

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2.5; ctx.strokeRect(310, 260, 100, 90);
                
                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let keys = Object.keys(aPitches);
                        ball.name = keys[Math.floor(Math.random() * keys.length)];
                        ball.tx = 310 + Math.random() * 100; ball.ty = 260 + Math.random() * 90;
                        ball.x = 360; ball.y = 210; ball.z = 0; ball.startX = 360; ball.startY = 210;
                        ball.active = true; ball.isHit = false; ball.isBunt = false; ball.isPassed = false; isSwung = false;
                        document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 투수 <b>" + aiPitcherName + "</b>이 <b>" + ball.name + "</b> 구종을 선택했습니다!";
                    }}
                }}

                if (ball.active) {{
                    let currentPitches = (currentMode === "pitcher") ? pPitches : aPitches;
                    let pData = currentPitches[ball.name] || {{ speed_mod: 0.035, type: "fast", color: "#ffffff", mastery: 3, miss: 0.05 }};
                    let currentSpeed = ball.isHit ? -0.042 : (ball.isPassed ? 0.035 : pData.speed_mod);
                    ball.z += currentSpeed; 
                    
                    if (!ball.isHit && !ball.isPassed) {{
                        let base_x = ball.startX + (ball.tx - ball.startX) * ball.z;
                        let base_y = ball.startY + (ball.ty - ball.startY) * ball.z;
                        let mFactor = pData.mastery * 14; 
                        
                        if (pData.type === "slider") base_x += Math.pow(ball.z, 2.3) * mFactor;
                        else if (pData.type === "curve") {{ base_y -= Math.sin(ball.z * Math.PI) * (mFactor * 0.9); base_y += Math.pow(ball.z, 2) * 25; }}
                        else if (pData.type === "changeup") base_y += Math.pow(ball.z, 2.8) * (mFactor * 0.7);
                        else if (pData.type === "sinker") {{ base_x -= Math.pow(ball.z, 2) * 25; base_y += Math.pow(ball.z, 2) * 30; }}
                        else if (pData.type === "splitter" && ball.z > 0.6) base_y += Math.pow(ball.z - 0.6, 2) * (mFactor * 2.8);
                        else if (pData.type === "cutter") base_x += Math.pow(ball.z, 2) * 15;
                        
                        ball.x = base_x; ball.y = base_y; ctx.fillStyle = pData.color;
                    }} else if (ball.isPassed) {{
                        ball.y += 4; ctx.fillStyle = "#ff5722";
                    }} else {{
                        ball.x = 360 + (ball.tx - 360) * ball.z; ball.y = 210 + (ball.ty - 210) * ball.z;
                        ctx.fillStyle = "#ffffff";
                    }}
                    
                    ball.size = ball.isHit ? (ball.isBunt ? 4 : Math.max(1, 2.5 + (ball.z * 12))) : (2.5 + (Math.pow(ball.z, 3.2) * 22));
                    ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                    if (currentMode === "pitcher" && !ball.isHit && !ball.isPassed) evalAiBatter();

                    if (!ball.isHit && !ball.isPassed && ball.z >= 1.0) {{
                        if (Math.random() < pData.miss) {{
                            ball.isPassed = true; let anyRunner = (bases[0] || bases[1] || bases[2]); advanceRunners("passed_ball");
                            if (anyRunner) document.getElementById('commentary').innerHTML = "🎙 폭투 야기! 공이 뒤로 구르며 루상 주자들이 진루합니다!";
                            else document.getElementById('commentary').innerHTML = "🎙️ 캐스터: 포수가 빠뜨립니다! 패스트볼!";
                        }} else {{
                            ball.active = false;
                            let insideZone = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                            if (insideZone) {{ game.s++; document.getElementById('commentary').innerHTML = "🎙️ 해설: 보더라인에 걸치는 스트라이크!"; }} 
                            else {{ game.b++; document.getElementById('commentary').innerHTML = "🎙️ 해설: 바깥쪽 빠진 볼."; }}
                            updateInningStatus(); aiPitchTimer = 55;
                        }}
                    }} else if (ball.isPassed && ball.y >= 440) {{
                        ball.active = false; ball.isPassed = false; game.b++; updateInningStatus(); aiPitchTimer = 55;
                    }} else if (ball.isHit && (ball.z <= -0.5 || ball.z >= 1.5)) {{ 
                        ball.active = false; aiPitchTimer = 55;
                    }}
                }}

                if (isBuntStance) {{
                    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(295, 350); ctx.lineTo(355, 350); ctx.stroke();
                }} else if (swingFrame > 0) {{
                    ctx.save(); let angleRatio = ((12 - swingFrame) / 12) * Math.PI; ctx.translate(290, 350); ctx.rotate(angleRatio - Math.PI / 5);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(75, 0); ctx.stroke(); ctx.restore(); swingFrame--;
                }} else {{
                    ctx.save(); let batIdle = Math.sin(animTicks * 0.1) * 0.05; ctx.translate(290, 340); ctx.rotate(-Math.PI / 2.8 + batIdle);
                    ctx.strokeStyle = "#b79457"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(65, 0); ctx.stroke(); ctx.restore();
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
