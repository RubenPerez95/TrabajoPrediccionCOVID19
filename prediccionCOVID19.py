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
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

#Ruta remota al área de trabajo
sys.path.insert(0, 'C:/Users/Lydia Prado Ibáñez/git/TrabajoPrediccionCOVID19')

pd.set_option("display.max_rows", None)
pd.options.mode.chained_assignment = None  # default='warn'

#Importacion de la clase CargaFuncionMatlab para poder usar sus funcionalidades
from cargaFuncionMatlab import CargaFuncionMatlab

'''Bloque para importar los datos procedentes del método listaCCAA'''
start_timeM = time()
pm = CargaFuncionMatlab()
listaCCAA = pm.listaCCAA()

#Variable para calcular el tiempo que tarda la ejecución de la clase CargaFuncionMatlab
elapsed_timeM = time() - start_timeM
'''Fin del bloque'''

#Lista con las variables que se van a predecir
variables = ["DailyCases", "Hospitalized", "Critical", "DailyDeaths", "DailyRecoveries"]

start_time = time()

#Bucle que itera a lo largo de los 16 días en los que se van a predecir las variables
for dia in range(0, 16):
    #Cada vez que se cambia de conjunto de fechas a predecir, también cambia el conjunto de datos que se usan para entrenar el modelo
    inicio = 40 + dia
    fin = 55 + dia
    diaPred = 15 + dia

    #Directorio que guarda los CSVs con el conjunto de días para predecir
    nombreTest = "Test/RPR_LPI_" + str(diaPred) + "_04_2020.csv"
    #Directorio que guarda los CSVs con los datos predichos para cada día
    nombreFinal = "RPR_LPI/RPR_LPI_" + str(diaPred) + "_04_2020.csv"

    #Construccion del DF para predecir
    test = pd.read_csv(nombreTest, parse_dates = True, header = 0, sep = ";")

    test["Date"] = pd.to_datetime(test["Date"], format = "%d/%m/%Y")

    '''Bloque para separar las fechas para que aporten más informacion a la hora de obtener las predicciones'''
    test["Day"] = pd.to_datetime(test["Date"]).dt.day
    test["Week"] = pd.to_datetime(test["Date"]).dt.week
    test["Month"] = pd.to_datetime(test["Date"]).dt.month
    test["WeekDay"] = pd.to_datetime(test["Date"]).dt.dayofweek
    '''Fin del bloque'''

    #Creación de dataframe que va a contener los datos de las predicciones
    dfFinal = pd.DataFrame(columns = ("Date", "DailyCases", "Hospitalized", "Critical", "DailyDeaths", "DailyRecoveries"))

    #Bucle que itera por cada comunidad autónoma
    for i in range(len(listaCCAA)):
        #Se obtiene cada dataframe de las CCAA
        dfOriginal = listaCCAA[i]
        comunidad = dfOriginal.iloc[1, 1]

        #Dataframe que contiene las filas necesarias para entrenar el modelo
        dfPred = dfOriginal.iloc[inicio:fin]

        '''Bloque que separa las fechas para que aporten más informacion a la hora de realizar el modelo de predicción'''
        dfPred["Day"] = pd.to_datetime(dfPred["Date"]).dt.day
        dfPred["Week"] = pd.to_datetime(dfPred["Date"]).dt.week
        dfPred["Month"] = pd.to_datetime(dfPred["Date"]).dt.month
        dfPred["WeekDay"] = pd.to_datetime(dfPred["Date"]).dt.dayofweek
        '''Fin del bloque'''

        #Definición del predictor
        predictors = dfPred[["Day", "Week", "WeekDay", "Month"]]

        #Bucle que itera a lo largo de todas las variables que se van a predecir
        for variable in variables:
            #Definición de la variable que se va a predecir
            target = dfPred[variable]
            
            #Creación de las variables de testeo y entrenamiento de la prediccion
            x_train, x_cv, y_train, y_cv = train_test_split(predictors, target, test_size = 0.3, random_state = 1)

            '''Bloque para la creacion del modelo con RF'''
            model = RandomForestRegressor(n_estimators = 320, max_depth = 6, n_jobs = 2, oob_score = True)
            model.fit(x_train, y_train)
            pred = model.predict(x_cv)
            '''Fin del bloque'''


            '''Bloque para la obtención de la prediccion final de una variable'''
            testFinal = test[["Day", "Week", "WeekDay", "Month"]]
            predFinal = model.predict(testFinal)
            test[variable] = predFinal.round(0)
            '''Fin del bloque'''
        
        '''Bloque que crea el dataframe final con todas las variables predichas
        para un día para todas las CCAA'''
        test["CCAA"] = comunidad
        dfFinal = dfFinal.append(test.drop(["Day", "Week", "Month", "WeekDay"], axis = 1), sort = False)
        dfFinal = dfFinal[["CCAA", "Date", "DailyCases", "Hospitalized", "Critical", "DailyDeaths", "DailyRecoveries"]]
        '''Fin del bloque'''

    '''Bloque para dar formato al dataframe de las comunidades autónomas y guardarlo en CSV final'''
    dfFinal["Date"] = pd.to_datetime(dfFinal["Date"], format = "%d/%m/%Y")
    dfFinal["Date"] = pd.to_datetime(dfFinal.Date)
    dfFinal = dfFinal.sort_values(["Date", "CCAA"])
    dfFinal["Date"] = dfFinal["Date"].dt.strftime("%d/%m/%Y")
    dfFinal.rename(columns = {"CCAA":"CCAA", "Date":"FECHA", "DailyCases":"CASOS", "Hospitalized":"Hospitalizados", "Critical":"UCI", "DailyDeaths":"Fallecidos", "DailyRecoveries":"Recuperados"}, inplace=True)
    dfFinal.to_csv(nombreFinal, index = False)
    '''Fin del bloque'''

    #Imprime cada CSV generado para poder ver pantalla que la ejecución avanza
    print(dfFinal)

elapsed_time = time() - start_time

#Imprime el tiempo que ha tardado la carga de datos desde la clase CargaFuncionMatlab
print("Tiempo de ejecución de la parte de matlab: %0.2f segundos." % elapsed_timeM)
#Imprime el tiempo total que han tardado todas las predicciones
print("Tiempo de ejecución: %0.2f segundos." % elapsed_time)


