import ctypes
import sys
import subprocess

class Yui:
    def is_admin():
    # Vérifie si le script est exécuté avec les droits administratifs
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
        
    def reset_proxy():
        subprocess.run('netsh winhttp reset proxy', shell=True)

    def set_proxy(proxy_url):
        command = f'netsh winhttp set proxy proxy-server="{proxy_url}"'
        subprocess.run(command, shell=True)
    
    def run_as_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    