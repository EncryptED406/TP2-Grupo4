from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def conseguir_direccion(latitud:str,longitud:str)->str:
    #Recibe 2 strings con las coordenadas  y devuelve otro con la direccion    
    geolocator= Nominatim(user_agent="TP2")
    try:
        direccion_de_infraccion=(str(geolocator.reverse(str(latitud)+","+str(longitud))))
    except TimeoutError:
        print("No se pudo acceder al proveedor para obtener los datos")
    return(direccion_de_infraccion)

def crear_lista_direcciones(latitud:list,longitud:list)->list:
#Recibe las listas latitud y longitud, las procesa con geopy y consigue la direccion, devuelve una lista      
    direcciones:list=[]

    for registro in range (len(latitud)):
        direccion_de_infraccion:str=str(conseguir_direccion(latitud[registro],longitud[registro]))
        direcciones.append(direccion_de_infraccion)

    return(direcciones)

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
    return(coordenadas)
    
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
        lat:float=float(coordenadas_infraccion[0])#esto lo pongo para facilitar la lectura del "if" q sigue a continuacion         
        lon:float=float(coordenadas_infraccion[1])#esto lo pongo para facilitar la lectura del "if" q sigue a continuacion
        #la condicion del if basicamente pide que se encuentre dentro del rectangulo delimitado por las calles dadas
        if ((lat>(zona_centro[0][0]) and lat<(zona_centro[1][0])) and (lon>(zona_centro[1][1]) and lon<(zona_centro[2][1]))):
            infracciones_zona_centro.append(infracciones_procesadas[registro])

    for registro in infracciones_zona_centro:
        print (registro)
    
def infracciones_estadios(infracciones:list):
#Recibe la lista de infracciones, muestra las 
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
    
    print ("Las siguientes infracciones se produjeron en las inmediaciones del estadio 'Alberto J. Armando'")
    for item in infracciones_bombonera:
        print(item)
    print ("Las siguientes infracciones se produjeron en las inmediaciones del estadio 'Mas Monumental'")
    for item in infracciones_monumental:
        print(item)

