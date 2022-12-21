import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

# import argparse
# import hypertune

from google.cloud import aiplatform
import datetime
import os
import time


NUM_EPOCHS = 10

train = pd.read_csv("gs://tensorflow-bucket-model/train.csv")

test_incomplete = pd.read_csv("gs://tensorflow-bucket-model/test.csv")
gender_ds = pd.read_csv("gs://tensorflow-bucket-model/gender_submission.csv")

test = test_incomplete.merge(gender_ds, on=["PassengerId"], how="outer")

train, val = train_test_split(train, test_size=0.2)

# def get_args():
#   parser = argparse.ArgumentParser()
#   parser.add_argument(
#       "--learning_rate",
#       required=True,
#       type=float,
#       help="learning_rate")
#   parser.add_argument(
#       "--num_units",
#       required=True,
#       type=int,
#       help="number of units in last hidden layer")
#   args = parser.parse_args()
  
#   return args

def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels=dataframe.pop("Survived")
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  ds = ds.prefetch(batch_size)
  return ds

def clean_dataset(dataset):
  dataset = dataset.drop(["Name", "Ticket", "Cabin", "Parch", "SibSp", "Embarked", "PassengerId"], axis=1)
  dataset['Age'] = dataset['Age'].fillna(dataset['Age'].median())
  return dataset

def get_category_encoding_layer(name, dataset, dtype, max_tokens=None):
  if dtype == "string":
    index = preprocessing.StringLookup(max_tokens=max_tokens)
  else:
    index = preprocessing.IntegerLookup(max_tokens=max_tokens)

  feature_ds = dataset.map(lambda x, y: x[name])
  index.adapt(feature_ds)
  encoder = preprocessing.CategoryEncoding(num_tokens=index.vocabulary_size())
  return lambda feature: encoder(index(feature))

def get_normalization_layer(name, dataset):
  normalizer = preprocessing.Normalization(axis=None)
  feature_ds = dataset.map(lambda x, y: x[name])
  normalizer.adapt(feature_ds)
  return normalizer

train = clean_dataset(train)
val = clean_dataset(val)
test = clean_dataset(test)

train_ds = df_to_dataset(train, batch_size=32)
val_ds = df_to_dataset(val, shuffle=False, batch_size=32)
test_ds = df_to_dataset(test, shuffle=False, batch_size=32)

all_inputs = []
encoded_features = []

for header in ["Pclass", "Age", "Fare"]:
  numeric_col = tf.keras.Input(shape=(1,), name=header)
  normalization_layer = get_normalization_layer(header, train_ds)
  encoded_numeric_col = normalization_layer(numeric_col)
  all_inputs.append(numeric_col)
  encoded_features.append(encoded_numeric_col)

categorical_col = tf.keras.Input(shape=(1,), name="Sex", dtype='string')
encoding_layer = get_category_encoding_layer("Sex", train_ds, dtype='string', max_tokens=5)
encoded_categorical_col = encoding_layer(categorical_col)
all_inputs.append(categorical_col)
encoded_features.append(encoded_categorical_col)

def create_model(num_units, learning_rate):
  all_features = tf.keras.layers.concatenate(encoded_features)
  x = tf.keras.layers.Dense(32, activation="relu")(all_features)
  x = tf.keras.layers.Dense(num_units, activation="relu")(x)
  x = tf.keras.layers.Dropout(0.3)(x)
  output = tf.keras.layers.Dense(1)(x)
  model = tf.keras.Model(all_inputs, output)

  model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=["accuracy"])
  
  return model

%%bash
# Create GCS bucket if it doesn't exist already...
exists=$(gsutil ls -d | grep -w gs://tensorflow-bucket-model/)

if [ -n "$exists" ]; then
    echo -e "Bucket exists, let's not recreate it."
else
    echo "Creating a new GCS bucket."
    gsutil mb -l europe-west4 gs://tensorflow-bucket-model
    echo "Here are your current buckets:"
    gsutil ls
fi

def save_model_deploy_vertex(model):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    output_path = "saved_model"
    export_path = os.path.join(output_path, timestamp)
    tf.saved_model.save(model, export_path)
    
    project = "wave46-mihaiadrian"
    bucket = "gs://tensorflow-bucket-model"
    region = "europe-west4"
    model_display_name = f"titanic_{timestamp}"
    
    serving_container_image_uri = (
        "us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-10:latest"
    )
    
    !gsutil cp -R $export_path $bucket/$model_display_name
    
    uploaded_model = aiplatform.Model.upload(
        display_name=model_display_name,
        artifact_uri=f"{bucket}/{model_display_name}",
        serving_container_image_uri=serving_container_image_uri,
    )
    
    MACHINE_TYPE = "n1-standard-4"

    endpoint = uploaded_model.deploy(
        machine_type=MACHINE_TYPE,
        accelerator_type=None,
        accelerator_count=None,
    )
    


def save_model(model):
    OUTPUT_PATH = "saved_model/my_model"
    model.save(OUTPUT_PATH)

def main():
  # args = get_args()
  model = create_model(num_units=30, learning_rate=0.01)
  # tf.keras.utils.plot_model(model, show_shapes=True, rankdir="LR")
  model.fit(train_ds, epochs=NUM_EPOCHS, validation_data=val_ds)
  save_model_deploy_vertex(model)

#   hp_metric = history.history['val_accuracy'][-1]

#   hpt = hypertune.HyperTune()
#   hpt.report_hyperparameter_tuning_metric(
#       hyperparameter_metric_tag='accuracy',
#       metric_value=hp_metric,
#       global_step=NUM_EPOCHS)

if __name__ == "__main__":
  main()
