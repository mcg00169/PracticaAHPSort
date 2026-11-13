# Análisis y clasificación jerárquica de los datos de los crímenes
Este programa consiste en obtener los datos de las prioridades locales y globales, tanto en la parte autonómica como nacional, así como una clasificación del nivel de seguridad según los perfiles centrales de cada nivel de seguridad (**Alto, Medio, Bajo**).
## Procedimiento
Para obtener la clasificación, el programa primero calculará los **pesos** de cada criterio, utilizando el método `np.linalg.eig()` de la librería `numpy` de Python, luego normaliza el autovector para sacar dichos pesos de todos los criterios (Crímenes, Robos, Relacionados con vehículos, Orden público y Drogas).

Después, pasará a recoger los datos de los perfiles centrales **(CP)** y puntos de referencia **(RP)**, así como los datos de las prioridades locales de cada uno.

La función que se encarga de obtener las **prioridades locales** de cada perfil, se llama `prioridades.prioridad_local(rango, puntos_x, puntos_y)`, en donde se pasa cualquier valor y se realiza la **interporlación** de cada uno de los puntos X e Y con ese valor.

Una vez que se obtengan todas las prioridades locales de cada perfil central, pasa a calcular la **prioridad global** mediante la función `ahpsort.prioridad_global(prioridades_locales, pesos)` en donde se calcula la **suma ponderada** de la multiplicación de las prioridades locales por los pesos de cada criterio.

Una vez que obtienen las prioridades globales de cada perfil central, pasa a calcular las prioridades locales de cada **alternativa** (las provincias, sean autonómicas o nacionales), pasando los valores de cada criterio e interpolando los puntos X e Y de cada CP y RP.

Después, calcula las prioridades globales de cada alternativa (provincia), realizando de nuevo la suma ponderada de las prioridades locales con los pesos de los criterios.

Por último, se realiza una **clasificación** de seguridad según el rango de los perfiles centrales (CP) y se guardan dichos resultados en archivos CSV. Estos archivos se guardan en un directorio llamado `resultados`.

Al finalizar el proceso, el programa mostrará un mapa de cada provincia, sea autonómica o nacional, en diversos colores según el nivel de seguridad:
- **Bajo** -> **Rojo**
- **Medio** -> **Amarillo**
- **Alto** -> **Verde**

## Funciones adicionales
- Para mejorar la clasificación, se utiliza un archivo llamado `habitantes.csv`, que permite **normalizar** los datos de los crímenes por cada **10000 habitantes** si los datos proporcionados no están normalizados.
- Para el caso de las prioridades locales, los formatos de los archivos CSV contienen los nombres de los criterios y los valores de los puntos formados en corchetes para que el programa permita **parsear** los puntos X e Y mediante un método privado llamado `_parsear_puntos(valor, columna, criterio)`. Un ejemplo de este formato es la siguiente:
```csv
Categoría,Punto_x,Punto_y
Cat1,[0,0.1,0.2,0.3,0.4],[0.333,0.298,0.122,0.074,0.03]
Cat2,[0,0.1,0.2,0.3,0.4],[0.333,0.298,0.122,0.074,0.03]
```
## Pasos para ejecutar el programa
1. Importante **crear** una carpeta denominada `/resultados`. Si no se crea, el programa no puede guardar los resultados.
2. **No debe** borrar los datos que contiene la carpeta `/datos`, ya que de lo contrario, el programa puede fallar.
3. Para la **muestra de los mapas**, hay que asegurar de tener instaladas las siguientes librerías: `matplotlib` y `geopandas`. Si no se encuentran, hay que instalarlas para que funcione:
```bat
pip install matplotlib
pip install geopandas
```
4. Para el **cálculo** de las prioridades locales y globales, la **lectura** de los datos y el **guardado** de los resultados, hay que tener instaladas las siguientes librerías: `numpy` y `pandas`. Si no se encuentran, hay que instalarlas para que funcionen:
```bat
pip install numpy
pip install pandas
```
5. Cuando esté todo listo, abrir el archivo ejecutable denominado `app.py`.