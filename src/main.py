from fastapi import FastAPI

import utils, model, db

app = FastAPI()
db.setup_database()
model_artifact = None


@app.get("/model/load")
async def load_model_endpoint():
    global model_artifact

    if not model_artifact:
        model_artifact = model.load()

    return {"status": "ok", "details": "Model loaded"}


@app.post("/model/predict")
async def predict_endpoint(flight: utils.FlightData):
    global model_artifact

    if not model_artifact:
        return {"error": "Prediction failed. Load the model."}

    prediction = model.predict(flight, model_artifact)

    db.store_prediction(flight, prediction)

    if prediction is not None:
        return {"prediction": prediction}
    else:
        return {"error": "Prediction failed. Check input data."}


@app.get("/history")
async def history_endpoint():
    history = db.get_prediction_history()
    return {"history": history}


@app.get("/health/")
async def health_check_endpoint():
    try:
        db.test_database_connection()

        if model_artifact is None:
            return {"status": "error", "details": "Model is not loaded"}

        return {"status": "ok", "details": "API is healthy"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
