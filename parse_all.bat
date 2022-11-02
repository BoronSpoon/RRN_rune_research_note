cd %~dp0
cd rrn
:loop
if not "%~nx1"=="" (
  python parse_all.py %~f1 & shift & goto loop
)
pause