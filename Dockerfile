# Use Python 3.11 as the base image
FROM python:3.11.0-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Spark and Java
ENV SPARK_VERSION=3.5.0
# ENV HADOOP_VERSION=3.3
ENV HADOOP_VERSION=3
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Install Python dependencies: Databricks Connect, MLflow, FastAPI, and Uvicorn
RUN pip install pyspark==3.5.0 \
    mlflow==2.15.1 \
    fastapi==0.95.0 \
    uvicorn==0.22.0
# databricks-connect==15.4.3 \

# Download and install Spark
RUN curl -o /tmp/spark.tgz -L https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xzf /tmp/spark.tgz -C /opt/ \
    && mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm /tmp/spark.tgz

# Copy the API and MLflow script into the container
COPY api.py /app/api.py
COPY load_model.py /app/load_model.py

# Set the entry point for the container to run the FastAPI app with Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
