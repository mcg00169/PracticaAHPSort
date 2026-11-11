import numpy as np
# Método para calcular la prioridad global a partir de las prioridades locales y los pesos de los criterios
def prioridad_global(prioridades_locales, pesos_criterios):
    """
    Calcula la prioridad global a partir de las prioridades locales y los pesos de los criterios.
    
    :param prioridades_locales: Lista de prioridades locales para cada criterio.
    :param pesos_criterios: Lista de pesos de los criterios.
    :return: Prioridad global calculada como la suma ponderada de las prioridades locales.
    """
    # Convertir listas a arrays de numpy para facilitar el cálculo
    prioridades_locales = np.array(prioridades_locales)
    pesos_criterios = np.array(pesos_criterios)

    # Calcular la prioridad global como la suma ponderada
    prioridad_global = np.sum(prioridades_locales * pesos_criterios)
    
    return prioridad_global


# Método para clasificar los valores de prioridad global en categorías (por ejemplo, baja, media, alta)
def clasificar(prioridad, umbrales):
    """
    Clasifica un valor de prioridad global en categorías según los umbrales definidos.
    
    :param prioridad: Valor de prioridad global a clasificar.
    :param umbrales: Lista de tuplas (categoria, min, max) que definen los rangos de clasificación.
    :return: Categoría correspondiente al valor de prioridad global.
    """
    for categoria, min_val, max_val in umbrales:
        if min_val <= prioridad < max_val:
            return categoria
    return "No clasificado"  # Si no cae en ningún rango definido