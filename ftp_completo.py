import ftplib
import os
import hashlib
import configparser
import json
import shutil
import datetime

config_file = "config.ini"
log_file = "download_log.txt"
sorting_config_file = "config_ordenamiento.json"
sorting_log_file = "ordenamiento_log.txt"

def load_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def update_config(ftp_user, ftp_password, download_folder):
    config = configparser.ConfigParser()
    config.read(config_file)
    config['FTP'] = {'User': ftp_user, 'Password': ftp_password, 'DownloadFolder': download_folder}
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def download_scenes():
    config = load_config()
    ftp_user = config.get('FTP', 'User')
    ftp_password = config.get('FTP', 'Password')
    download_folder = config.get('FTP', 'DownloadFolder')

    try:
        with ftplib.FTP('ftp.example.com') as ftp:  # Reemplaza con la dirección FTP correspondiente
            ftp.login(ftp_user, ftp_password)
            ftp.cwd(download_folder)

            files = ftp.nlst()

            for file_name in files:
                if file_name.endswith('.txt'):  # Cambia la extensión según tus necesidades
                    local_file_path = os.path.join(download_folder, file_name)
                    if not os.path.exists(local_file_path) and not is_already_downloaded(file_name):
                        with open(local_file_path, 'wb') as local_file:
                            ftp.retrbinary('RETR ' + file_name, local_file.write)
                        if verify_download(local_file_path):
                            log_successful_download(file_name, "Descarga exitosa")
                            automate_sorting(local_file_path)
                        else:
                            log_successful_download(file_name, "Descarga fallida")

    except ftplib.all_errors as e:
        print("Error: ", e)

def verify_download(file_path):
    # Verifica la integridad del archivo descargado, por ejemplo, usando CRC
    with open(file_path, 'rb') as file:
        file_hash = hashlib.md5(file.read()).hexdigest()
    # Compara el hash calculado con el hash conocido o almacenado
    # Retorna True si la descarga es exitosa, False en caso contrario

def log_successful_download(file_name, status):
    current_date = datetime.date.today().strftime("%Y%m%d")
    log_entry = f"{current_date}\t{file_name}\tusuario\t{status}"
    with open(log_file, 'a') as log:
        log.write(log_entry + "\n")

# Función para verificar si el archivo ya ha sido descargado
def is_already_downloaded(file_name):
    with open(log_file, 'r') as log:
        for line in log:
            if file_name in line:
                return True  # no lo descarga
    return False  # lo descarga

def load_sorting_config():
    with open(sorting_config_file, 'r') as file:
        sorting_config = json.load(file)
    return sorting_config

def move_scene(scene_path, destination_path):
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    try:
        shutil.move(scene_path, destination_path)
        log_successful_sorting(scene_path, destination_path, "Ordenamiento OK")
    except Exception as e:
        log_successful_sorting(scene_path, destination_path, "Ordenamiento Fallido")

def log_successful_sorting(scene_path, destination_path, status):
    current_datetime = datetime.datetime.now().isoformat()
    log_entry = f"{current_datetime}\t{os.path.basename(scene_path)}\t{destination_path}\t{status}"
    with open(sorting_log_file, 'a') as log:
        log.write(log_entry + "\n")

def automate_sorting(scene_path):
    sorting_config = load_sorting_config()

    scene_metadata = extract_metadata(scene_path)  # Implementa la función para extraer los metadatos de la escena

    for stack in sorting_config['stacks']:
        if metadata_matches(stack, scene_metadata):
            destination_path = build_destination_path(stack)
            move_scene(scene_path, destination_path)
            break

def manual_sorting(scene_path):
    destination_path = input("Ingrese la ruta de destino: ")
    move_scene(scene_path, destination_path)

def metadata_matches(stack, scene_metadata):
    # Implementa la lógica para verificar si los metadatos de la escena coinciden con los del stack
    # Retorna True si hay coincidencia, False en caso contrario

def build_destination_path(stack):
    root_path = stack['root_path']
    company = stack['company']
    project = stack['project']
    stack_id = generate_stack_id(stack)
    destination_path = os.path.join(root_path, company, project, stack_id)
    return destination_path 

def generate_stack_id(stack):
    orbit_direction = stack['orbit_direction']
    path = stack['path']
    row = stack['row']
    mode = stack['mode']
    polarization = stack['polarization']
    stack_id = f"{orbit_direction}_{path}_{row}_{mode}_{polarization}"
    return stack_id

def extract_metadata(scene_path):
    # Implementa la lógica para extraer los metadatos de la escena
    # según el formato de archivo utilizado
    metadata = {}

    # Ejemplo: Suponiendo que los metadatos están en un archivo de texto con el siguiente formato:
    # Línea 1: Nombre de la escena
    # Línea 2: Fecha de adquisición
    # Línea 3: Tipo de sensor

    with open(scene_path, 'r') as file:
        metadata['nombre'] = file.readline().strip()
        metadata['fecha_adquisicion'] = file.readline().strip()
        metadata['tipo_sensor'] = file.readline().strip()

    return metadata

def main():
    # Descarga escenas del FTP
    download_scenes()

    # Ejecución manual del script de ordenamiento
    scene_path = input("Ingrese la ruta de la escena a ordenar manualmente: ")
    manual_sorting(scene_path)

if __name__ == "__main__":
    main()
    
    