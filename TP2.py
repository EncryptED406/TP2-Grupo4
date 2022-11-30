import csv
import speech_recognition as sr
from geopy.geocoders import Nominatim
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from PIL import Image

def lectura_archivo(archivo:str)->list:
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

def escribir_archivo(denuncias_procesadas:list):
    try:
        with open ("denuncias_procesadas.csv","w",newline="") as new_file:
            writer=csv.writer(new_file,delimiter=",")
            header:list=["Timestamp","Teléfono", "Dirección","patente", "descripción texto","descripción audio"] 
            writer.writerow(header)
            writer.writerows(denuncias_procesadas)
    except:
        print("Se produjo un error al generar el archivo")

def obtener_descripcion_audio(rutas_audios:list)->list:

    descripciones: list = []
    for ruta in range(len(rutas_audios)):
        r = sr.Recognizer()

        with sr.AudioFile(rutas_audios[ruta]) as source:
            audio = r.record(source)
        
        descripcion: str = r.recognize_google(audio, language ='es_AR')
        
        descripciones.append(descripcion)

    return descripciones

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
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-35))
    ax.set_extent([-100, 30, 0, 80], crs=ccrs.PlateCarree())
    plt.annotate("denuncia", xy = (x,y), xytext=(-20,20))
    plt.show()

def muestra_mapa(datos_Brutos, datos_Procesados):
    patente: str = input("Ingrese la patente: ")
    for i in range(len(datos_Procesados)):
        if datos_Procesados[i][5]==patente:
            indice: int = i
    ruta_foto: str = datos_Brutos[i][4]
    mostrar_foto_patente(ruta_foto)

    lat = datos_Brutos[indice][2]
    long = datos_Brutos[indice][3]
    mostrar_mapa(lat, long)
def obtener_Datos(datos_Brutos: list, latitud: list, longitud: list, rutas_audios: list, rutas_fotos: list)->None:

    for registro in range(len(datos_Brutos)):
        latitud.append(datos_Brutos[registro][2])
        longitud.append(datos_Brutos[registro][3])
        rutas_audios.append(datos_Brutos[registro][6])
        rutas_fotos.append(datos_Brutos[registro][4])

def obtener_datos_Procesados(datos:list, fecha:list, direccion:list, localidad:list, provincia:list, patentes:list, descripciones_audios:list)->list:
    desc_txt: list = datos[i][5]
    for i in range(len(datos)):
        datos[i][0] = fecha[i]
        datos[i][2] = direccion[i]
        datos[i][3] = localidad[i]
        datos[i][4] = provincia[i]
        datos[i][5] = patentes[i]
        datos[i][6] = desc_txt[i]
        datos[i][7] = descripciones_audios[i]
    
    return datos

def procesar_Datos(datos_Brutos: list, latitud: list, longitud: list, rutas_audios: list, rutas_fotos: list)->list:
    fecha: str = obtener_timestamp(datos_Brutos[0])
    direccion, localidad, provincia: str = obtener_direccion(latitud, longitud) # devuelve lista de dirección tras procesar latitud y longitud
    patentes: str = obtener_patente(rutas_fotos) # devuelve lista de patentes tras procesar imágenes
    descripciones_audios: str = obtener_descripcion_audio(rutas_audios) # devuelve lista de descripciones tras procesar audio

    datos_Procesados: list = obtener_datos_procesados(datos_Brutos, fecha, direccion, localidad, provincia, patentes, descripciones_audios)

def main()->None:
    datos_Brutos: list = leer_Archivo() # obtiene matríz, recibe ruta del archivo csv
    latitud: list = []
    longitud: list = []
    rutas_audios: list = []
    rutas_fotos: list = []

    obtener_Datos(datos_Brutos, latitud, longitud, rutas_audios, rutas_fotos)
    direcciones, patentes, descripciones = procesar_Datos(latitud, longitud, rutas_audios, rutas_fotos)# obtiene datos procesados de Dirección, descripción, patentes

    escribir_csv() 

    # items 3 , 4 , 5 , 6 , 7.

main()