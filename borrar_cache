import os

# Eliminación de la carpeta caché
for root, dirs, files in os.walk(carpeta_cache, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(carpeta_cache)
