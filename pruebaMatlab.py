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

        dfCases = pd.DataFrame(dictCM["DailyCases"])
        dfCases = dfCases.transpose()
        dfCases.columns = ["DailyCases"]

        dfHospitalized = pd.DataFrame(dictCM["Hospitalized"])
        dfHospitalized = dfHospitalized.transpose()
        dfHospitalized.columns = ["Hospitalized"]

        dfCritical = pd.DataFrame(dictCM["Critical"])
        dfCritical = dfCritical.transpose()
        dfCritical.columns = ["Critical"]

        dfDeaths = pd.DataFrame(dictCM["DailyDeaths"])
        dfDeaths = dfDeaths.transpose()
        dfDeaths.columns = ["DailyDeaths"]

        dfRecoveries = pd.DataFrame(dictCM["DailyRecoveries"])
        dfRecoveries = dfRecoveries.transpose()
        dfRecoveries.columns = ["DailyRecoveries"]

        dfFinal = pd.DataFrame(dfFechas.values, columns = ["Date"])
        dfFinal["DailyCases"] = dfCases.values
        dfFinal["Hospitalized"] = dfHospitalized.values
        dfFinal["Critical"] = dfCritical.values
        dfFinal["DailyDeaths"] = dfDeaths.values
        dfFinal["DailyRecoveries"] = dfRecoveries.values

        dfFinal.DailyCases = dfFinal.DailyCases.astype(int)
        dfFinal.Hospitalized = dfFinal.Hospitalized.astype(int)
        dfFinal.Critical = dfFinal.Critical.astype(int)
        dfFinal.DailyDeaths = dfFinal.DailyDeaths.astype(int)
        dfFinal.DailyRecoveries = dfFinal.DailyRecoveries.astype(int)
        dfFinal["Date"] = pd.to_datetime(dfFinal["Date"], format = "%d-%m-%Y")

        #print(dfFinal)
        return dfFinal

'''pm = PruebaMatlab()

df = pm.dataFrame'''
