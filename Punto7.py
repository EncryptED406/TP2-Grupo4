import csv
import matplotlib.pyplot as plt

#REQUIERE LIBRERIA MATPLOTLIB

def graficar_denuncias_mensuales()->None:

    datos: list = []
    fechas: list = []

    with open("punto2.csv", newline='', encoding="UTF-8") as archivo_csv:

        next(archivo_csv)

        csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True)

        for lineas in csv_reader:
            datos.append(lineas[0])

    #Tengo que crear otro archivo solo para las fechas porque con las patentes y el numero de la calle la funcion
    # Quote NONNUMERIC rompe todo.

    with open("Probando.csv", 'w', newline ='', encoding="UTF-8") as archivo_csv:

            csv_writer = csv.writer(archivo_csv)

            csv_writer.writerow(["Timestamp"]) 

            csv_writer.writerow(datos)

    #Crea otro archivo csv con las fechas

    with open("Probando.csv", newline='', encoding="UTF-8") as archivo_csv:

        next(archivo_csv)

        csv_reader = csv.reader(archivo_csv, delimiter=',', skipinitialspace= True, quotechar='"', quoting= csv.QUOTE_NONNUMERIC)

        for lineas in csv_reader:
            fechas.append(lineas)


    #Crea una lista con las fechas en modo float. 

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

    for informacion in fechas:
        for fecha in informacion:
            if 20220101 <= fecha <= 20220131:
                enero += 1
            if 20220201 <= fecha <= 20220229:
                febrero += 1
            if 20220301 <= fecha <= 20220331:
                marzo += 1
            if 20220401 <= fecha <= 20220430:
                abril += 1
            if 20220501 <= fecha <= 20220531:
                mayo += 1
            if 20220601 <= fecha <= 20220630:
                junio += 1
            if 20220701 <= fecha <= 20220731:
                julio += 1
            if 20220801 <= fecha <= 20220831:
                agosto += 1
            if 20220901 <= fecha <= 20220930:
                septiembre += 1
            if 20221001 <= fecha <= 20221031:
                octubre += 1
            if 20221101 <= fecha <= 20221130:
                noviembre += 1
            if 20221201 <= fecha <= 20221231:
                diciembre += 1
            else:
                pass
                #Podriamos usar un Except error de que el mes ingresado no existe.

        
    x: list = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
    y: list = [enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,octubre,noviembre,diciembre]

    plt.bar(x,y,color = 'tab:purple')
    plt.xlabel('MESES', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.ylabel('DENUNCIAS', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.title('Denuncias registradas mensualmente', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.show()
