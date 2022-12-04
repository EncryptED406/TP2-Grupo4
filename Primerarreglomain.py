import csv
import speech_recognition as sr
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
import requests
import copy

#CAMBIOS:
# Se borraron espacios en blanco
# Se agrego un menu
# Se agregaron algunos ->list dsp de algunas funciones (faltan agregar todavia)
# Se cambio el Punto 7 (Se separo en dos funciones, sigo pensando una mejor solucion)


#PUNTO 1
def lectura_archivo()->list:
	denuncias:list=[]
	try:
		with open ("denuncias_bis.csv") as file:
			reader=csv.reader(file,delimiter=",")            
			next(reader)
			for linea in reader:
				denuncias.append(linea)
	except IOError:
		print("se produjo un error en la lectura del archivo" )

	return denuncias
#Termina PUNTO1
def obtener_datos_Brutos(datos_Brutos: list, timestamps: list, latitud: list, longitud: list, rutas_audios: list, rutas_fotos: list)->None:

	for registro in range(len(datos_Brutos)):
		timestamps.append(datos_Brutos[registro][0])
		latitud.append(datos_Brutos[registro][2])
		longitud.append(datos_Brutos[registro][3])
		rutas_audios.append(datos_Brutos[registro][6])
		rutas_fotos.append(datos_Brutos[registro][4])
#PUNTO 2
def obtener_timestamp(lista_timestamp:list)->list:
	lista_fechas: list = []	
    #Por si rompe, antes la linea era: lista_fechas = list()
	for valores in lista_timestamp:
		valores = datetime.fromtimestamp(float(valores))
		lista_fechas.append(valores)

	return lista_fechas

def obtener_direccion(latitud:str,longitud:str)->str:
	#Recibe 2 strings con las coordenadas  y devuelve otro con la direccion    
	geolocator= Nominatim(user_agent="TP2")
	try:
		direccion_de_infraccion=(str(geolocator.reverse(str(latitud)+","+str(longitud))))
	except TimeoutError:
		print("No se pudo acceder al proveedor para obtener los datos")
	return direccion_de_infraccion

def crear_lista_direcciones(latitud:list,longitud:list)->list:     
	direcciones:list=[]
	for registro in range (len(latitud)):
		direccion_de_infraccion:str=str(obtener_direccion(latitud[registro],longitud[registro]))
		direcciones.append(direccion_de_infraccion)

	return direcciones

def conseguir_coordenadas(direccion:str)->list:
	#devuelve las coordenadas de la direccion indicada como una lista cuyos elementos son float
	geolocator= Nominatim(user_agent="TP2")
	try:
		lat=float(geolocator.geocode(direccion).point.latitude)
		lon=float(geolocator.geocode(direccion).point.longitude)
		coordenadas:list=[lat,lon]
	except TimeoutError: 
		print ("Hubo un error al conseguir los datos, verifique su conexion.")
	except:
		print( "No se pudo localizar la dirección.")       
	return coordenadas

def mostrar_patente(ruta_imagen)->str:
	with open(ruta_imagen, 'rb') as fp:
		response = requests.post(
			'https://api.platerecognizer.com/v1/plate-reader/',
			files=dict(upload=fp), 
			headers={'Authorization': 'Token 15ca3097b892584724d956a3feed60f32614585c'}) #Este Token se obtiene al registrarse en la web

		for key, value in (response.json()).items():
			if key == "results":
				for valores in value: 
					patente: str = valores['plate']
					return patente

def validar_patentes(lista)->list:
	patentes: list = []
	for i in lista:
		patentes.append(mostrar_patente(i))
	return patentes

def obtener_descripcion_audio(rutas_audios:list)->list:
	descripciones: list = []
	for ruta in range(len(rutas_audios)):
		r = sr.Recognizer()
		with sr.AudioFile(rutas_audios[ruta]) as source:
			audio = r.record(source)
		descripcion: str = r.recognize_google(audio, language ='es_AR')
		descripciones.append(descripcion)

	return descripciones

def compaginar_datos_Procesados(datos_Brutos:list, fecha:list, direccion:list, patentes:list, descripciones_audios:list)->list:
	datos_procesados: list = copy.deepcopy(datos_Brutos)
	for i in range(len(datos_Brutos)):
		datos_procesados[i][0] = fecha[i]
		datos_procesados[i][2] = direccion[i]
		datos_procesados[i][3] = patentes[i]
		datos_procesados[i][4] = datos_Brutos[i][5]
		datos_procesados[i][5] = descripciones_audios[i]
		datos_procesados[i].pop(6)

	return datos_procesados

def escribir_archivo(denuncias_procesadas:list):
	try:
		with open ("denuncias_procesadas.csv","w",newline="") as new_file:
			writer=csv.writer(new_file,delimiter=",")
			header:list=["Fecha","Teléfono", "Dirección", "patente", "descripción texto","descripción audio"] 
			writer.writerow(header)
			writer.writerows(denuncias_procesadas)
	except:
		print("Se produjo un error al generar el archivo")
#TERMINA PUNTO 2
#PUNTO 3
def infracciones_estadios(infracciones:list):
#Recibe la lista de infracciones, muestra las direcciones
	infracciones_bombonera:list=[]
	infracciones_monumental:list=[]
	bombonera:list=conseguir_coordenadas("estadio Alberto J. Armando")
	monumental:list=conseguir_coordenadas("estadio Monumental")

	for registro in range (len(infracciones)):
		coord_infraccion:list=conseguir_coordenadas(infracciones[registro][2])
		if (geodesic(bombonera, coord_infraccion).kilometers<1):
			infracciones_bombonera.append(infracciones[registro])
		elif (geodesic(monumental, coord_infraccion).kilometers<1):
			infracciones_monumental.append(infracciones[registro])
	
	print ("\nLas siguientes infracciones se produjeron en las inmediaciones del estadio 'Alberto J. Armando'")
	for item in infracciones_bombonera:
		print(f"\n{item}")
	print ("\nLas siguientes infracciones se produjeron en las inmediaciones del estadio 'Mas Monumental'")
	for item in infracciones_monumental:
		print(item)
#TERMINA PUNTO 3
#PUNTO 4
def delimitar_zona_centro ()->list:
	coordenadas_esquina_a:list=conseguir_coordenadas("Av. Callao & Av. Rivadavia")
	coordenadas_esquina_b:list=conseguir_coordenadas("Av. Callao & Av. Córdoba")
	coordenadas_esquina_c:list=conseguir_coordenadas("Av. Leandro N. Alem & Av. Córdoba")
	coordenadas_esquina_d:list=conseguir_coordenadas("Av. Rivadavia 100, Monserrat, Buenos Aires")

	zona_centro:list=[coordenadas_esquina_a,coordenadas_esquina_b,coordenadas_esquina_c,coordenadas_esquina_d]

	return zona_centro

def infracciones_del_centro(infracciones_procesadas:list):
#Recibe la lista procesada, decide si la direccion esta o no en el area y muesta por pantalla aquellas q lo estan 
	zona_centro:list=delimitar_zona_centro()
	infracciones_zona_centro:list=[]

	for registro in range (len(infracciones_procesadas)):
		coordenadas_infraccion:list=conseguir_coordenadas(infracciones_procesadas[registro][2])
		lat:float=float(coordenadas_infraccion[0])        
		lon:float=float(coordenadas_infraccion[1])
		if ((lat>(zona_centro[0][0]) and lat<(zona_centro[1][0])) and (lon>(zona_centro[1][1]) and lon<(zona_centro[2][1]))):
			infracciones_zona_centro.append(infracciones_procesadas[registro])
	print("\nLas siguientes infracciones se produjeron en zona centro: ")
	for registro in infracciones_zona_centro:
		print (f"\n{registro}")
#TERMINA PUNTO 4
#PUNTO 5
def patente_sospechosa()->None:
	datos: list = []
    #Por si se rompe, antes era: datos = list(). Tmb se saco lo que recibia la funcion porque creo que no lo usaba
	with open("denuncias_procesadas.csv", newline='') as archivo_csv:
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
		if informacion[3] in patentes_buscada:
			patentes_alerta[informacion[3]] = [informacion[0], informacion[2]]

	for key, valor in patentes_alerta.items():
		print(f'El auto de patente {key} tiene pedido de captura. Visto el dia {valor[0]} en {valor[1]} ')
#TERMINA PUNTO 5
#PUNTO 6
def mostrar_foto_patente(ruta_foto: str):
	print("\nLa imágen asociada a la patente indicada es la siguiente: ")
	im = Image.open(ruta_foto) 
	im.show()

def mostrar_mapa(lat: str, long: str):
	print("\nA continucación, un mapa con la ubicación del auto indicado, en el momento de la denuncia: ")
	
	map = Basemap(width=9000000,height=5000000,projection='lcc',
			resolution=None,lat_1=-30.,lat_2=-40,lat_0=-35,lon_0=-60.)
	plt.figure(figsize=(19,20))
	map.bluemarble()
	x, y = map(long, lat)
	map.plot(x,y,marker='o',color='Red',markersize=5)
	plt.annotate("denuncia", xy = (x,y), xytext=(-20,20))
	plt.show()

def mostrar_infractor(datos_Brutos: list, datos_Procesados: list):
	patente: str = input("Ingrese la patente: ")
	for i in range(len(datos_Procesados)):
		if datos_Procesados[i][3] == patente:
			indice: int = i
		
	ruta_foto: str = datos_Brutos[indice][4]
	mostrar_foto_patente(ruta_foto)

	lat = datos_Brutos[indice][2]
	long = datos_Brutos[indice][3]
	mostrar_mapa(lat, long)
#TERMINA PUNTO 6
#PUNTO 7
def obtener_lista_timestamp()->list:
    lista_timestamp: list = []
    with open ("denuncias_bis.csv") as file:
            reader=csv.reader(file,delimiter=",")            
            next(reader)
            for linea in reader:
                lista_timestamp.append(linea[0])
    with open("Probando.csv", 'w', newline ='', encoding="UTF-8") as archivo_csv:
            csv_writer = csv.writer(archivo_csv)
            csv_writer.writerow(["Timestamp"]) 
            csv_writer.writerow(lista_timestamp)
            lista_timestamp.clear()
    with open("Probando.csv", newline='', encoding="UTF-8") as archivo_csv:
        next(archivo_csv)
        csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True, quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        for lineas in csv_reader:
            lista_timestamp.append(lineas)
    
    return lista_timestamp

def calcular_denuncias_mensuales(lista_timestamp:list)->list:

    informacion: list = lista_timestamp
    enero: int = 0  
    febrero: int = 0
    marzo: int = 0
    abril: int = 0
    mayo: int = 0
    junio: int = 0
    julio: int = 0
    agosto: int = 0
    septiembre: int = 0
    octubre: int = 0
    noviembre: int = 0
    diciembre: int = 0

    for timestamp in lista_timestamp:
        for fecha in timestamp:
            if 1641006000 <= fecha <= 1643684399:
                enero += 1
            if 1643684400 <= fecha <= 1646103599:
                febrero += 1
            if 1646103600 <= fecha <= 1648781999:
                marzo += 1
            if 1648782000 <= fecha <= 1651373999:
                abril += 1
            if 1651374000 <= fecha <= 1654052399:
                mayo += 1
            if 1654052400 <= fecha <= 1656644399:
                junio += 1
            if 1656644400 <= fecha <= 1659322799:
                julio += 1
            if 1659322800 <= fecha <= 1662001199:
                agosto += 1
            if 1662001200 <= fecha <= 1664593199:
                septiembre += 1
            if 1664593200 <= fecha <= 1667271599:
                octubre += 1
            if 1667271600 <= fecha <= 1669863599:
                noviembre += 1
            if 1669863600 <= fecha <= 1672541999:
                diciembre += 1
    eje_y: list = [enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,octubre,noviembre,diciembre]

    return eje_y

def graficar_denuncias_mensuales(eje_y:list)->None:
    x: list = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
    y: list = eje_y

    plt.bar(x,y,color = 'tab:purple')
    plt.xlabel('MESES', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.ylabel('DENUNCIAS', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.title('Denuncias registradas mensualmente', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.show()
#TERMINA PUNTO 7
#MENU
def menu(listaOpciones):
    """
    Pre: Se reciben 1 parámetros con la lista de opciones a ser mostradas
    Post: se retorna la opción seleccionada como entero.
    """
    for i in range(0, len(listaOpciones)):
        print(i + 1, "- " + listaOpciones[i])

    op = int(input("Elija una opción, 0 para salir"))
    return op
#TERMINA MENU (Si quieren otro tipo de menu se puede cambiar, este lo paso Bruno al principio)

def main()->None:
	datos_Brutos: list = lectura_archivo() # obtiene matríz, recibe ruta del archivo csv
	timestamps: list = []
	latitud: list = []
	longitud: list = []
	rutas_audios: list = []
	rutas_fotos: list = []

	obtener_datos_Brutos(datos_Brutos, timestamps, latitud, longitud, rutas_audios, rutas_fotos)

	opciones = ["PUNTO 1", "PUNTO 2", "PUNTO 3", "PUNTO 4","PUNTO 5","PUNTO 6","PUNTO 7"]

	op = menu(opciones)

	while op != 0:
        if op == 1:
            pass
        elif op == 2:
            pass
        elif op == 3:
            pass
        elif op == 4:
            pass
        elif op == 5:
            pass
        elif op == 6:
            pass
        elif op == 7:
            pass
        op = menu(opciones)
	
	#ITEM 2
	fechas: list = obtener_timestamp(timestamps)
	direcciones: list = crear_lista_direcciones(latitud, longitud)
	patentes: list = validar_patentes(rutas_fotos)
	descripciones_audios: list = obtener_descripcion_audio(rutas_audios)
	datos_Procesados: list = compaginar_datos_Procesados(datos_Brutos, fechas, direcciones ,patentes, descripciones_audios)

	for item in datos_Procesados:
		if item[3]==None:
			datos_Procesados.pop(datos_Procesados.index(item))

	escribir_archivo(datos_Procesados)
	#FIN DE ITEM 2

	infracciones_estadios(datos_Procesados)

	infracciones_del_centro(datos_Procesados)

	mostrar_infractor(datos_Brutos, datos_Procesados)

	fechas_lista: list = obtener_lista_timestamp()
	patente_sospechosa(fechas_lista)
	graficar_denuncias_mensuales(fechas_lista)

main()