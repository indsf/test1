# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import recommend_restaurants
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소 # fastapi에서는 8000포트 이용 다른 포트 이용해서 cors설정을 통해 react에서 요청
    allow_credentials=True,  # 쿠키 인증 정보를 포함할지 여부
    allow_methods=["*"],  # 허용할 HTTP 메서드 (GET, POST 등)
    allow_headers=["*"],  # 허용할 HTTP 헤더
)


# 요청 모델 정의
class RecommendRequest(BaseModel):
    food_category: str

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Recommendation API!"}


# 추천 엔드포인트 정의
@app.post("/recommend/")
async def recommend(request: RecommendRequest):
    recommendations = recommend_restaurants(request.food_category)
    if recommendations is None:
        raise HTTPException(status_code=404, detail=f"'{request.food_category}'에 해당하는 맛집을 찾을 수 없습니다.")
    
    return {"recommendations": recommendations}
