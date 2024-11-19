# recommendation.py
import torch
import torch.nn as nn
import pickle
import pandas as pd

# NCF 모델 정의
class NCF(nn.Module):
    def __init__(self, num_items, embed_dim=64):
        super(NCF, self).__init__()
        self.embedding_item = nn.Embedding(num_items, embed_dim)
        self.fc1 = nn.Linear(embed_dim, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.batchnorm1 = nn.BatchNorm1d(256)
        self.batchnorm2 = nn.BatchNorm1d(128)

    def forward(self, item_indices):
        item_embedding = self.embedding_item(item_indices)
        x = self.fc1(item_embedding)
        x = self.batchnorm1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.batchnorm2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        return torch.sigmoid(x).squeeze()

# 모델 및 데이터 로드
with open('models/ncf_model_with_data.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

num_restaurants = loaded_data["num_restaurants"]
model = NCF(num_restaurants)
model.load_state_dict(loaded_data["model_state_dict"])
model.eval()

test_df = loaded_data["test_data"]


def recommend_restaurants(food_category):
    filtered_df = test_df[test_df['카테고리'].str.contains(food_category, case=False, na=False)]
    if filtered_df.empty:
        return None

    filtered_restaurant_ids = filtered_df['restaurant_id'].unique()
    recommended_restaurants = []

    with torch.no_grad():
        for restaurant_id in filtered_restaurant_ids:
            restaurant_tensor = torch.tensor([restaurant_id], dtype=torch.long)
            prediction = model(restaurant_tensor)
            recommended_restaurants.append((int(restaurant_id), float(prediction.item())))  # numpy 타입을 int, float으로 변환

    top_restaurants = sorted(recommended_restaurants, key=lambda x: x[1], reverse=True)[:3]
    recommendations = [
        {"restaurant_id": res_id, "name": test_df[test_df['restaurant_id'] == res_id]['음식점'].iloc[0], "score": score}
        for res_id, score in top_restaurants
    ]
    return recommendations
