reg add HKEY_CURRENT_USER\Software\Classes\*\shell\vern /t REG_SZ /d process" "in" "VERN
reg add HKEY_CURRENT_USER\Software\Classes\*\shell\vern\command /t REG_EXPAND_SZ /d \^"%USERPROFILE%\Desktop\run_vern.bat\^"" "\^"%%1\^"
pause