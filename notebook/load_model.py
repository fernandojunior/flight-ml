import mlflow

import os
from pyspark.sql import SparkSession

# Set the environment variables for Databricks connection
databricks_host = os.getenv("DATABRICKS_HOST")
databricks_token = os.getenv("DATABRICKS_TOKEN")

# Set up the Databricks Connect environment variables
os.environ["DATABRICKS_HOST"] = databricks_host
os.environ["DATABRICKS_TOKEN"] = databricks_token

print("vai")

# Initialize Spark session
spark = SparkSession.builder \
    .master('local[*]') \
    .appName('Iniciando com Spark') \
    .config('spark.ui.port', '4050') \
    .getOrCreate()


def load_model():
    # Set MLflow to use the Databricks host
    mlflow.set_tracking_uri("databricks")

    # Load the model from the Databricks MLflow registry (replace with your model's URI)
    model_uri = 'runs:/07dd88439c0c47499ad34dce02d17e33/random_forest_flight_model'

    # Load the model
    model = mlflow.spark.load_model(model_uri=model_uri)

    return model
