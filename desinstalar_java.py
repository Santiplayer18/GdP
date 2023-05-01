import os

os.system('wmic product where "name like \'%%IBM Semeru%%\' and name like \'%%8u%%\'" call uninstall /nointeractive')
