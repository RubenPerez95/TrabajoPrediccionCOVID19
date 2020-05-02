
import matlab.engine
## Prueba de lectura de función Matlab ##


eng = matlab.engine.start_matlab()
[output, name_ccaa, iso_ccaa, data_spain] = eng.HistoricDataSpain(nargout=4)

#output.historic(7)

#print(output.historic(7))
#print(output)

a = output

print(a)

eng.quit()