# GdP Installer - Creado por Santiago Cano Muélledes

# Creación del fichero caché
import os
carpeta_cache = os.path.join(os.path.expanduser("~"), "Downloads", "cache_gdp")
os.makedirs(carpeta_cache, exist_ok=True)

# Importación de librerías
import logging
logging.basicConfig(filename=os.path.join(carpeta_cache, "latest.log"), level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
import tkinter as tk
import ctypes
from ctypes import wintypes
import sys
import subprocess
import urllib.request
import zipfile
import psutil

# Definición de funciones
def configurar_laucher(launcher, url, carpeta):
    logging.info(f"Comenzando proceso de descarga de {launcher}...")
    urllib.request.urlretrieve(url, os.path.join(carpeta_cache, f"{launcher}.zip"))
    logging.info("Descarga finalizada con éxito")

    logging.info(f"Comenzando proceso de descompresión de {launcher}...")
    with zipfile.ZipFile(os.path.join(carpeta_cache, f"{launcher}.zip"), "r") as zip_ref:
        zip_ref.extractall(carpeta)
    logging.info("Descompresión finalizada con éxito")

    ram_minecraft = psutil.virtual_memory().total / 2097152
    nucleos_cpu = psutil.cpu_count(logical=False)

    logging.info("Comenzando proceso de personalización de la RAM...")
    with open(os.path.join(carpeta, f"{launcher}.cfg"), "r+") as launcher_config:
        lineas = launcher_config.readlines()
        for i, linea in enumerate(lineas):
            if linea.startswith('MaxMemAlloc'):
                lineas[i] = f'MaxMemAlloc={ram_minecraft:.0f}\n'
            elif linea.startswith('MinMemAlloc'):
                lineas[i] = f'MinMemAlloc={ram_minecraft:.0f}\n'

        launcher_config.seek(0)
        launcher_config.writelines(lineas)
        launcher_config.truncate()
    logging.info("Personalización de la RAM finalizada con éxito")

    logging.info("Comenzando proceso de personalización de los núcleos...")
    with open(os.path.join(carpeta, "instances", "GdP-Client", "instance.cfg"), "r+") as instance_config:
        lineas = instance_config.readlines()
        for i, linea in enumerate(lineas):
            if linea.startswith('JvmArgs'):
                lineas[i] = lineas[i] = f'JvmArgs=-d64 -XX:+UseG1GC -Dsun.rmi.dgc.server.gcInterval=2147483646 -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M -XX:+UseStringDeduplication -XX:+UseCompressedOops -XX:+UseCodeCacheFlushing -XX:ParallelGCThreads={nucleos_cpu} -XX:SoftRefLRUPolicyMSPerMB=10000 -XX:ReservedCodeCacheSize=2048m -XX:+OptimizeStringConcat -XX:+AggressiveOpts -XX:+UseBiasedLocking -XX:SurvivorRatio=8 -XX:TargetSurvivorRatio=90 -XX:MaxTenuringThreshold=15 -Dfml.ignorePatchDiscrepancies=true -Dfml.ignoreInvalidMinecraftCertificates=true -XX:+UseFastAccessorMethods -XX:+UseAdaptiveGCBoundary -XX:-UseGCOverheadLimit -XX:+UseNUMA -XX:+CMSParallelRemarkEnabled -XX:MaxTenuringThreshold=15\n'

        instance_config.seek(0)
        instance_config.writelines(lineas)
        instance_config.truncate()
    logging.info("Personalización de los núcleos finalizada con éxito")

def crear_acceso(directorio_diana, directorio_acceso):
    logging.info("Comenzando proceso de creación del acceso directo...")
    shell_link = ctypes.CoCreateInstance(wintypes.CLSID_ShellLink, None, wintypes.CLSCTX_INPROC_SERVER, wintypes.IID_IShellLink)

    shell_link.SetPath(directorio_diana)

    persist_file = shell_link.QueryInterface(wintypes.IID_IPersistFile)
    persist_file.Save(directorio_acceso, True)
    logging.info("Creación del acceso directo finalizado con éxito")

# Inicio del programa
# Saludo al usuario y espera a confirmación para continuar
logging.info("Inicialización del programa")

logging.info("Comenzando proceso de saludo...")

menu_bienvenida = tk.Tk()
menu_bienvenida.geometry("500x80")
menu_bienvenida.title("GdP Installer")

tk.Label(menu_bienvenida, text="¡Bienvenido a GdP Installer! Cuando desee comenzar con la instalación, pulse 'Continuar'").pack(pady=10)
tk.Button(menu_bienvenida, text="Continuar", command=lambda: menu_bienvenida.destroy()).pack()

logging.info("Saludo mostrado con éxito")
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
    logging.error("Desinstalación no realizada")
    logging.error("Error fatal. Forzada finalización del programa")
    sys.exit()

#Instalación de la última versión de Java 8
logging.info("Comenzando proceso de instalación de la última versión de Java 8...")

urllib.request.urlretrieve("https://github.com/ibmruntimes/semeru8-binaries/releases/download/jdk8u372-b07_openj9-0.38.0/ibm-semeru-open-jdk_x64_windows_8u372b07_openj9-0.38.0.msi", os.path.join(carpeta_cache, "Java8.msi"))

try:
    subprocess.run(["msiexec.exe", "/i", os.path.join(carpeta_cache, "Java8.msi"), "/qn"], check=True)
    logging.info("Instalación finalizada con éxito")
except subprocess.CalledProcessError:
    logging.error("Instalación no realizada")
    logging.error("Error fatal. Forzada finalización del programa")
    sys.exit()

# Pregunta para dividir usuarios premium y no premium
logging.info("Comenzando proceso de pregunta sobre la posesión de Minecraft: Java Edition...")

menu_preguntamc = tk.Tk()
menu_preguntamc.geometry("300x90")
menu_preguntamc.title("GdP Installer")

tk.Label(menu_preguntamc, text="¿Actualmente posee Minecraft: Java Edition?").pack(pady=10)

mcpremium = tk.BooleanVar()
mcpremium.set(False)

marco_botones = tk.Frame(menu_preguntamc)
marco_botones.pack()

tk.Button(marco_botones, text="Sí", command=lambda: (mcpremium.set(True), menu_preguntamc.destroy(), logging.info("Respuesta afirmativa"))).pack(side=tk.LEFT, padx=10)
tk.Button(marco_botones, text="No", command=lambda: (menu_preguntamc.destroy(), logging.info("Respuesta negativa"))).pack(side=tk.LEFT, padx=10)

logging.info("Pregunta formulada con éxito")
menu_preguntamc.mainloop()

# Selección de acciones según respuesta
logging.info("Comenzando proceso de configuración del launcher...")

if mcpremium:
    carpeta_launcher = os.path.join(os.path.expanduser("~"), "Desktop", "PolyMC")
    configurar_laucher("PolyMC", "https://github.com/Santiplayer18/GdP/raw/modpack/PrismLauncher.zip", carpeta_launcher)
    crear_acceso(os.path.join(carpeta_launcher, "polymc.exe"), os.path.join(os.path.expanduser("~"), "Desktop", "PolyMC.lnk"))
else:
    carpeta_launcher = os.path.join(os.path.expanduser("~"), "Desktop", "PollyMC")
    configurar_laucher("PollyMC", "https://github.com/Santiplayer18/GdP/raw/modpack/PollyMC.zip", carpeta_launcher)
    crear_acceso(os.path.join(carpeta_launcher, "pollymc.exe"), os.path.join(os.path.expanduser("~"), "Desktop", "PollyMC.lnk"))

logging.info("Configuración del launcher finalizada con éxito")

# Aviso de finalización y pregunta de ejecución de launcher
logging.info("Comenzando proceso de aviso y pregunta sobre ejecución de launcher...")

menu_fin = tk.Tk()
menu_fin.geometry("400x180")
menu_fin.title("GdP Installer")

tk.Label(menu_fin, text="La instalación ha finalizado exitosamente").pack(pady=10)
tk.Label(menu_fin, text="Si lo desea, puede ejecutar directamente el launcher").pack(pady=10)

ejecutarlauncher = tk.BooleanVar()

casilla_verificacion = tk.Checkbutton(menu_fin, text="Ejecutar launcher", variable=ejecutarlauncher)
casilla_verificacion.pack(pady=10)

tk.Button(menu_fin, text="Finalizar", command=lambda: (menu_fin.destroy())).pack()

logging.info("Aviso y pregunta formulados con éxito")
menu_fin.mainloop()

logging.info("Comenzando proceso de ejecución del launcher...")
if ejecutarlauncher.get():
    if mcpremium:
        os.startfile(os.path.join(carpeta_launcher, "polymc.exe"))
        logging.info("Ejecución de PolyMC finalizada con éxito")
    else:
        os.startfile(os.path.join(carpeta_launcher, "pollymc.exe"))
        logging.info("Ejecución de PollyMC finalizada con éxito")

# Eliminación de la carpeta caché
logging.info("Comenzando proceso de eliminación de la carpeta caché...")

for root, dirs, files in os.walk(carpeta_cache, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(carpeta_cache)

# Fin del programa
