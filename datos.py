import pandas as pd
# Método para leer los datos a partir del archivo Excel y convertirlos en un DataFrame de pandas
def leer_datos_excel(ruta_archivo):
    """
    Lee un archivo Excel y devuelve un DataFrame de pandas.
    
    :param ruta_archivo: Ruta del archivo Excel a leer.
    :return: DataFrame con los datos del archivo.
    """
    try:
        df = pd.read_excel(ruta_archivo)
        return df
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return None

# Método para leer los datos a partir del archivo CSV y convertirlos en un DataFrame de pandas
def leer_datos_csv(ruta_archivo):
    """
    Lee un archivo CSV y devuelve un DataFrame de pandas.
    
    :param ruta_archivo: Ruta del archivo CSV a leer.
    :return: DataFrame con los datos del archivo.
    """
    try:
        df = pd.read_csv(ruta_archivo)
        return df
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None

# Método para guardar los resultados en un archivo CSV a partir de un DataFrame de pandas
def guardar_resultados_csv(df, ruta_archivo):
    """
    Guarda un DataFrame de pandas en un archivo CSV.
    
    :param df: DataFrame con los resultados a guardar.
    :param ruta_archivo: Ruta del archivo CSV donde se guardarán los resultados.
    """
    try:
        df.to_csv(ruta_archivo, index=False)
        print(f"Resultados guardados en {ruta_archivo}")
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")