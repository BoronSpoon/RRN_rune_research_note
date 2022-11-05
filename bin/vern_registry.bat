reg add HKEY_CURRENT_USER\Software\Classes\*\shell\vern /t REG_SZ /d process" "in" "VERN
for /f "tokens=* delims=" %%a in ('where vern') do set "vern=%%a"
reg add HKEY_CURRENT_USER\Software\Classes\*\shell\vern\command /t REG_EXPAND_SZ /d \^"%vern%\^"" "\^"%%1\^"
pause