import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendation_module import recommend_restaurant  # 함수 임포트

# 데이터 불러오기
file_path = "cbf/food_emotion.xlsx"
df = pd.read_excel(file_path)

# 유사도 계산
count_vectorizer = CountVectorizer()
genre_matrix = count_vectorizer.fit_transform(df['음식이름'])
genre_similarity = cosine_similarity(genre_matrix, genre_matrix)
tfidf_vectorizer = TfidfVectorizer()
emotion_matrix = tfidf_vectorizer.fit_transform(df['감정'])
emotion_similarity = cosine_similarity(emotion_matrix, emotion_matrix)
category_vectorizer = CountVectorizer()
category_matrix = category_vectorizer.fit_transform(df['카테고리'])
category_similarity = cosine_similarity(category_matrix, category_matrix)
weighted_similarity = (
    genre_similarity * 0.3 +
    emotion_similarity * 0.5 +
    category_similarity * 0.2
)

# 추천 시스템의 모든 요소를 딕셔너리로 묶기
recommendation_system = {
    "dataframe": df,
    "count_vectorizer": count_vectorizer,
    "tfidf_vectorizer": tfidf_vectorizer,
    "genre_similarity": genre_similarity,
    "emotion_similarity": emotion_similarity,
    "category_similarity": category_similarity,
    "weighted_similarity": weighted_similarity,
    "recommend_function": recommend_restaurant  # 모듈에서 가져온 함수 추가
}

# pickle 파일로 저장
with open("recommendation_system.pkl", "wb") as f:
    pickle.dump(recommendation_system, f)

print("recommendation_system.pkl 파일이 생성되었습니다.")
