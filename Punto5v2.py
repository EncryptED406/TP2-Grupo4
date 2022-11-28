import csv

from datetime import datetime

#Libreria DATETIME necesaria.

def obtener_timestamp()->list:

    datos: list = []
    fechas: list = []

    with open("punto2.csv", newline='', encoding="UTF-8") as archivo_csv:

        next(archivo_csv)

        csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True)

        for lineas in csv_reader:
            datos.append(lineas[0])


    with open("Probando.csv", 'w', newline ='', encoding="UTF-8") as archivo_csv:

            csv_writer = csv.writer(archivo_csv)

            csv_writer.writerow(["Timestamp"]) 

            csv_writer.writerow(datos)


    with open("Probando.csv", newline='', encoding="UTF-8") as archivo_csv:

        next(archivo_csv)

        csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True, quotechar='"', quoting= csv.QUOTE_NONNUMERIC)

        for lineas in csv_reader:
            fechas.append(lineas)
    
    return fechas


def patente_sospechosa(fechas)->None:

    datos = list()

    with open("punto2.csv", newline='', encoding="UTF-8") as archivo_csv:


        next(archivo_csv)

        csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True)


        for lineas in csv_reader:
            datos.append(lineas)
    
    

    with open("robados.txt", "r") as archivo:

		    patentes_buscada: list = []

		    for linea in archivo:
			    lineas = linea.rstrip("\n")
			    patentes_buscada.append(lineas)

		    patentes_buscada.pop(0)


    patentes_alerta: dict = {}


    for informacion in datos:
	    if informacion[5] in patentes_buscada:
		    patentes_alerta[informacion[5]] = [informacion[0], informacion[2]]


    for key, valor in patentes_alerta.items():

        fecha = datetime.fromtimestamp(float(valor[0]))

        print(f'El auto de patente {key} tiene pedido de captura. Visto el dia {fecha} en {valor[1]} ')


