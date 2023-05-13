import tkinter as tk
import os
import ctypes
import sys

# Determinación de privilegios de administrador
try:
    admin = os.getuid() == 0
except AttributeError:
    admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
 
if not admin:
    menu_noadmin = tk.Tk()
    menu_noadmin.geometry("400x90")
    menu_noadmin.title("GdP Installer")

    tk.Label(menu_noadmin, text="El programa no puede continuar al carecer de permisos de administrador").pack(pady=10)
    tk.Label(menu_noadmin, text="Por favor, vuélvalo a intentar con los permisos necesarios").pack(pady=10)

    logging.error("Privilegios de administrador no detectados")
    menu_noadmin.mainloop()

    logging.error("Error fatal. Forzada finalización del programa")
    sys.exit()
