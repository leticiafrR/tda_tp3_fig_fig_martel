import time
import sys
import csv
import tp
from benders_generator import *

# Este no lo traduzco puesto que se descarta para la entrega

def calcular_tiempo_algoritmo(algoritmo):
    tiempo_inicio = time.time()
    algoritmo()
    tiempo_fin = time.time()

    tiempo_ms = round((tiempo_fin - tiempo_inicio) * 1000, 6)
    return tiempo_ms

def calcular_primedio_tiempo(cantidad, algoritmo):
    sumatoria = 0
    for _ in range(cantidad):
        sumatoria += calcular_tiempo_algoritmo(algoritmo)

    promedio_tiempo_ms = round(sumatoria / cantidad, 6)
    return promedio_tiempo_ms


def calcular_datos(total, salto, const_b):
    datos = []

    #cant_grupos_list = [3, 1.5]
    cant_grupos_list = [1.5]
    #cant_grupos_list = [3]

    for cant_actual in range(salto, total + 1, salto):
        maestros = generate_benders(cant_actual, const_b)

        for cant_grupos in cant_grupos_list:
            cant_g = (int(len(maestros) / cant_grupos))
            if cant_g == 0:
                cant_g = 1
            #tiempo_ms = calcular_tiempo_algoritmo(lambda : tp.greedy_resolution(maestros, cant_g))
            #tiempo_ms = calcular_tiempo_algoritmo(lambda : tp.backtracking_algotithm(maestros, cant_g))
            #tiempo_ms = calcular_tiempo_algoritmo(lambda : tp.backtracking_greedy_algotithm(maestros, cant_g))
            
            tiempo_ms = calcular_tiempo_algoritmo(lambda : tp.lp_algorithm(maestros, cant_g))

            #tiempo_ms = calcular_primedio_tiempo(3, lambda : tp.greedy_resolution(maestros, cant_g))
            datos.append((cant_actual, cant_g, tiempo_ms))

            cant_grupos+=1

    return datos

def guardar_datos_csv(nombre_archivo, datos):
    archivo = open(nombre_archivo, "w", newline="")
    csv_escritor = csv.writer(archivo, delimiter=";")
    for dato in datos:
        dato = [str(dato[0]) + "_" + str(dato[1]), str(dato[2])]
        #dato = [str(dato[0]), str(dato[2])]
        csv_escritor.writerow(dato)
    archivo.close()

def main():
    nombre_archivo = sys.argv[1]
    total = int(sys.argv[2])
    salto = int(sys.argv[3])

    const_b = get_constant(sys.argv[4:])

    datos = calcular_datos(total, salto, const_b)
    guardar_datos_csv(nombre_archivo, datos)

if __name__ == "__main__":
    main()