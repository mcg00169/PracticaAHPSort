import unicodedata

import geopandas as gpd
import matplotlib.pyplot as plt


def _normalizar_nombre(valor):
    sin_tildes = unicodedata.normalize("NFKD", str(valor))
    return "".join(caracter for caracter in sin_tildes if not unicodedata.combining(caracter)).strip().casefold()


# Método para mostrar el mapa de la región de estudio a partir de un archivo shapefile
def mostrar_mapa_shapefile(ruta_shapefile, categorias, ruta_salida):
    """
    Muestra un mapa de la región de estudio a partir de un archivo shapefile.
    
    :param ruta_shapefile: Ruta del archivo shapefile a leer.
    :param categorias: Diccionario que relaciona el nombre de cada provincia
        con su categoría.
    """
    try:
        # Leer el archivo shapefile usando geopandas
        gdf = gpd.read_file(ruta_shapefile)
        columna_provincia = "PROVINCIA"
        if columna_provincia not in gdf.columns:
            raise ValueError(
                f"El shapefile no contiene la columna '{columna_provincia}'. "
                f"Columnas disponibles: {list(gdf.columns)}"
            )

        categorias_por_provincia = {
            _normalizar_nombre(provincia): _normalizar_nombre(categoria)
            for provincia, categoria in categorias.items()
        }
        categoria_por_fila = gdf[columna_provincia].map(
            lambda provincia: categorias_por_provincia.get(_normalizar_nombre(provincia))
        )
        colores = categoria_por_fila.map({
            "bajo": "red",
            "medio": "yellow",
            "alto": "green",
        }).fillna("lightblue")
        provincias_sin_categoria = gdf.loc[categoria_por_fila.isna(), columna_provincia].tolist()
        if provincias_sin_categoria:
            print(f"Advertencia: No hay categoría para estas provincias: {provincias_sin_categoria}")

        # Crear la figura y el eje para el mapa
        fig, ax = plt.subplots(figsize=(10, 10))

        # Mostrar el mapa
        gdf.plot(ax=ax, color=colores, edgecolor='black')

        # Guardar el mapa en un archivo PNG
        plt.savefig(ruta_salida, dpi=300)
        plt.show()
        
    except Exception as e:
        print(f"Error al mostrar el mapa: {e}")