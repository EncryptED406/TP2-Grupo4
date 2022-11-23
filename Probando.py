import csv

datos = list()

with open("punto2.csv", newline='', encoding="UTF-8") as archivo_csv:

    csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True)

	    #next(csv_reader) #Evitamos leer el header

    for lineas in csv_reader:
        datos.append(lineas)
    
    datos.pop(0)
    print(datos)