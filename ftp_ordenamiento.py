import os
import json
import glob
import datetime
import shutil
import xml.etree.ElementTree as ET

# Define los directorios de origen y destino
src_dir = "C:/Users/Username/Descargas/user_0000" #modificar
dest_dir_root = "C:/Users/Username/Grupos" #modificar 

# Lee el archivo de configuración de ordenamiento
with open("config_ordenamiento.json", "r") as f:
    config_data = json.load(f)

# Accede a la sección "Stacks" del archivo JSON
stacks_config = config_data.get("Stacks", [])

# Abre el archivo de registro en modo de escritura
log_file = open("log_ordenamiento.log", "a")

# Define patrones de búsqueda para las palabras clave
stack_keywords = ["OrbitDirection", "Path", "Row", "beamID", "acquiredPols"]

# Función para obtener el identificador de stack
def get_stack_identifier(orbit_direction, path, row, mode, polarization):
    return f"ASC_{orbit_direction}_{path}_{row}_{mode}_{polarization}"

# Función para obtener la ruta de destino
def get_destination_path(stack, dest_dir_root, scene_folder):
    grupo = stack["Grupo"]
    empresa = stack["Empresa"]
    proyecto = stack["Proyecto"]
    stack_identifier = get_stack_identifier(stack["OrbitDirection"], stack["Path"], stack["Row"], stack["polMode"], stack["acquiredPols"])
    return os.path.join(dest_dir_root, grupo, empresa, proyecto, stack_identifier, scene_folder)

# Crea un diccionario para rastrear las carpetas que se moverán a cada destino
folders_to_move = {}

# Busca carpetas en el directorio de origen
for folder in os.listdir(src_dir):
    folder_path = os.path.join(src_dir, folder)

    # Comprueba si es una carpeta y si no ha sido procesada antes
    if os.path.isdir(folder_path) and folder_path not in folders_to_move:
        # Obtén información del archivo .xemt dentro de la carpeta
        xemt_files = glob.glob(os.path.join(folder_path, "*.xemt"))
        zip_files = glob.glob(os.path.join(folder_path, "*.zip"))

        # Si se encuentra al menos un archivo .xemt y un archivo .zip
        if xemt_files and zip_files:
            xemt_file = xemt_files[0]
            zip_file = zip_files[0]

            # Intenta analizar el archivo .xemt como XML y obtener los metadatos relevantes
            try:
                tree = ET.parse(xemt_file)
                root = tree.getroot()

                # Supongamos que el formato XML contiene etiquetas como <OrbitDirection>, <Path>, <Row>, etc.
                # Puedes acceder a estos elementos XML de la siguiente manera:
                orbit_direction = root.find(".//OrbitDirection").text
                path = root.find(".//Path").text
                row = int(root.find(".//Row").text) # Se establece como entero
                mode = root.find(".//polMode").text
                polarization = root.find(".//Polarization").text

                # Itera sobre la lista de objetos JSON en stacks_config
                for stack in stacks_config:
                    if (stack["OrbitDirection"] == orbit_direction and
                        stack["Path"] == path and
                        stack["Row"] == row and
                        stack["polMode"] == mode and
                        stack["acquiredPols"] == polarization):

                        # Obtiene la ruta de destino
                        scene_folder = os.path.basename(folder_path)  # Nombre de la carpeta de la escena
                        dest_path = get_destination_path(stack, dest_dir_root, scene_folder)

                        # Mueve la carpeta completa de la escena a la ubicación de destino
                        shutil.move(folder_path, dest_path)

                        # Registra la acción en el archivo de registro
                        log_file.write(f"{datetime.datetime.now().isoformat()}   {folder}   Movido a {dest_path}\n")

                        # Marca la carpeta como procesada
                        break
                else:
                    # Escribe en el archivo de registro si no se encuentra el stack correspondiente
                    log_file.write(f"{datetime.datetime.now().isoformat()}   {folder}   No tiene Ordenamiento\n")
            except ET.ParseError:
                # Escribe en el archivo de registro si el archivo .xemt no es un XML válido
                log_file.write(f"{datetime.datetime.now().isoformat()}   {folder}   No es un archivo XML válido\n")

# Cierra el archivo de registro
log_file.close()
