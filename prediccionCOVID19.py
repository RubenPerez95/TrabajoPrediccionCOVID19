#Librerias necesarias
import sys
from datetime import datetime
from time import time

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
pd.options.mode.chained_assignment = None  # default='warn'

from pruebaMatlab import PruebaMatlab


#Importacion de los datos
start_timeM = time()
pm = PruebaMatlab()
listaCCAA = pm.dataFrame() #Carga DF con los datos originales
elapsed_timeM = time() - start_timeM


columns = ["DailyCases", "Hospitalized", "Critical", "DailyDeaths", "DailyRecoveries"]

start_time = time()

for dia in range(0, 16):
    inicio = 40 + dia
    fin = 55 + dia
    diaPred = 15 + dia
    nombreTest = "RPR_LPI/RPR_LPI_" + str(diaPred) + "_04_2020.csv"
    test = pd.read_csv(nombreTest, parse_dates = True, header = 0, sep = ";")
    dfFinal = pd.DataFrame(columns=("Date", "DailyCases", "Hospitalized", "Critical", "DailyDeaths", "DailyRecoveries"))

    for i in range(len(listaCCAA)):
        dfOriginal = listaCCAA[i]
        comunidad = dfOriginal.iloc[1, 1]
        dfPred = dfOriginal.iloc[inicio:fin]
        dfPred["Day"] = pd.to_datetime(dfPred["Date"]).dt.day
        dfPred["Week"] = pd.to_datetime(dfPred["Date"]).dt.week
        dfPred["Month"] = pd.to_datetime(dfPred["Date"]).dt.month
        dfPred["WeekDay"] = pd.to_datetime(dfPred["Date"]).dt.dayofweek
        #Definicion del predictor
        predictors = dfPred[["Day", "Week", "WeekDay", "Month"]]

        for valor in columns:
            variable = valor

            #Division de los datos para seleccionar los componentes y los predictores
            target = dfPred[variable]
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
            test["CCAA"] = comunidad
            

        dfFinal = dfFinal.append(test.drop(["Day", "Week", "Month", "WeekDay"], axis=1), sort = False)
        #test['Date'] =pd.to_datetime(test.Date, format = "%d/%m/%Y")
        #dfFinal['Date'] = test['Date'].apply(lambda x: x.strftime('%d/%m/%Y'))
        #dfFinal['Date'] =pd.to_datetime(dfFinal.Date, format = "%d/%m/%Y")
        #dfFinal['Date'] = pd.to_datetime(dfFinal["Date"]).dt.date
        #dfFinal["Date"] = dfFinal['Date'].dt.strftime('%d/%m/%Y')
        dfFinal['Date'] =pd.to_datetime(dfFinal.Date)
        print(dfFinal["Date"])
        dfFinal = dfFinal.sort_values(["Date", "CCAA"])
        dfFinal['Date'] = dfFinal['Date'].dt.strftime('%d/%m/%Y')
        
        dfFinal = dfFinal[["CCAA", "Date", "DailyCases", "Hospitalized", "Critical", "DailyDeaths", "DailyRecoveries"]]

    dfFinal.rename(columns={"CCAA":"CCAA", "Date":"FECHA", "DailyCases":"CASOS", "Hospitalized":"Hospitalizados", "Critical":"UCI","DailyDeaths":"Fallecidos", "DailyRecoveries":"Recuperados"}, inplace=True)
    dfFinal.to_csv(nombreTest, index = False)
    print(dfFinal)

elapsed_time = time() - start_time

print("Tiempo de ejecución de la parte de matlab: %0.2f segundos." % elapsed_timeM)
print("Tiempo de ejecución: %0.2f segundos." % elapsed_time)


