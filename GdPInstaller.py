# GdP Installer - Creado por Santiago Cano Muélledes

# Importación de librerías
import os
import logging
logging.basicConfig(filename=os.path.join(os.path.join(os.path.expanduser("~"), "Desktop"), "latest.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s"))
import tkinter as tk
import ctypes
from ctypes import wintypes
import sys
import subprocess
import urllib.request
import zipfile
import psutil

# Definición de variables clave
carpeta_cache = os.path.join(os.path.expanduser("~"), "Downloads", "cache_gdp")
os.makedirs(carpeta_cache, exist_ok=True)
mcpremium = False

# Definición de funciones
def configurar_laucher(launcher, url_launcher, carpeta_launcher):
    logging.info(f"Comenzando proceso de descarga de {launcher}...")
    urllib.request.urlretrieve(url_launcher, os.path.join(carpeta_cache, f"{launcher}.zip"))
    logging.info("Descarga finalizada con éxito")

    logging.info(f"Comenzando proceso de descompresión de {launcher}...")
    with zipfile.ZipFile(os.path.join(carpeta_cache, f"{launcher}.zip"), "r") as zip_ref:
        zip_ref.extractall(os.path.join(os.path.expanduser("~"), "Desktop", carpeta_launcher))
    logging.info("Descompresión finalizada con éxito")

    ram_minecraft = psutil.virtual_memory().total / 2097152

    logging.info("Comenzando proceso de personalización de la RAM...")
    with open(os.path.join(os.path.expanduser("~"), "Desktop", carpeta_launcher, f"{launcher}.cfg"), "r+") as mod_config:
        lineas = mod_config.readlines()
        for i, linea in enumerate(lineas):
            if linea.startswith('MaxMemAlloc'):
                lineas[i] = f'MaxMemAlloc={ram_minecraft:.0f}\n'
            elif linea.startswith('MinMemAlloc'):
                lineas[i] = f'MinMemAlloc={ram_minecraft:.0f}\n'

        mod_config.seek(0)
        mod_config.writelines(lineas)
        mod_config.truncate()
    logging.info("Personalización de la RAM finalizada con éxito")

def crear_acceso(target_path, shortcut_path):
    shell_link = ctypes.CoCreateInstance(
        wintypes.CLSID_ShellLink, None, wintypes.CLSCTX_INPROC_SERVER, wintypes.IID_IShellLink
    )

    shell_link.SetPath(target_path)

    persist_file = shell_link.QueryInterface(wintypes.IID_IPersistFile)
    persist_file.Save(shortcut_path, True)

# Inicio del programa
# Saludo al usuario y espera a confirmación para continuar
logging.info("Inicialización del programa")

logging.info("Comenzando proceso de saludo y espera a confirmación...")

menu_bienvenida = tk.Tk()
menu_bienvenida.geometry("500x80")
menu_bienvenida.title("GdP Installer")

tk.Label(menu_bienvenida, text="¡Bienvenido a GdP Installer! Cuando desee comenzar con la instalación, pulse 'Continuar'").pack(pady=10)
tk.Button(menu_bienvenida, text="Continuar", command=lambda: menu_bienvenida.destroy()).pack()

logging.info("Menú de bienvenida mostrado con éxito")
menu_bienvenida.mainloop()

# Determinación de privilegios de administrador
logging.info("Comenzando proceso de determinación de privilegios de administrador...")

try:
    admin = os.getuid() == 0
except AttributeError:
    admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if admin:
    logging.info("Privilegios de administrador detectados con éxito")
else:
    menu_noadmin = tk.Tk()
    menu_noadmin.geometry("400x90")
    menu_noadmin.title("GdP Installer")

    tk.Label(menu_noadmin, text="El programa no puede continuar al carecer de permisos de administrador").pack(pady=10)
    tk.Label(menu_noadmin, text="Por favor, vuélvalo a intentar con los permisos necesarios").pack(pady=10)

    logging.error("Privilegios de administrador no detectados")
    menu_noadmin.mainloop()

    logging.error("Error fatal. Forzada finalización del programa")
    sys.exit()

# Búsqueda y desinstalación de todas las versiones de Java 8 en el sistema
logging.info("Comenzando proceso de desinstalación de cualquier instancia de Java 8...")

try:
    subprocess.check_call(["wmic", "product", "where", "name like '%IBM Semeru%' and name like '%8u%'", "call", "uninstall", "/nointeractive"])
    logging.info("Proceso finalizado con éxito")
except subprocess.CalledProcessError:
    logging.error("Fallo en el proceso de desinstalación")

#Instalación de la última versión de Java 8
logging.info("Comenzando proceso de instalación de la última versión de Java 8...")

instalador_java = os.path.join(carpeta_cache, "ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi")
urllib.request.urlretrieve("https://github.com/ibmruntimes/semeru8-binaries/releases/download/jdk8u362-b09_openj9-0.36.0/ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi", instalador_java)

try:
    subprocess.run(["msiexec.exe", "/i", instalador_java, "/qn"], check=True)
    logging.info("Instalación completada con éxito")
except subprocess.CalledProcessError:
    logging.error("Fallo en el proceso de desinstalación")

# Pregunta para dividir usuarios premium y no premium
logging.info("Comenzando proceso de pregunta sobre la posesión de Minecraft: Java Edition...")

menu_preguntamc = tk.Tk()
menu_preguntamc.geometry("300x90")
menu_preguntamc.title("GdP Installer")

tk.Label(menu_preguntamc, text="¿Actualmente posee Minecraft: Java Edition?").pack(pady=10)

marco_botones = tk.Frame(menu_preguntamc)
marco_botones.pack()

tk.Button(marco_botones, text="Sí", command=lambda: (mcpremium.set(True), menu_preguntamc.destroy(), logging.info("Respuesta afirmativa"))).pack(side=tk.LEFT, padx=10)
tk.Button(marco_botones, text="No", command=lambda: (menu_preguntamc.destroy(), logging.info("Respuesta negativa"))).pack(side=tk.LEFT, padx=10)

logging.info("Pregunta formulada con éxito")
menu_preguntamc.mainloop()

# Selección de acciones según respuesta
logging.info("Comenzando proceso de configuración del launcher...")

if mcpremium:
    configurar_laucher("MultiMC", "https://files.multimc.org/downloads/mmc-develop-win32.zip", os.path.join(os.path.expanduser("~"), "Desktop", "MultiMC"))
    crear_acceso(os.path.join(os.path.expanduser("~"), "Desktop", "MultiMC", "MultiMC.exe"), os.path.join(os.path.expanduser("~"), "Desktop", "MultiMC.lnk"))
else:
    configurar_laucher("UltimMC", "https://nightly.link/UltimMC/Launcher/workflows/main/develop/mmc-cracked-win32.zip", os.path.join(os.path.expanduser("~"), "Desktop", "UltimMC"))
    crear_acceso(os.path.join(os.path.expanduser("~"), "Desktop", "MultiMC", "UltimMC.exe"), os.path.join(os.path.expanduser("~"), "Desktop", "UltimMC.lnk"))

# Eliminación de la carpeta caché
logging.info("Comenzando proceso de eliminación de la carpeta caché...")

for root, dirs, files in os.walk(carpeta_cache, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(carpeta_cache)

# Fin del programa
