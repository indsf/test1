from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from typing import Optional
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()


# 피클 파일 불러오기
with open("recommendation_system.pkl", "rb") as f:
    loaded_system = pickle.load(f)
    print("추천 시스템이 성공적으로 로드되었습니다.")  # 파일이 로드되면 메시지 출력

    

df = loaded_system["dataframe"]
count_vectorizer = loaded_system["count_vectorizer"]
tfidf_vectorizer = loaded_system["tfidf_vectorizer"]
genre_similarity = loaded_system["genre_similarity"]
emotion_similarity = loaded_system["emotion_similarity"]
category_similarity = loaded_system["category_similarity"]
weighted_similarity = loaded_system["weighted_similarity"]
recommend_restaurant = loaded_system["recommend_function"]





class EmotionInput(BaseModel):
    emotion: str

# 예외 처리 핸들러 정의
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),  # 유효성 검사 실패의 구체적인 오류 정보
            "body": exc.body if hasattr(exc, 'body') else None  # 요청 본문을 포함하여 디버깅 가능
        }
    )

@app.get("/")
async def root():
    return {"message": "FastAPI 서버가 정상적으로 실행 중입니다. /recommend 엔드포인트로 POST 요청을 보내 추천을 받아보세요."}


@app.post("/recommend")
async def post_recommendation(user_emotion: EmotionInput): 
    # 피클 파일에서 로드한 함수 호출하여 추천 결과를 가져옴
    recommended_restaurants = loaded_system["recommend_function"](user_emotion.emotion)
    
    # 함수 호출 후 반환된 결과를 DataFrame으로 취급하여 필요한 열을 선택
    result = recommended_restaurants[['음식이름', '감정', '카테고리']].to_dict(orient="records")
    return {"recommendations": result}


