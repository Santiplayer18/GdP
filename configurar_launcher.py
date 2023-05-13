import tkinter as tk
import os
import urllib.request
import zipfile
import psutil
import ctypes
from ctypes import wintypes

# Definición de funciones
def configurar_laucher(launcher, url_launcher, carpeta_launcher):
    urllib.request.urlretrieve(url_launcher, os.path.join(carpeta_cache, f"{launcher}.zip"))

    with zipfile.ZipFile(os.path.join(carpeta_cache, f"{launcher}.zip"), "r") as zip_ref:
        zip_ref.extractall(os.path.join(os.path.expanduser("~"), "Desktop", carpeta_launcher))

    ram_minecraft = psutil.virtual_memory().total / 2097152

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

def crear_acceso(directorio_diana, directorio_acceso):
    shell_link = ctypes.CoCreateInstance(
        wintypes.CLSID_ShellLink, None, wintypes.CLSCTX_INPROC_SERVER, wintypes.IID_IShellLink
    )

    shell_link.SetPath(directorio_diana)

    persist_file = shell_link.QueryInterface(wintypes.IID_IPersistFile)
    persist_file.Save(directorio_acceso, True)
    
# Pregunta para dividir usuarios premium y no premium
menu_preguntamc = tk.Tk()
menu_preguntamc.geometry("300x90")
menu_preguntamc.title("GdP Installer")

tk.Label(menu_preguntamc, text="¿Actualmente posee Minecraft: Java Edition?").pack(pady=10)

mcpremium = tk.BooleanVar()
mcpremium.set(False)

marco_botones = tk.Frame(menu_preguntamc)
marco_botones.pack()

tk.Button(marco_botones, text="Sí", command=lambda: (mcpremium.set(True), menu_preguntamc.destroy())).pack(side=tk.LEFT, padx=10)
tk.Button(marco_botones, text="No", command=lambda: (menu_preguntamc.destroy())).pack(side=tk.LEFT, padx=10)

menu_preguntamc.mainloop()
    
# Selección de acciones según respuesta
if mcpremium:
    configurar_laucher("MultiMC", "https://github.com/Santiplayer18/GdP/raw/modpack/MultiMC.zip", os.path.join(os.path.expanduser("~"), "Desktop", "MultiMC"))
    crear_acceso(os.path.join(os.path.expanduser("~"), "Desktop", "MultiMC", "MultiMC.exe"), os.path.join(os.path.expanduser("~"), "Desktop", "MultiMC.lnk"))
else:
    configurar_laucher("UltimMC", "https://github.com/Santiplayer18/GdP/raw/modpack/UltimMC.zip", os.path.join(os.path.expanduser("~"), "Desktop", "UltimMC"))
    crear_acceso(os.path.join(os.path.expanduser("~"), "Desktop", "UltimMC", "UltimMC.exe"), os.path.join(os.path.expanduser("~"), "Desktop", "UltimMC.lnk"))
