
from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_sentiment


app = FastAPI(
    title="Sentiment Analysis API",
    description="API for sentiment analysis using DistilBERT",
    version="1.0.0"
)


class TextInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "Sentiment Analysis API is running"
    }


@app.post("/predict")
def predict_api(data: TextInput):
    return predict_sentiment(data.text)
