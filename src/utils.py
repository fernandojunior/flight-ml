from pyspark.sql import SparkSession

from pydantic import BaseModel


spark = (
    SparkSession.builder.master("local[*]")
    .appName("Iniciando com Spark")
    .config("spark.ui.port", "4050")
    .getOrCreate()
)


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
