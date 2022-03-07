# write some code to build your image
FROM python:3.8.12-bullseye

COPY model.joblib /model.joblib
COPY api /api
COPY requirements.txt /requirements.txt
COPY FindYourInnerGamer / FindYourInnerGamer
# COPY /Users/laurabonnet/Documents/GITHUBK/main-cyclist-337816-8df14917206d.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
