import winreg
from shutil import which

for REG_PATH, CLASS, value in [
    [r"Software\Classes\*\shell\vern", winreg.REG_SZ, "process in VERN"],
    [r"Software\Classes\*\shell\vern\command", winreg.REG_EXPAND_SZ, f"\"{which('vern')}\" \"%1\""],
]:
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "", 0, CLASS, value)
        winreg.CloseKey(registry_key)
    except WindowsError:
        pass