import matlab.engine
import pandas as pd


## Prueba de lectura de función Matlab ##

class PruebaMatlab():

    def __init__(self):
        algo = 0

    def dataFrame(self):

        #columns = ["AcumulatedCases", "AcumulatedPRC", "AcumulatedTestAc", "Hospitalized", "Critical", "Deaths", "AcumulatedRecoveries", "label_x", "Cases", "DailyCases", "DailyDeaths", "DailyRecoveries"]
        #columns = ["AcumulatedCases", "AcumulatedPRC"]

        #Preparacion del DataFrame

        eng = matlab.engine.start_matlab()
        [output, name_ccaa, iso_ccaa, data_spain] = eng.HistoricDataSpain(nargout=4)
        eng.quit()
        dictCM = output["historic"][6]

        dfFechas = pd.DataFrame(dictCM["label_x"])
        dfFechas = dfFechas
        dfFechas.columns = ["label_x"]

        dfCases = pd.DataFrame(dictCM["Cases"])
        dfCases = dfCases.transpose()
        dfCases.columns = ["Cases"]

        dfHospitalized = pd.DataFrame(dictCM["Hospitalized"])
        dfHospitalized = dfHospitalized.transpose()
        dfHospitalized.columns = ["Hospitalized"]

        dfCritical = pd.DataFrame(dictCM["Critical"])
        dfCritical = dfCritical.transpose()
        dfCritical.columns = ["Critical"]

        dfDeaths = pd.DataFrame(dictCM["Critical"])
        dfDeaths = dfDeaths.transpose()
        dfDeaths.columns = ["Deaths"]

        dfRecoveries = pd.DataFrame(dictCM["AcumulatedRecoveries"])
        dfRecoveries = dfRecoveries.transpose()
        dfRecoveries.columns = ["Recoveries"]

        dfFinal = pd.DataFrame(dfFechas.values, columns = ["Date"])
        dfFinal["Cases"] = dfCases.values
        dfFinal["Hospitalized"] = dfHospitalized.values
        dfFinal["Critical"] = dfCritical.values
        dfFinal["Deaths"] = dfDeaths.values
        dfFinal["Recoveries"] = dfRecoveries.values

        dfFinal.Cases = dfFinal.Cases.astype(int)
        dfFinal.Hospitalized = dfFinal.Hospitalized.astype(int)
        dfFinal.Critical = dfFinal.Critical.astype(int)
        dfFinal.Deaths = dfFinal.Deaths.astype(int)
        dfFinal.Recoveries = dfFinal.Recoveries.astype(int)
        dfFinal["Date"] = pd.to_datetime(dfFinal["Date"], format = "%d-%m-%Y")

        #print(dfFinal)
        return dfFinal

'''pm = PruebaMatlab()

df = pm.dataFrame'''
