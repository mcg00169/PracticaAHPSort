import ahp, ahpsort, datos, mapa, prioridades
import numpy as np
import pandas as pd

def _parsear_puntos(valor, columna, criterio):
    if not isinstance(valor, str):
        raise ValueError(f"Valor no válido en {columna} para {criterio}: {valor!r}")

    contenido = valor.strip()
    if not (contenido.startswith("[") and contenido.endswith("]")):
        raise ValueError(f"Formato no válido en {columna} para {criterio}: {valor!r}")

    try:
        elementos = contenido[1:-1].split(";")
        return [float(elemento.strip()) for elemento in elementos]
    except ValueError as error:
        raise ValueError(f"Valor no numérico en {columna} para {criterio}: {valor!r}") from error


def ahpsort_ii():
    ## PRIMERA PARTE: Cálculo de prioridades locales y globales para cada alternativa y perfil
    # 1. Lee los datos necesarios desde un archivo CSV utilizando la función leer_datos_csv de datos.py.
    ruta_archivo = "datos/datosAndalucia.csv"  # Cambia esto a la ruta de tu archivo CSV
    df = datos.leer_datos_csv(ruta_archivo)
    if df is None:
        print("No se pudieron leer los datos. Asegúrate de que el archivo existe y tiene el formato correcto.")
        return
    # Muestra los criterios y alternativas leídos del archivo CSV
    columna_alternativas = ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"]
    print(f"Criterios: {df.columns.tolist()}")
    print(f"Alternativas: {columna_alternativas}")
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
    prlocales = datos.leer_datos_csv("datos/prlocales.csv")
    if prlocales is None:
        print("No se pudieron leer los datos de prioridades locales. Asegúrese de que el archivo existe y tiene el formato correcto.")
        return
    puntos_x = [
        _parsear_puntos(fila["Puntos_x"], "Puntos_x", fila["Criterios"])
        for _, fila in prlocales.iterrows()
    ]
    puntos_y = [
        _parsear_puntos(fila["Puntos_y"], "Puntos_y", fila["Criterios"])
        for _, fila in prlocales.iterrows()
    ]
    for criterio, valores_x, valores_y in zip(prlocales["Criterios"], puntos_x, puntos_y):
        if len(valores_x) != len(valores_y):
            raise ValueError(
                f"El criterio {criterio} tiene {len(valores_x)} puntos X y "
                f"{len(valores_y)} puntos Y."
            )
    # Para cada perfil central (CP), calculamos la prioridad local según los puntos de referencia (RF) y los valores de las alternativas
    lista_prioridades = {} # Diccionario para almacenar las prioridades locales de cada criterio y global para cada perfil
    prioridades_locales = []  # Lista para almacenar las prioridades locales de cada criterio
    prioridades_globales = []  # Lista para almacenar las prioridades globales de cada perfil
    prioridades_globales_perfiles = {}
    for i in range(len(vAlto)):
        prioridad = prioridades.prioridad_local(vAlto[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Alto: {prioridades_locales}")
    # Después, se calcula la prioridad global utilizando la función prioridad_global de ahpsort.py, pasando las prioridades locales y los pesos de los criterios como argumentos.
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Alto: {prioridad_global}")
    prioridades_globales_perfiles["Alto"] = prioridad_global
    lista_prioridades["Alto"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Alto en el diccionario de prioridades
    # Repetimos el proceso para los valores de prioridad local de vMedio y vBajo
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vMedio
    for i in range(len(vMedio)):
        prioridad = prioridades.prioridad_local(vMedio[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Medio: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Medio: {prioridad_global}")
    prioridades_globales_perfiles["Medio"] = prioridad_global
    lista_prioridades["Medio"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Medio en el diccionario de prioridades
    # Repetimos el proceso para los valores de prioridad local de vBajo
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vBajo
    for i in range(len(vBajo)):
        prioridad = prioridades.prioridad_local(vBajo[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Bajo: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Bajo: {prioridad_global}")
    prioridades_globales_perfiles["Bajo"] = prioridad_global
    lista_prioridades["Bajo"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Bajo en el diccionario de prioridades
    # Guardamos los resultados en un archivo CSV utilizando la función guardar_resultados_csv de datos.py.
    resultados_cp = pd.DataFrame.from_dict(lista_prioridades, orient='index', columns=[f'Prioridad Local {i+1}' for i in range(len(puntos_x))])
    ruta_resultados = "resultados/resultados_prioridades.csv"
    datos.guardar_resultados_csv(resultados_cp, ruta_resultados)

    # Calculamos ahora las prioridades locales para cada alternativa utilizando la función prioridad_local de prioridades.py, y luego calculamos la prioridad global utilizando la función prioridad_global de ahpsort.py.
    prioridades_locales = []
    prioridades_globales = []
    for i in range(len(columna_alternativas)):
        valores = df.iloc[i].values.flatten().tolist()  # Valores de cada alternativa
        for j in range(len(valores)):
            valor = valores[j]
            prioridad_local = prioridades.prioridad_local(valor, puntos_x[j], puntos_y[j])  # Calculamos la prioridad local para cada alternativa
            prioridades_locales.append(prioridad_local)
        print(f"Prioridades locales para la alternativa {columna_alternativas[i]}: {prioridades_locales}")
        prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
        print(f"Prioridad global para la alternativa {columna_alternativas[i]}: {prioridad_global}")
        prioridades_globales.append(prioridad_global)
        # Reiniciamos la lista de prioridades locales para la siguiente alternativa
        prioridades_locales = []

    # 5. De cada prioridad global calculada para cada alternativa, comparamos con los valores de prioridad global de los perfiles Alto, Medio y Bajo
    # y asignamos la categoría correspondiente a cada alternativa.
    umbrales = [("Bajo", prioridades_globales_perfiles["Bajo"], prioridades_globales_perfiles["Medio"]), ("Medio", prioridades_globales_perfiles["Medio"], prioridades_globales_perfiles["Alto"]), ("Alto", prioridades_globales_perfiles["Alto"], 1)]
    categorias_asignadas = {}
    for i, prioridad_global in enumerate(prioridades_globales):
        categoria = ahpsort.clasificar(prioridad_global, umbrales)
        categorias_asignadas[columna_alternativas[i]] = categoria
    print(f"Categorías asignadas: {categorias_asignadas}")

    # 6. Guardamos la tabla de clasificación en un archivo CSV utilizando la función guardar_resultados_csv de datos.py.
    resultados_clasificacion = pd.DataFrame.from_dict(categorias_asignadas, orient='index', columns=['Categoría'])
    ruta_resultados_clasificacion = "resultados/resultados_clasificacion.csv"
    datos.guardar_resultados_csv(resultados_clasificacion, ruta_resultados_clasificacion)

    # 7. Finalmente, podemos visualizar los resultados en un mapa utilizando la función de visualización de mapa.py.
    mapa.mostrar_mapa_shapefile("datos/da03_provincia.shp", categorias_asignadas, "resultados/mapa_prioridades.png")

    ## SEGUNDA PARTE: Normalización de los datos por habitantes y recálculo de prioridades locales y globales para cada alternativa y perfil
    # 1. Leemos los datos de los habitantes desde un archivo CSV
    datos_habitantes = datos.leer_datos_csv("datos/habitantes.csv")
    if datos_habitantes is None:
        print("No se pudieron leer los datos de los habitantes. Asegúrate de que el archivo existe y tiene el formato correcto.")
        return

    # Obtenemos la lista de provincias y la columna de habitantes
    provincias = datos_habitantes["Ciudad"].tolist()
    habitantes = datos_habitantes["Habitantes"].tolist()

    # Comprobamos cada provincia andaluza con las alternativas y normalizamos los datos por habitantes
    for i, provincia in enumerate(provincias):
        if provincia in columna_alternativas:
            indice_alternativa = columna_alternativas.index(provincia)
            for j in range(len(criterios)):
                valor_original = df.iloc[indice_alternativa, j]
                # Normalizamos el valor por cada 10000 habitantes
                valor_normalizado = (valor_original / habitantes[i]) * 10000
                df.iloc[indice_alternativa, j] = np.int64(valor_normalizado)  # Convertimos a entero para evitar decimales
        else:
            continue  # Si la provincia no está en las alternativas, continuamos con la siguiente

    # Guardamos los datos normalizados en un nuevo archivo CSV
    ruta_datos_normalizados = "resultados/datosAndalucia_normalizados.csv"
    datos.guardar_resultados_csv(df, ruta_datos_normalizados)

    # 2. Leemos los perfiles centrales y puntos de referencia recalculados
    rp2Data = datos.leer_datos_csv("datos/rpAndaluciaRecalculados.csv")
    cp2Data = datos.leer_datos_csv("datos/cpAndaluciaRecalculados.csv")
    if rp2Data is None or cp2Data is None:
            print("No se pudieron leer los datos de RP o CP. Asegúrate de que los archivos existen y tienen el formato correcto.")
            return
    # Almacenamos los valores de los perfiles centrales (CP) de cada criterio en una lista
    valores = cp2Data.values.flatten().tolist()
    vAlto = valores[0:5]
    vMedio = valores[5:10]
    vBajo = valores[10:15]

    # Leemos los datos de las prioridades locales recalculadas
    prlocales2 = datos.leer_datos_csv("datos/prlocales2.csv")
    if prlocales2 is None:
        print("No se pudieron leer los datos de prioridades locales. Asegúrese de que el archivo existe y tiene el formato correcto.")
        return
    puntos_x = [
        _parsear_puntos(fila["Puntos_x"], "Puntos_x", fila["Criterios"])
        for _, fila in prlocales2.iterrows()
    ]
    puntos_y = [
        _parsear_puntos(fila["Puntos_y"], "Puntos_y", fila["Criterios"])
        for _, fila in prlocales2.iterrows()
    ]
    for criterio, valores_x, valores_y in zip(prlocales2["Criterios"], puntos_x, puntos_y):
        if len(valores_x) != len(valores_y):
            raise ValueError(
                f"El criterio {criterio} tiene {len(valores_x)} puntos X y "
                f"{len(valores_y)} puntos Y."
            )
    # Para cada perfil central (CP), calculamos la prioridad local según los puntos de referencia (RF) y los valores de las alternativas
    lista_prioridades = {} # Diccionario para almacenar las prioridades locales de cada criterio y global para cada perfil
    prioridades_locales = []  # Lista para almacenar las prioridades locales de cada criterio
    prioridades_globales = []  # Lista para almacenar las prioridades globales de cada perfil
    prioridades_globales_perfiles = {}
    for i in range(len(vAlto)):
        prioridad = prioridades.prioridad_local(vAlto[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Alto: {prioridades_locales}")
    # Después, se calcula la prioridad global utilizando la función prioridad_global de ahpsort.py, pasando las prioridades locales y los pesos de los criterios como argumentos.
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Alto: {prioridad_global}")
    prioridades_globales_perfiles["Alto"] = prioridad_global
    lista_prioridades["Alto"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Alto en el diccionario de prioridades
    # Repetimos el proceso para los valores de prioridad local de vMedio y vBajo
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vMedio
    for i in range(len(vMedio)):
        prioridad = prioridades.prioridad_local(vMedio[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Medio: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Medio: {prioridad_global}")
    prioridades_globales_perfiles["Medio"] = prioridad_global
    lista_prioridades["Medio"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Medio en el diccionario de prioridades
    # Repetimos el proceso para los valores de prioridad local de vBajo
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vBajo
    for i in range(len(vBajo)):
        prioridad = prioridades.prioridad_local(vBajo[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Bajo: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Bajo: {prioridad_global}")
    prioridades_globales_perfiles["Bajo"] = prioridad_global
    lista_prioridades["Bajo"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Bajo en el diccionario de prioridades
    # Guardamos los resultados en un archivo CSV utilizando la función guardar_resultados_csv de datos.py.
    resultados_cp = pd.DataFrame.from_dict(lista_prioridades, orient='index', columns=[f'Prioridad Local {i+1}' for i in range(len(puntos_x))])
    ruta_resultados = "resultados/resultados_prioridades2.csv"
    datos.guardar_resultados_csv(resultados_cp, ruta_resultados)

    # Calculamos ahora las prioridades locales para cada alternativa utilizando la función prioridad_local de prioridades.py, y luego calculamos la prioridad global utilizando la función prioridad_global de ahpsort.py.
    prioridades_locales = []
    prioridades_globales = []
    for i in range(len(columna_alternativas)):
        valores = df.iloc[i].values.flatten().tolist()  # Valores de cada alternativa
        for j in range(len(valores)):
            valor = valores[j]
            prioridad_local = prioridades.prioridad_local(valor, puntos_x[j], puntos_y[j])  # Calculamos la prioridad local para cada alternativa
            prioridades_locales.append(prioridad_local)
        print(f"Prioridades locales para la alternativa {columna_alternativas[i]}: {prioridades_locales}")
        prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
        print(f"Prioridad global para la alternativa {columna_alternativas[i]}: {prioridad_global}")
        prioridades_globales.append(prioridad_global)
        # Reiniciamos la lista de prioridades locales para la siguiente alternativa
        prioridades_locales = []

    umbrales = [("Bajo", prioridades_globales_perfiles["Bajo"], prioridades_globales_perfiles["Medio"]), ("Medio", prioridades_globales_perfiles["Medio"], prioridades_globales_perfiles["Alto"]), ("Alto", prioridades_globales_perfiles["Alto"], 1)]
    categorias_asignadas = {}
    for i, prioridad_global in enumerate(prioridades_globales):
        categoria = ahpsort.clasificar(prioridad_global, umbrales)
        categorias_asignadas[columna_alternativas[i]] = categoria
    print(f"Categorías asignadas: {categorias_asignadas}")

    # 3. Guardamos los resultados clasificados a través de un archivo CSV
    resultados_clasificacion = pd.DataFrame.from_dict(categorias_asignadas, orient='index', columns=['Categoría'])
    ruta_resultados_clasificacion = "resultados/resultados_clasificacion2.csv"
    datos.guardar_resultados_csv(resultados_clasificacion, ruta_resultados_clasificacion)

    # 4. Visualizamos los nuevos resultados en un mapa utilizando la función de visualización de mapa.py.
    mapa.mostrar_mapa_shapefile("datos/da03_provincia.shp", categorias_asignadas, "resultados/mapa_prioridades2.png")

    ## TERCERA PARTE: Cálculo de prioridades locales y globales para cada alternativa y perfil de los datos nacionales del 2017
    # 1. Leemos los datos nacionales del 2017 por 10000 habitantes desde un archivo CSV utilizando la función leer_datos_csv de datos.py.
    datosNacionales2017 = datos.leer_datos_csv("datos/datosNacionales10000_2017.csv")
    if datosNacionales2017 is None:
        print("No se pudieron leer los datos nacionales. Asegúrate de que el archivo existe y tiene el formato correcto.")
        return
    # 2. Almacenamos también los perfiles centrales (CP) y puntos de referencia (RP) de cada criterio
    rp3Data = datos.leer_datos_csv("datos/rpNacionales2017.csv")
    cp3Data = datos.leer_datos_csv("datos/cpNacionales2017.csv")
    valores = cp3Data.values.flatten().tolist()
    vAlto = valores[0:5]
    vMedio = valores[5:10]
    vBajo = valores[10:15]

    # 3. Leemos los datos de las prioridades locales
    prlocales3 = datos.leer_datos_csv("datos/prlocales3.csv")
    if prlocales3 is None:
        print("No se pudieron leer los datos de prioridades locales. Asegúrese de que el archivo existe y tiene el formato correcto.")
        return
    puntos_x = [
        _parsear_puntos(fila["Puntos_x"], "Puntos_x", fila["Criterios"])
        for _, fila in prlocales3.iterrows()
    ]
    puntos_y = [
        _parsear_puntos(fila["Puntos_y"], "Puntos_y", fila["Criterios"])
        for _, fila in prlocales3.iterrows()
    ]
    for criterio, valores_x, valores_y in zip(prlocales3["Criterios"], puntos_x, puntos_y):
        if len(valores_x) != len(valores_y):
            raise ValueError(
                f"El criterio {criterio} tiene {len(valores_x)} puntos X y "
                f"{len(valores_y)} puntos Y."
            )
    # 4. Calculamos las funciones de prioridad local y obtenemos la global de cada perfil central
    lista_prioridades = {} # Diccionario para almacenar las prioridades locales de cada criterio y global para cada perfil
    prioridades_locales = []  # Lista para almacenar las prioridades locales de cada criterio
    prioridades_globales = []  # Lista para almacenar las prioridades globales de cada perfil
    prioridades_globales_perfiles = {}
    for i in range(len(vAlto)):
        prioridad = prioridades.prioridad_local(vAlto[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Alto: {prioridades_locales}")
    # Después, se calcula la prioridad global utilizando la función prioridad_global de ahpsort.py, pasando las prioridades locales y los pesos de los criterios como argumentos.
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Alto: {prioridad_global}")
    prioridades_globales_perfiles["Alto"] = prioridad_global
    lista_prioridades["Alto"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Alto en el diccionario de prioridades
    # Repetimos el proceso para los valores de prioridad local de vMedio y vBajo
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vMedio
    for i in range(len(vMedio)):
        prioridad = prioridades.prioridad_local(vMedio[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Medio: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Medio: {prioridad_global}")
    prioridades_globales_perfiles["Medio"] = prioridad_global
    lista_prioridades["Medio"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Medio en el diccionario de prioridades
    # Repetimos el proceso para los valores de prioridad local de vBajo
    prioridades_locales = []  # Reiniciamos la lista de prioridades locales para vBajo
    for i in range(len(vBajo)):
        prioridad = prioridades.prioridad_local(vBajo[i], puntos_x[i], puntos_y[i])
        prioridades_locales.append(prioridad)
    print(f"Prioridades locales para el perfil Bajo: {prioridades_locales}")
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global para el perfil Bajo: {prioridad_global}")
    prioridades_globales_perfiles["Bajo"] = prioridad_global
    lista_prioridades["Bajo"] = prioridades_locales  # Guardamos las prioridades locales y globales para el perfil Bajo en el diccionario de prioridades
    # Guardamos los resultados en un archivo CSV utilizando la función guardar_resultados_csv de datos.py.
    resultados_cp = pd.DataFrame.from_dict(lista_prioridades, orient='index', columns=[f'Prioridad Local {i+1}' for i in range(len(puntos_x))])
    ruta_resultados = "resultados/resultados_prioridades3.csv"
    datos.guardar_resultados_csv(resultados_cp, ruta_resultados)

    # 5. Calculamos ahora las prioridades locales de cada provincia española, y luego la prioridad global
    prioridades_locales = []
    prioridades_globales = []
    for i in range(len(provincias) - 2): # Ceuta y Melilla no se incluyen en las prioridades locales y globales
        valores = datosNacionales2017.iloc[i].values.flatten().tolist()  # Valores de cada alternativa
        for j in range(len(valores)):
            valor = valores[j]
            prioridad_local = prioridades.prioridad_local(valor, puntos_x[j], puntos_y[j])  # Calculamos la prioridad local para cada alternativa
            prioridades_locales.append(prioridad_local)
        print(f"Prioridades locales para la alternativa {provincias[i]}: {prioridades_locales}")
        prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
        print(f"Prioridad global para la alternativa {provincias[i]}: {prioridad_global}")
        prioridades_globales.append(prioridad_global)
        # Reiniciamos la lista de prioridades locales para la siguiente alternativa
        prioridades_locales = []

    # Asignamos cada provincia en la categoría correspondiente
    umbrales = [("Bajo", 0, prioridades_globales_perfiles["Bajo"]), ("Medio", prioridades_globales_perfiles["Bajo"], prioridades_globales_perfiles["Medio"]), ("Alto", prioridades_globales_perfiles["Medio"], 1)]
    categorias_asignadas = {}
    for i, prioridad_global in enumerate(prioridades_globales):
        categoria = ahpsort.clasificar(prioridad_global, umbrales)
        categorias_asignadas[provincias[i]] = categoria
    print(f"Categorías asignadas: {categorias_asignadas}")

    # 6. Guardamos los resultados clasificados a través de un archivo CSV
    resultados_clasificacion = pd.DataFrame.from_dict(categorias_asignadas, orient='index', columns=['Categoría'])
    ruta_resultados_clasificacion = "resultados/resultados_clasificacion3.csv"
    datos.guardar_resultados_csv(resultados_clasificacion, ruta_resultados_clasificacion)

    # 7. Visualizamos el mapa y lo guardamos en formato PNG
    mapa.mostrar_mapa_espana_shapefile("datos/recintos_provinciales_inspire_peninbal_etrs89.shp", categorias_asignadas, "resultados/mapa_prioridades3.png")

    ## CUARTA PARTE: Cálculo de prioridades locales y globales para cada alternativa y perfil de los datos nacionales del 2017
    # 1. Leemos los datos nacionales del 2023 por 10000 habitantes desde un archivo CSV utilizando la función leer_datos_csv de datos.py.
    datosNacionales2023 = datos.leer_datos_csv("datos/datosNacionales10000_2023.csv")
    if datosNacionales2023 is None:
        print("No se pudieron leer los datos nacionales. Asegúrate de que el archivo existe y tiene el formato correcto.")
        return
    # Utilizaremos los mismos datos del perfil central y puntos de referencia que hicimos con los datos nacionales del 2017
    # Los datos de la prioridad local de cada perfil central ya están calculadas, con lo que lo único que necesitamos es realizar un truncamiento de RPs
    # y calcular la clasificación de cada provincia de España con los datos del 2023.

    # 2. Calculamos las prioridades locales de cada provincia española, y luego la prioridad global
    prioridades_locales = []
    prioridades_globales = []
    for i in range(len(provincias) - 2): # Ceuta y Melilla no se incluyen en las prioridades locales y globales
        valores = datosNacionales2023.iloc[i].values.flatten().tolist()  # Valores de cada alternativa
        for j in range(len(valores)):
            valor = valores[j]
            prioridad_local = prioridades.prioridad_local(valor, puntos_x[j], puntos_y[j])  # Calculamos la prioridad local para cada alternativa
            prioridades_locales.append(prioridad_local)
        print(f"Prioridades locales para la alternativa {provincias[i]}: {prioridades_locales}")
        prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
        print(f"Prioridad global para la alternativa {provincias[i]}: {prioridad_global}")
        prioridades_globales.append(prioridad_global)
        # Reiniciamos la lista de prioridades locales para la siguiente alternativa
        prioridades_locales = []

    # Asignamos cada provincia en la categoría correspondiente
    umbrales = [("Bajo", 0, prioridades_globales_perfiles["Bajo"]), ("Medio", prioridades_globales_perfiles["Bajo"], prioridades_globales_perfiles["Medio"]), ("Alto", prioridades_globales_perfiles["Medio"], 1)]
    categorias_asignadas = {}
    for i, prioridad_global in enumerate(prioridades_globales):
        categoria = ahpsort.clasificar(prioridad_global, umbrales)
        categorias_asignadas[provincias[i]] = categoria
    print(f"Categorías asignadas: {categorias_asignadas}")

    # 3. Guardamos los resultados clasificados a través de un archivo CSV
    resultados_clasificacion = pd.DataFrame.from_dict(categorias_asignadas, orient='index', columns=['Categoría'])
    ruta_resultados_clasificacion = "resultados/resultados_clasificacion4.csv"
    datos.guardar_resultados_csv(resultados_clasificacion, ruta_resultados_clasificacion)

    # 4. Visualizamos el mapa y lo guardamos en formato PNG
    mapa.mostrar_mapa_espana_shapefile("datos/recintos_provinciales_inspire_peninbal_etrs89.shp", categorias_asignadas, "resultados/mapa_prioridades4.png")
if __name__ == "__main__":
    ahpsort_ii()