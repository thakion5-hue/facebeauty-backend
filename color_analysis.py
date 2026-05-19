"""
퍼스널 컬러 분석 모듈
스킨톤 + 언더톤 → 4계절(봄웜/여름쿨/가을웜/겨울쿨) 분류
"""
from typing import Dict


class PersonalColorAnalyzer:
    SEASON_PROFILES = {
        "spring_warm": {
            "name": "봄 웜톤 (Spring Warm)",
            "name_ko": "봄 웜",
            "characteristics": "맑고 화사한 노란빛 베이스. 생기있고 밝은 피부에 따뜻한 골든 기운이 감돌아요.",
            "best_colors": ["#FFB347", "#FF7F50", "#FFA07A", "#FFD700", "#FF6B6B", "#F0E68C", "#FFDAB9"],
            "avoid_colors": ["#000080", "#4B0082", "#2F4F4F", "#708090"],
            "lipstick": ["코랄", "피치", "오렌지 레드", "산호색", "살몬 핑크"],
            "blush": ["피치 핑크", "코랄", "살몬"],
            "eyeshadow": ["골드", "베이지", "브론즈", "웜 브라운", "크림"],
            "foundation_undertone": "yellow/warm",
        },
        "summer_cool": {
            "name": "여름 쿨톤 (Summer Cool)",
            "name_ko": "여름 쿨",
            "characteristics": "부드럽고 시원한 푸른빛 베이스. 뮤트하고 차분한 파스텔 컬러가 잘 어울려요.",
            "best_colors": ["#FFB6C1", "#E6E6FA", "#B0E0E6", "#DDA0DD", "#C8A2C8", "#87CEEB", "#F0F8FF"],
            "avoid_colors": ["#FF8C00", "#FFD700", "#8B4513", "#FF4500"],
            "lipstick": ["로즈 핑크", "모브", "베리", "라벤더 핑크", "뮤트 핑크"],
            "blush": ["쿨 핑크", "로즈", "라일락"],
            "eyeshadow": ["라벤더", "쿨 그레이", "소프트 핑크", "스카이 블루", "로즈 브라운"],
            "foundation_undertone": "pink/cool",
        },
        "autumn_warm": {
            "name": "가을 웜톤 (Autumn Warm)",
            "name_ko": "가을 웜",
            "characteristics": "깊고 차분한 황금빛 베이스. 풍부하고 무게감 있는 어스 톤이 잘 어울려요.",
            "best_colors": ["#8B4513", "#CD853F", "#D2691E", "#A0522D", "#BDB76B", "#6B8E23", "#DAA520"],
            "avoid_colors": ["#FF69B4", "#00CED1", "#9370DB", "#00FA9A"],
            "lipstick": ["벽돌색", "테라코타", "브릭 레드", "딥 오렌지", "카멜"],
            "blush": ["테라코타", "오렌지 브라운", "피치 코랄"],
            "eyeshadow": ["카키", "딥 브라운", "버건디", "올리브", "머스타드"],
            "foundation_undertone": "golden/warm",
        },
        "winter_cool": {
            "name": "겨울 쿨톤 (Winter Cool)",
            "name_ko": "겨울 쿨",
            "characteristics": "선명하고 강렬한 푸른빛 베이스. 대비가 강하고 비비드한 컬러가 잘 어울려요.",
            "best_colors": ["#DC143C", "#FF1493", "#00008B", "#8B0000", "#4B0082", "#FFFFFF", "#000000"],
            "avoid_colors": ["#F0E68C", "#FFE4B5", "#DEB887", "#F5DEB3"],
            "lipstick": ["체리 레드", "와인", "푸시아", "플럼", "딥 버건디"],
            "blush": ["딥 핑크", "플럼", "와인"],
            "eyeshadow": ["블랙", "차콜", "네이비", "퓨어 화이트", "다크 플럼"],
            "foundation_undertone": "pink/cool",
        },
    }

    def analyze(self, skin_tone: Dict) -> Dict:
        undertone = skin_tone.get("undertone", "neutral")
        category = skin_tone.get("category", "medium")

        if undertone == "warm":
            season = "spring_warm" if category in ["fair", "light"] else "autumn_warm"
        elif undertone == "cool":
            season = "summer_cool" if category in ["fair", "light"] else "winter_cool"
        else:  # neutral
            season = "spring_warm" if category in ["fair", "light"] else "autumn_warm"

        profile = self.SEASON_PROFILES[season]
        return {
            "season": season,
            "name": profile["name"],
            "name_ko": profile["name_ko"],
            "characteristics": profile["characteristics"],
            "best_colors": profile["best_colors"],
            "avoid_colors": profile["avoid_colors"],
            "foundation_undertone": profile["foundation_undertone"],
            "recommended": {
                "lipstick": profile["lipstick"],
                "blush": profile["blush"],
                "eyeshadow": profile["eyeshadow"],
            },
        }
