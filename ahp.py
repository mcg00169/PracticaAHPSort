import numpy as np

# Método para calcular los pesos de los criterios y subcriterios utilizando el método AHP
def calcular_pesos(matriz_comparacion):
    """
    Calcula los pesos de los criterios y subcriterios a partir de una matriz de comparación.
    
    :param matriz_comparacion: Matriz de comparación de criterios o subcriterios.
    :return: Vector de pesos normalizados.
    """
    # Calcula el autovector principal (eigenvector) y el autovalor máximo (eigenvalue) de la matriz de comparación
    eigenvalues, eigenvector = np.linalg.eig(matriz_comparacion)

    idx = np.argmax(eigenvalues.real)
    lambda_max = eigenvalues[idx].real

    # Normaliza el autovector para obtener los pesos
    pesos = eigenvector[:, idx].real
    pesos_normalizados = pesos / pesos.sum()

    return pesos_normalizados




# Método para calcular la ratio de consistencia (CR) de la matriz de comparación
def calcular_CR(matriz_comparacion):
    """
    Calcula la ratio de consistencia (CR) de una matriz de comparación.
    
    :param matriz_comparacion: Matriz de comparación de criterios o subcriterios.
    :return: Ratio de consistencia (CR).
    """
    n = matriz_comparacion.shape[0]
    eigenvalues, _ = np.linalg.eig(matriz_comparacion)
    lambda_max = np.max(eigenvalues.real)

    # Calcula el índice de consistencia (CI)
    CI = (lambda_max - n) / (n - 1)

    # Valores de RI (Random Index) para matrices de tamaño 1 a 10
    RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
               6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

    RI = RI_dict.get(n, None)
    if RI is None:
        raise ValueError("No hay un valor de RI definido para matrices de tamaño mayor a 10.")

    # Calcula la ratio de consistencia (CR)
    CR = CI / RI
    return CR