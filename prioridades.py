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
    # Asegurarse de que los puntos estén ordenados
    sorted_indices = np.argsort(puntos_x)
    puntos_x = np.array(puntos_x)[sorted_indices]
    puntos_y = np.array(puntos_y)[sorted_indices]

    # Interpolación lineal
    if valor <= puntos_x[0]:
        return puntos_y[0]
    elif valor >= puntos_x[-1]:
        return puntos_y[-1]
    else:
        return np.interp(valor, puntos_x, puntos_y)