"""
메이크업 추천 엔진
얼굴형 + 퍼스널컬러 + 이목구비 → 맞춤 화장법 + 튜토리얼
"""
from typing import Dict, List


class MakeupRecommender:
    FACE_SHAPE_STYLES = {
        "oval": {
            "name": "계란형",
            "strategy": "균형 잡힌 황금 비율의 얼굴형입니다. 어떤 화장법도 잘 어울리며, 자연스러운 컨투어로 본연의 매력을 살리세요.",
            "contour": "광대 아래쪽 가볍게 음영 처리, 턱선을 따라 자연스럽게",
            "highlight": "T존 전체, 광대뼈 위, 인중, 턱끝",
            "eyebrow": "자연스러운 소프트 아치형",
            "blush": "광대뼈 가장 높은 곳에서 안쪽으로 부드럽게",
            "icon": "🥚",
        },
        "round": {
            "name": "둥근형",
            "strategy": "세로 라인을 강조하여 얼굴에 갸름한 느낌을 줍니다. 각도를 살리는 음영이 포인트예요.",
            "contour": "헤어라인 양 옆, 광대뼈 아래, 턱선 따라 V존 음영 강조",
            "highlight": "이마 중앙, 코 중앙 세로선, 턱 중앙 (세로 라인 강조)",
            "eyebrow": "각진 상승형 아치 눈썹, 살짝 긴 길이",
            "blush": "광대뼈에서 관자놀이 방향으로 사선 블러셔",
            "icon": "⭕",
        },
        "square": {
            "name": "각진형",
            "strategy": "각진 라인을 부드럽게 풀어주는 것이 핵심. 곡선을 살리는 메이크업으로 여성스러움을 더하세요.",
            "contour": "각진 턱 모서리 2곳, 사각형 이마 양 모서리에 부드러운 음영",
            "highlight": "이마 중앙, 광대뼈 중앙, 턱 중앙",
            "eyebrow": "부드러운 아치형 (각 없이 둥글게)",
            "blush": "볼의 둥근 원형으로 광대뼈 위 중앙",
            "icon": "⬛",
        },
        "long": {
            "name": "긴형",
            "strategy": "가로 라인을 강조하여 얼굴이 짧아 보이게 합니다. 수평을 살리는 블러셔와 눈썹이 핵심이에요.",
            "contour": "이마 위쪽 가로 음영, 턱 아래쪽 가로 음영",
            "highlight": "광대뼈를 가로로 넓게",
            "eyebrow": "일자 수평 눈썹 (아치 없이 평평하게)",
            "blush": "광대뼈에서 코 방향으로 가로 폭 넓게",
            "icon": "🔲",
        },
        "heart": {
            "name": "하트형",
            "strategy": "넓은 이마를 줄이고 좁은 턱을 보완합니다. 턱선에 하이라이트, 이마에 음영이 포인트예요.",
            "contour": "헤어라인 양 옆 이마 끝 음영, 광대뼈 측면 살짝",
            "highlight": "턱 끝 (볼륨감), 광대뼈 가운데",
            "eyebrow": "둥근 소프트 아치형",
            "blush": "광대뼈 아래쪽, 안쪽으로 둥글게",
            "icon": "💗",
        },
        "diamond": {
            "name": "다이아몬드형",
            "strategy": "좁은 이마와 턱을 넓게 보완하고, 광대를 차분하게 만드는 것이 포인트입니다.",
            "contour": "광대뼈 측면에 음영으로 좁게 보이게",
            "highlight": "이마 중앙과 양 옆, 턱 중앙과 양 옆",
            "eyebrow": "스트레이트에서 소프트 아치 사이",
            "blush": "광대뼈 정중앙 작은 원형",
            "icon": "💎",
        },
    }

    def recommend_style(self, face_shape: str, personal_color: Dict, features: Dict) -> Dict:
        shape_info = self.FACE_SHAPE_STYLES.get(face_shape, self.FACE_SHAPE_STYLES["oval"])
        eye_tip = self._eye_recommendation(features["eyes"])
        lip_tip = self._lip_recommendation(features["lips"])
        nose_tip = self._nose_recommendation(features["nose"])

        return {
            "face_shape_name": shape_info["name"],
            "face_shape_icon": shape_info["icon"],
            "overall_strategy": shape_info["strategy"],
            "contour": shape_info["contour"],
            "highlight": shape_info["highlight"],
            "eyebrow_shape": shape_info["eyebrow"],
            "blush_method": shape_info["blush"],
            "eye_makeup_tip": eye_tip,
            "lip_makeup_tip": lip_tip,
            "nose_makeup_tip": nose_tip,
            "personal_color_palette": personal_color["best_colors"],
            "avoid_colors": personal_color["avoid_colors"],
            "recommended_lipstick_tones": personal_color["recommended"]["lipstick"],
            "recommended_eyeshadow_tones": personal_color["recommended"]["eyeshadow"],
            "recommended_blush_tones": personal_color["recommended"]["blush"],
            "foundation_undertone": personal_color.get("foundation_undertone", "neutral"),
        }

    def _eye_recommendation(self, eyes: Dict) -> str:
        size = eyes["size"]
        if size == "small":
            return "작은 눈: 아이라인은 속눈썹 사이만 채우고, 눈동자 위 화이트 또는 밝은 섀도로 하이라이트. 컬링 후 마스카라로 눈을 크게 연출하세요."
        if size == "large":
            return "큰 눈: 너무 진한 아이라인보다 그라데이션 섀도로 깊이감을 살리세요. 아이라인은 자연스럽게 얇게, 마스카라는 속눈썹 구분 위주로."
        return "중간 눈: 다양한 스타일이 가능합니다. 앞머리 부분 밝은 컬러, 쌍커풀 라인 이후 진한 컬러로 깊이감 있는 그라데이션을 추천합니다."

    def _lip_recommendation(self, lips: Dict) -> str:
        lip_type = lips["type"]
        if lip_type == "thin":
            return "얇은 입술: 누드 컬러로 입술선 살짝 바깥쪽에 그린 후 그라데이션. 립글로스나 글레이즈 립으로 볼륨감을 추가하세요. 매트보다 촉촉한 제형 추천."
        if lip_type == "full":
            return "두꺼운 입술: 매트 립스틱으로 선명한 라인, 입술 안쪽만 진하게 발라 그라데이션 효과를 줘 입술 크기를 좁아 보이게 연출하세요."
        return "균형 잡힌 입술: 어떤 컬러와 제형도 잘 어울립니다. 시즌 퍼스널컬러에 맞는 톤을 선택하세요."

    def _nose_recommendation(self, nose: Dict) -> str:
        nose_type = nose["type"]
        if nose_type == "long":
            return "긴 코: 코 끝에 하이라이트를 생략하고, 코 옆선 음영은 짧게. 콧날 위쪽에만 살짝 음영을 넣어 길이를 줄여주세요."
        if nose_type == "short":
            return "짧은 코: 코 옆선 음영을 코 시작부터 끝까지 길게 그려 길이감을 연출하세요. 코 끝 하이라이트로 입체감을 더하면 효과적입니다."
        return "균형 잡힌 코: 코 옆선에 자연스러운 쉐딩으로 입체감을 주고, 코 끝과 콧날에 가볍게 하이라이트로 마무리하세요."

    def generate_tutorial(self, face_shape: str, personal_color: Dict, features: Dict) -> List[Dict]:
        shape_info = self.FACE_SHAPE_STYLES.get(face_shape, self.FACE_SHAPE_STYLES["oval"])
        lipstick = ", ".join(personal_color["recommended"]["lipstick"][:2])
        eyeshadow = ", ".join(personal_color["recommended"]["eyeshadow"][:2])
        blush = ", ".join(personal_color["recommended"]["blush"][:2])
        eye_size = features["eyes"]["size"]
        lip_type = features["lips"]["type"]

        return [
            {
                "step": 1, "title": "스킨케어 & 베이스 준비",
                "duration_min": 5, "icon": "💧",
                "description": "토너 → 에센스 → 수분크림 순으로 흡수시켜 피부결을 정돈하세요. 마지막에 자외선 차단제(SPF30 이상)를 얇게 펴 발라줍니다.",
                "tip": "수분크림이 충분히 흡수된 후(3~5분 후) 메이크업을 시작해야 들뜸이 없어요.",
                "products_hint": "수분크림, 선크림",
            },
            {
                "step": 2, "title": "프라이머 & 파운데이션",
                "duration_min": 5, "icon": "🎨",
                "description": "모공 프라이머를 T존과 모공 넓은 부위에 얇게 펴 바른 후 1분 기다립니다. 파운데이션은 이마→코→볼 순서로 안에서 바깥으로 펴주세요.",
                "tip": "스펀지를 살짝 물에 적셔 짜낸 후 사용하면 밀착력이 올라가고 자연스러워져요.",
                "products_hint": f"프라이머, 파운데이션 ({personal_color.get('foundation_undertone', 'neutral')} 언더톤 추천)",
            },
            {
                "step": 3, "title": "컨실러 & 파우더 세팅",
                "duration_min": 3, "icon": "✨",
                "description": "다크서클, 잡티, 붉은 부위에만 소량의 컨실러를 사용하고 톡톡 블렌딩하세요. 루스 파우더로 T존 중심으로 가볍게 세팅합니다.",
                "tip": "건성 피부는 파우더를 최소화하거나 생략해도 좋아요. 지성 피부는 T존 전체에 꼼꼼히.",
                "products_hint": "컨실러, 루스 파우더 또는 세팅 파우더",
            },
            {
                "step": 4, "title": f"컨투어 ({shape_info['name']} 맞춤)",
                "duration_min": 4, "icon": "🌓",
                "description": f"{shape_info['contour']} 부위에 컨투어 쉐딩을 자연스럽게 터치해주세요.",
                "tip": "한 번에 진하게 바르지 말고, 얇은 층으로 여러 번 빌드업하세요. 경계가 생기면 블렌딩 브러쉬로 펴주세요.",
                "products_hint": "컨투어 파우더, 팬 브러쉬, 컨투어 브러쉬",
            },
            {
                "step": 5, "title": "하이라이터",
                "duration_min": 2, "icon": "⭐",
                "description": f"{shape_info['highlight']} 부위에 하이라이터를 가볍게 올려 입체감을 살려주세요.",
                "tip": "글리터 입자가 큰 제품보다 미세한 펄 제품이 자연스러운 빛을 냅니다.",
                "products_hint": "하이라이터 파우더 또는 리퀴드 하이라이터",
            },
            {
                "step": 6, "title": f"아이브로우 ({shape_info['eyebrow']})",
                "duration_min": 4, "icon": "📏",
                "description": f"눈썹은 {shape_info['eyebrow']} 형태로 자연스럽게 그려주세요. 부족한 부분만 채우듯이 그리세요.",
                "tip": "본인 머리카락 색보다 1~2톤 밝은 색상을 선택하면 자연스러워요.",
                "products_hint": "아이브로우 펜슬, 아이브로우 파우더, 스크류 브러쉬",
            },
            {
                "step": 7, "title": f"아이섀도 ({eyeshadow} 톤)",
                "duration_min": 6, "icon": "👁️",
                "description": f"베이스 컬러로 눈두덩 전체를, 포인트 컬러로 쌍커풀 라인에 그라데이션. {eyeshadow} 계열이 퍼스널컬러에 잘 어울려요.",
                "tip": "밝은 컬러 → 중간 컬러 → 진한 컬러 순서로 경계 없이 블렌딩하세요." if eye_size != "small" else "눈동자 바로 위에 밝은 컬러를 올리면 눈이 더 커 보여요.",
                "products_hint": f"아이섀도 팔레트 ({eyeshadow} 계열), 아이섀도 브러쉬",
            },
            {
                "step": 8, "title": "아이라인 & 마스카라",
                "duration_min": 4, "icon": "✏️",
                "description": "속눈썹 사이사이를 채우듯 아이라인을 그리고 꼬리 부분만 살짝 빼주세요. 속눈썹 컬링 후 마스카라를 지그재그로 발라줍니다.",
                "tip": "워터프루프 마스카라를 사용하면 번짐 없이 오래 유지됩니다.",
                "products_hint": "아이라이너 (펜슬 또는 리퀴드), 속눈썹 컬러, 마스카라",
            },
            {
                "step": 9, "title": f"블러셔 ({blush} 톤)",
                "duration_min": 2, "icon": "🌸",
                "description": f"{shape_info['blush']} 방식으로 {blush} 톤의 블러셔를 발색해주세요.",
                "tip": "웃었을 때 가장 도드라지는 볼 부분에 가볍게 시작해 조금씩 더해가는 것이 실패 없는 방법이에요.",
                "products_hint": f"블러셔 ({blush} 계열), 블러셔 브러쉬",
            },
            {
                "step": 10, "title": f"립 메이크업 ({lipstick})",
                "duration_min": 3, "icon": "💄",
                "description": f"{lipstick} 톤의 립 제품으로 마무리해주세요.",
                "tip": "그라데이션으로 볼륨감을 살리세요." if lip_type == "thin" else "또렷한 라인으로 깔끔하게 마무리하세요." if lip_type == "full" else "립 라이너로 선을 먼저 잡고 채우면 더 오래 지속됩니다.",
                "products_hint": f"립스틱 또는 립틴트 ({lipstick} 계열), 립글로스 (선택)",
            },
        ]
