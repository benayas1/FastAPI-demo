# import libraries
print('importing libraries...')
from fastapi import FastAPI, HTTPException
from pathlib import Path
import torch
import logging
import random
import time
import numpy as np
import requests, os
from io import BytesIO
from src.pytorch_model import *
from src.utils import read_img


# import settings
print('done!\nsetting up the directories and the model structure...')

data_dir = 'data'
path_to_model = os.path.join(data_dir, 'models', 'model.pth')
labels = ['Topic '+str(i) for i in range(39)]

print('Building model and loading weights')
model = ImageClassifier(b=4)
model.load_state_dict(torch.load(path_to_model, map_location=torch.device('cpu')))
model.eval()
model.to('cpu')

print('Model loaded')

print('done!\nlaunching the server...')

app = FastAPI()

@app.get("/ping")
async def pong():
    return {"ping": "Image classification example\n"}

@app.post("/predict", response_model=StockOut, status_code=200)
def predict(payload):
    url = payload.url
    app.logger.info("Classifying image %s" % (url),)
    response = requests.get(url)
    img = read_img(BytesIO(response.content))

    t = time.time() # get execution time
    with torch.no_grad():
        pred = model(img)
        pred = np.argmax(pred.numpy())

    dt = time.time() - t
    app.logger.info("Execution time: %0.02f seconds" % (dt))
    app.logger.info("Image %s classified as %s" % (url, labels[pred]))

    return {'label':labels[pred]}
