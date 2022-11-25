#def patente_sospechosa("punto2.csv"):
#De aca saco la ubicacion y la fecha. 
#No arme la funcion porque todavia no se si voy a recibir un archivo csv o una lista.
#El codigo esta hecho para que reciba una archivo csv pero se puede cambiar.

import csv

datos = list()

with open("punto2.csv", newline='', encoding="UTF-8") as archivo_csv:

    csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True)


    for lineas in csv_reader:
        datos.append(lineas)
    
    datos.pop(0)
    

with open("robados.txt", "r") as archivo:

		patentes_buscada: list = []

		for linea in archivo:
			lineas = linea.rstrip("\n")
			patentes_buscada.append(lineas)

		patentes_buscada.pop(0)
		


patentes_alerta: dict = {}

for informacion in datos:
	if informacion[5] in patentes_buscada:
		patentes_alerta[informacion[5]] = [informacion[0],informacion[2]]

#Devuelve diccionario. Clave = Patente. Contenido = fecha, calle

for key, valor in patentes_alerta.items():
   
	print(f'El auto de patente {key} tienen pedido de captura. Visto el dia {valor[0]} en {valor[1]} ')