const API_URL = "http://localhost:5000/api/predict";

export const makePrediction = async (image) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ image })
  });

  if (!response.ok) {
    throw new Error('Network response was not ok.');
  }

  const result = await response.text();
  return result;
};
