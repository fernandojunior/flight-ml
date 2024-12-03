from typing import Any
import os

from pyspark.ml.feature import VectorAssembler

import mlflow

import utils

databricks_host = os.getenv("DATABRICKS_HOST")
databricks_token = os.getenv("DATABRICKS_TOKEN")
mlflow_run_id = os.getenv("MLFLOW_RUN_ID")

os.environ["DATABRICKS_HOST"] = databricks_host
os.environ["DATABRICKS_TOKEN"] = databricks_token
os.environ["MLFLOW_RUN_ID"] = mlflow_run_id

mlflow.set_tracking_uri("databricks")


def load():
    model_uri = f"runs:/{mlflow_run_id}/random_forest_flight_model"
    model = mlflow.spark.load_model(model_uri=model_uri)
    return model


def predict(flight: utils.FlightData, model: Any):
    data = [
        (
            flight.year,
            flight.month,
            flight.day,
            flight.dep_time,
            flight.sched_dep_time,
            flight.dep_delay,
            flight.air_time,
            flight.distance,
            flight.hour,
            flight.minute,
        )
    ]

    columns = [
        "year",
        "month",
        "day",
        "dep_time",
        "sched_dep_time",
        "dep_delay",
        "air_time",
        "distance",
        "hour",
        "minute",
    ]

    flight_df = utils.spark.createDataFrame(data, columns)

    # dandle missing values (similar to your training code)
    for column_name, dtype in flight_df.dtypes:
        if dtype in ["int", "double"]:
            flight_df = flight_df.fillna({column_name: 0})
        elif dtype == "string":
            flight_df = flight_df.fillna({column_name: "missing"})

    assembler = VectorAssembler(inputCols=columns, outputCol="features")
    flight_df = assembler.transform(flight_df)

    predictions = model.transform(flight_df)

    prediction_result = predictions.select("prediction").collect()
    return prediction_result[0]["prediction"] if prediction_result else None
