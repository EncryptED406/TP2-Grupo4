with open("robados.txt", "r") as archivo:

		patentes_buscada: list = []

		for linea in archivo:
			lineas = linea.rstrip("\n")
			patentes_buscada.append(lineas)

		patentes_buscada.pop(0)
		print(patentes_buscada)


patentes_alerta: dict = {}

for patentes in patentes_buscada:
	patentes_alerta[patentes] = []

print(patentes_alerta)