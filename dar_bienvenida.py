import tkinter as tk

# Saludo al usuario y espera a confirmación para continuar
menu_bienvenida = tk.Tk()
menu_bienvenida.geometry("500x80")
menu_bienvenida.title("GdP Installer")

tk.Label(menu_bienvenida, text="¡Bienvenido a GdP Installer! Cuando desee comenzar con la instalación, pulse 'Continuar'").pack(pady=10)
tk.Button(menu_bienvenida, text="Continuar", command=lambda: menu_bienvenida.destroy()).pack()

menu_bienvenida.mainloop()
