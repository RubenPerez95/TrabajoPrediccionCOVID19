import matlab.engine
import pandas as pd


## Prueba de lectura de función Matlab ##

class PruebaMatlab():

    def __init__(self):

        eng = matlab.engine.start_matlab()
        [self.output, self.name_ccaa, self.iso_ccaa, self.data_spain] = eng.HistoricDataSpain(nargout=4)
        eng.quit()

    def dataFrame(self):

        #Preparacion del DataFrame
        listaCCAA = [None] * len(self.output["historic"])

        for i in range(len(self.output["historic"])):
            dictionary = self.output["historic"][i]
            comunidad = self.iso_ccaa[i]

            dfFechas = pd.DataFrame(dictionary["label_x"])
            dfFechas = dfFechas
            dfFechas.columns = ["label_x"]

            dfCases = pd.DataFrame(dictionary["DailyCases"])
            dfCases = dfCases.transpose()
            dfCases.columns = ["DailyCases"]

            dfHospitalized = pd.DataFrame(dictionary["Hospitalized"])
            dfHospitalized = dfHospitalized.transpose()
            dfHospitalized.columns = ["Hospitalized"]

            dfCritical = pd.DataFrame(dictionary["Critical"])
            dfCritical = dfCritical.transpose()
            dfCritical.columns = ["Critical"]

            dfDeaths = pd.DataFrame(dictionary["DailyDeaths"])
            dfDeaths = dfDeaths.transpose()
            dfDeaths.columns = ["DailyDeaths"]

            dfRecoveries = pd.DataFrame(dictionary["DailyRecoveries"])
            dfRecoveries = dfRecoveries.transpose()
            dfRecoveries.columns = ["DailyRecoveries"]

            dfFinal = pd.DataFrame(dfFechas.values, columns = ["Date"])
            dfFinal["CCAA"] = comunidad
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

            listaCCAA[i] = dfFinal
        return listaCCAA

