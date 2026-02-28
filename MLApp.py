import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle

# 1. Initialize FastAPI app
app = FastAPI()

# 2. Load trained model
pkl_file_path = "model.pkl"

with open(pkl_file_path, "rb") as file:
    model = pickle.load(file)

# 3. Input schema (exclude target)
class HeartInput(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

# 4. Prediction function
def predict_target(model, data: HeartInput):
    data_in = [[
        data.age,
        data.sex,
        data.cp,
        data.trestbps,
        data.chol,
        data.fbs,
        data.restecg,
        data.thalach,
        data.exang,
        data.oldpeak,
        data.slope,
        data.ca,
        data.thal
    ]]
    
    prediction = model.predict(data_in)[0]
    
    probability = None
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(data_in).max()

    return prediction, probability

# 5. API endpoint
@app.post("/predict")
def predict_endpoint(data: HeartInput):
    prediction, probability = predict_target(model, data)
    
    return {
        "target": int(prediction),
        "probability": probability
    }

# Optional: run using uvicorn
# uvicorn MLApp:app --reload --port 8900

# to run using uvicorn, use
# uvicorn filename:app --reload --port 8900

