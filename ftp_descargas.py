import ftputil
import os
import time

# Recordatorio: Configurar ruta para la dirección local de 'config.txt'

CONFIG_FILE = 'config.txt'
DOWNLOAD_LOG = 'download_log_{}.txt'  # Usar {} para reemplazar el usuario

def read_config():
    # Leer la configuración desde el archivo de configuración
    with open(CONFIG_FILE, 'r') as config_file:
        config = config_file.readlines()
    return config

def is_scene_registered(scene_name, downloaded_scenes):
    # Verifica si la escena está registrada en el archivo de registro
    return any(scene_name in line for line in downloaded_scenes)

def check_and_download_file(host, remote_file, local_file, ftp_user, downloaded_scenes):
    # Verifica si el archivo local existe y su tamaño es igual al remoto
    if os.path.exists(local_file) and os.path.getsize(local_file) == host.path.getsize(remote_file):
        print(f"{time.strftime('%Y%m%d')} {remote_file} {ftp_user} Archivo ya descargado")
        return False  # No es necesario descargar el archivo si ya existe y está completo

    # Verifica si la escena ya está en el archivo de registro
    if is_scene_registered(remote_file, downloaded_scenes):
        print(f"{time.strftime('%Y%m%d')} {remote_file} {ftp_user} Escena ya registrada en el archivo de registro")
        return False  # No es necesario descargar la escena si ya está registrada

    try:
        # Intenta descargar el archivo
        host.download(remote_file, local_file)
        with open(DOWNLOAD_LOG, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y%m%d')} {remote_file} {ftp_user} Descarga exitosa\n")
        print(f"{time.strftime('%Y%m%d')} {remote_file} {ftp_user} Descarga exitosa")
        return True
    except Exception as e:
        # Registra las descargas fallidas en el log
        with open(DOWNLOAD_LOG, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y%m%d')} {remote_file} {ftp_user} Descarga fallida: {e}\n")
        print(f"{time.strftime('%Y%m%d')} {remote_file} {ftp_user} Descarga fallida: {e}")
        return False

def download_folder(ftp_host, ftp_user, ftp_pass, remote_dir, local_dir, downloaded_scenes):
    # Establecer conexión FTP usando ftputil
    with ftputil.FTPHost(ftp_host, ftp_user, ftp_pass) as host:
        host.chdir(remote_dir)  # Cambia el directorio remoto al especificado
        remote_items = host.listdir(host.curdir)  # Lista los elementos en el directorio remoto
        for item in remote_items:
            if host.path.isdir(item):
                remote_scene = os.path.join(remote_dir, item)
                # Verifica si la escena ya está registrada en el archivo de registro
                if is_scene_registered(remote_scene, downloaded_scenes):
                    print(f"{time.strftime('%Y%m%d')} {remote_scene} {ftp_user} Escena ya registrada en el archivo de registro")
                else:
                    # Descarga las carpetas recursivamente
                    local_subdir = os.path.join(local_dir, item)  # Obtiene la ruta completa del subdirectorio local
                    if not os.path.exists(local_subdir):
                        os.makedirs(local_subdir)
                    download_folder(ftp_host, ftp_user, ftp_pass, remote_scene, local_subdir, downloaded_scenes)  # Recursivamente descarga subdirectorios
            else:
                remote_file = host.path.join(remote_dir, item)  # Obtiene la ruta completa del archivo remoto
                local_file = os.path.join(local_dir, item)  # Obtiene la ruta completa del archivo local

                # Verifica si el archivo local existe y su tamaño es igual al remoto
                if check_and_download_file(host, remote_file, local_file, ftp_user, downloaded_scenes):
                    downloaded_scenes.add(remote_file)

def main():
    config = read_config()
    server = config[0].strip()
    username = config[1].strip()
    password = config[2].strip()
    remote_dir = '/'
    local_dir = os.path.join(r'C:/Users/FTP_Automation', 'Descargas', username)  # Asignar ruta correspondiente para las descargas
    latency = int(config[5].strip())

    # Leer el contenido actual del archivo de registro
    downloaded_scenes = set()
    if os.path.exists(DOWNLOAD_LOG):
        with open(DOWNLOAD_LOG, 'r') as log_file:
            lines = log_file.readlines()
            for line in lines:
                parts = line.split()
                if len(parts) >= 3 and "Descarga exitosa" in line:
                    scene = parts[1]
                    downloaded_scenes.add(scene)

    while True:
        download_folder(server, username, password, remote_dir, local_dir, downloaded_scenes)
        last_download_time = time.time()  # Registra la hora de la última descarga completa
        time.sleep(latency)

        # Verifica si ha pasado suficiente tiempo para una nueva verificación de descargas
        if time.time() - last_download_time >= latency:
            print("Verificando nuevas descargas...")
            # Lógica para verificar nuevas descargas y descargar si es necesario

            # Actualizar la lista de escenas descargadas
            downloaded_scenes = set()
            if os.path.exists(DOWNLOAD_LOG):
                with open(DOWNLOAD_LOG, 'r') as log_file:
                    lines = log_file.readlines()
                    for line in lines:
                        parts = line.split()
                        if len(parts) >= 3 and "Descarga exitosa" in line:
                            scene = parts[1]
                            downloaded_scenes.add(scene)

if __name__ == "__main__":
    main()
