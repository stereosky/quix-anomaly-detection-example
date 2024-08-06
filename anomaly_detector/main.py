import numpy as np
import os
import pandas as pd

from huggingface_hub import from_pretrained_keras
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

model = from_pretrained_keras(os.environ["HUGGING_FACE_MODEL"])

def predict_anomaly(row):
    # Normalize the anomalous data
    df = pd.DataFrame.from_dict(row)
    anom_data = df.set_index("timestamp")

    # Use the Autoencoder to predict on the anomalous data
    predictions = model.predict(anom_data)

    # Calculate reconstruction error for each sequence
    mse = np.mean(np.power(anom_data.values[-predictions.shape[0]:] - predictions[:, -1, :], 2), axis=1)

    # Scale the MSE to a percentage
    min_mse = np.min(mse)
    max_mse = np.max(mse)
    mse_percentage = ((mse - min_mse) / (max_mse - min_mse)) * 100

    # Detect anomalies by comparing the scaled reconstruction error to some threshold
    threshold = float(os.environ["ANOMALY_THRESHOLD_PC"])  # Define a threshold value (in percentage)

    # Add 'is_anomalous' column to the DataFrame
    df["is_anomalous"] = mse_percentage > threshold
    df["mse_percentage"] = mse_percentage

    df = df.reset_index().rename(columns={"timestamp": "time"})
    print(df)

    return row


app = Application(
    consumer_group="anomaly-detector",
    auto_offset_reset="earliest",
)

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

sdf = (
    sdf.drop("machineID")
        .apply(predict_anomaly)
)

sdf = sdf.to_topic(output_topic)


if __name__ == "__main__":
    app.run(sdf)
