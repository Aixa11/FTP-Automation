## Reporte Técnico: Script de Descargas de Escenas

- Fecha: [5/6/23]

**Resumen**

_El presente reporte técnico describe el funcionamiento y la implementación de un script de descarga de escenas desde un servidor FTP. El script utiliza la biblioteca ftputil de Python para establecer conexión con el servidor FTP, autenticarse, navegar por el directorio de descarga y descargar los archivos especificados._

_El script lee la configuración desde un archivo config.ini, donde se almacenan las credenciales de acceso al servidor FTP y la carpeta de descarga. Luego, utiliza estas configuraciones para conectarse al servidor FTP, obtener la lista de archivos en el directorio y descargar aquellos que cumplen con ciertos criterios (por ejemplo, archivos con una extensión específica).

_Ademas, Recorre los directorios remotos, descarga archivos y verifica la integridad de las descargas. Tambien, registra los resultados en un archivo de log, es capaz de reanudar descargas interrumpidas y muestra un mensaje al completar todas las descargas en un ciclo. El código proporciona una solución para la automatización de descargas FTP._

**Funcionamiento** 

El objetivo principal del script es automatizar la descarga de archivos y carpetas desde un servidor FTP remoto a un directorio local específico. Además, el script realiza un seguimiento de las descargas exitosas y registra estas operaciones en un archivo de registro llamado 'download_log_{}.txt'.

1. Verificación de Descargas Previas (check_and_download_file): Antes de iniciar una descarga, el script utiliza la función check_and_download_file para verificar si un archivo ya ha sido descargado previamente. Esta función verifica si el archivo local existe y si su tamaño es igual al del archivo remoto antes de decidir si debe o no descargarlo nuevamente.

2. Registro de Descargas (check_and_download_file y download_folder): Cada vez que se completa una descarga exitosa, la función check_and_download_file registra la operación en el archivo 'download_log_Aixa.txt'. Además, la función download_folder utiliza esta función para registrar carpetas descargadas y subcarpetas de manera recursiva. El registro incluye la fecha, nombre del archivo o carpeta, usuario y estado (Descarga exitosa o Descarga fallida).

3. Descarga de Carpetas Recursivas (download_folder): El script utiliza la función download_folder para descargar carpetas y subcarpetas de manera recursiva desde el servidor FTP. Esto se logra al pasar el directorio remoto y local como argumentos, lo que permite gestionar la descarga de conjuntos de datos organizados en estructuras de carpetas complejas.

4. Verificación de Nuevas Descargas (main): El script realiza verificaciones periódicas de nuevas descargas utilizando la función main. Esta función compara la hora de la última descarga completa con el tiempo actual y, si ha pasado suficiente tiempo, inicia la verificación de nuevas descargas. Esto se hace para garantizar que las descargas se mantengan actualizadas y se evite descargar archivos o carpetas innecesariamente.

**Ejecución**

_Requisitos Previos_

1. Asegúrate de tener instalada la librería ftputil. Puedes instalarla usando el comando: 
```
pip install ftputil.

```
_Configuración_

1. Crea un archivo config.txt con la configuración necesaria. Incluye los detalles del servidor FTP, las credenciales, los directorios locales y otros parámetros requeridos.
2. Asegúrate de que los directorios locales existan y sean accesibles.

_Ejecución_

1. Ejecuta el script Python utilizando el intérprete adecuado.
2. El script se conectará al servidor FTP, descargará nuevas carpetas y archivos, y registrará las descargas exitosas y fallidas en download_log.txt.
3. Después de completar todas las descargas disponibles, el script esperará según el valor de latencia especificado antes de verificar nuevamente.

_Automatización_

Para automatizar la ejecución del script, se puede configurar un scheduler en el sistema operativo que ejecute el script a intervalos regulares, según la latencia definida en la configuración.

**Conclusión**
Este informe técnico ha detallado la implementación y funcionamiento del script de automatización de descargas desde un servidor FTP. El script cumple con los requisitos específicos, permitiendo la descarga automática y el registro de archivos y carpetas desde el servidor FTP, y la verificación automática de nuevas descargas en intervalos regulares. Su despliegue puede realizarse mediante la ejecución manual o la automatización a través de un scheduler en el sistema operativo.

**Mejoras Futuras**
Para mejorar el script de descarga de escenas FTP, se pueden considerar las siguientes implementaciones:

*Gestión de errores más detallada*: Mejorar la gestión de errores para proporcionar mensajes más descriptivos y capturar posibles excepciones durante la ejecución.

*Personalización de criterios de descarga*: Permitir la configuración de criterios adicionales para la descarga de archivos, como filtrado por fecha, tamaño o nombre.

*Interfaz de usuario (UI) o línea de comandos (CLI)*: Desarrollar una interfaz de usuario intuitiva o una interfaz de línea de comandos para facilitar la interacción y personalización del script.

*Gestión de archivos duplicados*: Implementar una verificación adicional para evitar la descarga de archivos duplicados o manejarlos de manera adecuada.

*Programación avanzada*: Agregar la capacidad de programar descargas en momentos específicos del día o en días específicos de la semana.

**Referencias**
Documentación de Python: https://docs.python.org/
Documentación de ftplib: https://docs.python.org/3/library/ftplib.html