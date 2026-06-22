import streamlit as st
import json

def main():
    st.set_page_config(page_title="MLB MATRIX v4 - FULL 30 TEAMS & ABS", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #0b1329; color: #f8fafc; font-family: -apple-system, sans-serif; }
        .stSelectbox > div > div { background-color: #1c2541 !important; color: #ffffff !important; border: 2px solid #3a86ff !important; border-radius: 8px !important; }
        .stButton > button {
            background: linear-gradient(135deg, #e63946 0%, #b7094c 100%) !important;
            color: #ffffff !important; font-weight: 800 !important; font-size: 16px !important;
            border-radius: 8px !important; border: none !important; padding: 12px 20px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

    # 🔗 가로 압축을 해제하고 세로로 가독성 있게 정렬한 30개 구단 원본 로스터
    mlb_all_30_data = {
        "Pittsburgh Pirates": {
            "pitchers": {
                "폴 스킨스": {
                    "fb_speed": 101,
                    "pitches": {
                        "101마일 스플린커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.032, "miss": 0.02},
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.026, "miss": 0.04},
                        "너클 커브": {"mastery": 4, "type": "curve", "color": "#ffb703", "speed_mod": 0.018, "miss": 0.06},
                        "체인지업": {"mastery": 3, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.022, "miss": 0.05}
                    }
                },
                "미치 켈러": {
                    "fb_speed": 95,
                    "pitches": {
                        "싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.025, "miss": 0.02},
                        "스위퍼": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024, "miss": 0.04}
                    }
                }
            },
            "catcher": "조이 바트",
            "lineup": ["오닐 크루즈", "브라이언 레이놀즈", "키브라이언 헤이즈", "라우디 텔레즈", "앤드류 맥커친", "코너 조", "자레드 트리올로", "마이클 A. 테일러"]
        },
        "LA Dodgers": {
            "pitchers": {
                "오타니 쇼헤이": {
                    "fb_speed": 100,
                    "pitches": {
                        "파워 포심": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.031, "miss": 0.01},
                        "명품 스위퍼": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024, "miss": 0.04},
                        "스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.023, "miss": 0.12}
                    }
                },
                "야마모토 요시노부": {
                    "fb_speed": 95,
                    "pitches": {
                        "포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.025, "miss": 0.01},
                        "폭포수 커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.015, "miss": 0.06},
                        "스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.024, "miss": 0.10}
                    }
                }
            },
            "catcher": "윌 스미스",
            "lineup": ["오타니 쇼헤이", "무키 베츠", "프레디 프리먼", "테오스카 에르난데스", "맥스 먼시", "토미 에드먼", "가빈 럭스", "앤디 파헤스"]
        },
        "San Diego Padres": {
            "pitchers": {
                "딜런 시즈": {
                    "fb_speed": 97,
                    "pitches": {
                        "포심 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.027, "miss": 0.01},
                        "고속 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024, "miss": 0.04}
                    }
                },
                "다르빗슈 유": {
                    "fb_speed": 95,
                    "pitches": {
                        "컷패스트볼": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.025, "miss": 0.02},
                        "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.022, "miss": 0.10}
                    }
                }
            },
            "catcher": "카일 히가시오카",
            "lineup": ["루이스 아라에즈", "페르난도 타티스 Jr.", "주릭슨 프로파", "매니 마차도", "잭슨 메рил", "김하성", "잰더 보가츠", "제이크 크로넨워스"]
        },
        "New York Yankees": {
            "pitchers": {
                "게릿 콜": {
                    "fb_speed": 98,
                    "pitches": {
                        "포심 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.028, "miss": 0.01},
                        "고속 슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.024, "miss": 0.04}
                    }
                },
                "카를로스 로돈": {
                    "fb_speed": 96,
                    "pitches": {
                        "파워 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.05}
                    }
                }
            },
            "catcher": "오스틴 웰스",
            "lineup": ["글레이버 토레스", "후안 소토", "애런 저지", "지안카를로 스탠튼", "재즈 치지금 Jr.", "앤서니 볼피", "알렉스 버두고", "앤서니 리조"]
        },
        "San Francisco Giants": {
            "pitchers": {
                "로건 웹": {
                    "fb_speed": 93,
                    "pitches": {
                        "명품 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.024, "miss": 0.03},
                        "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.017, "miss": 0.05}
                    }
                },
                "로비 레이": {
                    "fb_speed": 94,
                    "pitches": {
                        "K 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.022, "miss": 0.06}
                    }
                }
            },
            "catcher": "패트릭 베일리",
            "lineup": ["이정후", "맷 채프먼", "라몬테 웨이드", "솔레어", "콘포토", "야스트렘스키", "에스트라다", "베일리"]
        },
        "Arizona Diamondbacks": {
            "pitchers": {
                "잭 갤런": {
                    "fb_speed": 94,
                    "pitches": {
                        "너클 커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.015, "miss": 0.06}
                    }
                },
                "메릴 켈리": {
                    "fb_speed": 93,
                    "pitches": {
                        "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.017, "miss": 0.04}
                    }
                }
            },
            "catcher": "가브리엘 모레노",
            "lineup": ["코빈 캐롤", "케텔 마르테", "구리엘", "크리스티안 워커", "피더슨", "수아레즈", "토마스", "페르도모"]
        },
        "Colorado Rockies": {
            "pitchers": {
                "카일 프리랜드": {
                    "fb_speed": 92,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.022, "miss": 0.04}
                    }
                },
                "칼 콴트릴": {
                    "fb_speed": 93,
                    "pitches": {
                        "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.021, "miss": 0.08}
                    }
                }
            },
            "catcher": "제이콥 스탈링스",
            "lineup": ["블랙몬", "토바", "맥마흔", "존스", "로저스", "브라이언트", "토글리아", "도일"]
        },
        "Philadelphia Phillies": {
            "pitchers": {
                "잭 휠러": {
                    "fb_speed": 96,
                    "pitches": {
                        "파워 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.026, "miss": 0.03}
                    }
                },
                "애런 노라": {
                    "fb_speed": 93,
                    "pitches": {
                        "너클 커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.014, "miss": 0.07}
                    }
                }
            },
            "catcher": "J.T. 리얼무토",
            "lineup": ["슈와버", "터너", "하퍼", "봄", "카스테야노스", "스탓", "소사", "로하스"]
        },
        "Atlanta Braves": {
            "pitchers": {
                "맥스 프리드": {
                    "fb_speed": 94,
                    "pitches": {
                        "고속 커터": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.025, "miss": 0.02}
                    }
                },
                "크리스 세일": {
                    "fb_speed": 95,
                    "pitches": {
                        "지옥 슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.05}
                    }
                }
            },
            "catcher": "션 머피",
            "lineup": ["아쿠냐 Jr.", "알비스", "라일리", "올슨", "오수나", "해리스", "켈닉", "아르시아"]
        },
        "New York Mets": {
            "pitchers": {
                "센가 코다이": {
                    "fb_speed": 96,
                    "pitches": {
                        "유령 포크": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.023, "miss": 0.15}
                    }
                },
                "루이스 세베리노": {
                    "fb_speed": 95,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.04}
                    }
                }
            },
            "catcher": "프란시스코 알바레즈",
            "lineup": ["린도어", "니모", "알론소", "마르티네즈", "맥닐", "마르테", "비엔토스", "베이더"]
        },
        "Washington Nationals": {
            "pitchers": {
                "맥켄지 고어": {
                    "fb_speed": 95,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.05}
                    }
                },
                "제이크 이라빈": {
                    "fb_speed": 94,
                    "pitches": {
                        "커브": {"mastery": 4, "type": "curve", "color": "#ffb703", "speed_mod": 0.015, "miss": 0.06}
                    }
                }
            },
            "catcher": "키베르트 루이스",
            "lineup": ["에이브람스", "토마스", "윈커", "갈로", "로사리오", "가르시아", "영", "바르가스"]
        },
        "Miami Marlins": {
            "pitchers": {
                "샌디 알칸타라": {
                    "fb_speed": 98,
                    "pitches": {
                        "파워 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.028, "miss": 0.03}
                    }
                },
                "헤수스 루자르도": {
                    "fb_speed": 96,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.05}
                    }
                }
            },
            "catcher": "닉 포테즈",
            "lineup": ["치좀 Jr.", "데 라 크루즈", "버거", "벨", "산체스", "앤더슨", "고든", "브루한"]
        },
        "Chicago Cubs": {
            "pitchers": {
                "저스틴 스틸": {
                    "fb_speed": 93,
                    "pitches": {
                        "슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.022, "miss": 0.04}
                    }
                },
                "이마나가 쇼타": {
                    "fb_speed": 92,
                    "pitches": {
                        "라이징 패스트볼": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.025, "miss": 0.01},
                        "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.022, "miss": 0.10}
                    }
                }
            },
            "catcher": "미겔 아마야",
            "lineup": ["호너", "스완슨", "벨린저", "스즈키 세이야", "햅", "모렐", "부시", "타크먼"]
        },
        "Milwaukee Brewers": {
            "pitchers": {
                "프레디 페랄타": {
                    "fb_speed": 95,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.04}
                    }
                },
                "브랜든 우드러프": {
                    "fb_speed": 96,
                    "pitches": {
                        "싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.025, "miss": 0.02}
                    }
                }
            },
            "catcher": "윌리엄 콘트레라스",
            "lineup": ["츄리오", "콘트레라스", "아다메스", "호스킨스", "옐리치", "투랑", "오티즈", "프릭"]
        },
        "St. Louis Cardinals": {
            "pitchers": {
                "소니 그레이": {
                    "fb_speed": 93,
                    "pitches": {
                        "스위퍼": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.04}
                    }
                },
                "마일스 마이콜라스": {
                    "fb_speed": 93,
                    "pitches": {
                        "싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.023, "miss": 0.02}
                    }
                }
            },
            "catcher": "윌슨 콘트레라스",
            "lineup": ["윈", "골드슈미트", "아레나도", "콘트레라스", "도노반", "고먼", "누트바", "버leson"]
        },
        "Cincinnati Reds": {
            "pitchers": {
                "헌터 그린": {
                    "fb_speed": 99,
                    "pitches": {
                        "초고속 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.030, "miss": 0.01}
                    }
                },
                "앤드류 아보트": {
                    "fb_speed": 93,
                    "pitches": {
                        "커브": {"mastery": 4, "type": "curve", "color": "#ffb703", "speed_mod": 0.015, "miss": 0.05}
                    }
                }
            },
            "catcher": "타일러 스티븐슨",
            "lineup": ["데 라 크루즈", "인디아", "스티븐슨", "스티어", "캔델라리오", "페랄타", "페어차일드", "벤슨"]
        },
        "Baltimore Orioles": {
            "pitchers": {
                "코빈 번스": {
                    "fb_speed": 95,
                    "pitches": {
                        "명품 커터": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.025, "miss": 0.02}
                    }
                },
                "그레이슨 로드리게스": {
                    "fb_speed": 97,
                    "pitches": {
                        "체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.018, "miss": 0.04}
                    }
                }
            },
            "catcher": "애들리 러치맨",
            "lineup": ["헨더슨", "러치맨", "마운트캐슬", "산탄데르", "웨스트버그", "카오서", "멀린스", "마테오"]
        },
        "Boston Red Sox": {
            "pitchers": {
                "태너 후크": {
                    "fb_speed": 94,
                    "pitches": {
                        "싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.024, "miss": 0.02}
                    }
                },
                "루카스 지올리토": {
                    "fb_speed": 93,
                    "pitches": {
                        "체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.017, "miss": 0.04}
                    }
                }
            },
            "catcher": "코너 웡",
            "lineup": ["듀란", "데버스", "오닐", "카사스", "요시다", "라파엘라", "스토리", "웡"]
        },
        "Tampa Bay Rays": {
            "pitchers": {
                "타지 브래들리": {
                    "fb_speed": 96,
                    "pitches": {
                        "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.023, "miss": 0.10}
                    }
                },
                "셰인 바즈": {
                    "fb_speed": 96,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.04}
                    }
                }
            },
            "catcher": "벤 러트베트",
            "lineup": ["디아즈", "로저스", "아로자레나", "로베르토", "파레데스", "로사리오", "시리", "카바예로"]
        },
        "Toronto Blue Jays": {
            "pitchers": {
                "케빈 가우스먼": {
                    "fb_speed": 94,
                    "pitches": {
                        "마구 스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.023, "miss": 0.14}
                    }
                },
                "크리스 배싯": {
                    "fb_speed": 92,
                    "pitches": {
                        "싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.022, "miss": 0.02}
                    }
                }
            },
            "catcher": "알레한드로 커크",
            "lineup": ["스프링어", "게레로 Jr.", "비솃", "터너", "바쇼", "키어마이어", "클레멘트", "커크"]
        },
        "Cleveland Guardians": {
            "pitchers": {
                "태너 바이비": {
                    "fb_speed": 95,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.04}
                    }
                },
                "벤 라이블리": {
                    "fb_speed": 92,
                    "pitches": {
                        "싱커": {"mastery": 4, "type": "sinker", "color": "#f72585", "speed_mod": 0.022, "miss": 0.02}
                    }
                }
            },
            "catcher": "보 네일러",
            "lineup": ["콴", "히메네즈", "라미레즈", "네일러", "프라이", "브레넌", "로치오", "토마스"]
        },
        "Kansas City Royals": {
            "pitchers": {
                "콜 레이간스": {
                    "fb_speed": 96,
                    "pitches": {
                        "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.018, "miss": 0.05}
                    }
                },
                "세스 루고": {
                    "fb_speed": 93,
                    "pitches": {
                        "커브": {"mastery": 5, "type": "curve", "color": "#ffb703", "speed_mod": 0.014, "miss": 0.06}
                    }
                }
            },
            "catcher": "살바도르 페레즈",
            "lineup": ["가르시아", "위트 Jr.", "페레즈", "파스콴티노", "벨라스케스", "멜렌데즈", "프레이저", "이스벨"]
        },
        "Detroit Tigers": {
            "pitchers": {
                "타릭 스쿠발": {
                    "fb_speed": 96,
                    "pitches": {
                        "트리플A 체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.018, "miss": 0.06}
                    }
                },
                "잭 플래허티": {
                    "fb_speed": 94,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.04}
                    }
                }
            },
            "catcher": "제이크 로저스",
            "lineup": ["메도우스", "그린", "카펜터", "토켈슨", "키스", "바에즈", "어쉴라", "로저스"]
        },
        "Minnesota Twins": {
            "pitchers": {
                "파블로 로페즈": {
                    "fb_speed": 95,
                    "pitches": {
                        "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.017, "miss": 0.05}
                    }
                },
                "조 라이언": {
                    "fb_speed": 94,
                    "pitches": {
                        "스플리터": {"mastery": 4, "type": "splitter", "color": "#7209b7", "speed_mod": 0.022, "miss": 0.08}
                    }
                }
            },
            "catcher": "라이언 제퍼스",
            "lineup": ["벅스턴", "코레아", "루이스", "케플러", "제퍼스", "카스트로", "산타나", "마르곳"]
        },
        "Chicago White Sox": {
            "pitchers": {
                "개릿 크로셰": {
                    "fb_speed": 98,
                    "pitches": {
                        "파워 커터": {"mastery": 5, "type": "cutter", "color": "#4cc9f0", "speed_mod": 0.027, "miss": 0.03}
                    }
                },
                "크리스 플렉센": {
                    "fb_speed": 92,
                    "pitches": {
                        "체인지업": {"mastery": 3, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.016, "miss": 0.04}
                    }
                }
            },
            "catcher": "코리 리",
            "lineup": ["팜", "본", "로버트 Jr.", "히메네즈", "데종", "리", "로페즈", "멘딕"]
        },
        "Houston Astros": {
            "pitchers": {
                "프람버 발데스": {
                    "fb_speed": 94,
                    "pitches": {
                        "폭포수 싱커": {"mastery": 5, "type": "sinker", "color": "#f72585", "speed_mod": 0.025, "miss": 0.03}
                    }
                },
                "저스틴 벌랜더": {
                    "fb_speed": 94,
                    "pitches": {
                        "노련한 직구": {"mastery": 4, "type": "fast", "color": "#e63946", "speed_mod": 0.024, "miss": 0.01}
                    }
                }
            },
            "catcher": "야이너 디아즈",
            "lineup": ["알투베", "브레그먼", "알바레즈", "터커", "디아즈", "페냐", "싱글턴", "마이어스"]
        },
        "Seattle Mariners": {
            "pitchers": {
                "루이스 카스티요": {
                    "fb_speed": 96,
                    "pitches": {
                        "체인지업": {"mastery": 4, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.018, "miss": 0.04}
                    }
                },
                "조지 커비": {
                    "fb_speed": 96,
                    "pitches": {
                        "칼날 직구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.026, "miss": 0.00}
                    }
                }
            },
            "catcher": "칼 롤리",
            "lineup": ["크로포드", "로드리게스", "롤리", "가버", "폴랑코", "하니거", "로하스", "록클리어"]
        },
        "Texas Rangers": {
            "pitchers": {
                "네이선 이볼디": {
                    "fb_speed": 96,
                    "pitches": {
                        "스플리터": {"mastery": 5, "type": "splitter", "color": "#7209b7", "speed_mod": 0.024, "miss": 0.11}
                    }
                },
                "존 그레이": {
                    "fb_speed": 95,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.023, "miss": 0.04}
                    }
                }
            },
            "catcher": "조나 하임",
            "lineup": ["세미엔", "시거", "스미스", "가르시아", "랭포드", "하임", "로우", "타베라스"]
        },
        "Los Angeles Angels": {
            "pitchers": {
                "타일러 앤더슨": {
                    "fb_speed": 91,
                    "pitches": {
                        "체인지업": {"mastery": 5, "type": "changeup", "color": "#06d6a0", "speed_mod": 0.016, "miss": 0.05}
                    }
                },
                "패트릭 산도발": {
                    "fb_speed": 93,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.021, "miss": 0.04}
                    }
                }
            },
            "catcher": "로건 오호피",
            "lineup": ["샤누엘", "네토", "워드", "오호피", "필라", "아델", "드루리", "모니악"]
        },
        "Oakland Athletics": {
            "pitchers": {
                "JP 시어스": {
                    "fb_speed": 93,
                    "pitches": {
                        "슬라이더": {"mastery": 4, "type": "slider", "color": "#3a86ff", "speed_mod": 0.022, "miss": 0.04}
                    }
                },
                "메이슨 밀러": {
                    "fb_speed": 102,
                    "pitches": {
                        "102마일 광속구": {"mastery": 5, "type": "fast", "color": "#e63946", "speed_mod": 0.033, "miss": 0.01},
                        "슬라이더": {"mastery": 5, "type": "slider", "color": "#3a86ff", "speed_mod": 0.025, "miss": 0.05}
                    }
                }
            },
            "catcher": "셰어 랭겔리어스",
            "lineup": ["블레데이", "앤더슨", "루커", "랭겔리어스", "소더스트롬", "토로", "슈맨", "해리스"]
        }
    }
    
    mlb_teams = sorted(list(mlb_all_30_data.keys()))

    if not st.session_state.game_active:
        st.markdown("""
            <div style="background: #1c2541; padding: 35px; border-radius: 16px; text-align: center; border: 2px solid #3a86ff; max-width: 800px; margin: 40px auto;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 900;">⚾ MLB REAL JUDGEMENT MATRIX v4 (FULL)</h1>
                <p style="color: #06d6a0; margin-top: 10px; font-size: 15px; font-weight: bold;">📢 30개 전 구단 정식 릴리즈 완료! 보더라인 인간 심판 오심 및 실시간 ABS 트래킹 가동!</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            user_team = st.selectbox("🏃 내 구단 선택", mlb_teams, index=mlb_teams.index("Pittsburgh Pirates") if "Pittsburgh Pirates" in mlb_teams else 0)
            user_p_options = list(mlb_all_30_data[user_team]["pitchers"].keys())
            user_selected_p = st.selectbox("🔥 선발 투수 선택", user_p_options)
        with c2:
            ai_team = st.selectbox("🤖 AI 상대 구단 선택", mlb_teams, index=mlb_teams.index("LA Dodgers") if "LA Dodgers" in mlb_teams else 1)
            ai_p_options = list(mlb_all_30_data[ai_team]["pitchers"].keys())
            ai_selected_p = st.selectbox("🔥 상대 선발 선택", ai_p_options)
            
        if st.button("🏟️ 심판 오심 & ABS 모드 경기 시작"):
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

    col_game_screen, col_tactics_panel = st.columns([3, 1])

    with col_tactics_panel:
        st.markdown("### 🏟️ 판정 상태 바")
        st.info(f"**⚾ 내 팀:** {st.session_state.p_team}\n* 투수: {st.session_state.p_pitcher_name}")
        st.error(f"**🤖 AI 팀:** {st.session_state.a_team}\n* 투수: {st.session_state.a_pitcher_name}")
        st.warning("⚠️ **심판 성향:** 보더라인(경계선 구역) 판정 시 가끔 오심을 저지릅니다. 이때 상단 바에 리얼 ABS 판정 결과가 대조 추적됩니다.")
        
        if st.button("🚪 메인으로 나가기"):
            st.session_state.game_active = False
            st.rerun()

    with col_game_screen:
        pitch_buttons_html = ""
        for idx, (p_name, p_info) in enumerate(st.session_state.p_pitcher_data['pitches'].items(), 1):
            pitch_buttons_html += f'<button onclick="setPitch(\'{p_name}\')" id="btn-p{idx}" style="background: {"#e63946" if idx==1 else "#1c2541"}; color: white; border: 1px solid #4b5563; padding: 8px 4px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size:11px;">{p_name}</button>'

        html_part = f"""
        <div id="game-container" style="background: #0b1329; padding: 12px; border-radius: 14px; max-width: 760px; margin: 0 auto;">
            <div style="background: #020c1b; border: 2px solid #e63946; border-radius: 8px; padding: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; color: white;">
                <div>
                    <span id="current-turn-badge" style="background: #e63946; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size:12px;">공격 진행 중</span>
                    <span style="color: #4cc9f0; font-weight: 800; font-size:14px;">{st.session_state.p_team}</span> 
                    <span id="score-p" style="font-size: 22px; font-weight: 900; color: #4cc9f0;">0</span> : 
                    <span id="score-opp" style="font-size: 22px; font-weight: 900; color: #f72585;">0</span>
                    <span style="color: #f72585; font-weight: 800; font-size:14px;">{st.session_state.a_team}</span>
                </div>
                <div><span id="count-display" style="font-weight: bold; color: #ffb703; font-size: 15px;">B: 0 | S: 0 | O: 0</span></div>
            </div>

            <canvas id="baseballField" width="720" height="420" style="background: #1a4d2e; border: 2px solid #1c2541; display: block; border-radius: 8px;"></canvas>
            
            <div style="margin-top: 8px; background: #1c2541; padding: 10px; border-radius: 8px; text-align: center;">
                <div id="pitcher-controls" style="display: none; margin-bottom: 6px;">
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">{pitch_buttons_html}</div>
                </div>
                <div id="batter-controls" style="display: block; display: flex; justify-content: center; gap: 10px;">
                    <button onclick="triggerBunt()" style="background: #4caf50; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; cursor: pointer;">📐 기습 번트 모션</button>
                </div>
            </div>

            <div style="background: #020c1b; color: #f8fafc; padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 6px; border-left: 5px solid #3a86ff; min-height: 45px; font-size:13px;">
                <span id="commentary" style="color: #90e0ef;">🎙️ 시스템: 전 구단 정밀 대조 데이터 수립 완료. 인간 심판의 오심 확률과 ABS 로깅 연출이 조화롭게 작동합니다.</span>
            </div>
        </div>
        """

        js_part = f"""
        <script>
            const canvas = document.getElementById('baseballField');
            const ctx = canvas.getContext('2d');

            let currentMode = "batter"; 
            let game = {{ pScore: 0, oppScore: 0, b: 0, s: 0, o: 0 }};
            let bases = [false, false, false]; 

            const pLineup = {json.dumps(st.session_state.p_lineup, ensure_ascii=False)};
            const aLineup = {json.dumps(st.session_state.a_lineup, ensure_ascii=False)};
            const pPitches = {json.dumps(st.session_state.p_pitcher_data['pitches'], ensure_ascii=False)};
            const aPitches = {json.dumps(st.session_state.a_pitcher_data['pitches'], ensure_ascii=False)};

            let pBatterIndex = 0; let aBatterIndex = 0;
            let selectedPitch = Object.keys(pPitches)[0];

            let ball = {{ active: false, isHit: false, isBunt: false, isPassed: false, x: 360, y: 210, z: 0, startX: 360, startY: 210, tx: 360, ty: 310, size: 2, name: selectedPitch }};
            let aiPitchTimer = 55; let isSwung = false; let swingFrame = 0; let isBuntStance = false; let animTicks = 0;

            let umpSignal = {{ text: "", frame: 0, color: "#ffffff" }};
            let absSignal = {{ text: "", frame: 0, color: "#ffffff" }};

            function advanceRunners(hitType) {{
                if (hitType === "walk") {{
                    if (bases[0] && bases[1] && bases[2]) {{ game.pScore++; }}
                    else if (bases[0] && bases[1]) {{ bases[2] = true; }} else if (bases[0]) {{ bases[1] = true; }}
                    bases[0] = true;
                }} else if (hitType === "single") {{
                    if (bases[2]) {{ game.pScore++; bases[2] = false; }} 
                    if (bases[1]) {{ bases[2] = true; bases[1] = false; }} 
                    if (bases[0]) {{ bases[1] = true; bases[0] = false; }} 
                    bases[0] = true; 
                }}
                document.getElementById('score-p').innerText = game.pScore;
            }}

            function triggerBunt() {{
                isBuntStance = !isBuntStance;
                document.getElementById('commentary').innerHTML = isBuntStance ? "🎙️ 캐스터: 타자 번트 모션 돌입!" : "🎙️ 타격 자세 환원";
            }}

            canvas.addEventListener('mousedown', (e) => {{
                let rect = canvas.getBoundingClientRect(); let mx = e.clientX - rect.left; let my = e.clientY - rect.top;
                if (currentMode === "pitcher") {{
                    if (!ball.active) {{
                        ball.name = selectedPitch; ball.tx = mx; ball.ty = my; ball.x = 360; ball.y = 210; ball.z = 0;
                        ball.startX = 360; ball.startY = 210; ball.active = true; ball.isHit = false; ball.isBunt = false; isSwung = false;
                    }}
                }} else {{
                    if (isBuntStance) {{
                        if (ball.active && ball.z >= 0.70 && ball.z <= 0.96) {{
                            ball.isHit = true; ball.isBunt = true; isBuntStance = false;
                            advanceRunners("single"); document.getElementById('commentary').innerHTML = "🎙️ 기습 번트 내야 안타 성공!";
                            updateInningStatus();
                        }}
                        return;
                    }}
                    if (ball.active && !ball.isHit && !isSwung) {{ isSwung = true; evalBatterSwing(mx, my); }}
                }}
            }});

            function evalBatterSwing(mx, my) {{
                let hitDist = Math.hypot(mx - ball.x, my - ball.y);
                if (ball.z >= 0.76 && ball.z <= 0.95 && hitDist <= 50) {{
                    ball.isHit = true; ball.tx = 360 + (Math.random()*200-100); ball.ty = 80;
                    advanceRunners("single"); document.getElementById('commentary').innerHTML = "🎙️ 완벽한 라인드라이브 안타!"; updateInningStatus();
                }} else {{
                    game.s++; ball.active = false; updateInningStatus();
                }}
            }}

            function setPitch(type) {{ selectedPitch = type; }}

            function updateInningStatus() {{
                if (game.s >= 3) {{ game.o++; game.s = 0; game.b = 0; }}
                if (game.b >= 4) {{ game.s = 0; game.b = 0; advanceRunners("walk"); }}
                if (game.o >= 3) {{
                    game.o = 0; game.s = 0; game.b = 0; bases = [false, false, false];
                    currentMode = (currentMode === "batter") ? "pitcher" : "batter";
                    document.getElementById('pitcher-controls').style.display = (currentMode === "pitcher") ? 'block' : 'none';
                    document.getElementById('batter-controls').style.display = (currentMode === "batter") ? 'flex' : 'none';
                }}
                document.getElementById('count-display').innerText = "B: " + game.b + " | S: " + game.s + " | O: " + game.o;
            }}

            function drawScene() {{
                animTicks++; ctx.clearRect(0, 0, 720, 420); ctx.fillStyle = "#1a4d2e"; ctx.fillRect(0, 0, 720, 420);
                
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 2; ctx.strokeRect(310, 260, 100, 90);
                ctx.strokeStyle = "rgba(255, 183, 3, 0.25)"; ctx.strokeRect(295, 245, 130, 120);

                if (currentMode === "batter" && !ball.active) {{
                    aiPitchTimer--;
                    if (aiPitchTimer <= 0) {{
                        let keys = Object.keys(aPitches); ball.name = keys[Math.floor(Math.random() * keys.length)];
                        ball.tx = Math.random() > 0.5 ? 310 + (Math.random()*16-8) : 410 + (Math.random()*16-8);
                        ball.ty = 260 + Math.random()*90;
                        ball.x = 360; ball.y = 210; ball.z = 0; ball.startX = 360; ball.startY = 210;
                        ball.active = true; ball.isHit = false; isSwung = false;
                    }}
                }}

                if (ball.active) {{
                    let currentPitches = (currentMode === "pitcher") ? pPitches : aPitches;
                    let pData = currentPitches[ball.name] || {{ speed_mod: 0.024, color: "#ffffff" }};
                    ball.z += ball.isHit ? -0.04 : pData.speed_mod;
                    
                    if (!ball.isHit) {{
                        ball.x = ball.startX + (ball.tx - ball.startX) * ball.z;
                        ball.y = ball.startY + (ball.ty - ball.startY) * ball.z;
                    }} else {{
                        ball.x = 360 + (ball.tx - 360) * ball.z; ball.y = 210 + (ball.ty - 210) * ball.z;
                    }}
                    
                    ctx.fillStyle = ball.isHit ? "#ffffff" : pData.color;
                    ctx.beginPath(); ctx.arc(ball.x, ball.y, 3 + ball.z*8, 0, Math.PI*2); ctx.fill();

                    if (!ball.isHit && ball.z >= 1.0) {{
                        ball.active = false; aiPitchTimer = 55;
                        
                        let isRealStrike = (ball.x >= 310 && ball.x <= 410 && ball.y >= 260 && ball.y <= 350);
                        let isBorderLine = (ball.x >= 295 && ball.x <= 425 && ball.y >= 245 && ball.y <= 365);
                        
                        let callStrike = isRealStrike;
                        let isMissedCall = false;

                        if (isBorderLine && Math.random() < 0.25) {{
                            callStrike = !isRealStrike;
                            isMissedCall = true;
                        }}

                        if (callStrike) {{ game.s++; umpSignal = {{ text: "STRIKE", color: "#e63946", frame: 45 }}; }} 
                        else {{ game.b++; umpSignal = {{ text: "BALL", color: "#3a86ff", frame: 45 }}; }}

                        if (isMissedCall) {{
                            absSignal = {{ text: "📢 ABS 판정: 심판 오심 역추적 확인 [실제 판정: " + (isRealStrike ? "STRIKE" : "BALL") + "]", color: "#06d6a0", frame: 65 }};
                            document.getElementById('commentary').innerHTML = "🎙️ [판정 번복급 오심!] 심판은 " + (callStrike ? "스트라이크" : "볼") + "을 선언했으나, ABS 칩 데이터 추적 결과 정반대입니다!";
                        }} else {{
                            absSignal = {{ text: "📢 ABS 판정 판독치 일치함", color: "#90e0ef", frame: 40 }};
                            document.getElementById('commentary').innerHTML = "🎙️ 주심 판정: " + (callStrike ? "스트라이크!" : "볼!");
                        }}
                        updateInningStatus();
                    }}
                }}

                if (isBuntStance) {{
                    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(335, 335); ctx.lineTo(385, 335); ctx.stroke();
                }}

                if (umpSignal.frame > 0) {{
                    ctx.fillStyle = umpSignal.color; ctx.font = "black 900 38px sans-serif"; ctx.fillText(umpSignal.text, 310, 110); umpSignal.frame--;
                }}
                if (absSignal.frame > 0) {{
                    ctx.fillStyle = "rgba(2, 12, 27, 0.85)"; ctx.fillRect(10, 10, 480, 30);
                    ctx.fillStyle = absSignal.color; ctx.font = "bold 13px sans-serif"; ctx.fillText(absSignal.text, 20, 30); absSignal.frame--;
                }}

                requestAnimationFrame(drawScene);
            }}
            drawScene();
        </script>
        """
        st.components.v1.html(html_part + js_part, height=760)

if __name__ == "__main__":
    main()
