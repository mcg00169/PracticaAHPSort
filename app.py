import ahp, ahpsort, datos, mapa, prioridades
import numpy as np

def ahpsort_ii():
    # 1. Lee los datos necesarios desde un archivo Excel utilizando la función leer_datos_excel de datos.py.
    ruta_archivo = "datos/datos.xlsx"  # Cambia esto a la ruta de tu archivo Excel
    df = datos.leer_datos_excel(ruta_archivo)
    if df is None:
        print("No se pudieron leer los datos. Asegúrate de que el archivo existe y tiene el formato correcto.")
        return
    # Muestra los criterios y alternativas leídos del archivo Excel
    print("Criterios:", df.columns.tolist())
    print("Alternativas:", df.index.tolist())


    # 2. Define los pesos de los criterios y subcriterios utilizando la función calcular_pesos de ahp.py.
    matriz_comparacion = np.array([[1, 5, 3, 7, 3], 
                                   [0.2, 1, 3, 0.5, 0.25], 
                                   [0.333, 0.333, 1, 0.2, 0.2],
                                   [0.143, 2, 5, 1, 0.2],
                                   [0.3, 4, 5, 5, 1]])  # Ejemplo de matriz de comparación
    pesos = ahp.calcular_pesos(matriz_comparacion)
    ratios_consistencia = ahp.calcular_CR(matriz_comparacion)

    print("Pesos de los criterios:", pesos)
    print("Ratio de consistencia (CR):", ratios_consistencia)

    # 3. Calcula las prioridades locales para cada alternativa y criterio utilizando la función prioridad_local de prioridades.py.
    puntos_x = [0, 1, 2, 3]
    puntos_y = [0, 0.5, 0.75, 1]  # Ejemplo de prioridades correspondientes a los puntos de corte
    valores = df.values.flatten()  # Suponiendo que los valores están en el DataFrame
    prioridades_locales = [prioridades.prioridad_local(valor, puntos_x, puntos_y) for valor in valores]
    print(f"Prioridades locales: {prioridades_locales}")

    # 4. Una vez obtenidos los pesos y las prioridades locales, calcula la prioridad global para cada alternativa utilizando la función prioridad_global de ahpsort.py.
    prioridad_global = ahpsort.prioridad_global(prioridades_locales, pesos)
    print(f"Prioridad global: {prioridad_global}")

    # 5. Clasificamos las alternativas en categorías según los umbrales definidos utilizando la función clasificar de ahpsort.py.
    umbrales = [("Bajo", 0, 0.4), ("Medio", 0.4, 0.7), ("Alto", 0.7, 1)]
    categoria = ahpsort.clasificar(prioridad_global, umbrales)
    print(f"Categoría asignada: {categoria}")

    # 6. Finalmente, podemos visualizar los resultados en un mapa utilizando la función de visualización de mapa.py.
    mapa.visualizar_resultados(df.index.tolist(), prioridad_global, categoria)

if __name__ == "__main__":
    ahpsort_ii()