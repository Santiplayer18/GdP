import tkinter as tk

def respuesta(valor) :
    global mcpremium
    if valor == True :
        mcpremium = True
        menu_preguntamc.destroy()
    else :
        mcpremium = False
        menu_preguntamc.destroy()

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

menu_preguntamc.mainloop()
