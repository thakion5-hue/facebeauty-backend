"""
화장품 & 화장도구 데이터베이스
실제 서비스에서는 DB(PostgreSQL, MySQL 등) 연동 권장
"""
from typing import List, Dict


class ProductDatabase:
    PRODUCTS = [
        # ===== 봄 웜톤 =====
        {"id": "p001", "category": "lipstick", "name": "Juicy Lasting Tint (Coral)", "brand": "ROMAND",
         "color": "#FF7A6B", "season": ["spring_warm"], "price": 13000,
         "skin_tone": ["fair", "light", "medium"], "rating": 4.7, "review_count": 1243,
         "description": "산호빛 코랄 립틴트. 촉촉하고 생생한 발색이 봄 웜톤의 피부를 화사하게 살려줍니다."},
        {"id": "p002", "category": "blush", "name": "My Saison Blusher (Peach)", "brand": "ETUDE",
         "color": "#FFAB91", "season": ["spring_warm"], "price": 14000,
         "skin_tone": ["fair", "light", "medium"], "rating": 4.5, "review_count": 876,
         "description": "은은한 피치 빛 블러셔. 가볍게 터치해도 자연스러운 혈색을 만들어줍니다."},
        {"id": "p003", "category": "eyeshadow", "name": "Pro Eye Palette (Golden Sunset)", "brand": "CLIO",
         "color": "#D4A574", "season": ["spring_warm", "autumn_warm"], "price": 35000,
         "skin_tone": ["fair", "light", "medium", "tan"], "rating": 4.8, "review_count": 2341,
         "description": "골드 베이스 9컬러 팔레트. 봄/가을 웜톤에 어울리는 따뜻한 어스 톤 구성."},
        {"id": "p016", "category": "foundation", "name": "Stay All Day Foundation (W21)", "brand": "STILA",
         "color": "#F5D5B0", "season": ["spring_warm", "autumn_warm"], "price": 48000,
         "skin_tone": ["fair", "light"], "rating": 4.6, "review_count": 982,
         "description": "웜 언더톤 파운데이션. 황금빛 베이스로 봄·가을 웜톤 피부를 환하게."},

        # ===== 여름 쿨톤 =====
        {"id": "p004", "category": "lipstick", "name": "Rouge Dior (3D Roses)", "brand": "DIOR",
         "color": "#E91E63", "season": ["summer_cool"], "price": 58000,
         "skin_tone": ["fair", "light"], "rating": 4.9, "review_count": 4521,
         "description": "로즈 핑크 벨벳 립스틱. 쿨 핑크 발색이 여름 쿨톤 피부를 도자기처럼 빛나게."},
        {"id": "p005", "category": "blush", "name": "Studio Fix Powder Blush (Rose)", "brand": "MAC",
         "color": "#F48FB1", "season": ["summer_cool"], "price": 42000,
         "skin_tone": ["fair", "light", "medium"], "rating": 4.7, "review_count": 1876,
         "description": "쿨 핑크 파우더 블러셔. 섬세한 펄로 부드럽고 투명한 피부 표현."},
        {"id": "p006", "category": "eyeshadow", "name": "Multi Eye Color Palette (Lavender)", "brand": "3CE",
         "color": "#B39DDB", "season": ["summer_cool"], "price": 32000,
         "skin_tone": ["fair", "light", "medium"], "rating": 4.6, "review_count": 1432,
         "description": "라벤더/모브 톤 12컬러 팔레트. 시원하고 몽환적인 눈 메이크업에 최적."},
        {"id": "p017", "category": "foundation", "name": "Skin Tint (Cool Ivory)", "brand": "FENTY BEAUTY",
         "color": "#F0D8C8", "season": ["summer_cool", "winter_cool"], "price": 52000,
         "skin_tone": ["fair", "light"], "rating": 4.8, "review_count": 2134,
         "description": "쿨 핑크 언더톤 스킨틴트. 쿨톤 피부의 자연스러운 광채 연출."},

        # ===== 가을 웜톤 =====
        {"id": "p007", "category": "lipstick", "name": "Matte Lipstick (Brick)", "brand": "MAC",
         "color": "#A52A2A", "season": ["autumn_warm"], "price": 32000,
         "skin_tone": ["medium", "tan", "deep"], "rating": 4.8, "review_count": 3241,
         "description": "벽돌색 매트 립스틱. 깊고 풍부한 발색이 가을 웜톤의 분위기와 완벽한 조화."},
        {"id": "p008", "category": "blush", "name": "Blush (Taj Mahal)", "brand": "NARS",
         "color": "#CB6D51", "season": ["autumn_warm"], "price": 48000,
         "skin_tone": ["medium", "tan", "deep"], "rating": 4.7, "review_count": 2134,
         "description": "테라코타 톤 실크 블러셔. 어스 톤이 가을 웜톤 피부와 어우러져 자연스럽고 생기있는 혈색."},
        {"id": "p009", "category": "eyeshadow", "name": "Naked3 Palette", "brand": "URBAN DECAY",
         "color": "#8B6F47", "season": ["autumn_warm"], "price": 65000,
         "skin_tone": ["medium", "tan", "deep"], "rating": 4.9, "review_count": 5678,
         "description": "딥 브라운/카키/버건디 12컬러. 가을 웜톤을 위한 깊고 풍성한 어스 팔레트."},
        {"id": "p018", "category": "foundation", "name": "Double Wear Foundation (W3)", "brand": "ESTEE LAUDER",
         "color": "#D4A882", "season": ["autumn_warm"], "price": 68000,
         "skin_tone": ["medium", "tan"], "rating": 4.8, "review_count": 4312,
         "description": "골든 웜 언더톤 24시간 지속 파운데이션. 가을 웜톤 중간~어두운 피부에 최적."},

        # ===== 겨울 쿨톤 =====
        {"id": "p010", "category": "lipstick", "name": "Rouge Pur Couture (1966)", "brand": "YSL",
         "color": "#DC143C", "season": ["winter_cool"], "price": 58000,
         "skin_tone": ["fair", "light", "medium"], "rating": 4.9, "review_count": 6231,
         "description": "체리 레드 시그니처 립스틱. 선명하고 강렬한 발색이 겨울 쿨톤을 드라마틱하게."},
        {"id": "p011", "category": "blush", "name": "Les Beiges Blush (Plum)", "brand": "CHANEL",
         "color": "#8B3A62", "season": ["winter_cool"], "price": 68000,
         "skin_tone": ["medium", "tan", "deep"], "rating": 4.8, "review_count": 1987,
         "description": "플럼 톤 시어 파우더 블러셔. 깊고 세련된 발색으로 겨울 쿨톤의 입체감."},
        {"id": "p012", "category": "eyeshadow", "name": "Backstage Eye Palette (Cool)", "brand": "DIOR",
         "color": "#424242", "season": ["winter_cool"], "price": 95000,
         "skin_tone": ["fair", "light", "medium", "tan", "deep"], "rating": 4.9, "review_count": 3421,
         "description": "블랙/차콜/네이비 기반 스모키 팔레트. 겨울 쿨톤의 강렬한 눈 메이크업."},

        # ===== 공통 (베이스/도구) =====
        {"id": "p013", "category": "foundation", "name": "Skin Long-wear Weightless Foundation", "brand": "CLINIQUE",
         "color": "#E8C5A0", "season": ["all"], "price": 55000,
         "skin_tone": ["all"], "rating": 4.6, "review_count": 8765,
         "description": "24시간 지속 파운데이션. 40가지 쉐이드로 모든 피부색에 대응."},
        {"id": "p014", "category": "primer", "name": "The POREfessional Primer", "brand": "BENEFIT",
         "color": "transparent", "season": ["all"], "price": 48000,
         "skin_tone": ["all"], "rating": 4.7, "review_count": 12341,
         "description": "모공 커버 프라이머. 메이크업 지속력 향상과 매끄러운 베이스 완성."},
        {"id": "p015", "category": "highlighter", "name": "Trophy Wife Highlighter", "brand": "FENTY BEAUTY",
         "color": "#FFF8E7", "season": ["all"], "price": 48000,
         "skin_tone": ["all"], "rating": 4.8, "review_count": 9876,
         "description": "모든 피부톤에 어울리는 유니버설 하이라이터. 미세 펄로 자연스러운 광채."},
        {"id": "p019", "category": "setting_spray", "name": "All Nighter Setting Spray", "brand": "URBAN DECAY",
         "color": "transparent", "season": ["all"], "price": 38000,
         "skin_tone": ["all"], "rating": 4.8, "review_count": 15432,
         "description": "메이크업 16시간 고정 스프레이. 완성된 메이크업을 오래 유지."},
        {"id": "p020", "category": "concealer", "name": "Shape Tape Concealer", "brand": "TARTE",
         "color": "#E8C9A8", "season": ["all"], "price": 38000,
         "skin_tone": ["all"], "rating": 4.9, "review_count": 21543,
         "description": "고커버 컨실러. 다크서클, 잡티를 완벽히 커버. 다양한 쉐이드."},
    ]

    TOOLS = [
        {"id": "t001", "name": "앵글드 컨투어 브러쉬", "category": "contour",
         "for_face_shape": ["round", "square", "long", "heart"], "price": 22000,
         "brand": "SIGMA", "rating": 4.7,
         "description": "비스듬한 각도로 설계되어 얼굴 음영 작업에 최적화된 컨투어 브러쉬."},
        {"id": "t002", "name": "파우더 플러쉬 브러쉬", "category": "powder",
         "for_face_shape": ["oval", "heart", "diamond"], "price": 28000,
         "brand": "BOBBI BROWN", "rating": 4.8,
         "description": "부드럽고 풍성한 모로 파운데이션·파우더를 고르게 펴주는 브러쉬."},
        {"id": "t003", "name": "아이섀도 브러쉬 5종 세트", "category": "eye",
         "for_face_shape": ["all"], "price": 35000,
         "brand": "REAL TECHNIQUES", "rating": 4.8,
         "description": "베이스/블렌딩/라인/하이라이트/스머지 5종. 모든 눈 메이크업 커버."},
        {"id": "t004", "name": "뷰티 블렌더 오리지널", "category": "sponge",
         "for_face_shape": ["all"], "price": 28000,
         "brand": "BEAUTYBLENDER", "rating": 4.9,
         "description": "젖은 상태로 사용하면 밀착력이 극대화되는 메이크업 스펀지."},
        {"id": "t005", "name": "아이래쉬 컬러 (뷰러)", "category": "eye",
         "for_face_shape": ["all"], "for_features": ["small_eyes"], "price": 15000,
         "brand": "SHISEIDO", "rating": 4.8,
         "description": "자연스러운 C컬 완성. 특히 작은 눈의 볼륨업에 효과적."},
        {"id": "t006", "name": "립 브러쉬 (리트랙터블)", "category": "lip",
         "for_face_shape": ["all"], "for_features": ["thin_lips", "full_lips"], "price": 12000,
         "brand": "MAC", "rating": 4.6,
         "description": "정밀한 립 라인 작업. 얇은/두꺼운 입술 모두 깔끔한 마무리 가능."},
        {"id": "t007", "name": "팬 하이라이터 브러쉬", "category": "highlight",
         "for_face_shape": ["all"], "price": 18000,
         "brand": "ELF", "rating": 4.6,
         "description": "가볍게 쓸어 자연스러운 하이라이터 표현. 잔여 파우더 제거에도 활용."},
        {"id": "t008", "name": "블러셔 브러쉬 (타원형)", "category": "blush",
         "for_face_shape": ["all"], "price": 25000,
         "brand": "MORPHE", "rating": 4.7,
         "description": "둥근 타원형 모로 광대뼈 라인에 맞게 자연스러운 블러셔 표현."},
        {"id": "t009", "name": "아이브로우 스파일리 & 브러쉬", "category": "brow",
         "for_face_shape": ["all"], "price": 9000,
         "brand": "INNISFREE", "rating": 4.5,
         "description": "눈썹 정리와 브러쉬를 동시에. 눈썹 결 정돈 필수 아이템."},
        {"id": "t010", "name": "컨실러 브러쉬 (플랫)", "category": "concealer",
         "for_face_shape": ["all"], "price": 14000,
         "brand": "REAL TECHNIQUES", "rating": 4.7,
         "description": "플랫 브러쉬로 컨실러를 정밀하게 도포. 다크서클·잡티 커버 특화."},
    ]

    def get_products_for(self, season: str, skin_tone: str) -> List[Dict]:
        results = []
        for p in self.PRODUCTS:
            if season in p["season"] or "all" in p["season"]:
                if skin_tone in p["skin_tone"] or "all" in p["skin_tone"]:
                    results.append(p)
        return results

    def get_tools_for(self, face_shape: str, features: Dict) -> List[Dict]:
        results = []
        for t in self.TOOLS:
            if face_shape in t["for_face_shape"] or "all" in t["for_face_shape"]:
                feat_tags = t.get("for_features", [])
                if not feat_tags:
                    results.append(t)
                else:
                    if "small_eyes" in feat_tags and features["eyes"]["size"] == "small":
                        results.append(t)
                    elif "thin_lips" in feat_tags and features["lips"]["type"] == "thin":
                        results.append(t)
                    elif "full_lips" in feat_tags and features["lips"]["type"] == "full":
                        results.append(t)
        return results

    def get_by_category(self, category: str) -> List[Dict]:
        return [p for p in self.PRODUCTS if p["category"] == category]

    def get_all(self) -> List[Dict]:
        return self.PRODUCTS
