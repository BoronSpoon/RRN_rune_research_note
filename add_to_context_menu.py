keyVal = r'Directory\Background\shell'
try:
    key = OpenKey(HKEY_CLASSES_ROOT, keyVal, 0, KEY_ALL_ACCESS)
except:
    key = CreateKey(HKEY_CLASSES_ROOT, keyVal)
SetValueEx(key, "Start Page", 0, REG_SZ, "https://www.blog.pythonlibrary.org/")
CloseKey(key)