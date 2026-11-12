import numpy as np
# Método que, dado un valor y puntos de corte, devuelva la prioridad local
def prioridad_local(valor, puntos_x, puntos_y):
    """
    Calcula la prioridad local de un valor dado utilizando interpolación lineal.
    
    :param valor: Valor para el cual se desea calcular la prioridad local.
    :param puntos_x: Lista de puntos de corte en el eje x (valores).
    :param puntos_y: Lista de prioridades correspondientes a los puntos de corte.
    :return: Prioridad local calculada mediante interpolación lineal.
    """
    if np.ndim(valor) != 0:
        raise ValueError("valor debe ser un único número.")

    puntos_x = np.asarray(puntos_x, dtype=float)
    puntos_y = np.asarray(puntos_y, dtype=float)
    if puntos_x.ndim != 1 or puntos_y.ndim != 1:
        raise ValueError("puntos_x y puntos_y deben ser listas unidimensionales.")
    if puntos_x.size == 0 or puntos_x.size != puntos_y.size:
        raise ValueError("puntos_x y puntos_y deben tener la misma cantidad de elementos y no estar vacíos.")

    # Ordenar los puntos de corte y sus prioridades correspondientes.
    sorted_indices = np.argsort(puntos_x)
    puntos_x = puntos_x[sorted_indices]
    puntos_y = puntos_y[sorted_indices]

    # Interpolación lineal
    if valor <= puntos_x[0]:
        return puntos_y[0]
    elif valor >= puntos_x[-1]:
        return puntos_y[-1]
    else:
        return np.interp(valor, puntos_x, puntos_y)