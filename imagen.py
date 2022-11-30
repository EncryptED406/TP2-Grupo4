import requests

def mostrar_patente(ruta_imagen):
    with open(ruta_imagen, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=fp), 
            headers={'Authorization': 'Token 73c1e1139caf83e709ae221bf85c7053e157672b'}) #Este Token se obtiene al registrarse en la web

    if len(response.json()["results"]) == 0:
        devolver = False #No se pudo detectar la patente
    else:
        for key, value in (response.json()).items():
            if key == "results":
                for valores in value: 
                    for llave, info in valores.items(): 
                        if llave == 'plate':    #Si la clave del diccionario es 'plate' te devuelve la info que tiene
                            devolver = info
    return(devolver)

def validar_patente(lista):
    """"Recibe imagenes Devuelve patentes o False si no se pudo detectar patente"""
    patentes = []
    for i in lista:
        patentes.append(mostrar_patente(i))
    return patentes

imagenes = ['20221123_202154.jpg',"elefante.jpg",'auto.jpg','20221123_202321.jpg','20221123_201921.jpg','20221123_202321.jpg']
print(validar_patente(im))
