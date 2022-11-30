import csv
import speech_recognition as sr

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