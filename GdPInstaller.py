# GdP Installer - Por Santiplayer18

# Importación de librerías
import logging
logging.basicConfig(filename="latest.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s")

import tkinter as tk
import os
import ctypes
import sys
import urllib.request
import subprocess
import zipfile
import psutil

# Definición de funciones
def respuesta(valor) :
    global mcpremium
    if valor == True :
        mcpremium = True
        logging.info("Respuesta afirmativa")
        menu_preguntamc.destroy()
    else :
        mcpremium = False
        logging.info("Respuesta negativa")
        menu_preguntamc.destroy()

# Saludo al usuario y espera a confirmación para continuar

logging.info("Inicialización del programa")

logging.info("Comenzando proceso de saludo y espera a confirmación...")
menu_bienvenida = tk.Tk()
menu_bienvenida.geometry("500x100")
menu_bienvenida.title("GdP Installer")

texto = tk.Label(menu_bienvenida, text="¡Bienvenido a GdP Installer! Cuando desee comenzar con la instalación, pulse 'Continuar'")
texto.pack(pady=10)

boton = tk.Button(menu_bienvenida, text="Continuar", command=lambda: menu_bienvenida.destroy())
boton.pack(pady=10)

logging.info("Menú de bienvenida mostrado con éxito")
menu_bienvenida.mainloop()

# Determinación de privilegios de administrador del programa

logging.info("Comenzando proceso de determinación de privilegios de administrador...")
try :
 admin = os.getuid() == 0
except AttributeError:
 admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if admin == True:
    logging.info("Privilegios de administrador detectados con éxito")
else :
    menu_noadmin = tk.Tk()
    menu_noadmin.geometry("400x90")
    menu_noadmin.title("GdP Installer")

    texto1 = tk.Label(menu_noadmin, text="El programa no puede continuar al carecer de permisos de administrador")
    texto1.pack(pady=10)

    texto2 = tk.Label(menu_noadmin, text="Por favor, vuélvalo a intentar con los permisos necesarios")
    texto2.pack(pady=10)

    logging.error("Privilegios de administrador no detectados")
    menu_noadmin.mainloop()

    logging.error("Error fatal: forzada finalización del programa")
    sys.exit()

# Búsqueda de todas las versiones de Java 8 en el sistema y desinstalación una a una

logging.info("Comenzando proceso de desinstalación de cualquier instancia de Java 8...")
os.system('wmic product where "name like \'%%IBM Semeru%%\' and name like \'%%8u%%\'" call uninstall /nointeractive')
logging.info("Proceso finalizado con éxito")

# Instalación de la última versión de Java 8

logging.info("Comenzando proceso de instalación de la última versión de Java 8...")
carpeta_cache = os.path.join(os.path.expanduser("~"), "Downloads", "cache_gdp")
os.makedirs(carpeta_cache, exist_ok=True)

urllib.request.urlretrieve("https://github.com/ibmruntimes/semeru8-binaries/releases/download/jdk8u362-b09_openj9-0.36.0/ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi", os.path.join(carpeta_cache, "ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi"))

subprocess.call(["msiexec.exe", "/i", os.path.join(carpeta_cache, "ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi"), "/qn"])
logging.info("Instalación completada con éxito")

# Pregunta para dividir usuarios premium y no premium

logging.info("Comenzando proceso de pregunta sobre la posesión de Minecraft: Java Edition...")
menu_preguntamc = tk.Tk()
menu_preguntamc.geometry("300x90")
menu_preguntamc.title("GdP Installer")

label = tk.Label(menu_preguntamc, text="¿Actualmente posee Minecraft: Java Edition?")
label.pack(pady=10)

frame = tk.Frame(menu_preguntamc)
frame.pack()

button_yes = tk.Button(frame, text="Sí", command=lambda: respuesta(True))
button_yes.pack(side=tk.LEFT, padx=10)

button_no = tk.Button(frame, text="No", command=lambda: respuesta(False))
button_no.pack(side=tk.LEFT, padx=10)

logging.info("Pregunta formulada con éxito")
menu_preguntamc.mainloop()

# Respuesta afirmativa para Minecraft premium

if mcpremium == True :
    logging.info("Comenzando proceso de descarga y descompresión de MultiMC...")
    urllib.request.urlretrieve("https://files.multimc.org/downloads/mmc-develop-win32.zip", os.path.join(carpeta_cache, "mmc-develop-win32.zip"))

    with zipfile.ZipFile(os.path.join(carpeta_cache, "mmc-develop-win32.zip"), "r") as zip_ref :
        zip_ref.extractall(os.path.join(os.path.expanduser("~"), "Desktop"))

ram_mc = psutil.virtual_memory().total / 2097152

with open(os.path.join(os.path.expanduser('~'), 'Desktop\\MultiMC', 'multimc.cfg'), 'r+') as multimc_config :
    lineas = multimc_config.readlines()
    
    for i, linea in enumerate(lineas) :
        if linea.startswith('MaxMemAlloc') :
            lineas[i] = f'MaxMemAlloc={ram_mc:.0f}\n'
        elif linea.startswith('MinMemAlloc') :
            lineas[i] = f'MinMemAlloc={ram_mc:.0f}\n'
            
    multimc_config.seek(0)
    multimc_config.writelines(lineas)
    
    multimc_config.truncate()
    
# Respuesta negativa para Minecraft premium

if mcpremium == False :
    urllib.request.urlretrieve("https://nightly.link/UltimMC/Launcher/workflows/main/develop/mmc-cracked-win32.zip", os.path.join(carpeta_cache, "mmc-cracked-win32.zip"))

    with zipfile.ZipFile(os.path.join(carpeta_cache, "mmc-cracked-win32.zip"), "r") as zip_ref :
        zip_ref.extractall(os.path.join(os.path.expanduser("~"), "Desktop"))

ram_mc = psutil.virtual_memory().total / 2097152

with open(os.path.join(os.path.expanduser('~'), 'Desktop\\UltimMC', 'ultimmc.cfg'), 'r+') as ultimmc_config :
    lineas = ultimmc_config.readlines()
    
    for i, linea in enumerate(lineas) :
        if linea.startswith('MaxMemAlloc') :
            lineas[i] = f'MaxMemAlloc={ram_mc:.0f}\n'
        elif linea.startswith('MinMemAlloc') :
            lineas[i] = f'MinMemAlloc={ram_mc:.0f}\n'
            
    ultimmc_config.seek(0)
    ultimmc_config.writelines(lineas)
    
    ultimmc_config.truncate()
