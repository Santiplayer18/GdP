import subprocess
import sys

# Búsqueda y desinstalación de todas las versiones de Java 8 en el sistema
try:
    subprocess.check_call(["wmic", "product", "where", "name like '%IBM Semeru%' and name like '%8u%'", "call", "uninstall", "/nointeractive"])
except subprocess.CalledProcessError:
    sys.exit()
