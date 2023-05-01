import tkinter as tk
import os
import ctypes
import sys

try:
 admin = os.getuid() == 0
except AttributeError:
 admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if admin == True:
    menu_admin = tk.Tk()
    menu_admin.geometry("400x90")
    menu_admin.title("GdP Installer")

    texto = tk.Label(menu_admin, text="El programa posee permisos de administrador")
    texto.pack(pady=10)

    menu_admin.mainloop()
    sys.exit()
else :
    menu_noadmin = tk.Tk()
    menu_noadmin.geometry("400x90")
    menu_noadmin.title("GdP Installer")

    texto1 = tk.Label(menu_noadmin, text="El programa no puede continuar al carecer de permisos de administrador")
    texto1.pack(pady=10)

    texto2 = tk.Label(menu_noadmin, text="Por favor, vuélvalo a intentar con los permisos necesarios")
    texto2.pack(pady=10)

    menu_noadmin.mainloop()
    sys.exit()
