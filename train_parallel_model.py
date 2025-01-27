import pandas as pd 
import numpy as np
pd.options.mode.copy_on_write = True
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


df = pd.read_csv("preprocessed_data/olympics_data.csv")
cols  = list(df.columns)

event_cols = []
other_cols  = []
for c in cols:
    if "events" in c:
        event_cols.append(c)
    else:
        other_cols.append(c)
cols =other_cols


games_df = df[["year"] + event_cols].drop_duplicates().reindex()
record_df = df[cols]
record_df["country_total"] = record_df[["country_golds", "country_silvers", "country_bronzes"]].sum(axis=1)
X1 = []
X2 = []
y = []
for name in record_df["competing_country"].unique():
    country_df = record_df[record_df["competing_country"]==name]
    country_df.sort_values("year")
    if len(country_df)>5:
        #print(country_df.head(5))
        country_df.drop(['host_country', 'competing_country'],axis=1,inplace=True)
        for i in range(len(country_df)-6):
            #print(i)
            year = country_df.iloc[i+6]["year"]
            
            X1.append(country_df.iloc[i:i+5].to_numpy().reshape(-1))
            X2.append(games_df[games_df["year"]==year][event_cols].to_numpy().reshape(-1))
            y.append(country_df[["country_golds","country_total"]].iloc[i+6].to_numpy())

X1 = np.array(X1)[:,1:]
X2 = np.array(X2)
y = np.array(y)
print(X1.shape)
print(X2.shape)
print(y.shape)

import tensorflow as tf 

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers

inputs1 = keras.Input(shape=X1[0].shape)
inputs2 = keras.Input(shape=X2[0].shape)

x2 = inputs2
for _ in range(3):
    x2 = layers.Dense(1024, activation="sigmoid")(x2)
x2 = layers.Dense(512, activation="sigmoid")(x2)

x1 = inputs1
for _ in range(7):
    x1= layers.Dense(1024, activation="sigmoid")(x1)
x1 = layers.Dense(512, activation="sigmoid")(x1)

x = layers.Concatenate()([x1,x2])

for _ in range(3):
    x= layers.Dense(512, activation="sigmoid")(x)
    x = layers.Dropout(.5)(x)
outputs = layers.Dense(2, activation="softmax")(x)

model = keras.Model(inputs=[inputs1,inputs2], outputs=outputs)
model.compile(loss="mse")

X1_train, X1_test, X2_train, X2_test, y_train, y_test = train_test_split(X1,X2, y, test_size=0.2)

model.fit([X1_train,X2_train], y_train, epochs=100)
y_pred = model.predict([X1_test,X2_test])
print(y_pred)

mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)