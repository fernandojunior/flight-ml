from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from load_model import load_model


from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler



# Initialize Spark session
spark = SparkSession.builder \
    .appName("Databricks Connect FastAPI") \
    .getOrCreate()

# Initialize FastAPI app
app = FastAPI()


_model = None


@app.get("/load")
async def load_model_endpoint():
    global _model
    print("vai")
    if not _model:
        _model = load_model()


# Pydantic model for input data validation (one flight per request)
class FlightData(BaseModel):
    year: int
    month: int
    day: int
    dep_time: int
    sched_dep_time: int
    dep_delay: float
    air_time: float
    distance: float
    hour: int
    minute: int


# Prediction function
def predict_flight_delay(flight_data: FlightData):
    global _model
    # _model = load_model()

    # Convert the input data into a DataFrame
    data = [
        (
            flight_data.year,
            flight_data.month,
            flight_data.day,
            flight_data.dep_time,
            flight_data.sched_dep_time,
            flight_data.dep_delay,
            flight_data.air_time,
            flight_data.distance,
            flight_data.hour,
            flight_data.minute
            )
    ]

    columns = ['year', 'month', 'day', 'dep_time', 'sched_dep_time', 'dep_delay', 'air_time', 'distance', 'hour', 'minute']

    flight_df = spark.createDataFrame(data, columns)

    # Handle missing values (assuming similar logic to your training code)
    for column_name, dtype in flight_df.dtypes:
        if dtype in ['int', 'double']:
            flight_df = flight_df.fillna({column_name: 0})
        elif dtype == 'string':
            flight_df = flight_df.fillna({column_name: "missing"})

    # Assemble features

    assembler = VectorAssembler(inputCols=columns, outputCol='features')
    flight_df = assembler.transform(flight_df)

    # Predict using the pre-trained model
    predictions = _model.transform(flight_df)

    # Extract the predictions and return them
    prediction_result = predictions.select('prediction').collect()
    return prediction_result[0]['prediction'] if prediction_result else None


# Define the POST request endpoint (one flight per request)
@app.post("/predict")
async def predict(flight: FlightData):
    # Get prediction for the provided flight data
    prediction = predict_flight_delay(flight)

    if prediction is not None:
        return {"prediction": prediction}
    else:
        return {"error": "Prediction failed. Check input data."}
