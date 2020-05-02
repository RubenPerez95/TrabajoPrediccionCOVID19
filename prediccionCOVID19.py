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
test = pd.read_excel("Predicciones/CLM_15Abril.xlsx", parse_dates = True, squeeze = True)
dfOriginal = dfOriginal.iloc[20:]
dfOriginal["Day"] = pd.to_datetime(dfOriginal["Date"]).dt.day
dfOriginal["Week"] = pd.to_datetime(dfOriginal["Date"]).dt.week
dfOriginal["WeekDay"] = pd.to_datetime(dfOriginal["Date"]).dt.dayofweek
dfOriginal["Month"] = pd.to_datetime(dfOriginal["Date"]).dt.month


print(dfOriginal)



