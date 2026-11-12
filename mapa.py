import geopandas as gpd
import matplotlib.pyplot as plt
# Método para mostrar el mapa de la región de estudio a partir de un archivo shapefile
def mostrar_mapa_shapefile(ruta_shapefile, categorias):
    """
    Muestra un mapa de la región de estudio a partir de un archivo shapefile.
    
    :param ruta_shapefile: Ruta del archivo shapefile a leer.
    :param categorias: Lista de categorías para colorear las geometrías.
    """
    try:
        # Leer el archivo shapefile usando geopandas
        gdf = gpd.read_file(ruta_shapefile)

        # Buscar las etiquetas de las categorías en el GeoDataFrame y asignar colores
        for categoria in categorias:
            if categoria not in gdf.columns:
                print(f"Advertencia: La categoría '{categoria}' no se encuentra en el GeoDataFrame.")
                continue
            # Asignar un color a cada categoría (puedes personalizar los colores según tus necesidades)
            gdf[categoria] = gdf[categoria].astype(str)  # Asegurarse de que la columna sea de tipo string
            gdf[categoria] = gdf[categoria].map({
                'Bajo': 'red',
                'Medio': 'yellow',
                'Alto': 'green'
            }).fillna('lightblue')  # Color por defecto si no coincide con ninguna categoría

        # Crear la figura y el eje para el mapa
        fig, ax = plt.subplots(figsize=(10, 10))

        # Mostrar el mapa
        gdf.plot(ax=ax, color='lightblue', edgecolor='black')
        plt.show()

        # Guardar el mapa en un archivo PNG
        ruta_salida = "resultados/mapa_prioridades.png"
        plt.savefig(ruta_salida, dpi=300)
        
    except Exception as e:
        print(f"Error al mostrar el mapa: {e}")