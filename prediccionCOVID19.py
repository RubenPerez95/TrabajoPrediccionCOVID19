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
sys.path.insert(0, 'C:/Users/Lydia Prado Ibáñez/git/TrabajoPrediccionCOVID19')
pd.set_option("display.max_rows", None)

from pruebaMatlab import PruebaMatlab


#Importacion de los datos
pm = PruebaMatlab()
dfOriginal = pm.dataFrame() #Carga DF con los datos originales
columns = ["DailyCases", "Hospitalized", "Critical", "DailyDeaths", "DailyRecoveries"]
'''test = pd.read_excel("Predicciones/RPRLPI25_04_2020.xlsx", squeeze = True)
dfOriginal = dfOriginal.iloc[50:65]'''
dfOriginal["Day"] = pd.to_datetime(dfOriginal["Date"]).dt.day
dfOriginal["Week"] = pd.to_datetime(dfOriginal["Date"]).dt.week
dfOriginal["Month"] = pd.to_datetime(dfOriginal["Date"]).dt.month
dfOriginal["WeekDay"] = pd.to_datetime(dfOriginal["Date"]).dt.dayofweek
#Definicion del predictor
#predictors = dfOriginal[["Day", "Week", "WeekDay", "Month"]]


for dia in range(0, 16):
    x_train = 0
    x_cv = 0
    y_train = 0
    y_cv = 0
    predictors = 0
    target = 0

    inicio = 40 + dia
    fin = 55 + dia
    diaPred = 15 + dia
    dfOriginal = dfOriginal.iloc[inicio:fin]
    nombreTest = "Predicciones/RPRLPI" + str(diaPred) + "_04_2020.xlsx"
    print(nombreTest)
    test = pd.read_excel(nombreTest, squeeze = True)
    #Definicion del predictor
    predictors = dfOriginal[["Day", "Week", "WeekDay", "Month"]]

    for valor in columns:
        variable = valor

        #Division de los datos para seleccionar los componentes y los predictores
        target = dfOriginal[variable]
        x_train, x_cv, y_train, y_cv = train_test_split(predictors, target, test_size = 0.3, random_state = 1)

        #Creacion del modelo con RF
        model = RandomForestRegressor(n_estimators= 320, max_depth = 6, n_jobs = 2, oob_score = True)
        model.fit(x_train, y_train)
        pred = model.predict(x_cv)

        #Construccion del DF para predecir
        test["Day"] = pd.to_datetime(test["Date"]).dt.day
        test["Week"] = pd.to_datetime(test["Date"]).dt.week
        test["Month"] = pd.to_datetime(test["Date"]).dt.month
        test["WeekDay"] = pd.to_datetime(test["Date"]).dt.dayofweek

        #Generar la prediccion final
        testFinal = test[["Day", "Week", "WeekDay", "Month"]]
        predFinal = model.predict(testFinal)
        test[variable] = predFinal.round(0)




    print(test)



