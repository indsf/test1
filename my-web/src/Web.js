const fetchRecommendations = async () => {
    setError(null); // 이전 에러 초기화
    try {
      const response = await fetch("http://localhost:8000/recommend/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ food_category: category }), // 요청 데이터
      });
  
      console.log("Response Status:", response.status); // HTTP 상태 코드 확인
  
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error Response:", errorData); // 에러 응답 출력
        throw new Error(errorData.detail || "Failed to fetch recommendations");
      }
  
      const data = await response.json();
      console.log("Response Data:", data); // FastAPI 응답 데이터 확인
      setRecommendations(data.recommendations); // 추천 결과 저장
    } catch (err) {
      console.error("Fetch Error:", err.message); // 에러 메시지 출력
      setError(err.message); // 에러 상태 업데이트
    }
  };
  