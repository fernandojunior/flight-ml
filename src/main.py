from fastapi import FastAPI

import utils, model

app = FastAPI()
model_artifact = None


@app.get("/load")
async def load_model_endpoint():
    global model_artifact

    if not model_artifact:
        model_artifact = model.load()


@app.post("/predict")
async def predict(flight: utils.FlightData):
    global model_artifact

    prediction = model_artifact.predict(flight)

    if prediction is not None:
        return {"prediction": prediction}
    else:
        return {"error": "Prediction failed. Check input data."}
