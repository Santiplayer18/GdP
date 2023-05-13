import os
import urllib.request
import subprocess
import sys

carpeta_cache = os.path.join(os.path.expanduser("~"), "Downloads", "cache_gdp")
os.makedirs(carpeta_cache, exist_ok=True)

#Instalación de la última versión de Java 8
urllib.request.urlretrieve("https://github.com/ibmruntimes/semeru8-binaries/releases/download/jdk8u362-b09_openj9-0.36.0/ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi", os.path.join(carpeta_cache, "Java8.msi"))

try:
    subprocess.run(["msiexec.exe", "/i", os.path.join(carpeta_cache, "Java8.msi"), "/qn"], check=True)
except subprocess.CalledProcessError:
    sys.exit()
