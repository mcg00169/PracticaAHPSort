import ahp, ahpsort, datos, mapa, prioridades
import numpy as np
import pandas as pd

def ahpsort_ii():
    # 1. Lee los datos necesarios desde un archivo CSV utilizando la función leer_datos_csv de datos.py.
    ruta_archivo = "datos/datosAndalucia.csv"  # Cambia esto a la ruta de tu archivo CSV
    df = datos.leer_datos_csv(ruta_archivo)
    if df is None:
        print("No se pudieron leer los datos. Asegúrate de que el archivo existe y tiene el formato correcto.")
        return
    # Muestra los criterios y alternativas leídos del archivo CSV
    print(f"Criterios: {df.columns.tolist()}")
    print(f"Alternativas: {df.index.tolist()}")
    criterios = df.columns.tolist()

    # 2. Define los pesos de los criterios y subcriterios utilizando la función calcular_pesos de ahp.py.
    matriz_comparacion = np.array([[1, 5, 3, 7, 3], 
                                   [0.2, 1, 3, 0.5, 0.25], 
                                   [0.333, 0.333, 1, 0.2, 0.2],
                                   [0.143, 2, 5, 1, 0.2],
                                   [0.3, 4, 5, 5, 1]])  # Ejemplo de matriz de comparación
    pesos = ahp.calcular_pesos(matriz_comparacion)
    ratio_consistencia = ahp.calcular_CR(matriz_comparacion)

    print("Pesos de los criterios:\n")
    for i, criterio in enumerate(criterios):
        print(f"{criterio}: {pesos[i]:.4f}")
    print(f"Ratio de consistencia (CR): {ratio_consistencia}")
    if ratio_consistencia > 0.1:
        print("Advertencia: La matriz de comparación no es consistente (CR > 0.1). Considera revisar los valores de la matriz.")

    # 3. Calcula las prioridades locales para cada alternativa y criterio utilizando la función prioridad_local de prioridades.py.
    # Leemos los valores de los puntos de referencia (RF) y perfiles centrales (CP) de cada criterio desde el DataFrame
    rpData = datos.leer_datos_csv("datos/rpAndalucia.csv")
    cpData = datos.leer_datos_csv("datos/cpAndalucia.csv")
    if rpData is None or cpData is None:
        print("No se pudieron leer los datos de RP o CP. Asegúrate de que los archivos existen y tienen el formato correcto.")
        return
    # Almacenamos los valores de los perfiles centrales (CP) de cada criterio en una lista
    valores = cpData.values.flatten().tolist()  # Valores de los perfiles centrales (CP)
    vAlto = valores[0:5]
    vMedio = valores[5:10]
    vBajo = valores[10:15]

    # Leemos los puntos de corte RP y los valores de la prioridad local para cada criterio
    puntos_x = rpData.values.flatten().tolist()  # Puntos de corte (RF)
    puntos_y = cpData.values.flatten().tolist()  # Valores de prioridad local (CP)
    # Para cada perfil central (CP), calculamos la prioridad local según los puntos de referencia (RF) y los valores de las alternativas
    prioridades = {} # Diccionario para almacenar las prioridades locales de cada criterio y global para cada perfil
    prioridades_locales = []  # Lista para almacenar las prioridades locales de cada criterio
    prioridades_globales = []  # Lista para almacenar las prioridades globales de cada perfil
    for i in range(len(vAlto)):
        prioridad = prioridades.prioridad_local(vAlto[i], puntos_x, puntos_y)
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Alto: {prioridades_locales}")
    # Después, se calcula la prioridad global utilizando la función prioridad_global de ahpsort.py, pasando las prioridades locales y los pesos de los criterios como argumentos.
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Alto: {prioridad_global}")
    prioridades_globales.append(prioridad_global)
    prioridades_locales.append(prioridad_global)  # La prioridad global se añade a la lista de prioridades para guardar los resultados en un archivo CSV. 
    prioridades["Alto"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Alto en el diccionario de prioridades
    # Repetimos el proceso para los valores de prioridad local de vMedio y vBajo
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vMedio
    for i in range(len(vMedio)):
        prioridad = prioridades.prioridad_local(vMedio[i], puntos_x, puntos_y)
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Medio: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Medio: {prioridad_global}")
    prioridades_globales.append(prioridad_global)
    prioridades_locales.append(prioridad_global)
    prioridades["Medio"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Medio en el diccionario de prioridades
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vBajo
    for i in range(len(vBajo)):
        prioridad = prioridades.prioridad_local(vBajo[i], puntos_x, puntos_y)
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Bajo: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Bajo: {prioridad_global}")
    prioridades_globales.append(prioridad_global)
    prioridades_locales.append(prioridad_global)
    prioridades["Bajo"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Bajo en el diccionario de prioridades
    # Guardamos los resultados en un archivo CSV utilizando la función guardar_resultados_csv de datos.py.
    resultados_cp = pd.DataFrame.from_dict(prioridades, orient='index', columns=[f'Prioridad Local {i+1}' for i in range(len(puntos_x))] + ['Prioridad Global'])
    ruta_resultados = "resultados/resultados_prioridades.csv"
    datos.guardar_resultados_csv(resultados_cp, ruta_resultados)

    # Calculamos ahora las prioridades locales para cada alternativa utilizando la función prioridad_local de prioridades.py, y luego calculamos la prioridad global utilizando la función prioridad_global de ahpsort.py.
    prioridades_locales = []
    prioridades_globales = []
    for i in range(len(df)):
        valores = df.iloc[i].values.flatten().tolist()  # Valores de cada alternativa
        for j in range(len(valores)):
            valor = valores[j]
            puntos_x = rpData.iloc[j].values.flatten().tolist()  # Puntos de corte (RF) para el criterio j
            puntos_y = cpData.iloc[j].values.flatten().tolist()  # Valores de prioridad local (CP) para el criterio j
            prioridad_local = prioridades.prioridad_local(valor, puntos_x, puntos_y)  # Calculamos la prioridad local para cada alternativa
            prioridades_locales.append(prioridad_local)
        print(f"Prioridades locales para las alternativa {df.index[i]}: {prioridades_locales}")
        prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
        print(f"Prioridad global para la alternativa {df.index[i]}: {prioridad_global}")
        prioridades_globales.append(prioridad_global)
        # Reiniciamos la lista de prioridades locales para la siguiente alternativa
        prioridades_locales = []

    # 5. De cada prioridad global calculada para cada alternativa, comparamos con los valores de prioridad global de los perfiles Alto, Medio y Bajo
    # y asignamos la categoría correspondiente a cada alternativa.
    umbrales = [("Bajo", 0, prioridades["Bajo"][-1]), ("Medio", prioridades["Bajo"][-1], prioridades["Medio"][-1]), ("Alto", prioridades["Medio"][-1], 1)]
    categorias_asignadas = {}
    for i, prioridad_global in enumerate(prioridades_globales):
        categoria = ahpsort.clasificar(prioridad_global, umbrales)
        categorias_asignadas[df.index[i]] = categoria
    print(f"Categorías asignadas: {categorias_asignadas}")

    # 6. Guardamos la tabla de clasificación en un archivo CSV utilizando la función guardar_resultados_csv de datos.py.
    resultados_clasificacion = pd.DataFrame.from_dict(categorias_asignadas, orient='index', columns=['Categoría'])
    ruta_resultados_clasificacion = "resultados/resultados_clasificacion.csv"
    datos.guardar_resultados_csv(resultados_clasificacion, ruta_resultados_clasificacion)

    # 7. Finalmente, podemos visualizar los resultados en un mapa utilizando la función de visualización de mapa.py.
    mapa.visualizar_resultados(df.index.tolist(), prioridad_global, categoria)

if __name__ == "__main__":
    ahpsort_ii()