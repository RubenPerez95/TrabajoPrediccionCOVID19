#Librerias necesarias
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.tseries.offsets import *
from sklearn.ensemble import RandomForestRegressor

#Importar las librerias necesarias para crear el RF
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error, r2_score
'''from german_holidays import get_german_holiday_calendar'''
sys.path.insert(0, 'C:/Users/Lydia Prado Ibáñez/git/TrabajoPrediccionCOVID19')


#Importacion de los datos
df = pd.read_excel("SalesData.xlsx", parse_dates = True, squeeze = True)
test = pd.read_excel("predictionEmpty.xlsx", parse_dates = True, squeeze = True)

#Añadir más informacion al DF original para poder aplicar RF
df["Year"] = pd.to_datetime(df["Date"]).dt.year
df["Week"] = pd.to_datetime(df["Date"]).dt.week
df["Day"] = pd.to_datetime(df["Date"]).dt.day
df["WeekDay"] = pd.to_datetime(df["Date"]).dt.dayofweek

print(df.head())

'''#Uso de Six-Sigma
sns.set(rc = {"figure.figsize": (16.7, 10)})
sns.boxplot(x = df["Sold Units"])
sns.lineplot(df["Week"], df["Sold Units"])'''

#Division de los datos para seleccionar los componentes y los predictores

predictors = df.drop(["Date", "Sold Units"], axis = 1)
target = df["Sold Units"]
x_train, x_cv, y_train, y_cv = train_test_split(predictors, target, test_size = 0.4, random_state = 1)

#Creacion del modelo con RF
model = RandomForestRegressor(n_estimators = 500, oob_score = True, n_jobs = 1, random_state = 7, max_features = "auto", min_samples_leaf = 4)
model.fit(x_train, y_train)
pred = model.predict(x_cv)

#R2 Score
print(r2_score(pred, y_cv))

def mean_percentage_error(y_cv, pred):
    y_cv, pred = np.array(y_cv), np.array(pred)
    return np.mean(np.array((y_cv - pred) / y_cv)) * 100

print(mean_percentage_error(y_cv, pred))

test["Year"] = pd.to_datetime(test["Date"]).dt.year
test["Week"] = pd.to_datetime(test["Date"]).dt.week
test["Day"] = pd.to_datetime(test["Date"]).dt.day
test["WeekDay"] = pd.to_datetime(test["Date"]).dt.dayofweek

test1 = test.drop(["Sales", "Date"], axis = 1)
pred2 = model.predict(test1)
test["Sales"] = pred2.round(0)
print(test.head(20))