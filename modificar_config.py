import os
import psutil

ruta_archivo = os.path.join(os.path.expanduser('~'), 'Desktop\\MultiMC', 'multimc.cfg')
ram_mc = psutil.virtual_memory().total / 2097152

with open(ruta_archivo, 'r+') as multimc_config :
    lineas = multimc_config.readlines()
    
    for i, linea in enumerate(lineas) :
        if linea.startswith('MaxMemAlloc') :
            lineas[i] = f'MaxMemAlloc={ram_mc:.0f}\n'
        elif linea.startswith('MinMemAlloc') :
            lineas[i] = f'MinMemAlloc={ram_mc:.0f}\n'
            
    multimc_config.seek(0)
    multimc_config.writelines(lineas)
    
    multimc_config.truncate()
