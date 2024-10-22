## Reporte Técnico: Script de Ordenamiento de Escenas

- Fecha: [5/6/23]

**Resumen**

_El presente reporte técnico describe el funcionamiento y la implementación de un script de ordenamiento de escenas. Este script tiene como objetivo mover las escenas descargadas desde un directorio común de descarga hacia una ruta de destino predefinida, con el propósito de agruparlas de acuerdo al cliente, proyecto y stack al que pertenecen._

_El script puede ser ejecutado de manera automática o manual, dependiendo de las necesidades del usuario. Para determinar la ruta de destino de una escena en particular, el script compara la información contenida en los metadatos de la escena con un archivo de configuración de ordenamiento._

**Funcionamiento**

Python que se encarga de organizar carpetas en un directorio de origen en función de la información contenida en archivos XML y un archivo de configuración JSON. El script busca coincidencias entre los datos extraídos de los archivos XML y las configuraciones definidas en el archivo JSON y luego mueve las carpetas correspondientes al directorio de destino adecuado

1. Importación de Librerías: El script comienza importando las librerías necesarias, como os, json, glob, datetime, shutil, y xml.etree.ElementTree.

2. Definición de Directorios de Origen y Destino: Se definen los directorios de origen (src_dir) y destino (dest_dir_root). Estos directorios representan las rutas donde se encuentran las carpetas desorganizadas y donde se organizarán, respectivamente.

3. Lectura del Archivo de Configuración: El script carga la configuración desde un archivo JSON llamado config_ordenamiento.json, que se utiliza para definir cómo se deben organizar las carpetas. La sección "Stacks" de este archivo contiene una lista de objetos JSON que representan configuraciones de organización.

4. Apertura del Archivo de Registro: Se abre un archivo de registro (log_ordenamiento.log) en modo de escritura, que se utilizará para registrar las acciones realizadas por el script.

5. Definición de Palabras Clave: Se definen palabras clave (stack_keywords) que se utilizarán más adelante para buscar información relevante en los archivos XML.

6. Funciones Auxiliares:
   1. get_stack_identifier: Esta función genera un identificador de stack basado en ciertos atributos de la configuración.
   2. get_destination_path: Esta función genera la ruta de destino para una carpeta en función de la configuración y el nombre de la carpeta de la escena.

7. Diccionario para Rastrear Carpetas: Se crea un diccionario (folders_to_move) para rastrear las carpetas que se moverán a cada destino. Este diccionario se utiliza para evitar que las mismas carpetas se procesen múltiples veces.

8. Búsqueda de Carpetas en el Directorio de Origen: El script itera sobre las carpetas en el directorio de origen (src_dir) y verifica si cada carpeta es válida y no ha sido procesada antes.

9. Procesamiento de Carpetas:

   Se busca la presencia de archivos .xemt y .zip en la carpeta.
   Se intenta analizar el archivo .xemt como un archivo XML válido para extraer información relevante.
   Se compara la información extraída del archivo XML con la configuración definida en el archivo JSON.
   Si se encuentra una coincidencia en la configuración, se calcula la ruta de destino y se mueve la carpeta completa al directorio correspondiente.

10. Registro de Acciones: Se registran las acciones realizadas por el script en el archivo de registro, incluyendo la fecha y hora de la acción, el nombre de la carpeta y la ubicación de destino.

11. Cierre del Archivo de Registro: Finalmente, el archivo de registro se cierra correctamente.

**Ejecución**
El script puede ser ejecutado de dos maneras:

***Ejecución automática al descargar una escena exitosamente:***

- python:

```
scene_path = "ruta_de_la_escena.txt"  # Reemplaza con la ruta de la escena descargada
automate_sorting(scene_path)
```
En este caso, el script se encargará de realizar el ordenamiento automáticamente al identificar una escena descargada exitosamente. Se buscará una coincidencia entre los metadatos de la escena y los stacks definidos en el archivo de configuración. Si se encuentra una coincidencia, la escena será movida a la ruta de destino correspondiente. En caso de no encontrar coincidencias, se imprimir la escena será movida a la ruta de destino correspondiente. En caso de no encontrar coincidencias, se imprimirá un mensaje de falla.

***Ejecución manual del script de ordenamiento:***

- python:

```
scene_path = "ruta_de_la_escena.txt"  # Reemplaza con la ruta de la escena a ordenar manualmente
manual_sorting(scene_path)
```

En este caso, el usuario podrá ingresar manualmente la ruta de destino para la escena, y el script se encargará de moverla a dicha ruta.

**Reporte de Ejecución**
El script de ordenamiento de escenas proporciona mensajes de impresión que indican el resultado de la ejecución. Los mensajes se muestran en el siguiente formato:

```
[Fecha y hora]    [Ruta de la escena]    [Ruta de destino]    Ordenamiento OK
o
```

```
[Fecha y hora]    [Ruta de la escena]    Ordenamiento Fallido
```

El mensaje "Ordenamiento OK" indica que la escena fue movida exitosamente a la ruta de destino correspondiente. El mensaje "Ordenamiento Fallido" indica que no se encontró una coincidencia en los metadatos de la escena con los stacks definidos en el archivo de configuración.

**Conclusiones**
El script de ordenamiento de escenas proporciona una solución automatizada y manual para organizar las escenas descargadas en un directorio común. Al comparar los metadatos de las escenas con la información de los stacks definidos en el archivo de configuración, el script permite agrupar las escenas según el cliente, proyecto y stack al que pertenecen.

El uso de este script facilita el proceso de gestión y organización de las escenas, asegurando que cada una sea almacenada en la ubicación correcta, lo cual resulta útil para la posterior utilización y análisis de los datos.

**Mejoras Futuras**
Para mejorar el script, se pueden considerar las siguientes implementaciones:

*Validación de los metadatos*: Agregar una validación adicional de los metadatos de las escenas para garantizar que la información sea correcta y completa antes de realizar el ordenamiento.

*Ampliación de los criterios de coincidencia*: Permitir la configuración de criterios adicionales para la coincidencia de metadatos, como rangos de fechas o valores específicos de ciertos atributos.

*Interfaz gráfica de usuario (GUI)*: Desarrollar una interfaz gráfica intuitiva que facilite la interacción con el script y permita realizar el ordenamiento de manera visual y amigable.

*Registro de eventos*: Implementar un sistema de registro de eventos para almacenar un historial de las escenas ordenadas, incluyendo la fecha, la ruta de la escena y la ruta de destino. Esto proporcionaría una trazabilidad completa de las acciones realizadas por el script.

**Referencias**
Biblioteca rasterio: https://rasterio.readthedocs.io/
Documentación de Python: https://docs.python.org/