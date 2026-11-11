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