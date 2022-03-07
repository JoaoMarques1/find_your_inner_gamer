from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict():




    X_pred = pd.DataFrame(dict)
    #X_pred.set_index('key', inplace = True)

    model = joblib.load('model.joblib')
    pred = model.predict(X_pred)
    return { "fare" : pred[0] }
