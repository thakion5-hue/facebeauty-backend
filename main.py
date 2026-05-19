"""
FaceBeauty AI - Main FastAPI Application
얼굴 분석 및 메이크업 추천 API 서버
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import numpy as np
import cv2
from PIL import Image
import io
import base64
import logging

from face_analyzer import FaceAnalyzer
from makeup_recommender import MakeupRecommender
from color_analysis import PersonalColorAnalyzer
from product_database import ProductDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FaceBeauty AI API",
    description="얼굴 분석 기반 맞춤 메이크업 추천 서비스",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

face_analyzer = FaceAnalyzer()
makeup_recommender = MakeupRecommender()
color_analyzer = PersonalColorAnalyzer()
product_db = ProductDatabase()


class AnalysisResponse(BaseModel):
    success: bool
    face_shape: str
    skin_tone: Dict[str, Any]
    personal_color: Dict[str, Any]
    features: Dict[str, Any]
    landmarks_count: int
    annotated_image: Optional[str] = None


class RecommendationResponse(BaseModel):
    success: bool
    face_shape: str
    personal_color: str
    makeup_style: Dict[str, Any]
    products: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    tutorial_steps: List[Dict[str, Any]]


@app.get("/")
async def root():
    return {"service": "FaceBeauty AI", "status": "running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def read_image(file_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    # 최대 크기 제한 (서버 성능 보호)
    max_size = 1920
    w, h = image.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        image = image.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    img_array = np.array(image)
    return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_face(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img_bgr = read_image(contents)

        landmarks_result = face_analyzer.detect_landmarks(img_bgr)
        if not landmarks_result["success"]:
            raise HTTPException(
                status_code=400,
                detail="얼굴을 인식할 수 없습니다. 정면 사진을 사용해주세요."
            )

        landmarks = landmarks_result["landmarks"]
        face_shape = face_analyzer.classify_face_shape(landmarks, img_bgr.shape)
        skin_tone = face_analyzer.analyze_skin_tone(img_bgr, landmarks)
        personal_color = color_analyzer.analyze(skin_tone)
        features = face_analyzer.analyze_features(landmarks, img_bgr.shape)

        annotated = face_analyzer.draw_landmarks(img_bgr.copy(), landmarks)
        _, buffer = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])
        annotated_b64 = base64.b64encode(buffer).decode("utf-8")

        return AnalysisResponse(
            success=True,
            face_shape=face_shape,
            skin_tone=skin_tone,
            personal_color=personal_color,
            features=features,
            landmarks_count=len(landmarks),
            annotated_image=annotated_b64
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"분석 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.post("/api/recommend", response_model=RecommendationResponse)
async def recommend_makeup(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img_bgr = read_image(contents)

        landmarks_result = face_analyzer.detect_landmarks(img_bgr)
        if not landmarks_result["success"]:
            raise HTTPException(status_code=400, detail="얼굴 인식 실패. 정면 사진을 사용해주세요.")

        landmarks = landmarks_result["landmarks"]
        face_shape = face_analyzer.classify_face_shape(landmarks, img_bgr.shape)
        skin_tone = face_analyzer.analyze_skin_tone(img_bgr, landmarks)
        personal_color = color_analyzer.analyze(skin_tone)
        features = face_analyzer.analyze_features(landmarks, img_bgr.shape)

        makeup_style = makeup_recommender.recommend_style(face_shape, personal_color, features)
        products = product_db.get_products_for(personal_color["season"], skin_tone["category"])
        tools = product_db.get_tools_for(face_shape, features)
        tutorial_steps = makeup_recommender.generate_tutorial(face_shape, personal_color, features)

        return RecommendationResponse(
            success=True,
            face_shape=face_shape,
            personal_color=personal_color["season"],
            makeup_style=makeup_style,
            products=products,
            tools=tools,
            tutorial_steps=tutorial_steps,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"추천 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.get("/api/products/{category}")
async def get_products_by_category(category: str):
    return {"products": product_db.get_by_category(category)}


@app.get("/api/products")
async def get_all_products():
    return {"products": product_db.get_all()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
