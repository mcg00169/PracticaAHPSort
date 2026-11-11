import geopandas as gpd
import matplotlib.pyplot as plt
# Método para mostrar el mapa de la región de estudio a partir de un archivo shapefile
def mostrar_mapa_shapefile(ruta_shapefile):
    """
    Muestra un mapa de la región de estudio a partir de un archivo shapefile.
    
    :param ruta_shapefile: Ruta del archivo shapefile a leer.
    """
    try:
        # Leer el archivo shapefile usando geopandas
        gdf = gpd.read_file(ruta_shapefile)
        
        # Crear la figura y el eje para el mapa
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Graficar el GeoDataFrame
        gdf.plot(ax=ax, color='lightblue', edgecolor='black')
        
        # Configurar título y etiquetas
        ax.set_title('Mapa de la Región de Estudio', fontsize=15)
        ax.set_xlabel('Longitud', fontsize=12)
        ax.set_ylabel('Latitud', fontsize=12)
        
        # Mostrar el mapa
        plt.show()
        
    except Exception as e:
        print(f"Error al mostrar el mapa: {e}")