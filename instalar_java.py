import os
import urllib.request
import subprocess

carpeta_cache = os.path.join(os.path.expanduser("~"), "Downloads", "cache_gdp")
os.makedirs(carpeta_cache, exist_ok=True)

urllib.request.urlretrieve("https://github.com/ibmruntimes/semeru8-binaries/releases/download/jdk8u362-b09_openj9-0.36.0/ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi", os.path.join(carpeta_cache, "ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi"))

subprocess.call(['msiexec.exe', '/i', os.path.join(carpeta_cache, "ibm-semeru-open-jdk_x64_windows_8u362b09_openj9-0.36.0.msi"), '/qn'])
