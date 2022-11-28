import csv
from geopy.geocoders import Nominatim

def leer_archivo(archivo:str)->list:
    denuncias:list=[]
    try:
        with open (archivo) as file:
            reader=csv.reader(file,delimiter=",")            
            next(reader)
            for linea in reader:
                denuncias.append(linea)
    except IOError:
        print("se produjo un error en la lectura del archivo" )

    return(denuncias)

def escribir_csv(denuncias_procesadas:list):
    try:
        with open ("denuncias_procesadas.csv","w",newline="") as new_file:
            writer=csv.writer(new_file,delimiter=",")
            header:list=["Timestamp","Teléfono", "Dirección","patente", "descripción texto","descripción audio"] 
            writer.writerow(header)
            writer.writerows(denuncias_procesadas)
    except:
        print("Se produjo un error al generar el archivo")

def conseguir_direccion(latitud:str,longitud:str)->str:
    #Recibe 2 strings con las coordenadas  y devuelve otro con la direccion    
    geolocator= Nominatim(user_agent="TP2")
    direccion_de_infraccion=str(geolocator.reverse(latitud+","+longitud))

    return(direccion_de_infraccion)

def crear_lista_direcciones(latitud:list,longitud:list)->list:
#Recibe las listas latitud y longitud, las procesa con geopy y consigue la direccion, devuelve una lista      
    direcciones:list=[]

    for registro in range (len(latitud)):
        direccion_de_infraccion:str=str(conseguir_direccion(latitud[registro],longitud[registro]))
        direcciones.append(direccion_de_infraccion)

    return(direcciones)

def obtener_Datos(datos_Brutos: list, latitud: list, longitud: list, rutas_audios: list, rutas_fotos: list)->None:

    for registro in range(len(datos_Brutos)):
        latitud.append(datos_Brutos[registro][2])
        longitud.append(datos_Brutos[registro][3])
        rutas_audios.append(datos_Brutos[registro][6])
        rutas_fotos.append(datos_Brutos[registro][4])


# def procesar_Datos(latitud: list, longitud: list, rutas_audios: list, rutas_fotos: list)->list:
#     obtener_direccion(latitud, longitud) # devuelve lista de dirección tras procesar latitud y longitud
#     obtener_patente(rutas_fotos) # devuelve lista de patentes tras procesar imágenes
#     obtener_descripcion_audio(rutas_audios) # devuelve lista de descripciones tras procesar audio

def main()->None:
    datos_Brutos: list = leer_archivo("denuncias.csv") # obtiene matríz, recibe ruta del archivo csv
    latitud: list = []
    longitud: list = []
    rutas_audios: list = []
    rutas_fotos: list = []

    obtener_Datos(datos_Brutos, latitud, longitud, rutas_audios, rutas_fotos)

    
    #direcciones, patentes, descripciones = procesar_Datos(latitud, longitud, rutas_audios, rutas_fotos)# obtiene datos procesados de Dirección, descripción, patentes

    #escribir_csv() 

    # items 3 , 4 , 5 , 6 , 7.

main()