import tkinter as tk

menu_bienvenida = tk.Tk()
menu_bienvenida.geometry("500x100")
menu_bienvenida.title("GdP Installer")

texto = tk.Label(menu_bienvenida, text="¡Bienvenido a GdP Installer! Cuando desee comenzar con la instalación, pulse 'Continuar'")
texto.pack(pady=10)

boton = tk.Button(menu_bienvenida, text="Continuar", command=lambda: menu_bienvenida.destroy())
boton.pack(pady=10)

menu_bienvenida.mainloop()
