import csv
import matplotlib.pyplot as plt
from datetime import datetime

#REQUIERE LIBRERIA MATPLOTLIB Y DATETIME.

#REQUIERE LA FUNCION OBTENER_TIMESTAMP DEL PUNTO 5.

def graficar_denuncias_mensuales(fechas)->None:

    informacion: list = fechas

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

        
    x: list = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
    y: list = [enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,octubre,noviembre,diciembre]

    plt.bar(x,y,color = 'tab:purple')
    plt.xlabel('MESES', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.ylabel('DENUNCIAS', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.title('Denuncias registradas mensualmente', fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'g'})
    plt.show()