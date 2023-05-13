import tkinter as tk

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
