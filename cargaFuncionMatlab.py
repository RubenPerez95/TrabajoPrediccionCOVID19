import matlab.engine
import pandas as pd


class CargaFuncionMatlab():

    #Inicialización de la clase
    def __init__(self):

        eng = matlab.engine.start_matlab()
        [self.output, self.name_ccaa, self.iso_ccaa, self.data_spain] = eng.HistoricDataSpain(nargout=4)
        eng.quit()


    '''
    Este bucle recorre los datos producidos por la función de matlab y crea un dataframe para cada comunidad autónoma
    con las variables necesarias para realizar las predicciones.
    
    Devuelve una lista que contiene todos los dataframes de las CCAA
    '''
    def listaCCAA(self):

        #Declaracion de la lista que va a contener los dataframes de las CCAA
        listaCCAA = [None] * len(self.output["historic"])

        #Bucle para recorrer el diccionario con los datos de las CCAA
        for i in range(len(self.output["historic"])):
            #Selecciona el diccionario de una Comunidad Autónoma
            dictionary = self.output["historic"][i]
            #Selecciona el identificador de esa comunidad
            comunidad = self.iso_ccaa[i]

            '''Bloque para obtener las variables a predecir para la comunidad autónoma
            y guardar los datos en un dataframe'''
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
            '''Fin del bloque'''

            '''Bloque para añadir cada variable a un dataframe final que
            contine todas las variables de una comunidad'''
            dfFinal = pd.DataFrame(dfFechas.values, columns = ["Date"])
            dfFinal["CCAA"] = comunidad
            dfFinal["DailyCases"] = dfCases.values
            dfFinal["Hospitalized"] = dfHospitalized.values
            dfFinal["Critical"] = dfCritical.values
            dfFinal["DailyDeaths"] = dfDeaths.values
            dfFinal["DailyRecoveries"] = dfRecoveries.values
            '''Fin del bloque'''

            '''Bloque que parsea los datos a su formato específico'''
            dfFinal.DailyCases = dfFinal.DailyCases.astype(int)
            dfFinal.Hospitalized = dfFinal.Hospitalized.astype(int)
            dfFinal.Critical = dfFinal.Critical.astype(int)
            dfFinal.DailyDeaths = dfFinal.DailyDeaths.astype(int)
            dfFinal.DailyRecoveries = dfFinal.DailyRecoveries.astype(int)
            dfFinal["Date"] = pd.to_datetime(dfFinal["Date"], format = "%d-%m-%Y")
            '''Fin del bloque'''

            #Guarda el dataframe generado en la lista que contiene los dataframes de todas las CCAA
            listaCCAA[i] = dfFinal

        return listaCCAA

