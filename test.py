import os

model_path = 'package/models/ncf_model_with_data.pkl'  # 경로 확인

if os.path.exists(model_path):
    print("파일이 존재합니다.")
else:
    print("파일이 존재하지 않습니다. 경로를 확인해주세요.")
