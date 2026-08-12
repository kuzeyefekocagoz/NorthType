import winreg as reg
import os
import sys

def set_autostart(enabled=True):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "NorthType"
    app_path = os.path.abspath(sys.argv[0])
    
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)
        if enabled:
            reg.SetValueEx(key, app_name, 0, reg.REG_SZ, app_path)
        else:
            try:
                reg.DeleteValue(key, app_name)
            except:
                pass
        reg.CloseKey(key)
    except Exception as e:
        print(f"Hata: {e}")